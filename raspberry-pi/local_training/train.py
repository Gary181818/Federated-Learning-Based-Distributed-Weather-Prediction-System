# local_training/train.py
import os
import json
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from model import create_mlp, create_lstm

# ========== 配置 ==========
DATA_PATH = "dataset.csv"
MODEL_OUT = "local_model.h5"
WEIGHTS_JSON = "model_weights.json"

# 超參數（可調）
WINDOW = 3                # 如果用 LSTM 的時間窗
USE_LSTM = False          # True 用 LSTM, False 用 MLP
EPOCHS = 30
BATCH_SIZE = 16
TEST_SPLIT = 0.1

# ========== 輔助函式 ==========
def load_data(path):
    df = pd.read_csv(path, parse_dates=['timestamp'])
    # 若有缺值，簡單處理：前向填充
    df = df.fillna(method='ffill').dropna()
    return df

def make_windows(df, window=3, target_col='rain'):
    """
    若使用 LSTM：回傳 X:(n_samples, window, n_features) 與 y:(n_samples,)
    若使用 MLP：把 window 平坦化: X:(n_samples, window*n_features)
    """
    features = ['temperature', 'humidity', 'pressure']  # 可依情況修改
    arr = df[features].values
    y = df[target_col].values
    Xs, Ys = [], []
    for i in range(len(arr) - window):
        Xs.append(arr[i:i+window])
        Ys.append(y[i+window])  # predict next step
    Xs = np.array(Xs)
    Ys = np.array(Ys)
    return Xs, Ys

def flatten_windows(X):
    # X shape (n, window, features) -> (n, window*features)
    n, w, f = X.shape
    return X.reshape(n, w*f)

def split_train_test(X, y, test_ratio=0.1):
    n = len(X)
    split_idx = int(n * (1 - test_ratio))
    return X[:split_idx], X[split_idx:], y[:split_idx], y[split_idx:]

# ========== 主程式 ==========
def main():
    assert os.path.exists(DATA_PATH), f"{DATA_PATH} not found!"
    df = load_data(DATA_PATH)
    X, y = make_windows(df, window=WINDOW, target_col='rain')

    # 標準化 (對 feature 維度做)
    n_samples, w, f = X.shape
    X_2d = X.reshape(n_samples * w, f)  # 用整體資料 fit scaler
    scaler = StandardScaler().fit(X_2d)
    X_scaled = scaler.transform(X_2d).reshape(n_samples, w, f)

    if USE_LSTM:
        X_final = X_scaled
        model = create_lstm(WINDOW, f)
    else:
        X_flat = flatten_windows(X_scaled)
        X_final = X_flat
        model = create_mlp(X_flat.shape[1])

    # train / test split
    X_train, X_test, y_train, y_test = split_train_test(X_final, y, TEST_SPLIT)

    # callbacks
    callbacks = [
        EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True),
        ModelCheckpoint(MODEL_OUT, monitor='val_loss', save_best_only=True)
    ]

    # fit
    model.fit(X_train, y_train,
              validation_data=(X_test, y_test),
              epochs=EPOCHS,
              batch_size=BATCH_SIZE,
              callbacks=callbacks)

    # save final model (already saved by ModelCheckpoint)
    model.save(MODEL_OUT)

    # 序列化權重為 JSON（方便透過 MQTT 傳送）
    weights = model.get_weights()
    weights_serializable = [w.tolist() for w in weights]
    with open(WEIGHTS_JSON, 'w') as f:
        json.dump({"weights": weights_serializable, "scaler_mean": scaler.mean_.tolist(), "scaler_scale": scaler.scale_.tolist()}, f)
    print(f"Saved model to {MODEL_OUT} and weights to {WEIGHTS_JSON}")

if __name__ == "__main__":
    main()