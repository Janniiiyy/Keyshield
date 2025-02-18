import ctypes

def detect_keyboard_hooks():
    user32 = ctypes.windll.user32
    hook_count = user32.GetKeyboardLayoutList(0, None)  # Check keyboard hooks

    if hook_count > 1:  # Normal users have only 1 keyboard hook
        print("⚠️ Warning: Suspicious keyboard hook detected!")
    else:
        print("✅ No suspicious keyboard hooks found.")

# Run detection
if __name__ == "__main__":
    detect_keyboard_hooks()
