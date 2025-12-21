"""
BTHome Receiver Sensor Platform

Defines sensor entities for receiving BTHome v2 sensor data from BLE devices.
"""

import esphome.codegen as cg
from esphome.components import sensor
import esphome.config_validation as cv
from esphome.const import (
    CONF_ID,
    CONF_MAC_ADDRESS,
    DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_CURRENT,
    DEVICE_CLASS_DISTANCE,
    DEVICE_CLASS_DURATION,
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_ILLUMINANCE,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_PRESSURE,
    DEVICE_CLASS_SPEED,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_VOLTAGE,
    STATE_CLASS_MEASUREMENT,
    STATE_CLASS_TOTAL_INCREASING,
    UNIT_AMPERE,
    UNIT_CELSIUS,
    UNIT_DEGREES,
    UNIT_KILOGRAM,
    UNIT_KILOWATT_HOURS,
    UNIT_LUX,
    UNIT_METER,
    UNIT_MILLIMETER,
    UNIT_MICROGRAMS_PER_CUBIC_METER,
    UNIT_PARTS_PER_MILLION,
    UNIT_PERCENT,
    UNIT_HECTOPASCAL,
    UNIT_VOLT,
    UNIT_WATT,
    UNIT_SECOND,
)

# Not all units are defined in esphome.const
UNIT_METERS_PER_SECOND = "m/s"

from . import (
    BTHomeReceiverHub,
    BTHomeDevice,
    SENSOR_TYPES,
    CONF_ENCRYPTION_KEY,
    validate_encryption_key,
)

DEPENDENCIES = ["bthome_receiver"]

# Configuration key for sensor index (for multiple sensors of same type)
CONF_INDEX = "index"

