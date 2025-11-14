#!/usr/bin/env python3
"""
Script to create a complete Colab notebook for the quiz app
"""
import json

# Read existing notebook
with open('quiz_colab.ipynb', 'r') as f:
    notebook = json.load(f)

# Read the actual files we need to include
with open('app.py', 'r') as f:
    app_code = f.read()

with open('templates/index.html', 'r') as f:
    html_template = f.read()

with open('ai_text_detector/models.py', 'r') as f:
    models_code = f.read()

# Remove MPS-specific code from app.py for Colab
app_code_colab = app_code.replace(
    '# Fix macOS MPS issues - MUST be before ANY torch/transformers imports\nif sys.platform == "darwin":  # macOS\n    os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"\n    os.environ["TOKENIZERS_PARALLELISM"] = "false"\n    os.environ["OMP_NUM_THREADS"] = "1"\n    os.environ["PYTORCH_ENABLE_MPS"] = "0"\n\nimport torch\n\n# Disable MPS after torch import\nif sys.platform == "darwin":\n    try:\n        torch.backends.mps.enabled = False\n        torch.set_default_device("cpu")\n    except:\n        pass\n\n',
    'import torch\n'
)

# Add cells to create app.py
notebook['cells'].append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {"id": "create_app"},
    "outputs": [],
    "source": [
        f"# Create app.py (Colab-compatible, no MPS code)\\n",
        f"app_code_colab = '''{app_code_colab}'''\\n",
        "\\n",
        "with open('app.py', 'w') as f:\\n",
        "    f.write(app_code_colab)\\n",
        "\\n",
        "print('✓ Created app.py')"
    ]
})

# Add cell to create templates
notebook['cells'].append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {"id": "create_templates"},
    "outputs": [],
    "source": [
        "os.makedirs('templates', exist_ok=True)\\n",
        f"html_template = '''{html_template}'''\\n",
        "\\n",
        "with open('templates/index.html', 'w') as f:\\n",
        "    f.write(html_template)\\n",
        "\\n",
        "print('✓ Created templates/index.html')"
    ]
})

# Add cell to create ai_text_detector package
notebook['cells'].append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {"id": "create_ai_detector"},
    "outputs": [],
    "source": [
        "os.makedirs('ai_text_detector', exist_ok=True)\\n",
        "\\n",
        "with open('ai_text_detector/__init__.py', 'w') as f:\\n",
        "    f.write('# AI Text Detector Package\\n')\\n",
        "\\n",
        f"models_code = '''{models_code}'''\\n",
        "\\n",
        "# Remove MPS-specific code for Colab\\n",
        "models_code_colab = models_code.replace('if sys.platform == \\\"darwin\\\":', 'if False:')  # Disable MPS checks\\n",
        "\\n",
        "with open('ai_text_detector/models.py', 'w') as f:\\n",
        "    f.write(models_code_colab)\\n",
        "\\n",
        "print('✓ Created ai_text_detector/models.py')"
    ]
})

# Add cell to run the app
notebook['cells'].append({
    "cell_type": "markdown",
    "metadata": {"id": "run_app"},
    "source": [
        "## Step 4: Run the Quiz App\\n",
        "\\n",
        "The app will start and you'll get a public URL to access it!"
    ]
})

notebook['cells'].append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {"id": "start_flask"},
    "outputs": [],
    "source": [
        "from pyngrok import ngrok\\n",
        "import threading\\n",
        "import time\\n",
        "\\n",
        "# Start Flask app in background\\n",
        "def run_flask():\\n",
        "    from app import app\\n",
        "    app.run(host='0.0.0.0', port=5000, debug=False)\\n",
        "\\n",
        "flask_thread = threading.Thread(target=run_flask, daemon=True)\\n",
        "flask_thread.start()\\n",
        "\\n",
        "# Wait for Flask to start\\n",
        "time.sleep(5)\\n",
        "\\n",
        "# Create ngrok tunnel\\n",
        "public_url = ngrok.connect(5000)\\n",
        "print(f'\\n🚀 Quiz is running at: {public_url}')\\n",
        "print(f'\\n📝 Open this URL in your browser to play the quiz!')\\n",
        "print(f'\\n⚠️  Note: The ngrok URL will expire when this Colab session ends.')"
    ]
})

# Fix the pip install command
for cell in notebook['cells']:
    if cell.get('source') and '!pip install' in ''.join(cell['source']):
        cell['source'] = ['%pip install flask flask-cors pandas scikit-learn torch transformers pyyaml pyngrok -q\n']

# Save the updated notebook
with open('quiz_colab.ipynb', 'w') as f:
    json.dump(notebook, f, indent=1)

print("✓ Updated quiz_colab.ipynb with all necessary cells")

