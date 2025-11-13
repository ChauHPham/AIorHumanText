# 🚀 Deployment Guide

## Google Colab (Recommended for Mac M2)

**Perfect for Mac M2 users** - avoids PyTorch MPS mutex lock issues!

### Quick Start

1. Open [Google Colab](https://colab.research.google.com/)
2. Create a new notebook
3. Run:

```python
!pip install -q transformers torch pandas gradio kagglehub
!git clone https://github.com/ChauHPham/AITextDetector.git
%cd AITextDetector
!git checkout main
!python gradio_app.py
```

4. **Get your public link**: After running, you'll see:
   ```
   * Running on public URL: https://xxxxx.gradio.live
   ```
   This link is shareable and works as long as the Colab notebook is running!

### Keep It Running

- Enable "Keep runtime alive" in Colab's runtime settings
- The public link expires after 1 week of inactivity
- For permanent hosting, use Hugging Face Spaces (see below)

---

## Hugging Face Spaces (Permanent Hosting)

Deploy your app permanently to Hugging Face Spaces for free!

### Option 1: Using Gradio CLI

```bash
# Install gradio if not already installed
pip install gradio

# Deploy from your project directory
gradio deploy
```

Follow the prompts to:
1. Login to Hugging Face (or create account)
2. Choose/create a Space
3. Deploy!

### Option 2: Manual Deployment

1. Create a new Space on [Hugging Face Spaces](https://huggingface.co/spaces)
2. Choose "Gradio" as the SDK
3. Upload your files:
   - `gradio_app.py`
   - `ai_text_detector/` (entire package)
   - `requirements.txt`
   - `README.md`
4. Add a `README.md` in the Space with:
   ```yaml
   ---
   title: AI Text Detector
   emoji: 🔍
   colorFrom: blue
   colorTo: purple
   sdk: gradio
   app_file: gradio_app.py
   pinned: false
   ---
   ```
5. The Space will automatically build and deploy!

---

## Local Deployment

### Requirements

- Python 3.8+
- See `requirements.txt`

### Run Locally

```bash
# Install dependencies
pip install -r requirements.txt
pip install -e .

# Run Gradio app
python gradio_app.py
```

**Note for Mac M2 users**: Local training may fail due to PyTorch MPS bugs. Use Google Colab for training instead.

---

## Docker Deployment

```bash
# Build
docker build -t ai-text-detector .

# Run
docker run -p 7860:7860 ai-text-detector
```

---

## Troubleshooting

### Mac M2 Issues

If you encounter `mutex.cc lock blocking` errors on Mac M2:
- ✅ **Use Google Colab** (recommended)
- ✅ Use Docker with Linux base image
- ❌ Local training may not work due to PyTorch MPS bugs

### Model Loading Issues

The app automatically uses the Desklib pre-trained model if no trained model is found. The model downloads automatically on first use (~1.7GB).

