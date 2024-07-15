import argparse
import asyncio
import platform
import csv
from bleak import BleakClient
from bleak import BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic
from datetime import datetime

ADDRESS = (
    "F1:56:8B:BD:1E:D5"
    if platform.system() != "Darwin"
    else "40D93FB2-EA47-F481-7DAF-6E71515A391F"
)

custom_svc_uuid = "4A981234-1CC4-E7C1-C757-F1267DD021E8"
custom_wrt_char_uuid = "4A981235-1CC4-E7C1-C757-F1267DD021E8"
custom_read_char_uuid = "4A981236-1CC4-E7C1-C757-F1267DD021E8"

async def main():
    def handle_rx(_: BleakGATTCharacteristic, data: bytearray):
        with open('sample_temps.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            c = datetime.now()
            curr_time = c.strftime('%H:%M:%S')
            t, h = data.decode().split(', ')
            writer.writerow([curr_time, t, h])
        print("received:", data.decode())
    async with BleakClient(ADDRESS) as client:
        print(f"Connected: {client.is_connected}")
        await client.start_notify(custom_read_char_uuid, handle_rx)
        while True:
           data = await client.read_gatt_char(custom_read_char_uuid)
           await asyncio.sleep(1.0)
            
if __name__ == "__main__":
    asyncio.run(main())
