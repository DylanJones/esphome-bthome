---
title: Basic Setup
description: Configure the BTHome component options
---

## Configuration Options

The BTHome component supports the following configuration options:

```yaml
bthome:
  min_interval: 1s
  max_interval: 1s
  tx_power: 0
  ble_stack: bluedroid  # Optional, ESP32 only: bluedroid or nimble
  trigger_based: false  # Optional, for event-driven devices
  encryption_key: "your_32_hex_char_key"  # Optional
  sensors:
    # ... sensor configuration
  binary_sensors:
    # ... binary sensor configuration
```

### Options Reference

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `min_interval` | Time | `1s` | Minimum advertising interval (1s - 10240ms) |
| `max_interval` | Time | `1s` | Maximum advertising interval (1s - 10240ms) |
| `tx_power` | Integer | `0` | Transmit power in dBm |
| `ble_stack` | String | `bluedroid` | ESP32 only: `bluedroid` or `nimble` (see [BTHome Component](/components/bthome)) |
| `trigger_based` | Boolean | `false` | Mark device as trigger-based (event-driven) |
| `encryption_key` | String | - | Optional 16-byte encryption key (32 hex chars) |
| `sensors` | List | - | List of sensor measurements to broadcast |
| `binary_sensors` | List | - | List of binary sensor measurements to broadcast |

## Advertising Interval

The advertising interval controls how often your device broadcasts sensor data:

```yaml
bthome:
  min_interval: 5s   # Broadcast at least every 5 seconds
  max_interval: 10s  # But no more than every 10 seconds
```

:::tip[Battery Life]
Longer intervals save battery power. For battery-powered sensors, consider intervals of 30s or more.
:::

:::caution[Latency]
Longer intervals mean more latency before Home Assistant sees sensor updates. For motion sensors, use `advertise_immediately: true` instead.
:::

## TX Power

Transmit power affects range and battery consumption:

### ESP32 TX Power Levels

| dBm | Description |
|-----|-------------|
| -12 | Minimum power, shortest range |
| -9 | Low power |
| -6 | Below default |
| -3 | Slightly below default |
| 0 | Default |
| 3 | Above default |
| 6 | High power |
| 9 | Maximum power, longest range |

### nRF52 TX Power Levels

| dBm | Description |
|-----|-------------|
| -40 | Ultra low power |
| -20 | Very low power |
| -16, -12, -8, -4 | Low power options |
| 0 | Default |
| 2, 3, 4, 5, 6, 7, 8 | High power options |

Example:
```yaml
bthome:
  tx_power: 4  # Increase range
```

## Trigger-Based Devices

Set `trigger_based: true` for devices that only send data on events rather than continuously. This tells Home Assistant not to expect regular updates from the device.

Use cases for trigger-based mode:
- **Push buttons** - Only broadcast when pressed
- **Remote controls** - Only broadcast on button press
- **Door bells** - Only broadcast when activated
- **Event-driven sensors** - Any sensor that reports discrete events rather than continuous measurements

```yaml
bthome:
  trigger_based: true
  binary_sensors:
    - type: generic_boolean
      id: button_press
      advertise_immediately: true
```

:::tip[When to use trigger_based]
Enable this for battery-powered devices where you want to maximize battery life by only transmitting on user interaction or events, not on a regular schedule.
:::

## Sensor Configuration

Each sensor measurement requires:

| Option | Required | Description |
|--------|----------|-------------|
| `type` | Yes | BTHome sensor type (see [Sensor Types](/reference/sensor-types)) |
| `id` | Yes | Reference to an ESPHome sensor |
| `advertise_immediately` | No | Broadcast immediately on value change (default: false) |

```yaml
bthome:
  sensors:
    - type: temperature
      id: my_temp_sensor
      advertise_immediately: false
    - type: humidity
      id: my_humidity_sensor
    - type: battery
      id: battery_percent
```

## Binary Sensor Configuration

Each binary sensor measurement requires:

| Option | Required | Description |
|--------|----------|-------------|
| `type` | Yes | BTHome binary sensor type (see [Binary Sensor Types](/reference/binary-sensor-types)) |
| `id` | Yes | Reference to an ESPHome binary sensor |
| `advertise_immediately` | No | Broadcast immediately on state change (default: false) |

```yaml
bthome:
  binary_sensors:
    - type: motion
      id: pir_motion
      advertise_immediately: true  # Important for motion sensors!
    - type: door
      id: door_contact
      advertise_immediately: true
```

:::tip[Immediate Advertising]
For binary sensors like motion or door contacts, enable `advertise_immediately: true` to get instant notifications in Home Assistant instead of waiting for the next advertising interval.
:::

## Next Steps

- [Sensors](/configuration/sensors) - All supported sensor types
- [Binary Sensors](/configuration/binary-sensors) - All supported binary sensor types
- [Encryption](/configuration/encryption) - Secure your sensor data
- [Power Saving](/configuration/power-saving) - Optimize for battery-powered devices
