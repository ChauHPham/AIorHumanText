# ⚡ Quick Fix for MPS Mutex Lock

## The Problem
Even with PyTorch 2.9.0, model loading still triggers MPS mutex locks on M2 Mac.

## ✅ Solution: Install CPU-Only PyTorch

Run this command:

```bash
bash INSTALL_CPU_PYTORCH.sh
```

Or manually:

```bash
pip uninstall torch torchvision torchaudio -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

## Why This Works

- **CPU-only PyTorch**: No MPS backend = no mutex locks
- **Stable**: Works reliably on macOS
- **Trade-off**: Slower inference (CPU vs GPU), but still fast enough for inference

## After Installation

```bash
python gradio_app.py
```

Should work without mutex lock errors!

## Alternative: Upgrade PyTorch

If you want to keep GPU support, try:

```bash
pip install --upgrade torch torchvision torchaudio
```

But CPU-only is more reliable for M2 Mac right now.
