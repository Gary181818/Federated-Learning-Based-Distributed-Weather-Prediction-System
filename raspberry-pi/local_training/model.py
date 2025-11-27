# local_training/model.py
from tensorflow.keras import models, layers, optimizers

def create_mlp(input_dim, lr=0.001):
    """
    輕量 MLP，適合非時序或用滑動窗把時序攤平成向量的情形。
    input_dim: 整數 (features 或 window*features)
    """
    model = models.Sequential([
        layers.Input(shape=(input_dim,)),
        layers.Dense(32, activation='relu'),
        layers.Dense(16, activation='relu'),
        layers.Dense(1, activation='linear')  # 如果要分類改 sigmoid + loss=binary_crossentropy
    ])
    model.compile(optimizer=optimizers.Adam(lr), loss='mse', metrics=['mae'])
    return model

def create_lstm(window, n_features, lr=0.001):
    """
    小型 LSTM，輸入為 (window, n_features)
    """
    model = models.Sequential([
        layers.Input(shape=(window, n_features)),
        layers.LSTM(32, return_sequences=False),
        layers.Dense(16, activation='relu'),
        layers.Dense(1, activation='linear')
    ])
    model.compile(optimizer=optimizers.Adam(lr), loss='mse', metrics=['mae'])
    return model