#!/usr/bin/env python
"""
Helper script to check Python environment and install missing packages.
Run this to diagnose and fix imageio installation issues.
"""

import sys
import subprocess

print("=" * 60)
print("Python Environment Checker")
print("=" * 60)
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")
print()

# Check for imageio
try:
    import imageio
    print(f"✅ imageio is installed (version: {imageio.__version__})")
except ImportError:
    print("❌ imageio is NOT installed")
    print("\nInstalling imageio...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "imageio", "imageio-ffmpeg"])
    print("✅ Installation complete! Please restart your Jupyter kernel.")

# Check for imageio-ffmpeg
try:
    import imageio_ffmpeg
    print(f"✅ imageio-ffmpeg is installed (version: {imageio_ffmpeg.__version__})")
except ImportError:
    print("❌ imageio-ffmpeg is NOT installed")
    print("\nInstalling imageio-ffmpeg...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "imageio-ffmpeg"])
    print("✅ Installation complete! Please restart your Jupyter kernel.")

# Check other required packages
packages = ['xarray', 'matplotlib', 'cartopy', 'numpy', 'pandas', 'tqdm']
print("\nChecking other required packages...")
for pkg in packages:
    try:
        __import__(pkg)
        print(f"✅ {pkg} is installed")
    except ImportError:
        print(f"❌ {pkg} is NOT installed")

print("\n" + "=" * 60)
print("If any packages are missing, install them with:")
print(f"  {sys.executable} -m pip install -r requirements.txt")
print("=" * 60)

