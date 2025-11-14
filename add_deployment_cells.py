#!/usr/bin/env python3
"""Add Hugging Face Spaces deployment cells to the Colab notebook"""
import json

# Read notebook
with open('quiz_colab.ipynb', 'r') as f:
    nb = json.load(f)

# Read files to include
with open('gradio_quiz_app.py', 'r') as f:
    gradio_code = f.read()

with open('SPACE_README.md', 'r') as f:
    space_readme = f.read()

# Add deployment section
nb['cells'].append({
    'cell_type': 'markdown',
    'metadata': {'id': 'deploy_section'},
    'source': [
        '## Step 4: Deploy to Hugging Face Spaces 🚀\n',
        '\n',
        'Choose one of the following options:\n',
        '\n',
        '### Option A: Deploy to Hugging Face Spaces (Permanent URL)\n',
        'This creates a permanent, shareable URL that never expires!'
    ]
})

# Add cell to create gradio_quiz_app.py
nb['cells'].append({
    'cell_type': 'code',
    'execution_count': None,
    'metadata': {'id': 'create_gradio_app'},
    'outputs': [],
    'source': [
        '# Create Gradio quiz app for HF Spaces\n',
        f'gradio_code = """{gradio_code}"""\n',
        '\n',
        "with open('gradio_quiz_app.py', 'w') as f:\n",
        "    f.write(gradio_code)\n",
        '\n',
        "print('✓ Created gradio_quiz_app.py')"
    ]
})

# Add cell to create Space README
nb['cells'].append({
    'cell_type': 'code',
    'execution_count': None,
    'metadata': {'id': 'create_space_readme'},
    'outputs': [],
    'source': [
        '# Create README.md for Hugging Face Space\n',
        f'space_readme = """{space_readme}"""\n',
        '\n',
        "with open('README.md', 'w') as f:\n",
        "    f.write(space_readme)\n",
        '\n',
        "print('✓ Created README.md for Hugging Face Space')"
    ]
})

# Add deployment instructions
nb['cells'].append({
    'cell_type': 'markdown',
    'metadata': {'id': 'deploy_instructions'},
    'source': [
        '### Deploy to Hugging Face Spaces\n',
        '\n',
        '**Prerequisites:**\n',
        '1. Create a Hugging Face account at [huggingface.co/join](https://huggingface.co/join)\n',
        '2. Get your access token from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)\n',
        '   - Click "New token"\n',
        '   - Name it (e.g., "colab-deploy")\n',
        '   - Select "Write" permissions\n',
        '   - Copy the token'
    ]
})

# Install HF Hub
nb['cells'].append({
    'cell_type': 'code',
    'execution_count': None,
    'metadata': {'id': 'install_hf'},
    'outputs': [],
    'source': [
        '# Install Hugging Face Hub and Gradio\n',
        '%pip install -q gradio huggingface_hub'
    ]
})

# Login cell
nb['cells'].append({
    'cell_type': 'code',
    'execution_count': None,
    'metadata': {'id': 'login_hf'},
    'outputs': [],
    'source': [
        '# Login to Hugging Face\n',
        'from huggingface_hub import login\n',
        '\n',
        '# Paste your token when prompted\n',
        'login()\n',
        '\n',
        "print('✅ Logged in to Hugging Face!')"
    ]
})

# Deploy cell
nb['cells'].append({
    'cell_type': 'code',
    'execution_count': None,
    'metadata': {'id': 'deploy_hf'},
    'outputs': [],
    'source': [
        '# Deploy to Hugging Face Spaces!\n',
        '!gradio deploy\n',
        '\n',
        "print('\\n🚀 Your quiz app is being deployed to Hugging Face Spaces!')\n",
        "print('\\n⏳ This usually takes 5-10 minutes. Check your Spaces dashboard:')\n",
        "print('   https://huggingface.co/spaces')"
    ]
})

# Save notebook
with open('quiz_colab.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)

print('✓ Added Hugging Face Spaces deployment cells to notebook')

