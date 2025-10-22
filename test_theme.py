"""
Test script for Theme Manager
"""
from utils.theme_manager import theme

print("=" * 50)
print("🧪 TESTING THEME MANAGER")
print("=" * 50)

# Test 1: Get default theme
print("\n📌 Test 1: Default Theme")
print(f"Current theme: {theme.get_theme()}")
print(f"Stylesheet preview (first 200 chars):\n{theme.get_stylesheet()[:200]}...")

# Test 2: Get full Light theme stylesheet
print("\n📌 Test 2: Light Theme Stylesheet")
print(f"Theme: {theme.get_theme()}")
light_style = theme.get_stylesheet()
print(f"Stylesheet length: {len(light_style)} characters")
print(f"Contains 'QMainWindow': {'QMainWindow' in light_style}")
print(f"Contains 'sidebar': {'sidebar' in light_style}")

# Test 3: Switch to Dark theme
print("\n📌 Test 3: Switch to Dark Theme")
theme.set_theme('dark')
print(f"Current theme: {theme.get_theme()}")
dark_style = theme.get_stylesheet()
print(f"Stylesheet length: {len(dark_style)} characters")
print(f"Stylesheet preview (first 200 chars):\n{dark_style[:200]}...")

# Test 4: Compare themes
print("\n📌 Test 4: Compare Themes")
print(f"Light theme length: {len(light_style)}")
print(f"Dark theme length: {len(dark_style)}")
print(f"Themes are different: {light_style != dark_style}")

# Test 5: Switch back to Light
print("\n📌 Test 5: Switch Back to Light")
theme.set_theme('light')
print(f"Current theme: {theme.get_theme()}")

# Test 6: Test invalid theme
print("\n📌 Test 6: Invalid Theme")
theme.set_theme('invalid_theme')
print(f"Current theme (should still be 'light'): {theme.get_theme()}")

# Test 7: Observer pattern
print("\n📌 Test 7: Observer Pattern")
observer_called = []

def on_theme_change():
    observer_called.append(True)
    print("  🔔 Observer notified! Theme changed.")

theme.add_observer(on_theme_change)
print("Observer added. Changing theme to 'dark'...")
theme.set_theme('dark')
print(f"Observer was called: {len(observer_called) > 0}")

# Test 8: Check key QSS elements
print("\n📌 Test 8: Check Key QSS Elements")
current_style = theme.get_stylesheet()
elements = [
    'QMainWindow',
    'QWidget',
    'QPushButton',
    'QLineEdit',
    'QTableWidget',
    'QScrollBar',
    'sidebar'
]
print("Checking if key elements are in stylesheet:")
for element in elements:
    present = element in current_style
    status = "✓" if present else "✗"
    print(f"  {status} {element}: {present}")

print("\n" + "=" * 50)
print("✅ TESTS COMPLETED!")
print("=" * 50)
