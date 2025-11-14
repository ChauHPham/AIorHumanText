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

## How to Play

1. **Choose** the number of questions (10, 20, or 30)
2. **Read** each text sample carefully
3. **Guess** whether it's AI-generated or Human-written
4. **See** if you're correct and compare with the AI model's prediction
5. **Track** your score and accuracy throughout the quiz

## Features

- 🎮 Interactive quiz interface
- 📊 Real-time scoring and accuracy tracking
- 🤖 See AI model predictions after each answer
- 📈 View confidence scores and probabilities
- 🎯 Multiple difficulty levels (10/20/30 questions)

## Dataset

The quiz uses text samples from the dataset in the `data/` folder. Make sure your CSV files have:
- A `text` column with the text samples
- A `label` column with values "AI-generated" or "Human-written"

## Model

Uses the Desklib AI Text Detector model for predictions. The model automatically loads on startup.

