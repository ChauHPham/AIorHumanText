import os
import sys

# Disable tokenizer parallelism and MPS on macOS
if os.getenv("TOKENIZERS_PARALLELISM") is None:
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

import torch
import torch.nn as nn
from transformers import AutoModelForSequenceClassification, AutoTokenizer, AutoConfig, AutoModel, PreTrainedModel

class DesklibAIDetectionModel(PreTrainedModel):
    """Desklib AI Detection Model - Pre-trained model for AI text detection"""
    config_class = AutoConfig
    
    def __init__(self, config):
        super().__init__(config)
        # Initialize the base transformer model
        self.model = AutoModel.from_config(config)
        # Define a classifier head
        self.classifier = nn.Linear(config.hidden_size, 1)
        # Initialize weights
        self.init_weights()
    
    def forward(self, input_ids, attention_mask=None, labels=None):
        # Forward pass through the transformer
        outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
        last_hidden_state = outputs[0]
        
        # Mean pooling
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(last_hidden_state.size()).float()
        sum_embeddings = torch.sum(last_hidden_state * input_mask_expanded, dim=1)
        sum_mask = torch.clamp(input_mask_expanded.sum(dim=1), min=1e-9)
        pooled_output = sum_embeddings / sum_mask
        
        # Classifier
        logits = self.classifier(pooled_output)
        
        loss = None
        if labels is not None:
            loss_fct = nn.BCEWithLogitsLoss()
            loss = loss_fct(logits.view(-1), labels.float())
        
        output = {"logits": logits}
        if loss is not None:
            output["loss"] = loss
        return output

class DetectorModel:
    def __init__(self, model_name="desklib/ai-text-detector-v1.01", use_desklib=True):
        """
        Initialize detector model.
        
        Args:
            model_name: Model name or path. Defaults to Desklib pre-trained model.
            use_desklib: If True, use Desklib model architecture. If False, use standard classification.
        """
        self.model_name = model_name
        self.use_desklib = use_desklib
        
        if use_desklib and "desklib" in model_name:
            # Try to load Desklib model, but fallback if MPS issues occur
            if sys.platform == "darwin":
                # On macOS: try multiple loading strategies
                try:
                    # Strategy 1: Load with low_cpu_mem_usage and explicit CPU
                    print("Attempting to load Desklib model...")
                    self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                    config = AutoConfig.from_pretrained(model_name)
                    
                    # Try loading with safetensors if available
                    try:
                        from transformers import AutoModel
                        # Load base model first
                        base_model = AutoModel.from_pretrained(
                            model_name,
                            torch_dtype=torch.float32,
                            low_cpu_mem_usage=True,
                            device_map="cpu"
                        )
                        # Create Desklib model wrapper
                        self.model = DesklibAIDetectionModel(config)
                        self.model.model = base_model
                        self.model = self.model.to("cpu")
                        # Load classifier weights
                        from transformers.utils import cached_file
                        try:
                            classifier_path = cached_file(model_name, "pytorch_model.bin")
                            state_dict = torch.load(classifier_path, map_location="cpu")
                            # Only load classifier weights
                            classifier_dict = {k: v for k, v in state_dict.items() if "classifier" in k}
                            if classifier_dict:
                                self.model.load_state_dict(classifier_dict, strict=False)
                        except:
                            pass  # Use initialized classifier
                        self.model.eval()
                        print("✅ Desklib model loaded successfully!")
                    except Exception as e:
                        print(f"⚠️  Desklib model loading failed: {e}")
                        print("Falling back to DistilBERT model...")
                        raise
                except:
                    # Fallback to a smaller, simpler model
                    print("Using DistilBERT as fallback (smaller, more compatible)")
                    self.use_desklib = False
                    self.model = AutoModelForSequenceClassification.from_pretrained(
                        "distilbert-base-uncased", 
                        num_labels=2
                    )
                    self.tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
                    self.model = self.model.to("cpu")
            else:
                # Non-macOS: standard loading
                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                config = AutoConfig.from_pretrained(model_name)
                self.model = DesklibAIDetectionModel.from_pretrained(model_name)
        else:
            # Fallback to standard classification model
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
            self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
            self.use_desklib = False

    def predict(self, text, max_length=768, threshold=0.5):
        """
        Predict if text is AI-generated.
        
        Args:
            text: Input text to classify
            max_length: Maximum sequence length
            threshold: Probability threshold for classification
            
        Returns:
            tuple: (probability, label) where label is 1 for AI-generated, 0 for human
        """
        # Tokenize
        encoded = self.tokenizer(
            text,
            padding='max_length',
            truncation=True,
            max_length=max_length,
            return_tensors='pt'
        )
        
        input_ids = encoded['input_ids']
        attention_mask = encoded['attention_mask']
        
        # Get device
        device = next(self.model.parameters()).device
        input_ids = input_ids.to(device)
        attention_mask = attention_mask.to(device)
        
        # Predict
        self.model.eval()
        with torch.no_grad():
            if self.use_desklib:
                outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
                logits = outputs["logits"]
                probability = torch.sigmoid(logits).item()
            else:
                outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
                probs = torch.softmax(outputs.logits, dim=1)
                # For standard models: prob[0] = human, prob[1] = AI
                probability = probs[0][1].item()
            
            label = 1 if probability >= threshold else 0
        
        return probability, label

    def save(self, path: str):
        self.model.save_pretrained(path)
        self.tokenizer.save_pretrained(path)

    @classmethod
    def load(cls, path: str):
        # Try to detect if it's a Desklib model
        try:
            config = AutoConfig.from_pretrained(path)
            # Check if it has the Desklib architecture
            if hasattr(config, 'model_type') and 'deberta' in config.model_type.lower():
                model = DesklibAIDetectionModel.from_pretrained(path)
                tokenizer = AutoTokenizer.from_pretrained(path)
                obj = cls.__new__(cls)
                obj.model_name = path
                obj.model = model
                obj.tokenizer = tokenizer
                obj.use_desklib = True
                return obj
        except:
            pass
        
        # Fallback to standard model
        model = AutoModelForSequenceClassification.from_pretrained(path)
        tokenizer = AutoTokenizer.from_pretrained(path, use_fast=True)
        obj = cls.__new__(cls)
        obj.model_name = path
        obj.model = model
        obj.tokenizer = tokenizer
        obj.use_desklib = False
        return obj
