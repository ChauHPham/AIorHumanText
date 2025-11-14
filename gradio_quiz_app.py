"""
Gradio Quiz App for Hugging Face Spaces
A quiz game where you guess if text is AI-generated or human-written
"""
import os
import sys
import random
import logging

# No MPS code needed for HF Spaces (runs on Linux)
import torch
import gradio as gr
import pandas as pd

from ai_text_detector.models import DetectorModel
from src.quiz_dataset_loader import QuizDatasetLoader

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables
detector = None
quiz_loader = None
current_question = 0
score = {"correct": 0, "total": 0}
current_sample = None
used_ids = set()

def load_model():
    """Load the AI Text Detector model"""
    global detector
    
    model_path = "models/ai_detector"
    
    # Check if model directory exists AND has model files
    has_model = False
    if os.path.exists(model_path):
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
            logger.info("Falling back to RoBERTa base model...")
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
    
    return None

# Initialize on import
load_model()
load_quiz_dataset()

def start_quiz(num_questions):
    """Start a new quiz"""
    global current_question, score, used_ids, current_sample
    
    current_question = 0
    score = {"correct": 0, "total": 0}
    used_ids.clear()
    current_sample = None
    
    return get_next_question(num_questions) + (gr.update(visible=True), gr.update(visible=False))

def get_next_question(num_questions):
    """Get the next question"""
    global current_sample, quiz_loader
    
    if quiz_loader is None or len(quiz_loader) == 0:
        return (
            "⚠️ No quiz dataset available. Please ensure CSV files exist in the data/ directory.",
            gr.update(visible=False),
            gr.update(visible=False),
            f"Question 0/{num_questions}",
            "Score: 0/0 | Accuracy: 0%"
        )
    
    # Get random sample (avoid repeats)
    attempts = 0
    sample = None
    sample_id = None
    
    while attempts < 10:
        sample_id, sample = quiz_loader.get_random_sample()
        if sample_id not in used_ids:
            break
        attempts += 1
    
    if sample is None:
        return (
            "⚠️ Could not load quiz sample. Please try again.",
            gr.update(visible=False),
            gr.update(visible=False),
            f"Question 0/{num_questions}",
            "Score: 0/0 | Accuracy: 0%"
        )
    
    used_ids.add(sample_id)
    current_sample = sample
    
    progress = f"Question {current_question + 1}/{num_questions}"
    score_text = f"Score: {score['correct']}/{score['total']} | Accuracy: {(score['correct']/score['total']*100) if score['total'] > 0 else 0:.0f}%"
    
    return (
        sample['text'],
        gr.update(visible=True),
        gr.update(visible=True),
        progress,
        score_text
    )

def check_answer(user_answer, num_questions):
    """Check the user's answer"""
    global current_question, score, current_sample, detector
    
    if current_sample is None:
        return (
            "⚠️ No question loaded. Please start a new quiz.",
            gr.update(visible=False),
            gr.update(visible=False),
            "",
            "",
            f"Question 0/{num_questions}",
            "Score: 0/0 | Accuracy: 0%"
        )
    
    text = current_sample['text']
    true_label = current_sample['label_name']
    
    # Get model prediction
    try:
        ai_prob, predicted_label = detector.predict(text, max_length=768, threshold=0.5)
        predicted_label_name = 'AI-generated' if predicted_label == 1 else 'Human-written'
        human_prob = 1 - ai_prob
        
        # Check if user is correct
        is_correct = user_answer == true_label
        
        # Update score
        score['total'] += 1
        current_question += 1
        if is_correct:
            score['correct'] += 1
        
        # Create result message
        result_icon = "✅" if is_correct else "❌"
        result_text = f"{result_icon} {'Correct!' if is_correct else 'Incorrect'}\n\n"
        result_text += f"**Your Answer:** {user_answer}\n"
        result_text += f"**Correct Answer:** {true_label}\n\n"
        result_text += f"**🤖 AI Model Prediction:** {predicted_label_name}\n"
        result_text += f"**Confidence:** {(ai_prob if predicted_label == 1 else human_prob) * 100:.1f}%\n\n"
        result_text += f"**Probabilities:**\n"
        result_text += f"- AI-generated: {ai_prob * 100:.1f}%\n"
        result_text += f"- Human-written: {human_prob * 100:.1f}%"
        
        progress = f"Question {current_question}/{num_questions}"
        accuracy = (score['correct'] / score['total'] * 100) if score['total'] > 0 else 0
        score_text = f"Score: {score['correct']}/{score['total']} | Accuracy: {accuracy:.0f}%"
        
        # Check if quiz is complete
        if current_question >= num_questions:
            final_text = result_text + f"\n\n🎉 **Quiz Complete!**\n\n"
            final_text += f"**Final Score:** {score['correct']}/{score['total']}\n"
            final_text += f"**Final Accuracy:** {accuracy:.0f}%"
            return (
                final_text,
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=True, value="🎉 Quiz Complete! Play Again?"),
                "",
                progress,
                score_text
            )
        
        return (
            result_text,
            gr.update(visible=False),
            gr.update(visible=True),
            "",
            "",
            progress,
            score_text
        )
        
    except Exception as e:
        logger.error(f"Error checking answer: {e}")
        return (
            f"⚠️ Error processing answer: {str(e)}",
            gr.update(visible=False),
            gr.update(visible=False),
            "",
            "",
            f"Question {current_question}/{num_questions}",
            f"Score: {score['correct']}/{score['total']} | Accuracy: {(score['correct']/score['total']*100) if score['total'] > 0 else 0:.0f}%"
        )

