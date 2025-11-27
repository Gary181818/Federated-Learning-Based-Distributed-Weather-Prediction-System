# pip install pyserial

import serial
import csv
from datatime import datatime

SERIAL_PORT = ''
BAUD_RATE = 9600
CSV_FILE = 'dataset.csv'

ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

with open(CSV_FILE, mode='a', newline='') as file:
    writer = csv.writer(file)

    # 寫入標題（如果檔案是空的）
    if file.tell() == 0:
        writer.writerow(["timestamp", "temperature", "humidity", "pressure", "rain"])

    print("Starting data collection...")

    while True:
        line = ser.readline().decode().strip()
        values = line.split(",")

        if len(values) == 4:
            timestamp = datetime.now().isoformat()
            row = [timestamp] + values
            writer.writerow(row)
            print("Saved:", row)