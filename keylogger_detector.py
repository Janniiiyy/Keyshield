import psutil
import time

# Load blacklisted process names from file
def load_blacklist():
    try:
        with open("blacklist.txt", "r") as file:
            return [line.strip().lower() for line in file.readlines()]
    except FileNotFoundError:
        return []

# Function to detect suspicious processes
def detect_suspicious_processes():
    blacklist = load_blacklist()
    detected_processes = set()  # Store detected PIDs to avoid duplicate alerts

    print("\n🔍 Real-time monitoring for keyloggers...\n")

    while True:
        for process in psutil.process_iter(attrs=['pid', 'name']):
            try:
                process_name = process.info['name'].lower()
                process_pid = process.info['pid']

                # Check if the process is in the blacklist
                if process_name in blacklist and process_pid not in detected_processes:
                    print(f"⚠️ ALERT! Suspicious process detected: PID {process_pid} - {process_name}")
                    detected_processes.add(process_pid)

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        time.sleep(5)  # Wait for 5 seconds before scanning again

if __name__ == "__main__":
    detect_suspicious_processes()
