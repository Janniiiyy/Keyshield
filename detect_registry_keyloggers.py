import winreg

# List of registry keys where malware often hides
REGISTRY_PATHS = [
    r"Software\Microsoft\Windows\CurrentVersion\Run",
    r"Software\Microsoft\Windows\CurrentVersion\RunOnce",
    r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run",
]

# List of suspicious process names
SUSPICIOUS_NAMES = ["keylogger", "logger", "stealer", "record"]

def scan_registry_for_keyloggers():
    print("\n🔍 Scanning Windows Registry for startup programs...\n")
    
    found = False
    for reg_path in REGISTRY_PATHS:
        print(f"📂 Checking: {reg_path}")  # Debugging print statement

        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_READ) as key:
                i = 0
                while True:
                    try:
                        value_name, value_data, _ = winreg.EnumValue(key, i)
                        print(f"🔹 Found Registry Entry: {value_name} -> {value_data}")  # Show all entries

                        if any(susp_name in value_data.lower() for susp_name in SUSPICIOUS_NAMES):
                            print(f"⚠️ Suspicious Registry Entry Found: {value_name} -> {value_data}")
                            found = True
                    except OSError:
                        break
                    i += 1
        except FileNotFoundError:
            print(f"❌ Registry key not found: {reg_path}")  # Debugging print statement
            continue
    
    if not found:
        print("✅ No suspicious registry entries found.")

# Run the function
if __name__ == "__main__":
    scan_registry_for_keyloggers()
    
    choice = input("\nDo you want to remove detected threats? (yes/no): ")
if choice.lower() == "yes":
    print("\n🔄 Attempting to remove detected threats...")
    found_any = False  # Track if any threats were found

    for reg_path in REGISTRY_PATHS:
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_READ) as key:
                i = 0
                while True:
                    try:
                        value_name, value_data, _ = winreg.EnumValue(key, i)
                        if any(susp_name in value_data.lower() for susp_name in SUSPICIOUS_NAMES):
                            print(f"🚨 Removing: {value_name} -> {value_data}")  # Debugging print
                            remove_registry_entry(reg_path, value_name)
                            found_any = True
                    except OSError:
                        break
                    i += 1
        except FileNotFoundError:
            continue
    
    if not found_any:
        print("✅ No suspicious registry entries to remove.")  # Debugging print

