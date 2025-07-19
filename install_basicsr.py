import subprocess
import os

basicsr_path = "C:/Users/ASUS/Desktop/Headshot enhancer/models/basicsr"

try:
    print(f"Attempting to install basicsr from: {basicsr_path}")
    result = subprocess.run(
        ["python", "-m", "pip", "install", "-e", "."],
        cwd=basicsr_path,
        check=True,
        capture_output=True,
        text=True
    )
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
    print("basicsr installed successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error installing basicsr: {e}")
    print("STDOUT:", e.stdout)
    print("STDERR:", e.stderr)
except Exception as e:
    print(f"An unexpected error occurred: {e}")