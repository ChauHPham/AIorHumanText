"""
Safe model loading for macOS - uses subprocess to isolate MPS issues
"""
import subprocess
import sys
import os
import pickle
import tempfile

def load_model_in_subprocess(model_name="desklib/ai-text-detector-v1.01"):
    """
    Load model in a subprocess to avoid MPS mutex lock issues.
    Returns model and tokenizer objects.
    """
    # Create a temporary script to load the model
    script = f"""
import sys
import os
import torch

# Aggressively disable MPS
os.environ['PYTORCH_ENABLE_MPS'] = '0'
os.environ['TOKENIZERS_PARALLELISM'] = 'false'
os.environ['OMP_NUM_THREADS'] = '1'

# Disable MPS before any imports
if hasattr(torch.backends, 'mps'):
    torch.backends.mps.enabled = False

from transformers import AutoTokenizer, AutoConfig
from ai_text_detector.models import DesklibAIDetectionModel

# Load tokenizer and config
tokenizer = AutoTokenizer.from_pretrained("{model_name}")
config = AutoConfig.from_pretrained("{model_name}")

# Create model and load weights manually
model = DesklibAIDetectionModel(config)
model = model.to("cpu")

# Load state dict
from transformers.utils import cached_file
state_dict_path = cached_file("{model_name}", "pytorch_model.bin")
state_dict = torch.load(state_dict_path, map_location="cpu")
model.load_state_dict(state_dict, strict=False)
model.eval()

# Save to temp file
import pickle
with open("{tempfile.gettempdir()}/model_temp.pkl", "wb") as f:
    pickle.dump((model, tokenizer), f)

print("SUCCESS")
"""
    
    # Run in subprocess
    result = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        text=True,
        cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    
    if "SUCCESS" in result.stdout:
        # Load from temp file
        with open(f"{tempfile.gettempdir()}/model_temp.pkl", "rb") as f:
            model, tokenizer = pickle.load(f)
        return model, tokenizer
    else:
        raise RuntimeError(f"Failed to load model: {result.stderr}")
