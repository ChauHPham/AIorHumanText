#!/bin/bash
# Quick deployment script for Hugging Face Spaces

echo "🚀 Deploying AI Text Detector to Hugging Face Spaces..."
echo ""
echo "Make sure you have:"
echo "  1. Hugging Face account (https://huggingface.co/join)"
echo "  2. Gradio installed (pip install gradio)"
echo "  3. Hugging Face CLI installed (pip install huggingface_hub)"
echo ""
read -p "Press Enter to continue or Ctrl+C to cancel..."

# Deploy using Gradio CLI
gradio deploy

echo ""
echo "✅ Deployment complete!"
echo "Your app will be available at: https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME"

