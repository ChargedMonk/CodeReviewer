# 🤖 DiffReviewer — Local AI Code Review on Every Commit

**DiffReviewer** is a lightweight, local-first AI assistant that reviews your code on every Git commit and provides helpful suggestions 
about:

* 🔍 Code quality
* ⚙️ Logical issues
* ✨ Readability and improvements

It uses a local GGUF-compatible LLM (like Mistral or StarCoder) through `llama.cpp`, and runs silently in the background without blocking your workflow.

---

## 🚀 Features

* ✅ Runs locally (no data is sent to the cloud)
* ✅ Hooks into Git using a global pre-commit hook
* ✅ Queues and reviews changes asynchronously — never blocks your commits
* ✅ Automatically deduplicates model loads (only one review at a time)
* ✅ Diff-aware (only reviews staged changes)
* ✅ Saves feedback in a `.diff_review/` folder per repo
* ✅ Supports models like Mistral, StarCoder, DeepSeek etc.
* ✅ Works with or without GPU
* ✅ Highly configurable during setup

---

## 📦 Installation

### 🔹 Option 1: From PyPI

```bash
pip install diff-reviewer
```

### 🔹 Option 2: From GitHub (latest)

```bash
pip install git+https://github.com/your-username/DiffReviewer.git
```

### 🔹 Option 3: Local development install

```bash
git clone https://github.com/ChargedMonk/DiffReviewer.git
cd DiffReviewer
pip install .
```

## 💠 One-Time Setup

To set up the global Git hook and configure the reviewer:

```bash
diff-reviewer init \
  --model-dir ~/.models \
  --model-file mistral-7b-instruct-v0.2.Q4_K_M.gguf \
  --gdrive-model-url https://drive.google.com/file/d/1IVrCT8mzSNtfUJ5rTyDbLfcxbHzkcX2K/view \
  --text-context 8192 \
  --review-dir .diff_review \
  --prompt-prefix "You are a senior code reviewer. Given the diff and surrounding code context, suggest improvements in code quality, logic, and readability. Be precise and constructive." \
  --max-tokens 1024
```

This will:

* Register a global Git pre-commit hook at `~/.git-hooks/`
* Persist your config to `~/.diff_reviewer_config.json`
* Start reviewing staged changes in background after every commit

## 💾 Model Setup

Download a `.gguf` model (e.g., from HuggingFace or Google Drive), then place it in your preferred directory:

```
~/.models/mistral-7b-instruct-v0.2.Q4_K_M.gguf
```

Then use `--model-dir` and `--model-file` during `init`.

You can also provide a Google Drive download URL via `--gdrive-model-url` if the model isn't present — it will be downloaded automatically.

---

## 🧠 How Queued Reviews Work

To avoid system freezes and GPU overload:

✅ DiffReviewer now uses a file-based job queue.
Each commit writes a job to ~/.diff_reviewer/queue, and a single background worker handles them one at a time.
Why it matters:

    ⏱ Multiple commits don’t overload your system

    🔄 Model is only loaded once per session

    💻 Your terminal and Git remain fully responsive

    ♻️ Crashed or exited workers restart automatically

---

## 💡 How It Works

1. On commit, the pre-commit hook captures the staged diff. 
2. The diff is base64-encoded and enqueued as a job. 
3. A background worker processes jobs one by one. 
4. Each changed file is reviewed using a local LLM. 
5. Suggestions are saved in .diff_review/<filename>.<commit-id>.review.txt

Example output:

```bash
📤 Running code reviewer in background... (log: /tmp/diff_reviewer_1234.log)
✅ Review completed!
```

Check `.diff_review/` in your repo to view suggestions.

---

## 🧐 Example Suggestion

```text
📝 Suggestions for utils.py:
- The function `process_data` has nested conditionals that could be flattened for readability.
- Consider using `enumerate()` instead of manually managing the index.
```

---

## ⚙️ Configuration Options (via `diff-reviewer init`)

| Option               | Description                                            |
| -------------------- | ------------------------------------------------------ |
| `--model-dir`        | Path to directory where `.gguf` models are stored      |
| `--model-file`       | Name of the model file to load                         |
| `--gdrive-model-url` | Optional Google Drive URL to download model if missing |
| `--text-context`     | Max context length to use (e.g., 8192)                 |
| `--review-dir`       | Directory to save review suggestions in each repo      |
| `--prompt-prefix`    | Prompt to guide the AI reviewer                        |
| `--max-tokens`       | Max tokens in the generated review output              |

Config is saved in `~/.diff_reviewer_config.json` and used automatically on every commit.

---

## 🐛 Troubleshooting

### 📌 Review doesn’t run on commit?

* Ensure you ran: `diff-reviewer init`
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
