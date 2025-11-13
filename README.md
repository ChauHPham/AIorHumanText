# AI Text Detector

A learning project for detecting AI-generated vs. human-written text with a modular Python package, YAML configs, GPU auto-detection, CLI, and a **Gradio web interface**.
<img width="3794" height="1082" alt="image" src="https://github.com/user-attachments/assets/c0b36d58-b3d1-4629-ad8d-2dedaea7f1c3" />

## 🌐 Web Interface (Gradio)

**Try it now on Google Colab** (works perfectly on Mac M2!):

```python
!pip install -q transformers torch pandas gradio kagglehub
!git clone https://github.com/ChauHPham/AITextDetector.git
%cd AITextDetector
!python gradio_app.py
```

Get a **public shareable link** instantly! See [DEPLOY.md](DEPLOY.md) for deployment options.

### 🍎 Mac M2 Users

**Google Colab is recommended** - local training may fail due to PyTorch MPS mutex lock issues. The Gradio app works great in Colab with free GPU!

## Quickstart (CLI)

```bash
# 1) Create & activate a virtualenv (recommended)
python -m venv .venv && source .venv/bin/activate

# 2) Install
pip install -r requirements.txt
pip install -e .

# 3) (Optional) Download Kaggle datasets into data/
python scripts/kaggle_downloader.py

# 4) Configure
cp configs/default.yaml configs/local.yaml
# edit local.yaml if desired (change data_path, hyperparams, etc.)

# 5) Train
ai-detector train --data data/dataset.csv --config configs/local.yaml

# 6) Evaluate
ai-detector eval --model-path models/ai_detector --data data/dataset.csv --config configs/local.yaml
```

## Datasets

* LLM Detect AI Generated Text Dataset (Kaggle)
* AI vs Human Text (Kaggle)

Use `scripts/kaggle_downloader.py` to fetch them. You may need to normalize/merge columns; the loader tries common names (`text`, `content`, `essay` and `label`, `class`, `target`).

## Config

See `configs/default.yaml`. Key fields:

* `base_model`: e.g., `roberta-base`
* `max_length`, `batch_size`, `num_epochs`, `lr`
* `fp16`: set `null` to auto-enable on CUDA

## Notes

* Labels standardized to `0=human`, `1=ai`.
* Mixed precision (fp16) auto-enables on CUDA.
* Evaluate with accuracy, macro-F1, and confusion matrix.
* **Mac M2 users**: Use Google Colab for training (see above) to avoid PyTorch MPS bugs.

## Deployment

See [DEPLOY.md](DEPLOY.md) for:
- Google Colab setup (recommended for Mac M2)
- Hugging Face Spaces deployment (`gradio deploy`)
- Docker deployment
- Troubleshooting guide
