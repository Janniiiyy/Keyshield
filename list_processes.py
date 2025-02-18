import psutil
import datetime

# List of known suspicious process names
SUSPICIOUS_NAMES = ["keylogger.exe", "logger.exe", "stealer.exe", "record.exe"]
LOG_FILE = "detections.log"

def log_detection(process_name, pid):
    """Logs detected keyloggers to a file with a timestamp."""
    with open(LOG_FILE, "a") as log:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"{timestamp} - Suspicious Process Detected: {process_name} (PID: {pid})\n")

def detect_and_kill_suspicious_processes():
    print("\n🔍 Scanning for suspicious processes...\n")
    
    found = False
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            process_name = proc.info['name']
            if process_name and any(susp_name in process_name.lower() for susp_name in SUSPICIOUS_NAMES):
                print(f"⚠️ Suspicious Process Detected: {process_name} (PID: {proc.info['pid']})")
                log_detection(process_name, proc.info['pid'])  # Log detection
                terminate_process(proc.info['pid'])
                found = True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    if not found:
        print("✅ No suspicious processes found.")

def terminate_process(pid):
    try:
        proc = psutil.Process(pid)
        proc.terminate()
        print(f"🚨 Suspicious process (PID {pid}) terminated!")
    except Exception as e:
        print(f"❌ Error terminating process: {e}")

# Run detection & auto-kill
if __name__ == "__main__":
    detect_and_kill_suspicious_processes()
