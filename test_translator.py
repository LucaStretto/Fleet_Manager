"""
Test script for Translator
"""
from utils.translator import tr

print("=" * 50)
print("🧪 TESTING TRANSLATOR")
print("=" * 50)

# Test 1: Greek (default)
print("\n📌 Test 1: Greek (Default Language)")
print(f"Current language: {tr.get_language()}")
print(f"app_title: {tr('app_title')}")
print(f"add_vehicle: {tr('add_vehicle')}")
print(f"license_plate: {tr('license_plate')}")
print(f"search: {tr('search')}")

# Test 2: Switch to English
print("\n📌 Test 2: Switch to English")
tr.set_language('en')
print(f"Current language: {tr.get_language()}")
print(f"app_title: {tr('app_title')}")
print(f"add_vehicle: {tr('add_vehicle')}")
print(f"license_plate: {tr('license_plate')}")
print(f"search: {tr('search')}")

# Test 3: Back to Greek
print("\n📌 Test 3: Switch back to Greek")
tr.set_language('el')
print(f"Current language: {tr.get_language()}")
print(f"menu_vehicles: {tr('menu_vehicles')}")
print(f"menu_drivers: {tr('menu_drivers')}")
print(f"menu_maintenance: {tr('menu_maintenance')}")

# Test 4: Missing key (fallback)
print("\n📌 Test 4: Missing Key (Fallback)")
print(f"nonexistent_key: {tr('nonexistent_key')}")
print(f"nonexistent_key with fallback: {tr('nonexistent_key', 'Custom Fallback')}")

# Test 5: All vehicle-related keys
print("\n📌 Test 5: Vehicle Fields (Greek)")
vehicle_fields = [
    'license_plate', 'brand', 'model', 'year', 'vin', 
    'color', 'fuel_type', 'engine', 'transmission', 'mileage', 'status'
]
for field in vehicle_fields:
    print(f"{field}: {tr(field)}")

print("\n" + "=" * 50)
print("✅ TESTS COMPLETED!")
print("=" * 50)
