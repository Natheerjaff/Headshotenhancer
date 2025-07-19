# generate_license.py
import hashlib
import uuid
import platform
import subprocess

# IMPORTANT: This secret MUST be identical to the one in your src/licensing.py file.
SECRET = "my_super_secret" 

def get_local_machine_id():
    """
    A helper function to show the developer their own machine ID
    without needing to run the main application.
    """
    try:
        if platform.system() == "Windows":
            return subprocess.check_output("wmic csproduct get uuid").decode().split("\n")[1].strip()
        elif platform.system() == "Linux":
            return subprocess.check_output(["cat", "/sys/class/dmi/id/product_uuid"]).decode().strip()
        elif platform.system() == "Darwin": # macOS
            return subprocess.check_output("system_profiler SPHardwareDataType | awk '/UUID/ { print $3 }'", shell=True).decode().strip()
    except Exception:
        return str(uuid.getnode())

def create_license_for_machine(machine_id: str) -> str:
    """Creates a license key hash for a given machine ID."""
    hasher = hashlib.sha256(f"{machine_id}-{SECRET}".encode())
    return hasher.hexdigest()

if __name__ == "__main__":
    print("--- License Key Generator ---")
    
    # Display the developer's own machine ID for convenience
    local_id = get_local_machine_id()
    print(f"\nYour local machine ID is: {local_id}")
    print("(This is useful for creating a key for yourself.)\n")
    
    # Prompt the user (the developer) to enter the customer's machine ID
    customer_machine_id = input("Enter the customer's Machine ID to generate a key: ")
    
    if customer_machine_id:
        license_key = create_license_for_machine(customer_machine_id.strip())
        print("\n-----------------------------")
        print("  GENERATED LICENSE KEY:")
        print(f"  {license_key}")
        print("-----------------------------\n")
        print("Send this key to the customer.")
    else:
        print("\nNo Machine ID entered. Exiting.")