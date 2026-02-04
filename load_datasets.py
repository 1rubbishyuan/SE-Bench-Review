import os
import json
from datasets import load_dataset

def save_to_jsonl(dataset_name, config_name, output_path):
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Load dataset
    print(f"Loading {config_name}...")
    dataset = load_dataset(dataset_name, config_name)
    
    # Save to JSONL
    # Note: As per instructions, data is located in dataset['train']
    with open(output_path, 'w', encoding='utf-8') as f:
        for item in dataset['train']:
            f.write(json.dumps(item) + '\n')
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    REPO_ID = "jintailin/SE-Bench"
    
    # Define tasks
    tasks = [
        ("train", "datasets/train/train.jsonl"),
        ("single_test", "datasets/test/single_test.jsonl"),
        ("multiple_test", "datasets/test/multiple_test.jsonl")
    ]
    
    for config, path in tasks:
        save_to_jsonl(REPO_ID, config, path)