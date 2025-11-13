import os
import sys

# Fix macOS MPS issues - MUST be before ANY torch/transformers imports
if sys.platform == "darwin":  # macOS
    os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["PYTORCH_ENABLE_MPS"] = "0"  # Explicitly disable MPS

import gradio as gr
import torch

# Disable MPS after torch import
if sys.platform == "darwin":
    try:
        torch.backends.mps.enabled = False
        torch.set_default_device("cpu")
    except:
        pass

from ai_text_detector.models import DetectorModel
from ai_text_detector.datasets import DatasetLoader

# Initialize model and tokenizer
model = None
tokenizer = None

def load_model():
    """Load the trained model if it exists, otherwise use a base model for demo"""
    global model, tokenizer
    
    model_path = "models/ai_detector"
    
    # Check if model directory exists AND has model files
    has_model = False
    if os.path.exists(model_path):
        # Check for required model files
        required_files = ["config.json", "pytorch_model.bin"]
        has_model = all(os.path.exists(os.path.join(model_path, f)) for f in required_files)
    
    if has_model:
        try:
            print(f"Loading trained model from {model_path}")
            model = DetectorModel.load(model_path)
            tokenizer = model.tokenizer
        except Exception as e:
            print(f"Failed to load model: {e}")
            print("Using Desklib pre-trained model instead.")
            model = DetectorModel("desklib/ai-text-detector-v1.01", use_desklib=True)
            tokenizer = model.tokenizer
    else:
        print("No trained model found. Using Desklib pre-trained AI detector model.")
        # Use Desklib pre-trained model (no training needed!)
        model = DetectorModel("desklib/ai-text-detector-v1.01", use_desklib=True)
        tokenizer = model.tokenizer

# Load model lazily (on first use) to avoid startup issues
_model_loaded = False

def ensure_model_loaded():
    """Load model if not already loaded"""
    global model, tokenizer, _model_loaded
    if not _model_loaded:
        load_model()
        _model_loaded = True

def detect_text(text):
    """Detect if text is AI-generated or human-written"""
    global model, tokenizer
    
    # Load model on first use
    ensure_model_loaded()
    
    if not text.strip():
        return "Please enter some text to analyze."
    
    try:
        # Use the model's predict method
        ai_prob, predicted_label = model.predict(text, max_length=768, threshold=0.5)
        
        # Determine prediction
        if predicted_label == 1:
            label = "🤖 AI-generated"
            confidence = ai_prob
        else:
            label = "🧑 Human-written"
            confidence = 1 - ai_prob  # Human probability is 1 - AI probability
        
        return f"{label} (confidence: {confidence:.1%})"
        
    except Exception as e:
        return f"Error processing text: {str(e)}"

# Create Gradio interface (model will load on first detection)
print("Starting Gradio app... Model will load on first use.")
with gr.Blocks(title="AI Text Detector", theme=gr.themes.Soft()) as app:
    gr.Markdown("# 🔍 AI Text Detector")
    gr.Markdown("Paste any text below to detect if it was written by AI or a human.")
    
    with gr.Row():
        with gr.Column():
            text_input = gr.Textbox(
                label="Text to analyze",
                placeholder="Enter text here...",
                lines=5,
                max_lines=10
            )
            detect_btn = gr.Button("🔍 Detect", variant="primary")
        
        with gr.Column():
            result_output = gr.Textbox(
                label="Prediction",
                interactive=False,
                lines=3
            )
    
    # Connect the button to the function
    detect_btn.click(
        fn=detect_text,
        inputs=text_input,
        outputs=result_output
    )
    
    # Also detect on Enter key
    text_input.submit(
        fn=detect_text,
        inputs=text_input,
        outputs=result_output
    )
    
    # Add some example texts
    gr.Markdown("### 💡 Try these examples:")
    
    examples = [
        "The sunset painted the sky in hues of crimson and gold, casting long shadows across the meadow.",
        "The quantum tensor optimization algorithm significantly reduced inference latency by 23.7%.",
        "I went to the store yesterday and bought some milk and bread.",
        "The implementation leverages advanced neural architecture search techniques to optimize model performance."
    ]
    
    gr.Examples(
        examples=examples,
        inputs=text_input,
        outputs=result_output,
        fn=detect_text,
        cache_examples=False
    )

if __name__ == "__main__":
    app.launch(share=False, server_name="0.0.0.0", server_port=7860)
