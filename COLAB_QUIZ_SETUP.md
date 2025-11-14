# AI Text Detector Quiz - Google Colab Setup

This guide helps you run the quiz app in Google Colab, avoiding MPS errors on M2 Macs.

## Quick Start

1. **Open Google Colab**: Go to [colab.research.google.com](https://colab.research.google.com/)

2. **Upload the notebook**: Upload `quiz_colab.ipynb` or create a new notebook and copy the cells below

3. **Run the cells in order**:
   - Install dependencies
   - Upload your CSV dataset files
   - Create quiz files (automated)
   - Run the app

4. **Access the quiz**: You'll get a public ngrok URL to access the quiz!

## Step-by-Step Instructions

### Cell 1: Install Dependencies
```python
%pip install flask flask-cors pandas scikit-learn torch transformers pyyaml pyngrok -q
```

### Cell 2: Upload Dataset
```python
from google.colab import files
import os

os.makedirs('data', exist_ok=True)
uploaded = files.upload()

for filename in uploaded.keys():
    if filename.endswith('.csv'):
        os.rename(filename, f'data/{filename}')
        print(f'✓ Uploaded {filename} to data/')
```

### Cell 3: Create Quiz Files
Run the cells in `quiz_colab.ipynb` that create:
- `src/quiz_dataset_loader.py`
- `app.py` (Colab-compatible version)
- `templates/index.html`
- `ai_text_detector/models.py`

### Cell 4: Run the App
```python
from pyngrok import ngrok
import threading
import time

# Start Flask app in background
def run_flask():
    from app import app
    app.run(host='0.0.0.0', port=5000, debug=False)

flask_thread = threading.Thread(target=run_flask, daemon=True)
flask_thread.start()

# Wait for Flask to start
time.sleep(5)

# Create ngrok tunnel
public_url = ngrok.connect(5000)
print(f"\n🚀 Quiz is running at: {public_url}")
print(f"\n📝 Open this URL in your browser to play the quiz!")
```

## Notes

- The ngrok URL will expire when the Colab session ends
- For a permanent solution, consider deploying to Hugging Face Spaces
- Make sure your CSV files have `text` and `label` columns
- Labels should be "AI-generated" or "Human-written"

## Troubleshooting

**"No module named 'ai_text_detector'"**
- Make sure you ran all the cells that create the package files

**"No quiz samples available"**
- Check that CSV files were uploaded correctly
- Verify CSV files have `text` and `label` columns

**ngrok URL not working**
- Wait a few seconds after running the cell
- Check that Flask started successfully (look for "Running on" message)

