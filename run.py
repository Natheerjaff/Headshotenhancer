# run.py

import sys
import os
import shutil
import subprocess

# Ensure models and weights directories are clean
shutil.rmtree("models", ignore_errors=True)
shutil.rmtree("gfpgan/weights", ignore_errors=True)

# --- The Bulletproof Path Fix ---
# Get the absolute path of the directory where this run.py file exists.
# This will be the root of your project.
project_root = os.path.abspath(os.path.dirname(__file__))

# Add the project root to the Python path.
# This ensures that Python can find the 'src' package.
sys.path.insert(0, project_root)

# Handle basicsr
basicsr_path = os.path.join(project_root, "models", "basicsr")
if os.path.exists(basicsr_path):
    print(f"Attempting to forcefully remove existing basicsr directory: {basicsr_path}")
    os.system(f'rmdir /s /q "{basicsr_path}"')
    if os.path.exists(basicsr_path):
        print(f"Warning: Could not fully remove {basicsr_path}. Manual deletion may be required.")

print("Cloning basicsr repository...")
subprocess.run(["git", "clone", "https://github.com/xinntao/BasicSR.git", basicsr_path], check=True)
print("basicsr cloned successfully.")

# Modify basicsr/__init__.py to handle version import robustly
basicsr_init_path = os.path.join(basicsr_path, "basicsr", "__init__.py")
with open(basicsr_init_path, 'r') as f:
    content = f.read()
content = content.replace(
    "from .version import __gitsha__, __version__",
    "try:\n    from .version import __gitsha__, __version__\nexcept ImportError:\n    __gitsha__ = 'unknown'\n    __version__ = '0.0.0'"
)
with open(basicsr_init_path, 'w') as f:
    f.write(content)

# Download GFPGANv1.4.pth
gfpgan_model_path = os.path.join(project_root, "models", "gfpgan", "GFPGANv1.4.pth")
os.makedirs(os.path.dirname(gfpgan_model_path), exist_ok=True)
print(f"Downloading GFPGANv1.4.pth to {gfpgan_model_path}...")
subprocess.run(["curl", "-L", "https://huggingface.co/gmk123/GFPGAN/resolve/main/GFPGANv1.4.pth", "-o", gfpgan_model_path], check=True)
print("GFPGANv1.4.pth downloaded successfully.")

sys.path.insert(0, basicsr_path)


# Now that the path is fixed, we can import from src.
from src.main import main

if __name__ == "__main__":
    """
    This is the single, official entry point for the application.
    Running this file will start the program.
    """
    print(f"Project root added to path: {project_root}")
    print("Starting application...")
    main()