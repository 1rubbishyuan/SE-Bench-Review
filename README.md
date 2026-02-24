<!-- # SE-Bench: Benchmarking Self-Evolution with Knowledge Internalization -->

<p align="center">
  <a href="https://github.com/thunlp/SE-Bench">
    <img src="assets/sebench_logo_2.png" style="height: 10em; border-radius: 15px;" alt="se-bench" />
  </a>
</p>


<p align="center">
    <a href="https://www.python.org/">
        <img alt="Build" src="https://img.shields.io/badge/Python-3.12+-1f425f.svg?color=purple">
    </a>
    <a href="https://copyright.princeton.edu/policy">
        <img alt="License" src="https://img.shields.io/badge/License-MIT-blue">
    </a>
    <a href="https://huggingface.co/datasets/jintailin/SE-Bench">
        <img src="https://img.shields.io/badge/%F0%9F%A4%97%20Datasets-SE--Bench-yellow">
    </a>
    <a href="https://arxiv.org/pdf/2602.04811">
        <img src="https://img.shields.io/badge/arXiv-Paper-b31b1b">
    </a>
</p>
<h1>SE-Bench: Benchmarking Self-Evolution with Knowledge Internalization</h1>

SE-Bench is a diagnostic environment designed to rigorously measure an agent's ability to **internalize** novel knowledge, which is a foundational capability for true self-evolution.

## 🚀 Environment Setup
First, create and activate a dedicated Conda environment, then install the required dependencies for the project.

### Prerequisites
- Conda (Anaconda/Miniconda) installed
- Docker (required for evaluation sandbox)


### Installation Steps
```bash
# Create a Conda environment named "se-bench" with Python 3.12
conda create -n se-bench python==3.12 -y

# Activate the Conda environment
conda activate se-bench

# Navigate to the SE-Bench project root directory
cd SE-Bench

# Install all required dependencies
pip install -r requirements.txt
```

### Data Preparation
You can load the dataset using the Hugging Face `datasets` library:

```python
from datasets import load_dataset

dataset = load_dataset("jintailin/SE-Bench", "train")
# Data is in dataset['train']
print(dataset)
dataset = load_dataset("jintailin/SE-Bench", "single_test")
# Data is in dataset['train']
print(dataset)
dataset = load_dataset("jintailin/SE-Bench", "multiple_test")
# Data is in dataset['train']
print(dataset)
```

Alternatively, you can run the provided `load_datasets.py` script to download and save the data to the local directory structure:
```bash
python load_datasets.py
```

This will generate the following file structure:
| Path | Description | Usage |
| :--- | :--- | :--- |
| `datasets/train/api_doc.jsonl` | API documentation for the `zwc` package | Training material |
| `datasets/train/train.jsonl` | Training questions | Training material |
| `datasets/test/single_test.jsonl` | Single-function problems | Evaluation |
| `datasets/test/multiple_test.jsonl` | Multi-function composition problems | Evaluation |

**Protocol**: Train your model or agent using **only** the information provided in `datasets/train/`, then evaluate on problems in `datasets/test/` **without** access to documentation. This tests whether the model has truly internalized the API knowledge.


## ▶️ Model Rollout (Inference)

### Model Deployment
Before running the rollout scripts, you need to deploy the model (e.g., Qwen3-8B) locally. We support deployment via **vLLM** or **SGLang** at `localhost:8800`.

**Option 1: Deploy with vLLM**
```bash
pip install vllm
python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen3-8B \
    --port 8800 \
    --host localhost
```

**Option 2: Deploy with SGLang**
```bash
pip install "sglang[all]"
python -m sglang.launch_server \
    --model-path Qwen/Qwen3-8B \
    --port 8800 \
    --host localhost
```

### Rollout Without API Documentation
Run the `query_only.py` script to perform inference using only the query content:
```bash
cd src
python query_only.py \
 --num_workers 1 \
 --input_path ../datasets/test/single_test.jsonl \
 --output_path ../rollout_results/query_only.jsonl \
 --model_name Qwen3-8B \
 --host localhost \
 --ports 8800 \
 --sample_count 1 \
 --temperature 0.6 \
 --max_length 8192
```

