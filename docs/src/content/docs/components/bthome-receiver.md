---
title: BTHome Receiver
description: Receive BTHome v2 BLE advertisements from external devices
---

The **BTHome Receiver** component allows your ESP32 to receive and decode BTHome v2 BLE advertisements from external devices. This enables your ESPHome device to act as a BTHome gateway, collecting sensor data from multiple BTHome-compatible devices.

## Features

- Receives BTHome v2 BLE advertisements from external devices
- Supports 60+ sensor types (temperature, humidity, pressure, etc.)
- Supports 28 binary sensor types (motion, door, window, etc.)
- Supports text sensors for UTF-8 strings and raw binary data
- AES-128-CCM encryption support with replay protection
- Button and dimmer event triggers for automation
- Multiple device support with individual configurations
- Optional per-device encryption keys
- **Two BLE stack options**: Bluedroid (default) or NimBLE (lightweight)
- **Periodic device dump**: Log all detected BTHome devices at configurable intervals for discovery and debugging

## BLE Stack Selection

The BTHome Receiver supports two different BLE stacks: **Bluedroid** (default) and **NimBLE**. The choice of stack affects memory usage, features, and compatibility.

### Bluedroid Stack (Default)

The default BLE stack for ESP32. Use this when:
- You need compatibility with other ESPHome BLE components (`esp32_ble_tracker`, `bluetooth_proxy`, etc.)
- You want to use BLE for multiple purposes (scanning, connections, etc.)
- You're already using the `esp32_ble` component

```yaml
esp32_ble_tracker:
  scan_parameters:
    active: false

bthome_receiver:
  ble_stack: bluedroid  # Default, can be omitted
  devices:
    - mac_address: "AA:BB:CC:DD:EE:FF"
```

### NimBLE Stack

A lightweight, standalone BLE stack optimized for observer-only scenarios. Choose NimBLE when:
- **Memory is limited** - Saves approximately 253KB flash and 10KB RAM
- **Receiving only** - Your device only needs to receive BTHome advertisements
- **No other BLE features needed** - You don't need BLE scanning for other purposes or connections
- **Battery-powered devices** - Smaller footprint means less power consumption

```yaml
bthome_receiver:
  ble_stack: nimble
  devices:
    - mac_address: "AA:BB:CC:DD:EE:FF"
```

:::tip[Memory Savings]
NimBLE can free up significant resources on memory-constrained devices, making room for more features or reducing overall power consumption.
:::

:::caution[NimBLE Limitations]
NimBLE is **standalone** and cannot coexist with other ESPHome BLE components like `esp32_ble`, `esp32_ble_tracker`, or `bluetooth_proxy`. If your configuration uses any of these components, you must use the default Bluedroid stack.
:::

### Stack Comparison

Actual measurements from BTHome receiver on ESP32-S3:

| Feature | Bluedroid | NimBLE | Savings |
|---------|-----------|--------|---------|
| Flash Usage | 1,151KB (62.7%) | 898KB (48.9%) | **~253KB** |
| RAM Usage | 50KB (15.3%) | 40KB (12.3%) | **~10KB** |
| BLE Scanning | Via esp32_ble_tracker | Built-in passive | - |
| Compatible with esp32_ble | Yes | No | - |
| Compatible with bluetooth_proxy | Yes | No | - |
| Best For | Multi-function BLE | Receive-only gateway | - |

## Device Discovery Mode

Use the `dump_interval` option to periodically log all detected BTHome devices. This is useful for:

- Finding MAC addresses of new devices
- Identifying what sensor types a device broadcasts
- Debugging encrypted devices (shows if encryption is enabled)
- Monitoring device health and signal presence

### Enabling Device Discovery

```yaml
bthome_receiver:
  dump_interval: 10s  # Log all devices every 10 seconds (0 = disabled)
```

### Log Output

At each interval, all detected BTHome devices are logged with their cached sensor data:

```
[I][bthome_receiver:396]: [A4:C1:38:12:34:56] | temperature=31.82 humidity=22.28 battery=100
[I][bthome_receiver:396]: [AA:BB:CC:DD:EE:FF] ENC | (encrypted data)
[I][bthome_receiver:476]:   ^ (last seen 2s ago) [REGISTERED]
```

The output shows:
- **MAC address** in standard format
- **ENC** flag if device uses encryption
- **Parsed sensor values** from the last received advertisement
- **Last seen time** for monitoring device availability
- **[REGISTERED]** tag for devices configured in your YAML

:::tip[Disable After Discovery]
Set `dump_interval: 0` or remove it after discovering your devices to reduce log output.
:::

