# AI Text Detector Quiz

A fun quiz game where you guess whether text samples are AI-generated or human-written!

## Features

- Interactive quiz interface with beautiful UI
- Choose between 10, 20, or 30 questions
- Real-time scoring and accuracy tracking
- See AI model predictions after each answer
- Uses text samples from the dataset in the `data/` folder

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure your dataset CSV files are in the `data/` folder:
   - `ai_vs_human_text.csv`
   - `dataset.csv`

## Running the Quiz

Start the Flask app:
```bash
python app.py
```

Then open your browser to:
```
http://localhost:5000
```

The app will automatically:
- Load the AI text detector model (Desklib pre-trained model or your trained model)
- Load text samples from CSV files in the `data/` directory
- Start the quiz interface

## How It Works

1. **Start Screen**: Choose how many questions you want (10, 20, or 30)
2. **Quiz Screen**: 
   - Read each text sample
   - Click "AI-generated" or "Human-written" to make your guess
   - See if you're correct and compare with the AI model's prediction
   - View confidence scores and probabilities
3. **Results Screen**: See your final score, correct answers, and accuracy

## API Endpoints

- `GET /` - Main quiz interface
- `GET /health` - Health check endpoint
- `GET /quiz/text` - Get a random text sample
- `GET /quiz/text/<id>` - Get a specific text sample by ID
- `POST /quiz/check` - Check your answer (requires `text_id` and `answer` in JSON body)

## Notes

- The quiz uses text samples from CSV files in the `data/` directory
- Labels should be in a column named `label` with values like "AI-generated" or "Human-written"
- Text should be in a column named `text`, `content`, `body`, or `essay`
- The app will automatically load the best available model (trained model > Desklib model > RoBERTa fallback)

