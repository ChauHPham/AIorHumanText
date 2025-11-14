# 🚀 Deploy Quiz App to Hugging Face Spaces

This guide shows you how to deploy the AI Text Detector Quiz to Hugging Face Spaces for permanent hosting.

## Quick Deploy from Colab

### Step 1: Open the Colab Notebook
1. Upload `quiz_colab.ipynb` to Google Colab
2. Run all cells up to "Step 3: Create Quiz Files"

### Step 2: Deploy to Hugging Face Spaces

**Prerequisites:**
1. Create a Hugging Face account: [huggingface.co/join](https://huggingface.co/join)
2. Get your access token: [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
   - Click "New token"
   - Name it (e.g., "colab-deploy")
   - Select "Write" permissions
   - Copy the token

**Deploy:**
1. Run the cell that installs `gradio` and `huggingface_hub`
2. Run the login cell and paste your token when prompted
3. Run the deployment cell: `!gradio deploy`
4. Follow the prompts:
   - Enter your Hugging Face username
   - Enter a Space name (e.g., `ai-text-detector-quiz`)
5. Wait 5-10 minutes for deployment

**Your app will be live at:**
```
https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
```

## Manual Deployment

If you prefer to deploy manually:

### Step 1: Prepare Files

Make sure you have these files:
- `gradio_quiz_app.py` - The Gradio quiz app
- `src/quiz_dataset_loader.py` - Quiz dataset loader
- `ai_text_detector/models.py` - Model code
- `data/ai_vs_human_text.csv` - Dataset (or your CSV files)
- `README.md` - Space README with metadata
- `requirements.txt` - Dependencies

### Step 2: Create a New Space

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Fill in:
   - **Space name**: e.g., `ai-text-detector-quiz`
   - **SDK**: Select "Gradio"
   - **Hardware**: CPU (free) or GPU if needed
   - **Visibility**: Public or Private
4. Click "Create Space"

### Step 3: Upload Files

Upload all the files from Step 1 to your Space using:
- The web interface (drag and drop)
- Git: `git clone` your Space repo and push files
- Or use `huggingface_hub` Python library

### Step 4: Wait for Build

Hugging Face will automatically:
- Install dependencies from `requirements.txt`
- Build your app
- Deploy it

Check the "Logs" tab in your Space to see the build progress.

## Files Needed for Deployment

### `gradio_quiz_app.py`
The main Gradio app file (already created)

### `README.md`
```yaml
---
title: AI Text Detector Quiz
emoji: 📝
colorFrom: blue
colorTo: purple
sdk: gradio
app_file: gradio_quiz_app.py
pinned: false
---

# AI Text Detector Quiz

A fun interactive quiz game where you test your ability to distinguish AI-generated text from human-written text!
```

### `requirements.txt`
```
pandas
scikit-learn
torch
transformers
gradio
```

## Troubleshooting

### "Module not found" errors
- Make sure all Python files are uploaded
- Check that `requirements.txt` includes all dependencies
- Verify file paths are correct

### "No quiz dataset available"
- Upload your CSV files to the `data/` directory in your Space
- Make sure CSV files have `text` and `label` columns

### Build fails
- Check the Logs tab in your Space
- Verify all files are uploaded correctly
- Make sure `app_file` in README.md matches your Gradio app filename

### Model loading issues
- The app will automatically use Desklib pre-trained model
- Model downloads automatically on first use (~1.7GB)
- This may take a few minutes on first load

## Benefits of Hugging Face Spaces

✅ **Free permanent hosting**  
✅ **No expiration** (unlike ngrok URLs)  
✅ **Shareable URL** that works forever  
✅ **Automatic updates** when you push code  
✅ **GPU support** (free tier available)  
✅ **Public or private** Spaces  
✅ **Community features** (likes, comments, etc.)

## Updating Your Space

To update your deployed app:
1. Make changes to your files locally
2. Upload the updated files to your Space
3. Or use Git to push changes
4. The Space will automatically rebuild

Enjoy your permanently hosted quiz app! 🎉