def next_question(num_questions):
    """Move to next question"""
    if current_question >= num_questions:
        return start_quiz(num_questions)
    return get_next_question(num_questions) + (gr.update(visible=True), gr.update(visible=False))

# Create Gradio interface
with gr.Blocks(title="AI Text Detector Quiz", theme=gr.themes.Soft()) as app:
    gr.Markdown("# 📝 AI Text Detector Quiz")
    gr.Markdown("Test your ability to distinguish AI-generated text from human-written text!")
    
    with gr.Row():
        num_questions = gr.Dropdown(
            choices=[10, 20, 30],
            value=10,
            label="Number of Questions",
            interactive=True
        )
        start_btn = gr.Button("Start Quiz", variant="primary", size="lg")
    
    progress_display = gr.Markdown("", visible=False)
    score_display = gr.Markdown("", visible=False)
    
    with gr.Row(visible=False) as quiz_row:
        with gr.Column():
            text_display = gr.Textbox(
                label="Text Sample",
                lines=10,
                max_lines=15,
                interactive=False,
                show_label=True
            )
            
            with gr.Row():
                ai_btn = gr.Button("🤖 AI-generated", variant="stop", size="lg")
                human_btn = gr.Button("👤 Human-written", variant="primary", size="lg")
        
        with gr.Column():
            result_display = gr.Markdown("", visible=False)
            next_btn = gr.Button("Next Question →", visible=False, variant="secondary")
            restart_btn = gr.Button("🎉 Quiz Complete! Play Again?", visible=False, variant="primary")
    
    # Event handlers
    start_btn.click(
        fn=start_quiz,
        inputs=num_questions,
        outputs=[text_display, quiz_row, progress_display, progress_display, score_display]
    )
    
    def check_ai_answer(num_q):
        return check_answer("AI-generated", num_q)
    
    def check_human_answer(num_q):
        return check_answer("Human-written", num_q)
    
    ai_btn.click(
        fn=check_ai_answer,
        inputs=[num_questions],
        outputs=[result_display, ai_btn, human_btn, restart_btn, next_btn, progress_display, score_display]
    )
    
    human_btn.click(
        fn=check_human_answer,
        inputs=[num_questions],
        outputs=[result_display, ai_btn, human_btn, restart_btn, next_btn, progress_display, score_display]
    )
    
    next_btn.click(
        fn=next_question,
        inputs=num_questions,
        outputs=[text_display, ai_btn, human_btn, progress_display, score_display, restart_btn, next_btn]
    )
    
    restart_btn.click(
        fn=start_quiz,
        inputs=num_questions,
        outputs=[text_display, quiz_row, progress_display, progress_display, score_display]
    )

if __name__ == "__main__":
    app.launch(share=True)

