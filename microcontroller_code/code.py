# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
# Updated for CircuitPython 9.0
"""WiFi Simpletest"""

import os

import adafruit_connection_manager
import wifi

import adafruit_ntp

import adafruit_requests

import time
import board
import neopixel
import rtc

import circuitpython_schedule as schedule

# Get WiFi details, ensure these are setup in settings.toml
ssid = os.getenv("CIRCUITPY_WIFI_SSID")
password = os.getenv("CIRCUITPY_WIFI_PASSWORD")

TEXT_URL = "https://express-api-bice.vercel.app/light"
JSON_GET_URL = "https://httpbin.org/get"
JSON_POST_URL = "https://httpbin.org/post"

# Initalize Wifi, Socket Pool, Request Session
pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
requests = adafruit_requests.Session(pool, ssl_context)
rssi = wifi.radio.ap_info.rssi

pixel = neopixel.NeoPixel(board.NEOPIXEL,1)
pixel.brightness=0.3

print(f"\nConnecting to {ssid}...")
print(f"Signal Strength: {rssi}")
try:
    # Connect to the Wi-Fi network
    wifi.radio.connect(ssid, password)
except OSError as e:
    print(f"❌ OSError: {e}")
print("✅ Wifi!")


TZ_OFFSET = 9  # time zone offset in hours from UTC

ntp = adafruit_ntp.NTP(pool, tz_offset=TZ_OFFSET, cache_seconds=3600)
rtc.RTC().datetime=ntp.datetime
now = time.localtime()

def main():
    ntp = adafruit_ntp.NTP(pool, tz_offset=TZ_OFFSET, cache_seconds=3600)
    rtc.RTC().datetime=ntp.datetime
    now = time.localtime()

    print("current time is "+str(now))
    
    with requests.get(TEXT_URL) as response:
        json_resp=response.json()
        print(json_resp['power'])
        if json_resp['power']=='on':
            pixel.fill((255,0,0))
            time.sleep(0.25)
            pixel.fill((0, 255, 0))
            time.sleep(0.25)
            pixel.fill((0, 0, 255))
            time.sleep(0.25)
            pixel.fill((255,255,255))
        else:
            pixel.fill((0,0,0))

def daily_job(x, t=None):
    schedule.every().day.at(t).do(x)

daily_job(main, '17:30:00')

while True:
    schedule.run_pending()
    time.sleep(1)

print("Finished!")
