import psutil

# List of suspicious process names (you can expand this)
SUSPICIOUS_PROCESSES = ["keylogger", "logger", "stealer", "record"]

def scan_running_processes():
    print("\n🔍 Scanning for suspicious running processes...\n")
    
    found = False
    for process in psutil.process_iter(['pid', 'name']):
        try:
            process_name = process.info['name'].lower()
            if any(susp_name in process_name for susp_name in SUSPICIOUS_PROCESSES):
                print(f"⚠️ Suspicious Process Found: {process.info['name']} (PID: {process.info['pid']})")
                found = True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue  # Skip if the process no longer exists or is protected
    
    if not found:
        print("✅ No suspicious processes detected.")

if __name__ == "__main__":
    scan_running_processes()
