#!/bin/bash
# Install CPU-only PyTorch to fix MPS mutex lock issues on M2 Mac

echo "🔧 Installing CPU-only PyTorch..."
echo "This will remove MPS and use CPU only (slower but stable)"
echo ""

# Uninstall current PyTorch
echo "Step 1: Uninstalling current PyTorch..."
pip uninstall torch torchvision torchaudio -y

# Install CPU-only version
echo ""
echo "Step 2: Installing CPU-only PyTorch..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

echo ""
echo "✅ Done! CPU-only PyTorch installed."
echo ""
echo "Now try:"
echo "  python gradio_app.py"
echo "  python test_desklib.py"