### Rollout With API Documentation
Run the `query_doc.py` script to perform inference with API documentation (requires specifying the document path):
```bash
cd src
python query_doc.py \
 --num_workers 1 \
 --input_path ../datasets/test/single_test.jsonl \
 --output_path ../rollout_results/query_doc.jsonl \
 --doc_path ../datasets/train/api_doc.jsonl \
 --model_name Qwen3-8B \
 --host localhost \
 --ports 8800 \
 --sample_count 1 \
 --temperature 0.6 \
 --max_length 8192
```

### Key Parameter Explanation
| Parameter       | Description                                                                 |
|-----------------|-----------------------------------------------------------------------------|
| `--num_workers` | Number of parallel worker processes (adjust based on hardware)              |
| `--input_path`  | Path to input test dataset (JSONL format)                                   |
| `--output_path` | Path to save rollout (inference) results                                    |
| `--doc_path`    | Path to API documentation (required only for `query_doc.py`)                |
| `--model_name`  | Name of the model to use (e.g., Qwen3-8B)                           |
| `--host`        | Host address of locally deployed models                       |
| `--ports`       | Port(s) of locally deployed models                            |
| `--base_url`    | Base URL for OpenAI-compatible APIs            |
| `--api_key`     | API key for OpenAI-compatible models           |
| `--sample_count`| Number of samples to generate per input                                     |
| `--temperature` | Sampling temperature (higher values = more random outputs)                  |
| `--max_length`  | Maximum length of generated text by the model                               |

## 🧪 Result Evaluation
The evaluation phase requires building a Docker sandbox for safe code execution, followed by filtering correct inference trajectories.

### Build Docker Sandbox
The sandbox provides a secure environment for code execution and is deployed at `http://localhost:8111` by default:
```bash
# Build and start the Docker sandbox (Docker must be running)
bash sandbox_build_and_run.sh
```

> **Note**: To change the sandbox port, modify the port configuration in `src/evaluation/worker.py`.

### Run Evaluation
After the sandbox is successfully started, execute the evaluation script to filter correct results:
```bash
cd src
python filter_correct_trajectory.py \
 --input_path ../rollout_results/query_only.jsonl \
 --num_workers 64 \
 --output_path ../evaluation_results/correct_trajectories.jsonl  # Optional: Path to save correct trajectories
```

### Evaluation on Custom Rollout Results
If you are not using our generation scripts (`query_only.py` or `query_doc.py`) and wish to evaluate your own model outputs, you must format your rollout results as a JSONL file. Each line should be a dictionary containing the following keys:

| Key | Description |
| :--- | :--- |
| `query` | The original question from the dataset. |
| `response` | The model's generation, containing the execution code wrapped in ```python``` blocks and the reasoning process. |
| `test_cases` | The original test cases from the dataset. Format: `[{"input":..., "output":...}, ...]`. |
| `right_exe_result` | The original ground truth executable result string from the dataset. |

Once your data is formatted correctly, you can directly run the evaluation script above.


## Construct SFT Data
First, run the `query_doc.py` to make rollouts.
Remember to deploy model via **vLLM** or **SGLang** before rollout.
```bash
cd src
python query_doc.py \
 --num_workers 1 \
 --input_path ../datasets/test/train.jsonl \
 --output_path ../SFT_data/rollout_SFT_data.jsonl \
 --doc_path ../datasets/train/api_doc.jsonl \
 --model_name Qwen3-8B \
 --host localhost \
 --ports 8800 \
 --sample_count 5 \
 --temperature 0.6 \
 --max_length 8192
```
Then, run the `filter_correct_trajectory.py` to filter out corrcet trajectories.
Remember to Build sandbox before filtering.
```bash
python filter_correct_trajectory.py --input_path ../SFT_data/rollout_SFT_data.jsonl --output_path ../SFT_data/valid_SFT_data.jsonl --num_workers 64
```

## 📝 Notes
- Adjust `--num_workers` based on your hardware resources (avoid overloading the system)
- The sandbox must remain running during the entire evaluation process
- All output paths will be created automatically if they do not exist


## ✍️ Citation & License
This project is licensed under the [MIT License](LICENSE).
You can check `LICENSE.md` 

If you find our work or dataset helpful for your research, please consider citing our paper:

```bibtex
@article{yuan2026se,
  title={SE-Bench: Benchmarking Self-Evolution with Knowledge Internalization},
  author={Yuan, Jiarui and Jin, Tailin and Chen, Weize and Liu, Zeyuan and Liu, Zhiyuan and Sun, Maosong},
  journal={arXiv preprint arXiv:2602.04811},
  year={2026}
}
```
