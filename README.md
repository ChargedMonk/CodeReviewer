# 🤖 CodeReviewer — Local AI Code Review on Every Commit

**CodeReviewer** is a lightweight, local-first AI assistant that reviews your code on every Git commit and provides helpful suggestions about:

* 🔍 Code quality
* ⚙️ Logical issues
* ✨ Readability and improvements

It uses a local GGUF-compatible LLM (like Mistral or StarCoder) through `llama.cpp`, and runs silently in the background without blocking your workflow.

---

## 🚀 Features

* ✅ Runs locally (no data is sent to the cloud)
* ✅ Hooks into Git using a global pre-commit hook
* ✅ Diff-aware (only reviews staged changes)
* ✅ Saves feedback in a `.code_review/` folder per repo
* ✅ Supports models like Mistral, StarCoder, DeepSeek etc.
* ✅ Works with or without GPU
* ✅ Highly configurable during setup

---

## 📦 Installation

### 🔹 Option 1: From PyPI

```bash
pip install code-reviewer
```

### 🔹 Option 2: From GitHub (latest)

```bash
pip install git+https://github.com/your-username/CodeReviewer.git
```

### 🔹 Option 3: Local development install

```bash
git clone https://github.com/ChargedMonk/CodeReviewer.git
cd CodeReviewer
pip install .
```

## 💠 One-Time Setup

To set up the global Git hook and configure the reviewer:

```bash
code-reviewer init \
  --model-dir ~/.models \
  --model-file mistral-7b-instruct-v0.2.Q4_K_M.gguf \
  --gdrive-model-url https://drive.google.com/file/d/1IVrCT8mzSNtfUJ5rTyDbLfcxbHzkcX2K/view \
  --text-context 8192 \
  --review-dir .code_review \
  --prompt-prefix "You are a senior code reviewer. Given the diff and surrounding code context, suggest improvements in code quality, logic, and readability. Be precise and constructive." \
  --max-tokens 1024
```

This will:

* Register a global Git pre-commit hook at `~/.git-hooks/`
* Persist your config to `~/.code_reviewer_config.json`
* Start reviewing staged changes in background after every commit

## 💾 Model Setup

Download a `.gguf` model (e.g., from HuggingFace or Google Drive), then place it in your preferred directory:

```
~/.models/mistral-7b-instruct-v0.2.Q4_K_M.gguf
```

Then use `--model-dir` and `--model-file` during `init`.

You can also provide a Google Drive download URL via `--gdrive-model-url` if the model isn't present — it will be downloaded automatically.

---

## 💡 How It Works

1. On commit, the global pre-commit hook captures the staged diff.
2. CodeReviewer runs asynchronously in the background.
3. Each changed file is reviewed using a local LLM.
4. Suggestions are saved in `.code_review/<filename>.<commit-id>.review.txt`

Example output:

```bash
📤 Running code reviewer in background... (log: /tmp/code_reviewer_1234.log)
✅ Review completed!
```

Check `.code_review/` in your repo to view suggestions.

---

## 🧐 Example Output

```text
📝 Suggestions for utils.py:
- The function `process_data` has nested conditionals that could be flattened for readability.
- Consider using `enumerate()` instead of manually managing the index.
```

---

## ⚙️ Configuration Options (via `code-reviewer init`)

| Option               | Description                                            |
| -------------------- | ------------------------------------------------------ |
| `--model-dir`        | Path to directory where `.gguf` models are stored      |
| `--model-file`       | Name of the model file to load                         |
| `--gdrive-model-url` | Optional Google Drive URL to download model if missing |
| `--text-context`     | Max context length to use (e.g., 8192)                 |
| `--review-dir`       | Directory to save review suggestions in each repo      |
| `--prompt-prefix`    | Prompt to guide the AI reviewer                        |
| `--max-tokens`       | Max tokens in the generated review output              |

Config is saved in `~/.code_reviewer_config.json` and used automatically on every commit.

---

## 🐛 Troubleshooting

### 📌 Review doesn’t run on commit?

* Ensure you ran: `code-reviewer init`
* Check that `~/.git-hooks/pre-commit` exists and is executable
* Make sure the model `.gguf` file is correctly named and placed

### 🤊 Too slow?

* Use smaller quantized models (e.g., Q4\_K\_M instead of Q8\_0)
* Avoid very large models like 13B unless you have a GPU
* Check that your `text-context` and `max-tokens` aren't too high

### 💥 Terminal frozen?

Ensure the reviewer is backgrounded correctly. This is handled automatically via the `pre-commit` script placed in `~/.git-hooks/`.

---

## 📜 License

MIT License

## 🙌 Credits

Powered by `llama-cpp-python` and open-source GGUF models from Hugging Face, Google Drive, and the open source AI community.