## Basic Configuration

### Hub Setup

First, configure the BTHome receiver hub:

```yaml
bthome_receiver:
  devices:
    - mac_address: "AA:BB:CC:DD:EE:FF"
      name: "Living Room Sensor"
```

### Receiving Sensors

Configure sensors to receive data from a specific device:

```yaml
sensor:
  - platform: bthome_receiver
    mac_address: "AA:BB:CC:DD:EE:FF"
    temperature:
      name: "Living Room Temperature"
    humidity:
      name: "Living Room Humidity"
    battery:
      name: "Living Room Battery"
```

### Receiving Binary Sensors

Configure binary sensors for motion, door, window, etc.:

```yaml
binary_sensor:
  - platform: bthome_receiver
    mac_address: "AA:BB:CC:DD:EE:FF"
    motion:
      name: "Living Room Motion"
    door:
      name: "Front Door"
```

### Receiving Text Sensors

Configure text sensors for UTF-8 text or raw binary data:

```yaml
text_sensor:
  - platform: bthome_receiver
    mac_address: "AA:BB:CC:DD:EE:FF"
    text:
      name: "Device Status Text"
    raw:
      name: "Raw Data"
```

## Configuration Options

### Hub Configuration

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `ble_stack` | string | No | `bluedroid` | BLE stack to use: `bluedroid` or `nimble` |
| `dump_interval` | time | No | `0` | Interval for periodic device dump (e.g., `10s`, `1min`). Set to `0` to disable. |
| `devices` | list | No | `[]` | List of known devices with optional encryption keys |

#### Device Entry

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `mac_address` | MAC | Yes | Device MAC address in format `AA:BB:CC:DD:EE:FF` |
| `name` | string | No | Friendly name for the device |
| `encryption_key` | string | No | 32 hex characters (16 bytes) for AES-128-CCM decryption |
| `on_button` | trigger | No | Automation trigger for button events |
| `on_dimmer` | trigger | No | Automation trigger for dimmer events |

### Sensor Platform

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `mac_address` | MAC | Yes | Device MAC address |
| `encryption_key` | string | No | 32 hex characters (16 bytes) for AES-128-CCM decryption |
| `[sensor_type]` | sensor | No | Any supported sensor type (see tables below) |

### Binary Sensor Platform

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `mac_address` | MAC | Yes | Device MAC address |
| `encryption_key` | string | No | 32 hex characters (16 bytes) for AES-128-CCM decryption |
| `[binary_sensor_type]` | binary_sensor | No | Any supported binary sensor type (see table below) |

### Text Sensor Platform

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `mac_address` | MAC | Yes | Device MAC address |
| `encryption_key` | string | No | 32 hex characters (16 bytes) for AES-128-CCM decryption |
| `text` | text_sensor | No | UTF-8 text string (object ID 0x53) |
| `raw` | text_sensor | No | Raw binary data as hex string (object ID 0x54) |

## Supported Sensor Types

The BTHome receiver supports all 60+ sensor types from the BTHome v2 specification:

### Basic Sensors

| Type | Object ID | Resolution | Unit | Description |
|------|-----------|------------|------|-------------|
| `packet_id` | 0x00 | 1 | - | Packet identifier for deduplication |
| `battery` | 0x01 | 1 | % | Battery level percentage |
| `temperature` | 0x02 | 0.01 | °C | Temperature (signed) |
| `humidity` | 0x03 | 0.01 | % | Relative humidity |
| `pressure` | 0x04 | 0.01 | hPa | Atmospheric pressure |
| `illuminance` | 0x05 | 0.01 | lux | Light intensity |
| `mass_kg` | 0x06 | 0.01 | kg | Mass in kilograms |
| `mass_lb` | 0x07 | 0.01 | lb | Mass in pounds |
| `dewpoint` | 0x08 | 0.01 | °C | Dew point temperature |
| `count_uint8` | 0x09 | 1 | - | 8-bit counter (0-255) |
| `energy` | 0x0A | 0.001 | kWh | Energy consumption |
| `power` | 0x0B | 0.01 | W | Power consumption |
| `voltage` | 0x0C | 0.001 | V | Voltage |
| `pm2_5` | 0x0D | 1 | µg/m³ | PM2.5 particulate matter |
| `pm10` | 0x0E | 1 | µg/m³ | PM10 particulate matter |
| `co2` | 0x12 | 1 | ppm | Carbon dioxide level |
| `tvoc` | 0x13 | 1 | µg/m³ | Total volatile organic compounds |
| `moisture` | 0x14 | 0.01 | % | Soil/material moisture |

