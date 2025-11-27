# Federated-Learning-Based-Distributed-Weather-Prediction-System

## Project Framework
federated-weather-prediction/
│
├── arduino/
│   ├── sensors/
│   │   └── weather_station.ino          # 讀取 DHT22 / BMP280 / 雨滴感測器
│   ├── communication/
│   │   └── mqtt_sender.ino              # Arduino → MQTT → Server
│   └── README.md
│
├── raspberry-pi/
│   ├── data_collection/
│   │   ├── serial_read.py               # 收集 Arduino Serial、儲存資料成 CSV
│   │   └── config.json                  # serail port、baudrate 設定
│   ├── automation/
│   │   ├── run_collector.sh             # 啟動資料收集（bash）
│   │   ├── train_local.sh               # 啟動本地 TFF 訓練
│   │   └── weather-collector.service    # systemd 自動啟動
│   ├── local_training/
│   │   ├── model.py                     # 本地模型（LSTM/MLP）
│   │   ├── train.py                     # 本地訓練流程
│   │   └── dataset.csv                  # 本地感測資料
│   └── README.md
│
├── server-aggregator/
│   ├── tff_server/
│   │   ├── server.py                    # 聯邦學習中心 Server
│   │   ├── aggregator.py                # 模型權重聚合（FedAvg）
│   │   ├── dockerfile                   # 部署 Server 用 Dockerfile
│   │   └── requirements.txt
│   │
│   ├── client_script/
│   │   ├── client.py                    # Pi 端送本地模型更新到 Server
│   │   └── config.json                  # server URL、client ID
│   │
│   └── models/
│       ├── lstm.py
│       └── mlp.py
│
├── mqtt/
│   ├── hivemq_config/
│   │   ├── credentials.txt              # username/password（不 commit）
│   │   └── README.md
│   ├── subscriber/
│   │   └── data_receiver.py             # Server 訂閱感測資料
│   └── publisher/
│       └── test_publisher.py
│
├── docker/
│   ├── broker/                          # 可選：本地 Mosquitto image
│   │   ├── docker-compose.yml
│   │   └── mosquitto.conf
│   ├── federated_server/
│   │   └── docker-compose.yml
│   └── README.md
│
├── docs/
│   ├── architecture/
│   │   ├── system_architecture.png
│   │   ├── federated_learning_flow.png
│   │   └── mqtt_network_diagram.png
│   ├── ppt/
│   │   └── presentation.pptx            # 簡報
│   ├── api_spec.md
│   └── project_overview.md
│
├── scripts/
│   ├── install_dependencies.sh          # 一鍵安裝 Pi 所需套件
│   ├── setup_docker_server.sh
│   └── setup_mqtt.sh
│
├── .gitignore
├── LICENSE
└── README.md