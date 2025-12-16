---
title: Quick Start
description: Get started with ESPHome BTHome in minutes
---

import { Tabs, TabItem } from '@astrojs/starlight/components';

This guide will help you create a simple BTHome temperature and humidity sensor.

## Choose Your Platform

<Tabs>
  <TabItem label="ESP32">
    ```yaml
    esphome:
      name: bthome-sensor
      friendly_name: BTHome Sensor

    esp32:
      board: esp32dev
      framework:
        type: esp-idf

    logger:

    external_components:
      - source:
          type: git
          url: https://github.com/dz0ny/esphome-bthome
          ref: main
        components: [bthome]

    # I2C for BME280 sensor
    i2c:
      sda: GPIO21
      scl: GPIO22
      scan: true

    sensor:
      - platform: bme280_i2c
        address: 0x76
        temperature:
          id: bme_temperature
          name: "Temperature"
        humidity:
          id: bme_humidity
          name: "Humidity"
        pressure:
          id: bme_pressure
          name: "Pressure"
        update_interval: 30s

    # BTHome configuration
    bthome:
      sensors:
        - type: temperature
          id: bme_temperature
        - type: humidity
          id: bme_humidity
        - type: pressure
          id: bme_pressure
    ```
  </TabItem>
  <TabItem label="nRF52 (XIAO BLE)">
    ```yaml
    esphome:
      name: bthome-sensor
      friendly_name: BTHome Sensor

    nrf52:
      board: xiao_ble
      bootloader: adafruit

    logger:

    external_components:
      - source:
          type: git
          url: https://github.com/dz0ny/esphome-bthome
          ref: main
        components: [bthome]

    # I2C for BME280 sensor
    i2c:
      sda: 4
      scl: 5
      scan: true

    sensor:
      - platform: bme280_i2c
        address: 0x76
        temperature:
          id: bme_temperature
          name: "Temperature"
        humidity:
          id: bme_humidity
          name: "Humidity"
        pressure:
          id: bme_pressure
          name: "Pressure"
        update_interval: 30s

    # BTHome configuration
    bthome:
      sensors:
        - type: temperature
          id: bme_temperature
        - type: humidity
          id: bme_humidity
        - type: pressure
          id: bme_pressure
    ```
  </TabItem>
</Tabs>

## Build and Flash

1. **Compile** the configuration:
   ```bash
   esphome compile your_config.yaml
   ```

2. **Flash** to your device:
   ```bash
   esphome upload your_config.yaml
   ```

3. **Monitor** the logs to verify it's working:
   ```bash
   esphome logs your_config.yaml
   ```

## Verify in Home Assistant

Once your device is running:

1. Open Home Assistant
2. Go to **Settings** → **Devices & Services** → **BTHome**
3. Your device should appear automatically
4. Click **Configure** to add it

You should now see your temperature, humidity, and pressure sensors in Home Assistant!

## What's Next?

- [Configuration Options](/configuration/basic-setup) - Customize advertising intervals and TX power
- [Add More Sensors](/configuration/sensors) - See all supported sensor types
- [Enable Encryption](/configuration/encryption) - Secure your sensor data