### Extended Sensors

| Type | Object ID | Resolution | Unit | Description |
|------|-----------|------------|------|-------------|
| `humidity_uint8` | 0x2E | 1 | % | Humidity (8-bit) |
| `moisture_uint8` | 0x2F | 1 | % | Moisture (8-bit) |
| `count_uint16` | 0x3D | 1 | - | 16-bit counter |
| `count_uint32` | 0x3E | 1 | - | 32-bit counter |
| `rotation` | 0x3F | 0.1 | ° | Rotation angle |
| `distance_mm` | 0x40 | 1 | mm | Distance in millimeters |
| `distance_m` | 0x41 | 0.1 | m | Distance in meters |
| `duration` | 0x42 | 0.001 | s | Time duration |
| `current` | 0x43 | 0.001 | A | Current |
| `speed` | 0x44 | 0.01 | m/s | Speed |
| `temperature_01` | 0x45 | 0.1 | °C | Temperature (lower precision) |
| `uv_index` | 0x46 | 0.1 | - | UV index |
| `volume_l_01` | 0x47 | 0.1 | L | Volume (liters) |
| `volume_ml` | 0x48 | 1 | mL | Volume (milliliters) |
| `volume_flow_rate` | 0x49 | 0.001 | m³/hr | Flow rate |
| `voltage_01` | 0x4A | 0.1 | V | Voltage (lower precision) |
| `gas` | 0x4B | 0.001 | m³ | Gas consumption |
| `gas_uint32` | 0x4C | 0.001 | m³ | Gas consumption (32-bit) |
| `energy_uint32` | 0x4D | 0.001 | kWh | Energy (32-bit) |
| `volume_l` | 0x4E | 0.001 | L | Volume in liters |
| `water` | 0x4F | 0.001 | L | Water consumption |
| `timestamp` | 0x50 | 1 | s | Unix timestamp |
| `acceleration` | 0x51 | 0.001 | m/s² | Acceleration |
| `gyroscope` | 0x52 | 0.001 | °/s | Angular velocity |
| `volume_storage` | 0x55 | 0.001 | L | Storage volume |
| `conductivity` | 0x56 | 1 | µS/cm | Electrical conductivity |
| `temperature_sint8` | 0x57 | 1 | °C | Temperature (8-bit integer) |
| `temperature_sint8_035` | 0x58 | 0.35 | °C | Temperature (8-bit, 0.35°C steps) |
| `count_sint8` | 0x59 | 1 | - | 8-bit signed counter |
| `count_sint16` | 0x5A | 1 | - | 16-bit signed counter |
| `count_sint32` | 0x5B | 1 | - | 32-bit signed counter |
| `power_sint32` | 0x5C | 0.01 | W | Power (signed) |
| `current_sint16` | 0x5D | 0.001 | A | Current (signed) |
| `direction` | 0x5E | 0.01 | ° | Compass direction |
| `precipitation` | 0x5F | 0.1 | mm | Rainfall |
| `channel` | 0x60 | 1 | - | Channel number |
| `rotational_speed` | 0x61 | 1 | rpm | Rotational speed |

## Supported Binary Sensor Types

All 28 binary sensor types from BTHome v2 are supported:

| Type | Object ID | Device Class | Description |
|------|-----------|--------------|-------------|
| `generic_boolean` | 0x0F | - | Generic on/off |
| `power` | 0x10 | power | Power state |
| `opening` | 0x11 | opening | Generic opening |
| `battery_low` | 0x15 | battery | Battery low warning |
| `battery_charging` | 0x16 | battery_charging | Battery charging status |
| `carbon_monoxide` | 0x17 | carbon_monoxide | CO detector |
| `cold` | 0x18 | cold | Cold warning |
| `connectivity` | 0x19 | connectivity | Connectivity status |
| `door` | 0x1A | door | Door sensor |
| `garage_door` | 0x1B | garage_door | Garage door sensor |
| `gas` | 0x1C | gas | Gas detector |
| `heat` | 0x1D | heat | Heat warning |
| `light` | 0x1E | light | Light detection |
| `lock` | 0x1F | lock | Lock state |
| `moisture_binary` | 0x20 | moisture | Moisture detection |
| `motion` | 0x21 | motion | Motion detector |
| `moving` | 0x22 | moving | Movement detection |
| `occupancy` | 0x23 | occupancy | Occupancy sensor |
| `plug` | 0x24 | plug | Plug state |
| `presence` | 0x25 | presence | Presence detection |
| `problem` | 0x26 | problem | Problem indicator |
| `running` | 0x27 | running | Running state |
| `safety` | 0x28 | safety | Safety status |
| `smoke` | 0x29 | smoke | Smoke detector |
| `sound` | 0x2A | sound | Sound detection |
| `tamper` | 0x2B | tamper | Tamper detection |
| `vibration` | 0x2C | vibration | Vibration detection |
| `window` | 0x2D | window | Window sensor |

