# 🤖 CodeReviewer — Local AI Code Review on Every Commit

**CodeReviewer** is a lightweight, local-first AI assistant that reviews your code on every Git commit and provides helpful suggestions about:

- 🔍 Code quality
- ⚙️ Logical issues
- ✨ Readability and improvements

It uses a local GGUF-compatible LLM (like Mistral or StarCoder) through `llama.cpp`, and runs silently in the background without blocking your workflow.

---

## 🚀 Features

- ✅ Runs locally (no data is sent to the cloud)
- ✅ Hooks into Git using a global pre-commit hook
- ✅ Diff-aware (only reviews staged changes)
- ✅ Saves feedback in a `.ai_review/` folder per repo
- ✅ Supports models like Mistral, StarCoder, DeepSeek etc.
- ✅ Works with or without GPU

---

## 📦 Installation

### 🔸 Option 1: From PyPI

```bash
pip install code-reviewer
```

### 🔸 Option 2: From GitHub (latest)

```bash
pip install git+https://github.com/your-username/CodeReviewer.git
```

### 🔸 Option 3: Local development install

```bash
git clone https://github.com/ChargedMonk/CodeReviewer.git
cd CodeReviewer
pip install .
```

## 🛠️ One-Time Setup

To set up the global Git hook and model path:

```bash
code-reviewer init
```

This will:

* Register a global Git pre-commit hook at ~/.git-hooks/
* Ensure the hook runs for all Git repos
* Run reviews automatically in background after each commit

## 💾 Model Setup

Place your .gguf model file inside:

```
CodeReviewer/models/
```

Example:

_models/mistral-7b-instruct-v0.2.Q4_K_M.gguf_

You can also modify reviewer.py to download the model from a custom URL (e.g. Google Drive) if needed.

## 💡 How It Works

    On commit, a global Git pre-commit hook captures the staged diff.

    CodeReviewer runs asynchronously in the background.

    Each changed file is reviewed using an LLM.

    Suggestions are saved as .review.txt files under: .code_review/<filename>.<commit-id>.review.txt

You’ll see output like this:

```bash
📤 Running code reviewer in background... (log: /tmp/code_reviewer_1234.log)

✅ Review completed!
```

Check .code_review/ in your repo to view suggestions.
## 🧠 Example Output

```text
📝 Suggestions for utils.py:
- The function `process_data` has nested conditionals that could be flattened for readability.
- Consider using `enumerate()` instead of manually managing the index.
```

## ⚙️ Configuration

You can change the model or tweak behavior in `code_reviewer/reviewer.py`:

    Adjust max_tokens

    Change the model path

    Use os.cpu_count() to tune performance

    Swap prompt style (e.g., “Summarize”, “Fix bugs”, etc.)

## 🐛 Troubleshooting
### 📌 Review doesn’t run on commit?

    Make sure you ran: code-reviewer init

    Check that ~/.git-hooks/pre-commit exists and is executable

    Ensure the model .gguf file is placed correctly

### 🧊 Too slow?

    Use smaller quantized models (e.g. Q4_K_M instead of Q8_0)

    Avoid very large models like 6.7B or 13B on CPUs

    Use a GPU build of llama-cpp-python if available

### 💥 Terminal frozen?

Ensure you're using a non-blocking background process in the hook. This is handled automatically if you installed via code-reviewer init.

## 📘 License

MIT License.

## 🙌 Credits

Powered by llama-cpp-python and open-source GGUF models from Hugging Face & beyond.



