import os
import sys
import random
import logging
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# Fix macOS MPS issues - MUST be before ANY torch/transformers imports
if sys.platform == "darwin":  # macOS
    os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["PYTORCH_ENABLE_MPS"] = "0"

import torch

# Disable MPS after torch import
if sys.platform == "darwin":
    try:
        torch.backends.mps.enabled = False
        torch.set_default_device("cpu")
    except:
        pass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import the detector model and quiz loader
from ai_text_detector.models import DetectorModel
from src.quiz_dataset_loader import QuizDatasetLoader

app = Flask(__name__)
CORS(app)

# Global detector instance and quiz dataset
detector = None
quiz_loader = None

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/health')
def health():
    """Health check endpoint"""
    quiz_status = 'loaded' if (quiz_loader and len(quiz_loader) > 0) else 'not loaded'
    
    return jsonify({
        'status': 'healthy',
        'model_loaded': detector is not None,
        'device': str(next(detector.model.parameters()).device) if detector else 'unknown',
        'quiz_loader_status': quiz_status,
        'quiz_loader_count': len(quiz_loader) if quiz_loader else 0
    })

@app.route('/quiz/text', methods=['GET'])
def get_quiz_text():
    """Get a random text sample from the quiz dataset"""
    try:
        if quiz_loader and len(quiz_loader) > 0:
            idx, sample_data = quiz_loader.get_random_sample()
            if sample_data:
                return jsonify({
                    'text_id': idx,
                    'text': sample_data['text'],
                    'true_label': sample_data['label_name']
                })
            else:
                logger.error(f"Failed to get sample data for index {idx}")
                return jsonify({'error': 'Failed to load text data'}), 500
        else:
            error_msg = 'Quiz dataset not available. '
            if not quiz_loader:
                error_msg += 'Quiz loader not initialized. '
            elif len(quiz_loader) == 0:
                error_msg += 'Quiz loader has 0 samples. '
            error_msg += 'Please check data/ directory for CSV files.'
            
            logger.error(error_msg)
            return jsonify({'error': error_msg}), 500
    except Exception as e:
        logger.error(f"Error getting quiz text: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/quiz/text/<int:text_id>', methods=['GET'])
def get_quiz_text_by_id(text_id):
    """Get a specific text sample by ID"""
    try:
        if quiz_loader and text_id < len(quiz_loader):
            sample = quiz_loader.get_sample(text_id)
            if sample:
                return jsonify({
                    'text_id': text_id,
                    'text': sample['text'],
                    'true_label': sample['label_name']
                })
            else:
                return jsonify({'error': f'Text sample {text_id} not found'}), 404
        
        return jsonify({'error': f'Invalid text ID: {text_id}'}), 404
    except Exception as e:
        logger.error(f"Error getting quiz text {text_id}: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/quiz/check', methods=['POST'])
def check_quiz_answer():
    """Check user's answer and return result with model prediction"""
    try:
        data = request.json
        text_id = data.get('text_id')
        user_answer = data.get('answer')  # 'AI-generated' or 'Human-written'
        
        if text_id is None or user_answer is None:
            return jsonify({'error': 'Missing text_id or answer'}), 400
        
        # Get text and label from quiz_loader
        if quiz_loader is None or text_id >= len(quiz_loader):
            return jsonify({'error': 'Invalid text ID'}), 404
        
        sample = quiz_loader.get_sample(text_id)
        if sample is None:
            return jsonify({'error': 'Text sample not found'}), 404
        
        text = sample['text']
        true_label = sample['label_name']
        
        # Get model prediction
        ai_prob, predicted_label = detector.predict(text, max_length=768, threshold=0.5)
        
        # Map predicted label to label name
        predicted_label_name = 'AI-generated' if predicted_label == 1 else 'Human-written'
        
        # Calculate human probability
        human_prob = 1 - ai_prob
        
        # Check if user is correct
        is_correct = user_answer == true_label
        
        return jsonify({
            'is_correct': is_correct,
            'user_answer': user_answer,
            'true_label': true_label,
            'model_prediction': predicted_label_name,
            'model_confidence': ai_prob if predicted_label == 1 else human_prob,
            'model_probabilities': {
                'AI-generated': ai_prob,
                'Human-written': human_prob
            }
        })
    except Exception as e:
        logger.error(f"Error checking quiz answer: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

def load_detector():
    """Load the AI Text Detector"""
    global detector
    
    model_path = "models/ai_detector"
    
    # Check if model directory exists AND has model files
    has_model = False
    if os.path.exists(model_path):
        # Check for required model files
        required_files = ["config.json", "pytorch_model.bin"]
        has_model = all(os.path.exists(os.path.join(model_path, f)) for f in required_files)
    
    if has_model:
        try:
            logger.info(f"Loading trained model from {model_path}")
            detector = DetectorModel.load(model_path)
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            logger.info("Using Desklib pre-trained model instead.")
            detector = DetectorModel("desklib/ai-text-detector-v1.01", use_desklib=True)
    else:
        logger.info("No trained model found. Loading Desklib pre-trained AI detector model...")
        try:
            detector = DetectorModel("desklib/ai-text-detector-v1.01", use_desklib=True)
            logger.info("✅ Desklib model loaded successfully!")
        except Exception as e:
            logger.error(f"⚠️  Failed to load Desklib model: {e}")
            logger.info("Falling back to RoBERTa base model (will need training for good results)...")
            import traceback
            traceback.print_exc()
            detector = DetectorModel("roberta-base", use_desklib=False)
    
    return detector

def load_quiz_dataset(data_dir='data'):
    """Load the quiz dataset from CSV files"""
    global quiz_loader
    
    logger.info(f"Loading quiz dataset from {data_dir}...")
    
    try:
        quiz_loader = QuizDatasetLoader(data_dir=data_dir)
        
        if len(quiz_loader) > 0:
            msg = f"✓ Quiz dataset loaded: {len(quiz_loader)} text samples"
            print(msg)
            logger.info(msg)
            return quiz_loader
        else:
            logger.warning("QuizDatasetLoader created but has 0 samples")
    except Exception as e:
        error_msg = f"Warning: Could not load quiz dataset: {e}"
        print(error_msg)
        logger.error(error_msg, exc_info=True)
        quiz_loader = None
    
    warning_msg = "⚠️  No quiz dataset available. Quiz will not work."
    print(warning_msg)
    logger.warning(warning_msg)
    print("   Please ensure CSV files exist in the data/ directory")
    return None

# Initialize on import (for gunicorn) - must be after function definitions
def init_app():
    """Initialize the app - called on startup"""
    global detector, quiz_loader
    
    # Load detector
    try:
        load_detector()
    except Exception as e:
        logger.error(f"Failed to load detector: {e}")
    
    # Load quiz dataset
    try:
        load_quiz_dataset()
    except Exception as e:
        logger.error(f"Failed to load quiz dataset: {e}")

# Initialize when module is imported (works with gunicorn)
init_app()

if __name__ == '__main__':
    # Load detector on startup (already done by init_app, but keep for direct execution)
    if detector is None:
        load_detector()
    if quiz_loader is None:
        load_quiz_dataset()
    # Get port from environment variable (for deployment) or use default
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