## Encryption

To receive encrypted BTHome advertisements, specify the 16-byte AES-128 key as 32 hexadecimal characters.

### Method 1: Hub-Level Configuration

Register the device and encryption key in the hub:

```yaml
bthome_receiver:
  devices:
    - mac_address: "AA:BB:CC:DD:EE:FF"
      name: "Secure Sensor"
      encryption_key: "231d39c1d7cc1ab1aee224cd096db932"

sensor:
  - platform: bthome_receiver
    mac_address: "AA:BB:CC:DD:EE:FF"
    temperature:
      name: "Secure Temperature"
```

### Method 2: Platform-Level Configuration

Specify the encryption key directly in each platform configuration:

```yaml
sensor:
  - platform: bthome_receiver
    mac_address: "AA:BB:CC:DD:EE:FF"
    encryption_key: "231d39c1d7cc1ab1aee224cd096db932"
    temperature:
      name: "Secure Temperature"
    humidity:
      name: "Secure Humidity"

binary_sensor:
  - platform: bthome_receiver
    mac_address: "AA:BB:CC:DD:EE:FF"
    encryption_key: "231d39c1d7cc1ab1aee224cd096db932"
    motion:
      name: "Secure Motion"
```

:::note
The component automatically handles replay protection by tracking packet counters for encrypted devices.
:::

## Event Triggers

The BTHome receiver supports automation triggers for button and dimmer events.

### Button Events

Button events support multiple press types:

```yaml
bthome_receiver:
  devices:
    - mac_address: "AA:BB:CC:DD:EE:FF"
      name: "Smart Button"
      on_button:
        - button_index: 0
          event: "press"
          then:
            - light.toggle: living_room_light
        - button_index: 0
          event: "double_press"
          then:
            - scene.apply: movie_mode
        - button_index: 0
          event: "long_press"
          then:
            - light.turn_off: all_lights
```

#### Supported Button Events

- `none` (0x00) - No event
- `press` (0x01) - Single press
- `double_press` (0x02) - Double press
- `triple_press` (0x03) - Triple press
- `long_press` (0x04) - Long press
- `long_double_press` (0x05) - Long double press
- `long_triple_press` (0x06) - Long triple press
- `hold_press` (0x80) - Hold/continuous press

### Dimmer Events

Dimmer events provide step values for brightness control:

```yaml
bthome_receiver:
  devices:
    - mac_address: "AA:BB:CC:DD:EE:FF"
      name: "Smart Dimmer"
      on_dimmer:
        - then:
            - light.dim_relative:
                id: living_room_light
                relative_brightness: !lambda 'return steps * 0.05;'
```

The `steps` variable contains the dimmer step count (positive for increase, negative for decrease).

## Complete Examples

### Bluedroid Stack (Default)

Use this configuration when you need compatibility with other ESPHome BLE components:

```yaml
esphome:
  name: bthome-receiver-bluedroid

esp32:
  board: esp32dev
  framework:
    type: esp-idf

wifi:
  ap:
    ssid: "BTHome-Receiver"

captive_portal:

# Required for Bluedroid mode
esp32_ble_tracker:
  scan_parameters:
    active: false

# BTHome Receiver with Bluedroid (default)
bthome_receiver:
  ble_stack: bluedroid  # Can be omitted, this is the default
  # dump_interval: 10s  # Uncomment to discover devices
  devices:
    # Encrypted temperature sensor
    - mac_address: "AA:BB:CC:DD:EE:FF"
      name: "Living Room Sensor"
      encryption_key: "231d39c1d7cc1ab1aee224cd096db932"

    # Smart button with automation
    - mac_address: "11:22:33:44:55:66"
      name: "Bedroom Button"
      on_button:
        - button_index: 0
          event: "press"
          then:
            - logger.log: "Button pressed!"

# Receive sensor data
sensor:
  - platform: bthome_receiver
    mac_address: "AA:BB:CC:DD:EE:FF"
    temperature:
      name: "Living Room Temperature"
    humidity:
      name: "Living Room Humidity"
    battery:
      name: "Living Room Sensor Battery"

# Receive binary sensor data
binary_sensor:
  - platform: bthome_receiver
    mac_address: "AA:BB:CC:DD:EE:FF"
    motion:
      name: "Living Room Motion"
```

