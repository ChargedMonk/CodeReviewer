from llama_cpp import Llama
from pathlib import Path
import gdown
import time

model_path = Path(__file__).parent.parent / "models" / "mistral-7b-instruct-v0.2.Q4_K_M.gguf"
gdrive_url = "https://drive.google.com/uc?id=FILE_ID"

if not model_path.exists():
    print("📥 Downloading model...")
    gdown.download(gdrive_url, str(model_path), quiet=False)

llm = Llama(model_path=str(model_path), n_ctx=16384//2, verbose=False)

def parse_diff_file(diff_path: Path):
    file_diffs = {}
    current_file = None
    current_chunk = []

    for line in diff_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("+++ b/"):
            if current_file and current_chunk:
                file_diffs[current_file] = "\n".join(current_chunk)
                current_chunk = []

            current_file = line[6:]
        elif current_file:
            current_chunk.append(line)

    if current_file and current_chunk:
        file_diffs[current_file] = "\n".join(current_chunk)

    return file_diffs

def run_diff_review(diff_path: Path, commit_id: str):
    start_time = time.time()
    file_diffs = parse_diff_file(diff_path)
    if not file_diffs:
        print("⚠️ No relevant changes found in diff.")
        return

    review_dir = Path(".code_review")
    review_dir.mkdir(exist_ok=True)

    for file, diff_chunk in file_diffs.items():
        prompt = (f"You are a senior code reviewer. Given the diff and surrounding code context, suggest improvements in code quality, logic, and readability. "
                  f"Be precise and constructive.\nFile: `{file}`\nDiff:\n```diff\n{diff_chunk}\n```")
        print(f"🧠 Reviewing {file}\nPrompt:\n{prompt}")
        try:
            response = llm(prompt, max_tokens=1024)
            suggestion = response["choices"][0]["text"].strip()

            output_file = review_dir / f"{Path(file).name}_{commit_id}.review.txt"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(f"📝 Suggestions for {file}:\n{suggestion}\n")

        except Exception as e:
            print(f"❌ Error reviewing {file}: {e}")

    print(f"✅ Review completed. See .code_review/ folder for suggestions.\n{round(time.time()-start_time)} sec")
    print("REVIEW DONE")
