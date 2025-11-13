# 🔧 Fix PyTorch MPS Issue - Required Steps

## The Problem
Even the Desklib model hits the mutex lock because `from_pretrained()` triggers PyTorch MPS initialization.

## ✅ Solution: Install CPU-Only PyTorch

This is the **only reliable fix** for M2 Mac:

```bash
# Uninstall current PyTorch
pip uninstall torch torchvision torchaudio -y

# Install CPU-only version (no MPS, no GPU)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

**This will:**
- ✅ Remove MPS completely (no mutex locks)
- ✅ Use CPU only (slower but stable)
- ✅ Work perfectly on M2 Mac
- ✅ Allow model loading without crashes

## After Installing CPU-Only PyTorch

Then try again:
```bash
python gradio_app.py
# or
python test_desklib.py
```

## Alternative: Upgrade PyTorch

```bash
pip install --upgrade torch torchvision torchaudio
```

Newer versions (2.9+) may have fixed the MPS bug.

## Why This Works

- **CPU-only PyTorch**: No MPS backend = no mutex locks
- **Stable**: Works reliably on macOS
- **Trade-off**: Slower inference (CPU vs GPU), but still fast enough

## Recommendation

**Install CPU-only PyTorch** - it's the most reliable solution for M2 Mac right now.