### NimBLE Stack (Lightweight)

Use this configuration for memory-constrained devices or receive-only gateways:

```yaml
esphome:
  name: bthome-receiver-nimble

esp32:
  board: seeed_xiao_esp32s3
  framework:
    type: esp-idf  # Required for NimBLE

wifi:
  ap:
    ssid: "BTHome-Receiver"

captive_portal:

# BTHome Receiver with NimBLE (lightweight, standalone)
# Note: Cannot coexist with esp32_ble_tracker or bluetooth_proxy
bthome_receiver:
  ble_stack: nimble
  # dump_interval: 10s  # Uncomment to discover devices
  devices:
    # Encrypted temperature sensor
    - mac_address: "AA:BB:CC:DD:EE:FF"
      name: "Living Room Sensor"
      encryption_key: "231d39c1d7cc1ab1aee224cd096db932"

    # Smart button with automation
    - mac_address: "11:22:33:44:55:66"
      name: "Bedroom Button"
      on_button:
        - button_index: 0
          event: "press"
          then:
            - logger.log: "Button pressed!"

# Receive sensor data
sensor:
  - platform: bthome_receiver
    mac_address: "AA:BB:CC:DD:EE:FF"
    temperature:
      name: "Living Room Temperature"
    humidity:
      name: "Living Room Humidity"
    battery:
      name: "Living Room Sensor Battery"

# Receive binary sensor data
binary_sensor:
  - platform: bthome_receiver
    mac_address: "AA:BB:CC:DD:EE:FF"
    motion:
      name: "Living Room Motion"
```

## Multiple Device Configuration

You can receive data from multiple BTHome devices by configuring multiple sensor/binary_sensor platforms:

```yaml
sensor:
  # Device 1
  - platform: bthome_receiver
    mac_address: "AA:BB:CC:DD:EE:FF"
    temperature:
      name: "Sensor 1 Temperature"

  # Device 2
  - platform: bthome_receiver
    mac_address: "11:22:33:44:55:66"
    temperature:
      name: "Sensor 2 Temperature"

  # Device 3 (encrypted)
  - platform: bthome_receiver
    mac_address: "77:88:99:AA:BB:CC"
    encryption_key: "231d39c1d7cc1ab1aee224cd096db932"
    temperature:
      name: "Sensor 3 Temperature"
```

## Tips and Best Practices

1. **Use discovery mode first** - Set `dump_interval: 10s` to find devices and see their sensor types before configuring
2. **Use encryption** for sensitive data or devices accessible in public areas
3. **Register devices in the hub** when using event triggers or hub-level encryption
4. **Monitor battery levels** by including the `battery` sensor for battery-powered devices
5. **BLE Scanner range** - Keep devices within 10-30 meters depending on environment
6. **Scan parameters** - Use `active: false` in `esp32_ble_tracker` for better compatibility
7. **Packet deduplication** - The receiver automatically handles duplicate packets using packet IDs
8. **Disable discovery mode** after configuring devices by removing `dump_interval` to reduce log output

## Troubleshooting

### Device not discovered

- **Enable discovery mode** by setting `dump_interval: 10s` to see all BTHome devices in range
- Verify the MAC address is correct (check the dump output or use a BLE scanner app)
- Ensure the device is within BLE range (typically 10-30 meters)
- For Bluedroid: Check that `esp32_ble_tracker` is configured and running
- Verify the device is broadcasting BTHome v2 advertisements (UUID 0xFCD2)

### Encrypted data not decrypted

- Set `dump_interval: 10s` to confirm the device is encrypted (look for "ENC" flag)
- Verify the encryption key matches the broadcasting device (32 hex characters)
- Check that the key is correctly formatted (no spaces or dashes)
- Ensure the device is broadcasting with encryption enabled (device info byte should be 0x41)

### Missing sensor values

- Set `dump_interval: 10s` to see exactly what sensor types the device broadcasts
- Verify the sensor type name matches what the device is broadcasting (check the object ID)
- Check the ESPHome logs for decoding errors
- Ensure the object ID in the advertisement matches the configured sensor type

## See Also

- [BTHome Protocol Specification](https://bthome.io/) - Official BTHome documentation
- [ESP32 BLE Tracker Component](https://esphome.io/components/esp32_ble_tracker.html) - ESPHome BLE tracker documentation
- [BTHome Broadcaster Component](/configuration/basic-setup) - Broadcast BTHome advertisements
