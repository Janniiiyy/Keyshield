import psutil

print("\n🔍 Listing all running processes...\n")
for proc in psutil.process_iter(['pid', 'name', 'exe']):
    try:
        print(f"🟢 {proc.info['name']} (PID: {proc.info['pid']}) - Path: {proc.info['exe']}")
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass
