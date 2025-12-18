import 'dart:async';
import 'package:flutter/foundation.dart';
import 'package:flutter_blue_plus/flutter_blue_plus.dart';
import '../models/bthome_device.dart';
import 'key_storage.dart';

/// BLE Scanner service for discovering BTHome devices
class BleScanner extends ChangeNotifier {
  final Map<String, BthomeDevice> _devices = {};
  final Map<String, Uint8List> _keyCache = {};
  bool _isScanning = false;
  String? _error;
  StreamSubscription<List<ScanResult>>? _scanSubscription;
  StreamSubscription<BluetoothAdapterState>? _adapterSubscription;
  BluetoothAdapterState _adapterState = BluetoothAdapterState.unknown;

  /// All discovered BTHome devices (sorted by RSSI)
  List<BthomeDevice> get devices {
    final list = _devices.values.toList();
    // Sort by RSSI (stronger signal first)
    list.sort((a, b) => b.rssi.compareTo(a.rssi));
    return list;
  }

  /// Whether scanning is currently active
  bool get isScanning => _isScanning;

  /// Current error message, if any
  String? get error => _error;

  /// Bluetooth adapter state
  BluetoothAdapterState get adapterState => _adapterState;

  /// Whether Bluetooth is available and on
  bool get isBluetoothReady => _adapterState == BluetoothAdapterState.on;

  BleScanner() {
    FlutterBluePlus.setLogLevel(LogLevel.warning, color: false);
    _initAdapterListener();
    _loadKeys();
  }

  void _initAdapterListener() {
    _adapterSubscription = FlutterBluePlus.adapterState.listen((state) {
      _adapterState = state;
      notifyListeners();

      if (state == BluetoothAdapterState.on && !_isScanning) {
        // Auto-start scanning when Bluetooth becomes available
        startScan();
      } else if (state != BluetoothAdapterState.on && _isScanning) {
        stopScan();
      }
    });
  }

  Future<void> _loadKeys() async {
    final storedDevices = await KeyStorage.getStoredDevices();
    for (final mac in storedDevices) {
      final key = await KeyStorage.getKey(mac);
      if (key != null) {
        _keyCache[mac.toUpperCase().replaceAll(':', '').replaceAll('-', '')] = key;
      }
    }
  }

  /// Add or update encryption key for a device
  Future<void> setKey(String macAddress, String keyHex) async {
    await KeyStorage.setKeyFromHex(macAddress, keyHex);
    final key = await KeyStorage.getKey(macAddress);
    if (key != null) {
      final normalizedMac = macAddress.toUpperCase().replaceAll(':', '').replaceAll('-', '');
      _keyCache[normalizedMac] = key;
      if (_devices.containsKey(macAddress)) {
        notifyListeners();
      }
    }
  }

  /// Remove encryption key for a device
  Future<void> removeKey(String macAddress) async {
    await KeyStorage.removeKey(macAddress);
    final normalizedMac = macAddress.toUpperCase().replaceAll(':', '').replaceAll('-', '');
    _keyCache.remove(normalizedMac);
    notifyListeners();
  }

  /// Check if device has stored key
  bool hasKey(String macAddress) {
    final normalizedMac = macAddress.toUpperCase().replaceAll(':', '').replaceAll('-', '');
    return _keyCache.containsKey(normalizedMac);
  }

  /// Start scanning for BTHome devices
  Future<void> startScan() async {
    if (_isScanning) return;

    _error = null;

    if (_adapterState != BluetoothAdapterState.on) {
      _error = 'Bluetooth is not available';
      notifyListeners();
      return;
    }

    try {
      _isScanning = true;
      notifyListeners();

      _scanSubscription = FlutterBluePlus.onScanResults.listen(
        _handleScanResults,
        onError: (e) {
          _error = 'Scan error: $e';
          _isScanning = false;
          notifyListeners();
        },
      );

      // Auto-cancel subscription when scan completes
      FlutterBluePlus.cancelWhenScanComplete(_scanSubscription!);

      // Continuous scanning - no timeout
      // BTHome uses service DATA (0xFCD2), not advertised service UUIDs
      await FlutterBluePlus.startScan(
        androidScanMode: AndroidScanMode.lowLatency,
        continuousUpdates: true,
      );
    } catch (e) {
      _error = 'Failed to start scan: $e';
      _isScanning = false;
      notifyListeners();
    }
  }

