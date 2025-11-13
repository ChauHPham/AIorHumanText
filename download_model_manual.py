"""
Manually download model files to avoid from_pretrained() MPS bug
Run this ONCE, then use the downloaded model
"""
import os
import sys
import subprocess

# Use huggingface_hub to download without loading
print("Installing huggingface_hub...")
subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "huggingface_hub"])

from huggingface_hub import snapshot_download

print("Downloading Desklib model files (this may take a few minutes)...")
model_dir = "models/desklib_model"

try:
    snapshot_download(
        repo_id="desklib/ai-text-detector-v1.01",
        local_dir=model_dir,
        local_dir_use_symlinks=False
    )
    print(f"✅ Model downloaded to {model_dir}")
    print("\nNow try running gradio_app.py again!")
except Exception as e:
    print(f"❌ Download failed: {e}")
    print("\nTry running this in Google Colab instead!")
