# ESPHome BTHome Component

A custom ESPHome component that broadcasts sensor data using the [BTHome v2](https://bthome.io/) BLE protocol. BTHome is an open standard natively supported by Home Assistant and other home automation platforms.

## Features

- **BTHome v2 Protocol** - Full compliance with the [BTHome v2 specification](https://bthome.io/format/)
- **Multi-Platform** - Supports ESP32 (ESP-IDF) and nRF52 (Zephyr) platforms
- **60+ Sensor Types** - Temperature, humidity, pressure, power, energy, and many more
- **28 Binary Sensor Types** - Motion, door, window, smoke, occupancy, etc.
- **AES-CCM Encryption** - Optional 128-bit encryption for secure broadcasts
- **Immediate Advertising** - Instant broadcast on state change for time-critical sensors
- **Configurable TX Power** - Adjust transmission power for range/battery trade-off
- **Home Assistant Auto-Discovery** - Devices appear automatically in Home Assistant

## Installation

Add the component to your ESPHome configuration:

```yaml
external_components:
  - source:
      type: local
      path: components
    components: [bthome]
```

Or from a git repository:

```yaml
external_components:
  - source:
      type: git
      url: https://github.com/yourusername/esphome-bthome
    components: [bthome]
```

## Platform Requirements

### ESP32

Requires ESP-IDF framework and the `esp32_ble` component:

```yaml
esp32:
  board: esp32dev
  framework:
    type: esp-idf

esp32_ble:
  id: ble
```

### nRF52

Requires Zephyr framework:

```yaml
nrf52:
  board: xiao_ble
  bootloader: adafruit
```

## Configuration

```yaml
bthome:
  # Advertising interval (20ms - 10240ms)
  min_interval: 5s
  max_interval: 10s

  # TX power in dBm
  # ESP32: -12, -9, -6, -3, 0, 3, 6, 9
  # nRF52: -40, -20, -16, -12, -8, -4, 0, 2, 3, 4, 5, 6, 7, 8
  tx_power: 0

  # Optional: 16-byte AES encryption key (32 hex characters)
  # Generate with: openssl rand -hex 16
  # encryption_key: "231d39c1d7cc1ab1aee224cd096db932"

  # Sensor measurements
  sensors:
    - type: temperature
      id: my_temperature_sensor
    - type: humidity
      id: my_humidity_sensor
    - type: battery
      id: my_battery_sensor

  # Binary sensor measurements
  binary_sensors:
    - type: motion
      id: my_motion_sensor
      advertise_immediately: true  # Instant broadcast on state change
    - type: door
      id: my_door_sensor
      advertise_immediately: true
```

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `min_interval` | time | `1s` | Minimum advertising interval (20ms - 10240ms) |
| `max_interval` | time | `1s` | Maximum advertising interval (20ms - 10240ms) |
| `tx_power` | int | `0` | Transmission power in dBm |
| `encryption_key` | string | - | Optional 32-character hex key for AES-CCM encryption |
| `sensors` | list | - | List of sensor measurements to broadcast |
| `binary_sensors` | list | - | List of binary sensor measurements to broadcast |

### Sensor Entry Options

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `type` | string | Yes | BTHome sensor type (see list below) |
| `id` | id | Yes | Reference to an ESPHome sensor |
| `advertise_immediately` | bool | No | Broadcast immediately on state change (default: false) |

## Supported Sensor Types

### Basic Sensors
| Type | Object ID | Resolution | Unit |
|------|-----------|------------|------|
| `packet_id` | 0x00 | 1 | - |
| `battery` | 0x01 | 1 | % |
| `temperature` | 0x02 | 0.01 | °C |
| `humidity` | 0x03 | 0.01 | % |
| `pressure` | 0x04 | 0.01 | hPa |
| `illuminance` | 0x05 | 0.01 | lux |
| `mass_kg` | 0x06 | 0.01 | kg |
| `mass_lb` | 0x07 | 0.01 | lb |
| `dewpoint` | 0x08 | 0.01 | °C |

### Environmental Sensors
| Type | Object ID | Resolution | Unit |
|------|-----------|------------|------|
| `co2` | 0x12 | 1 | ppm |
| `tvoc` | 0x13 | 1 | µg/m³ |
| `moisture` | 0x14 | 0.01 | % |
| `pm2_5` | 0x0D | 1 | µg/m³ |
| `pm10` | 0x0E | 1 | µg/m³ |

### Electrical Sensors
| Type | Object ID | Resolution | Unit |
|------|-----------|------------|------|
| `voltage` | 0x0C | 0.001 | V |
| `current` | 0x43 | 0.001 | A |
| `power` | 0x0B | 0.01 | W |
| `energy` | 0x0A | 0.001 | kWh |

### Count Sensors
| Type | Object ID | Signed | Bytes |
|------|-----------|--------|-------|
| `count_uint8` | 0x09 | No | 1 |
| `count_uint16` | 0x3D | No | 2 |
| `count_uint32` | 0x3E | No | 4 |
| `count_sint8` | 0x59 | Yes | 1 |
| `count_sint16` | 0x5A | Yes | 2 |
| `count_sint32` | 0x5B | Yes | 4 |

### Distance & Motion
| Type | Object ID | Resolution | Unit |
|------|-----------|------------|------|
| `distance_mm` | 0x40 | 1 | mm |
| `distance_m` | 0x41 | 0.1 | m |
| `rotation` | 0x3F | 0.1 | ° |
| `speed` | 0x44 | 0.01 | m/s |
| `acceleration` | 0x51 | 0.001 | m/s² |
| `gyroscope` | 0x52 | 0.001 | °/s |
| `direction` | 0x5E | 0.01 | ° |

### Volume & Flow
| Type | Object ID | Resolution | Unit |
|------|-----------|------------|------|
| `volume_l_01` | 0x47 | 0.1 | L |
| `volume_ml` | 0x48 | 1 | mL |
| `volume_l` | 0x4E | 0.001 | L |
| `volume_flow_rate` | 0x49 | 0.001 | m³/hr |
| `water` | 0x4F | 0.001 | L |
| `gas` | 0x4B | 0.001 | m³ |
| `gas_uint32` | 0x4C | 0.001 | m³ |

### Other Sensors
| Type | Object ID | Resolution | Unit |
|------|-----------|------------|------|
| `duration` | 0x42 | 0.001 | s |
| `timestamp` | 0x50 | 1 | s |
| `uv_index` | 0x46 | 0.1 | - |
| `conductivity` | 0x56 | 1 | µS/cm |
| `precipitation` | 0x5F | 0.1 | mm |
| `channel` | 0x60 | 1 | - |
| `rotational_speed` | 0x61 | 1 | rpm |

### Alternate Precision Types
| Type | Object ID | Resolution | Unit |
|------|-----------|------------|------|
| `humidity_uint8` | 0x2E | 1 | % |
| `moisture_uint8` | 0x2F | 1 | % |
| `temperature_01` | 0x45 | 0.1 | °C |
| `voltage_01` | 0x4A | 0.1 | V |
| `temperature_sint8` | 0x57 | 1 | °C |
| `energy_uint32` | 0x4D | 0.001 | kWh |
| `power_sint32` | 0x5C | 0.01 | W |
| `current_sint16` | 0x5D | 0.001 | A |

## Supported Binary Sensor Types

| Type | Object ID | States |
|------|-----------|--------|
| `generic_boolean` | 0x0F | off/on |
| `power` | 0x10 | off/on |
| `opening` | 0x11 | closed/open |
| `battery_low` | 0x15 | normal/low |
| `battery_charging` | 0x16 | not charging/charging |
| `carbon_monoxide` | 0x17 | clear/detected |
| `cold` | 0x18 | normal/cold |
| `connectivity` | 0x19 | disconnected/connected |
| `door` | 0x1A | closed/open |
| `garage_door` | 0x1B | closed/open |
| `gas` | 0x1C | clear/detected |
| `heat` | 0x1D | normal/hot |
| `light` | 0x1E | no light/light |
| `lock` | 0x1F | locked/unlocked |
| `moisture_binary` | 0x20 | dry/wet |
| `motion` | 0x21 | clear/detected |
| `moving` | 0x22 | not moving/moving |
| `occupancy` | 0x23 | clear/detected |
| `plug` | 0x24 | unplugged/plugged |
| `presence` | 0x25 | away/home |
| `problem` | 0x26 | ok/problem |
| `running` | 0x27 | not running/running |
| `safety` | 0x28 | unsafe/safe |
| `smoke` | 0x29 | clear/detected |
| `sound` | 0x2A | clear/detected |
| `tamper` | 0x2B | off/on |
| `vibration` | 0x2C | clear/detected |
| `window` | 0x2D | closed/open |

## Encryption

BTHome supports AES-CCM encryption for secure broadcasts. To enable:

1. Generate a 16-byte key:
   ```bash
   openssl rand -hex 16
   ```

2. Add the key to your configuration:
   ```yaml
   bthome:
     encryption_key: "231d39c1d7cc1ab1aee224cd096db932"
   ```

3. In Home Assistant, add the same key when configuring the BTHome device.

## Example Configurations

### ESP32 Temperature/Humidity Sensor

```yaml
esphome:
  name: bthome-sensor

esp32:
  board: esp32dev
  framework:
    type: esp-idf

esp32_ble:
  id: ble

external_components:
  - source:
      type: local
      path: components
    components: [bthome]

sensor:
  - platform: dht
    pin: GPIO4
    model: DHT22
    temperature:
      id: dht_temp
    humidity:
      id: dht_hum
    update_interval: 30s

bthome:
  min_interval: 5s
  max_interval: 10s
  sensors:
    - type: temperature
      id: dht_temp
    - type: humidity
      id: dht_hum
```

### nRF52 Motion Sensor with Deep Sleep

```yaml
esphome:
  name: bthome-motion

nrf52:
  board: xiao_ble
  bootloader: adafruit

external_components:
  - source:
      type: local
      path: components
    components: [bthome]

deep_sleep:
  run_duration: 10s
  sleep_duration: 5min
  wakeup_pin:
    number: GPIO2
    mode: INPUT_PULLDOWN

binary_sensor:
  - platform: gpio
    pin:
      number: GPIO2
      mode: INPUT_PULLDOWN
    id: pir_motion
    device_class: motion

bthome:
  min_interval: 1s
  max_interval: 5s
  tx_power: 4
  binary_sensors:
    - type: motion
      id: pir_motion
      advertise_immediately: true
```

## Home Assistant Integration

BTHome devices are automatically discovered by Home Assistant through the [BTHome integration](https://www.home-assistant.io/integrations/bthome/). No additional configuration is needed.

If using encryption, you'll be prompted to enter the encryption key when adding the device.

## Protocol Details

- **Service UUID**: 0xFCD2 (sponsored by Allterco Robotics/Shelly)
- **Device Info Byte**: 0x40 (unencrypted) or 0x41 (encrypted)
- **Version**: BTHome v2 (bits 5-7 of device info = 0b010)
- **Encryption**: AES-CCM with 4-byte MIC
- **Nonce**: MAC (6) + UUID (2) + Device Info (1) + Counter (4) = 13 bytes

## License

MIT License - See [bthome.io](https://bthome.io/) for protocol specification.