# Map sensor type names to their metadata for ESPHome integration
# Format: type_name: (device_class, unit_of_measurement, state_class, accuracy_decimals)
SENSOR_METADATA = {
    # Basic sensors
    "packet_id": (None, None, None, 0),
    "battery": (DEVICE_CLASS_BATTERY, UNIT_PERCENT, STATE_CLASS_MEASUREMENT, 0),
    "temperature": (DEVICE_CLASS_TEMPERATURE, UNIT_CELSIUS, STATE_CLASS_MEASUREMENT, 2),
    "humidity": (DEVICE_CLASS_HUMIDITY, UNIT_PERCENT, STATE_CLASS_MEASUREMENT, 2),
    "pressure": (DEVICE_CLASS_PRESSURE, UNIT_HECTOPASCAL, STATE_CLASS_MEASUREMENT, 2),
    "illuminance": (DEVICE_CLASS_ILLUMINANCE, UNIT_LUX, STATE_CLASS_MEASUREMENT, 2),
    "mass_kg": (None, UNIT_KILOGRAM, STATE_CLASS_MEASUREMENT, 2),
    "mass_lb": (None, "lb", STATE_CLASS_MEASUREMENT, 2),
    "dewpoint": (DEVICE_CLASS_TEMPERATURE, UNIT_CELSIUS, STATE_CLASS_MEASUREMENT, 2),
    "count_uint8": (None, None, STATE_CLASS_MEASUREMENT, 0),
    "energy": (DEVICE_CLASS_ENERGY, UNIT_KILOWATT_HOURS, STATE_CLASS_TOTAL_INCREASING, 3),
    "power": (DEVICE_CLASS_POWER, UNIT_WATT, STATE_CLASS_MEASUREMENT, 2),
    "voltage": (DEVICE_CLASS_VOLTAGE, UNIT_VOLT, STATE_CLASS_MEASUREMENT, 3),
    "pm2_5": (None, UNIT_MICROGRAMS_PER_CUBIC_METER, STATE_CLASS_MEASUREMENT, 0),
    "pm10": (None, UNIT_MICROGRAMS_PER_CUBIC_METER, STATE_CLASS_MEASUREMENT, 0),
    "co2": (None, UNIT_PARTS_PER_MILLION, STATE_CLASS_MEASUREMENT, 0),
    "tvoc": (None, UNIT_MICROGRAMS_PER_CUBIC_METER, STATE_CLASS_MEASUREMENT, 0),
    "moisture": (None, UNIT_PERCENT, STATE_CLASS_MEASUREMENT, 2),
    "humidity_uint8": (DEVICE_CLASS_HUMIDITY, UNIT_PERCENT, STATE_CLASS_MEASUREMENT, 0),
    "moisture_uint8": (None, UNIT_PERCENT, STATE_CLASS_MEASUREMENT, 0),
    # Extended sensors
    "count_uint16": (None, None, STATE_CLASS_MEASUREMENT, 0),
    "count_uint32": (None, None, STATE_CLASS_TOTAL_INCREASING, 0),
    "rotation": (None, UNIT_DEGREES, STATE_CLASS_MEASUREMENT, 1),
    "distance_mm": (DEVICE_CLASS_DISTANCE, UNIT_MILLIMETER, STATE_CLASS_MEASUREMENT, 0),
    "distance_m": (DEVICE_CLASS_DISTANCE, UNIT_METER, STATE_CLASS_MEASUREMENT, 1),
    "duration": (DEVICE_CLASS_DURATION, UNIT_SECOND, STATE_CLASS_MEASUREMENT, 3),
    "current": (DEVICE_CLASS_CURRENT, UNIT_AMPERE, STATE_CLASS_MEASUREMENT, 3),
    "speed": (DEVICE_CLASS_SPEED, UNIT_METERS_PER_SECOND, STATE_CLASS_MEASUREMENT, 2),
    "temperature_01": (DEVICE_CLASS_TEMPERATURE, UNIT_CELSIUS, STATE_CLASS_MEASUREMENT, 1),
    "uv_index": (None, None, STATE_CLASS_MEASUREMENT, 1),
    "volume_l_01": (None, "L", STATE_CLASS_MEASUREMENT, 1),
    "volume_ml": (None, "mL", STATE_CLASS_MEASUREMENT, 0),
    "volume_flow_rate": (None, "m³/hr", STATE_CLASS_MEASUREMENT, 3),
    "voltage_01": (DEVICE_CLASS_VOLTAGE, UNIT_VOLT, STATE_CLASS_MEASUREMENT, 1),
    "gas": (None, "m³", STATE_CLASS_TOTAL_INCREASING, 3),
    "gas_uint32": (None, "m³", STATE_CLASS_TOTAL_INCREASING, 3),
    "energy_uint32": (DEVICE_CLASS_ENERGY, UNIT_KILOWATT_HOURS, STATE_CLASS_TOTAL_INCREASING, 3),
    "volume_l": (None, "L", STATE_CLASS_TOTAL_INCREASING, 3),
    "water": (None, "L", STATE_CLASS_TOTAL_INCREASING, 3),
    "timestamp": (None, "s", None, 0),
    "acceleration": (None, "m/s²", STATE_CLASS_MEASUREMENT, 3),
    "gyroscope": (None, "°/s", STATE_CLASS_MEASUREMENT, 3),
    "volume_storage": (None, "L", STATE_CLASS_MEASUREMENT, 3),
    "conductivity": (None, "µS/cm", STATE_CLASS_MEASUREMENT, 0),
    "temperature_sint8": (DEVICE_CLASS_TEMPERATURE, UNIT_CELSIUS, STATE_CLASS_MEASUREMENT, 0),
    "temperature_sint8_035": (DEVICE_CLASS_TEMPERATURE, UNIT_CELSIUS, STATE_CLASS_MEASUREMENT, 2),
    "count_sint8": (None, None, STATE_CLASS_MEASUREMENT, 0),
    "count_sint16": (None, None, STATE_CLASS_MEASUREMENT, 0),
    "count_sint32": (None, None, STATE_CLASS_MEASUREMENT, 0),
    "power_sint32": (DEVICE_CLASS_POWER, UNIT_WATT, STATE_CLASS_MEASUREMENT, 2),
    "current_sint16": (DEVICE_CLASS_CURRENT, UNIT_AMPERE, STATE_CLASS_MEASUREMENT, 3),
    "direction": (None, UNIT_DEGREES, STATE_CLASS_MEASUREMENT, 2),
    "precipitation": (None, "mm", STATE_CLASS_MEASUREMENT, 1),
    "channel": (None, None, None, 0),
    "rotational_speed": (None, "rpm", STATE_CLASS_MEASUREMENT, 0),
}


