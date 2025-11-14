"""
Quiz dataset loader - handles loading quiz text samples from CSV files
"""
import os
import random
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class QuizDatasetLoader:
    """
    Loads quiz text samples from CSV files
    """
    def __init__(self, data_dir='data', csv_files=None):
        self.data_dir = data_dir
        self.csv_files = csv_files or ['ai_vs_human_text.csv', 'dataset.csv']
        self.samples = []
        self.class_names = ['Human-written', 'AI-generated']
        self.load_samples()
    
    def load_samples(self):
        """Load samples from CSV files"""
        all_samples = []
        
        for csv_file in self.csv_files:
            csv_path = os.path.join(self.data_dir, csv_file)
            if not os.path.exists(csv_path):
                logger.warning(f"CSV file not found: {csv_path}")
                continue
            
            try:
                df = pd.read_csv(csv_path)
                
                # Normalize column names
                text_col = None
                label_col = None
                
                # Find text column
                for col in ['text', 'content', 'body', 'essay']:
                    if col in df.columns:
                        text_col = col
                        break
                
                # Find label column
                for col in ['label', 'target', 'class', 'is_ai']:
                    if col in df.columns:
                        label_col = col
                        break
                
                if text_col is None or label_col is None:
                    logger.warning(f"Could not find text or label column in {csv_file}")
                    continue
                
                # Normalize labels
                def normalize_label(label):
                    if pd.isna(label):
                        return None
                    label_str = str(label).strip().lower()
                    if label_str in ['ai-generated', 'ai', 'machine', 'generated', 'gpt', 'llm', 'chatgpt', '1']:
                        return 1  # AI-generated
                    elif label_str in ['human-written', 'human', 'person', 'authored', 'real', '0']:
                        return 0  # Human-written
                    return None
                
                # Process rows
                for idx, row in df.iterrows():
                    text = str(row[text_col]).strip()
                    label = normalize_label(row[label_col])
                    
                    if text and text != 'nan' and label is not None:
                        all_samples.append({
                            'id': len(all_samples),
                            'text': text,
                            'label': label,
                            'label_name': self.class_names[label]
                        })
                
                logger.info(f"Loaded {len(df)} rows from {csv_file}")
                
            except Exception as e:
                logger.error(f"Error loading {csv_file}: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        if all_samples:
            self.samples = all_samples
            logger.info(f"Loaded {len(self.samples)} quiz text samples total")
        else:
            logger.warning("No quiz samples available. Quiz will not work.")
            logger.warning("Please ensure CSV files exist in the data/ directory")
            self.samples = []
    
    def get_random_sample(self):
        """Get a random sample"""
        if not self.samples:
            return None, None
        idx = random.randint(0, len(self.samples) - 1)
        return idx, self.get_sample(idx)
    
    def get_sample(self, idx):
        """Get sample by index"""
        if idx < 0 or idx >= len(self.samples):
            return None
        return self.samples[idx]
    
    def __len__(self):
        return len(self.samples)

