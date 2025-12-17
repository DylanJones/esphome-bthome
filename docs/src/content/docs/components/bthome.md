---
title: BTHome Component
description: Configuration reference for the BTHome component
---

The BTHome component is the core of ESPHome BTHome, providing BLE broadcasting capabilities for ESP32 and nRF52 platforms.

## Platform Support

| Platform | BLE Stack | Status |
|----------|-----------|--------|
| ESP32, ESP32-S3, ESP32-C3 | Bluedroid (default) | Supported |
| ESP32, ESP32-S3, ESP32-C3 | NimBLE | Supported |
| nRF52840 | Zephyr BT | Supported |

## BLE Stack Selection (ESP32 Only)

ESP32 platforms support two different BLE stacks: **Bluedroid** (default) and **NimBLE**. The choice of stack affects memory usage, features, and compatibility.

### Bluedroid Stack

The default BLE stack for ESP32. Use this when:
- You need compatibility with other ESPHome BLE components (`esp32_ble_tracker`, `bluetooth_proxy`, etc.)
- You're already using the `esp32_ble` component
- You need full BLE functionality (scanning, connections, etc.)

```yaml
bthome:
  ble_stack: bluedroid  # Default, can be omitted
```

### NimBLE Stack

A lightweight, standalone BLE stack optimized for broadcast-only scenarios. Choose NimBLE when:
- **Memory is limited** - Saves approximately 170KB flash and 100KB RAM
- **Broadcasting only** - Your device only needs to send BTHome advertisements
- **No other BLE features needed** - You don't need BLE scanning or connections
- **Battery-powered devices** - Smaller footprint means less power consumption

```yaml
bthome:
  ble_stack: nimble
```

:::tip[Memory Savings]
NimBLE can free up significant resources on memory-constrained devices, making room for more features or reducing overall power consumption.
:::

:::caution[NimBLE Limitations]
NimBLE is **standalone** and cannot coexist with other ESPHome BLE components like `esp32_ble`, `esp32_ble_tracker`, or `bluetooth_proxy`. If your configuration uses any of these components, you must use the default Bluedroid stack.
:::

### Stack Comparison

| Feature | Bluedroid | NimBLE |
|---------|-----------|--------|
| Flash Usage | ~340KB | ~170KB |
| RAM Usage | ~200KB | ~100KB |
| Broadcasting | Yes | Yes |
| Scanning | Yes | No |
| Connections | Yes | No |
| Encryption Library | mbedtls | tinycrypt |
| Compatible with esp32_ble | Yes | No |
| Compatible with bluetooth_proxy | Yes | No |
| Best For | Multi-function BLE | Broadcast-only sensors |

### Supported Devices

NimBLE is available on:
- ESP32 (original)
- ESP32-S3
- ESP32-C3

Other ESP32 variants (ESP32-S2, ESP32-C6) may have varying support depending on ESP-IDF version.

## Complete Configuration Example

### Basic BTHome with NimBLE

```yaml
esphome:
  name: bthome-sensor
  friendly_name: BTHome Sensor

esp32:
  board: esp32dev
  framework:
    type: esp-idf

logger:

wifi:
  ap:
    ssid: "BTHome-Sensor"

captive_portal:

external_components:
  - source:
      type: git
      url: https://github.com/dz0ny/esphome-bthome
      ref: main
    components: [bthome]

# I2C bus for BME280
i2c:
  sda: GPIO21
  scl: GPIO22

# Temperature and humidity sensor
sensor:
  - platform: bme280_i2c
    address: 0x76
    temperature:
      id: temperature
      name: "Temperature"
    humidity:
      id: humidity
      name: "Humidity"
    update_interval: 30s

# BTHome configuration with NimBLE
bthome:
  ble_stack: nimble  # Use lightweight NimBLE stack
  min_interval: 10s
  max_interval: 30s
  tx_power: 3
  sensors:
    - type: temperature
      id: temperature
    - type: humidity
      id: humidity
```

### Low-Power Battery Sensor with NimBLE

Maximize battery life using NimBLE's smaller footprint and deep sleep:

