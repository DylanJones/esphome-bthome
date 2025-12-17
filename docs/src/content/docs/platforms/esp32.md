---
title: ESP32
description: Using BTHome with ESP32 boards
---

The BTHome component fully supports ESP32 boards using the ESP-IDF framework.

## Supported Boards

Any ESP32 board with Bluetooth LE support:
- ESP32 (original)
- ESP32-C3
- ESP32-S3
- ESP32-C6

## Basic Configuration

```yaml
esphome:
  name: bthome-esp32
  friendly_name: BTHome ESP32

esp32:
  board: esp32dev
  framework:
    type: esp-idf

logger:

wifi:
  ap:
    ssid: "BTHome-ESP32"

captive_portal:

external_components:
  - source:
      type: git
      url: https://github.com/dz0ny/esphome-bthome
      ref: main
    components: [bthome]
```

## Framework Requirement

BTHome requires the **ESP-IDF** framework (not Arduino):

```yaml
esp32:
  board: esp32dev
  framework:
    type: esp-idf  # Required!
```

:::caution
Arduino framework is not supported. You must use ESP-IDF.
:::

## BLE Stack Options

ESP32 supports two BLE stacks:

- **Bluedroid** (default) - Full-featured BLE stack, compatible with other ESPHome BLE components
- **NimBLE** - Lightweight alternative that saves ~170KB flash and ~100KB RAM

For broadcast-only sensors, NimBLE offers significant memory savings. See the [BTHome Component](/components/bthome) documentation for detailed comparison and configuration.

```yaml
bthome:
  ble_stack: nimble  # Optional: use lightweight NimBLE stack
```

## TX Power Levels

ESP32 supports these transmit power levels:

| Setting | Power | Description |
|---------|-------|-------------|
| -12 | -12 dBm | Minimum, ~1m range |
| -9 | -9 dBm | Very low |
| -6 | -6 dBm | Low |
| -3 | -3 dBm | Below default |
| 0 | 0 dBm | Default |
| 3 | +3 dBm | Above default |
| 6 | +6 dBm | High |
| 9 | +9 dBm | Maximum, ~30m+ range |

```yaml
bthome:
  tx_power: 6  # High power for longer range
```

## Complete Example

Temperature, humidity, and motion sensor:

```yaml
esphome:
  name: bthome-esp32
  friendly_name: BTHome ESP32 Sensor

esp32:
  board: esp32dev
  framework:
    type: esp-idf

logger:

wifi:
  ap:
    ssid: "BTHome-ESP32"

captive_portal:

external_components:
  - source:
      type: git
      url: https://github.com/dz0ny/esphome-bthome
      ref: main
    components: [bthome]

# I2C bus
i2c:
  sda: GPIO21
  scl: GPIO22

# Sensors
sensor:
  - platform: bme280_i2c
    address: 0x76
    temperature:
      id: temperature
      name: "Temperature"
    humidity:
      id: humidity
      name: "Humidity"
    pressure:
      id: pressure
      name: "Pressure"
    update_interval: 30s

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

# BTHome configuration
bthome:
  min_interval: 10s
  max_interval: 30s
  tx_power: 3
  sensors:
    - type: temperature
      id: temperature
    - type: humidity
      id: humidity
    - type: pressure
      id: pressure
  binary_sensors:
    - type: motion
      id: motion
      advertise_immediately: true
```

## Power Optimization

For battery-powered ESP32 devices:

### Use Deep Sleep

```yaml
deep_sleep:
  run_duration: 10s
  sleep_duration: 5min
```

### Reduce TX Power

```yaml
bthome:
  tx_power: -6  # Lower power saves battery
```

### Increase Advertising Interval

```yaml
bthome:
  min_interval: 30s
  max_interval: 60s
```

## Troubleshooting

### BLE not initializing

Ensure you're using ESP-IDF framework:
```yaml
esp32:
  framework:
    type: esp-idf
```

### Short range

Increase TX power:
```yaml
bthome:
  tx_power: 9  # Maximum
```

### High power consumption

Reduce advertising frequency and TX power:
```yaml
bthome:
  min_interval: 30s
  max_interval: 60s
  tx_power: -3
```

## See Also

- [nRF52 Platform](/platforms/nrf52) - For ultra-low-power applications
- [Basic Setup](/configuration/basic-setup) - General configuration options