def sensor_schema(sensor_type):
    """Generate schema for a specific sensor type.

    Supports either a single sensor config or a list of configs with index.
    Examples:
        temperature_01:
          name: "Temperature"

        speed:  # Multiple sensors of same type
          - name: "Wind Speed"
            index: 0
          - name: "Wind Gusts"
            index: 1
    """
    if sensor_type not in SENSOR_TYPES:
        return None

    metadata = SENSOR_METADATA.get(sensor_type, (None, None, STATE_CLASS_MEASUREMENT, 2))
    device_class, unit, state_class, decimals = metadata

    schema_kwargs = {"accuracy_decimals": decimals}
    if device_class:
        schema_kwargs["device_class"] = device_class
    if unit:
        schema_kwargs["unit_of_measurement"] = unit
    if state_class:
        schema_kwargs["state_class"] = state_class

    # Base sensor schema with optional index
    base_schema = sensor.sensor_schema(**schema_kwargs).extend({
        cv.Optional(CONF_INDEX, default=0): cv.int_range(min=0, max=255),
    })

    # Allow either single config or list of configs
    return cv.Any(base_schema, cv.ensure_list(base_schema))


# Build CONFIG_SCHEMA dynamically with all sensor types
_schema_dict = {
    cv.GenerateID(): cv.declare_id(BTHomeDevice),
    cv.Required(CONF_MAC_ADDRESS): cv.mac_address,
    cv.Optional(CONF_ENCRYPTION_KEY): validate_encryption_key,
    cv.GenerateID("bthome_receiver_id"): cv.use_id(BTHomeReceiverHub),
}

# Add all sensor types as optional configuration keys
for _sensor_type in SENSOR_TYPES.keys():
    _schema = sensor_schema(_sensor_type)
    if _schema:
        _schema_dict[cv.Optional(_sensor_type)] = _schema

CONFIG_SCHEMA = cv.Schema(_schema_dict)


async def to_code(config):
    """Generate C++ code for the sensor platform."""
    hub = await cg.get_variable(config["bthome_receiver_id"])
    mac = config[CONF_MAC_ADDRESS]

    # Create the BTHomeDevice
    device_var = cg.new_Pvariable(config[CONF_ID], hub)
    cg.add(device_var.set_mac_address(mac.as_hex))

    # Set encryption key if provided
    if CONF_ENCRYPTION_KEY in config:
        key = config[CONF_ENCRYPTION_KEY]
        key_bytes = [cg.RawExpression(f"0x{key[i:i+2]}") for i in range(0, len(key), 2)]
        key_array = cg.RawExpression(f"std::array<uint8_t, 16>{{{{{', '.join(str(b) for b in key_bytes)}}}}}")
        cg.add(device_var.set_encryption_key(key_array))

    # Register each configured sensor type
    for sensor_type, type_info in SENSOR_TYPES.items():
        if sensor_type in config:
            sensor_configs = config[sensor_type]
            object_id = type_info[0]  # First element is object_id

            # Normalize to list (handles both single config and list of configs)
            if not isinstance(sensor_configs, list):
                sensor_configs = [sensor_configs]

            for sensor_config in sensor_configs:
                # Get index (default 0)
                index = sensor_config.get(CONF_INDEX, 0)

                # Create the ESPHome sensor
                sens = await sensor.new_sensor(sensor_config)

                # Register sensor with device (object_id, index, sensor*)
                cg.add(device_var.add_sensor(object_id, index, sens))

    # Register device with hub
    cg.add(hub.register_device(device_var))