```yaml
esphome:
  name: battery-sensor
  friendly_name: Battery Sensor

esp32:
  board: esp32dev
  framework:
    type: esp-idf

logger:
  level: WARN  # Reduce logging overhead

external_components:
  - source:
      type: git
      url: https://github.com/dz0ny/esphome-bthome
      ref: main
    components: [bthome]

# Deep sleep for maximum battery savings
deep_sleep:
  run_duration: 10s
  sleep_duration: 5min

# ADC for battery voltage
sensor:
  - platform: adc
    pin: GPIO34
    id: battery_voltage
    attenuation: 11db
    filters:
      - multiply: 2.0  # Voltage divider compensation

  - platform: template
    id: battery_percent
    name: "Battery"
    unit_of_measurement: "%"
    accuracy_decimals: 0
    lambda: |-
      // Convert voltage to percentage (3.0V = 0%, 4.2V = 100%)
      float voltage = id(battery_voltage).state;
      return ((voltage - 3.0) / 1.2) * 100.0;

# BTHome with NimBLE - minimal memory footprint
bthome:
  ble_stack: nimble  # Save ~170KB flash, ~100KB RAM
  min_interval: 1s
  max_interval: 1s
  tx_power: -3  # Low power for battery savings
  sensors:
    - type: battery
      id: battery_percent
```

### Motion Sensor with Encryption

```yaml
esphome:
  name: motion-sensor
  friendly_name: Motion Sensor

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

# PIR motion sensor
binary_sensor:
  - platform: gpio
    pin:
      number: GPIO4
      mode: INPUT_PULLDOWN
    id: motion
    name: "Motion"
    device_class: motion
    filters:
      - delayed_off: 30s

# BTHome with NimBLE and encryption
bthome:
  ble_stack: nimble  # Lightweight stack
  encryption_key: "231d39c1d7cc1ab1aee224cd096db932"  # 32 hex chars
  min_interval: 30s
  max_interval: 60s
  tx_power: 0
  binary_sensors:
    - type: motion
      id: motion
      advertise_immediately: true  # Instant updates on motion
```

:::note[Encryption with NimBLE]
NimBLE uses **tinycrypt** for AES-CCM encryption instead of mbedtls, providing the same security with a smaller code footprint (saves an additional ~7KB).
:::

## Migration Guide

### From Bluedroid to NimBLE

If you have an existing BTHome configuration using Bluedroid and want to switch to NimBLE:

1. **Check for conflicts** - Remove any incompatible components:
   - `esp32_ble` or `esp32_ble_tracker`
   - `bluetooth_proxy`
   - Any other components that use BLE scanning or connections

2. **Add ble_stack option**:
   ```yaml
   bthome:
     ble_stack: nimble  # Add this line
     # ... rest of your config
   ```

3. **Recompile and flash** - The firmware will be smaller and use less RAM

### From NimBLE to Bluedroid

If you need to add BLE scanning or other features:

1. **Change or remove ble_stack**:
   ```yaml
   bthome:
     ble_stack: bluedroid  # Or omit this line entirely
     # ... rest of your config
   ```

2. **Add required components** - Now you can use `esp32_ble`, `bluetooth_proxy`, etc.

3. **Recompile and flash**

## Troubleshooting

### Build fails with NimBLE

**Symptom**: Compilation errors related to NimBLE headers or configuration.

**Solution**: Ensure you're using ESP-IDF framework (not Arduino):
```yaml
esp32:
  framework:
    type: esp-idf  # Required
```

### NimBLE conflicts with other components

**Symptom**: Build errors about conflicting BLE configurations.

**Solution**: Remove incompatible BLE components (`esp32_ble`, `bluetooth_proxy`, etc.) or switch to Bluedroid stack.

### High memory usage despite using NimBLE

**Symptom**: Still running out of memory even with NimBLE.

**Solution**:
- Reduce logging level: `logger: level: WARN`
- Disable unnecessary features
- Use deep sleep to reduce runtime memory usage
- Check for other memory-intensive components

## See Also

- [ESP32 Platform](/platforms/esp32) - ESP32-specific configuration
- [Basic Setup](/configuration/basic-setup) - General BTHome configuration
- [Encryption](/configuration/encryption) - Securing your sensor data
- [Power Saving](/configuration/power-saving) - Battery optimization techniques
