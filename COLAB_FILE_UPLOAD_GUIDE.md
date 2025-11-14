# 📤 How to Upload Files in Google Colab

## Step-by-Step Guide

### Step 1: Run the Upload Cell

When you run this code in a Colab cell:
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

### Step 2: Look for the File Upload Button

After running the cell, you'll see:
- A button that says **"Choose Files"** or **"Browse"**
- This appears below the cell output

### Step 3: Click the Button

1. Click **"Choose Files"** or **"Browse"**
2. A file picker dialog will open

### Step 4: Select Your CSV Files

1. Navigate to where your CSV files are stored (Downloads folder, Desktop, etc.)
2. Select one or both files:
   - `ai_vs_human_text.csv`
   - `dataset.csv`
3. You can select multiple files by:
   - **Windows/Linux**: Hold `Ctrl` and click each file
   - **Mac**: Hold `Cmd` and click each file
4. Click **"Open"**

### Step 5: Wait for Upload

- You'll see a progress bar showing upload progress
- The files will upload to Colab
- Once complete, you'll see output like:
  ```
  ✓ Uploaded ai_vs_human_text.csv to data/
  ✓ Uploaded dataset.csv to data/
  ```

## Visual Example

```
┌─────────────────────────────────────────┐
│ [Run] [Runtime] [File] [Edit] [View]   │
├─────────────────────────────────────────┤
│ from google.colab import files          │
│ uploaded = files.upload()               │
│                                         │
│ ┌─────────────────────────────────┐     │
│ │   📁 Choose Files               │     │ ← Click this button!
│ └─────────────────────────────────┘     │
│                                         │
│ Files will appear here after upload    │
└─────────────────────────────────────────┘
```

## Alternative: Drag and Drop

Some Colab versions also support drag-and-drop:
1. Have your CSV files ready in a file explorer window
2. Drag the files directly onto the Colab cell output area
3. Drop them when you see the upload indicator

## Troubleshooting

### "Choose Files" button doesn't appear
- Make sure you ran the cell (click the play button or press `Shift+Enter`)
- Wait a moment for the widget to load
- Try refreshing the page

### Files not uploading
- Check your internet connection
- Make sure files aren't too large (Colab has size limits)
- Try uploading one file at a time

### Files uploaded but not in data/ folder
- Check the cell output for any error messages
- Verify the file names end with `.csv`
- Look in the file browser (left sidebar) to see where files ended up

### Can't find your CSV files
- Check your Downloads folder
- Use your computer's search function to find `ai_vs_human_text.csv`
- Make sure the files are actually CSV files (not Excel files)

## Quick Tips

✅ **Upload both files** if you have them - the more data, the better!  
✅ **Check file size** - very large files (>100MB) may take longer  
✅ **Verify upload** - Check the `data/` folder in Colab's file browser (left sidebar)  
✅ **Re-upload if needed** - You can run the cell again to upload more files

## After Upload

Once files are uploaded, you can verify they're in the right place:

```python
import os
print("Files in data/ folder:")
for file in os.listdir('data'):
    print(f"  - {file}")
```

You should see:
```
Files in data/ folder:
  - ai_vs_human_text.csv
  - dataset.csv
```

Now you're ready to continue with the quiz setup! 🎉