  void _handleScanResults(List<ScanResult> results) async {
    for (final result in results) {
      final macAddress = result.device.remoteId.str;
      final name = result.advertisementData.advName;
      final serviceData = result.advertisementData.serviceData;

      // Check if this device has BTHome service data
      // Use string comparison since Guid equality may fail
      final bthomeKey = serviceData.keys.firstWhere(
        (key) => key.str.toLowerCase().contains('fcd2'),
        orElse: () => Guid('00000000-0000-0000-0000-000000000000'),
      );
      final hasBthomeData = bthomeKey.str.toLowerCase().contains('fcd2');

      if (hasBthomeData) {
        final data = serviceData[bthomeKey]!;
        final normalizedMac = macAddress.toUpperCase().replaceAll(':', '').replaceAll('-', '');

        // Extract scan response data
        final txPowerLevel = result.advertisementData.txPowerLevel;
        final appearance = result.advertisementData.appearance;

        // Extract manufacturer data (first entry if exists)
        int? manufacturerId;
        Uint8List? manufacturerData;
        if (result.advertisementData.manufacturerData.isNotEmpty) {
          final entry = result.advertisementData.manufacturerData.entries.first;
          manufacturerId = entry.key;
          manufacturerData = Uint8List.fromList(entry.value);
        }

        final device = await BthomeParser.parse(
          macAddress: macAddress,
          name: name.isNotEmpty ? name : null,
          rssi: result.rssi,
          serviceData: Uint8List.fromList(data),
          encryptionKey: _keyCache[normalizedMac],
          txPowerLevel: txPowerLevel,
          appearance: appearance,
          manufacturerId: manufacturerId,
          manufacturerData: manufacturerData,
        );

        if (device != null) {
          // Merge measurements from multiple packets (e.g., weather stations)
          final existing = _devices[macAddress];
          if (existing != null && device.measurements.isNotEmpty) {
            // Create a map of measurements by type for merging
            final measurementMap = <int, BthomeMeasurement>{};

            // Add existing measurements first
            for (final m in existing.measurements) {
              measurementMap[m.type.objectId] = m;
            }

            // Update/add new measurements
            for (final m in device.measurements) {
              measurementMap[m.type.objectId] = m;
            }

            // Create merged device with combined measurements
            _devices[macAddress] = device.copyWith(
              measurements: measurementMap.values.toList(),
              // Preserve existing scan response data if new one is missing
              txPowerLevel: device.txPowerLevel ?? existing.txPowerLevel,
              appearance: device.appearance ?? existing.appearance,
              manufacturerId: device.manufacturerId ?? existing.manufacturerId,
              esphomeVersion: device.esphomeVersion ?? existing.esphomeVersion,
            );
          } else {
            _devices[macAddress] = device;
          }
          notifyListeners();
        }
      }
      // Skip non-BTHome devices - only show BTHome devices
    }
  }

  /// Stop scanning
  Future<void> stopScan() async {
    if (!_isScanning) return;

    try {
      await FlutterBluePlus.stopScan();
    } catch (e) {
      // Ignore stop scan errors
    }

    _isScanning = false;
    await _scanSubscription?.cancel();
    _scanSubscription = null;
    notifyListeners();
  }

  /// Clear all discovered devices
  void clearDevices() {
    _devices.clear();
    notifyListeners();
  }

  /// Refresh scan (stop and start)
  Future<void> refresh() async {
    await stopScan();
    clearDevices();
    await startScan();
  }

  @override
  void dispose() {
    stopScan();
    _adapterSubscription?.cancel();
    super.dispose();
  }
}
