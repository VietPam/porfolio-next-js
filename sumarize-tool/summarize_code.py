import os
import re
from pathlib import Path

SOURCE_EXTENSIONS = [".ts", ".tsx", ".js", ".jsx"]
OUTPUT_FOLDER = "output"
OUTPUT_FILE = "all_code.txt"
COMPRESS_OUTPUT = True

def remove_comments(content):
    pattern = r'(\".*?\"|\'.*?\'|\`.*?\`)|(/\*.*?\*/|//[^\n]*)'

    def replacer(match):
        if match.group(2) is not None:
            return ""
        return match.group(1)

    return re.sub(pattern, replacer, content, flags=re.DOTALL)

def compress_code(content):
    lines = content.splitlines()
    cleaned = []
    for line in lines:
        stripped = line.strip()
        if stripped:
            cleaned.append(stripped)
    return " ".join(cleaned)

def collect_files(base_dir):
    files = []
    for root, dirs, filenames in os.walk(base_dir):
        if ".next" in root:
            continue
        if "node_modules" in root:
            continue
        if ".wrangler" in root:
            continue
        if "summarize-tool" in root:
            continue
        for name in filenames:
            path = Path(root) / name
            if path.suffix in SOURCE_EXTENSIONS:
                files.append(path)
    return files

def read_file_content(file_path):
    if file_path.name == "worker-configuration.d.ts":
        with open(file_path, "r", encoding="utf-8") as f:
            lines = []
            for i, line in enumerate(f):
                if i >= 20:
                    break
                lines.append(line)
            return "".join(lines)

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def write_output(files, base_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    output_path = Path(output_dir) / OUTPUT_FILE

    with open(output_path, "w", encoding="utf-8") as out:
        for file_path in sorted(files):
            relative_path = file_path.relative_to(base_dir)

            content = read_file_content(file_path)
            content = remove_comments(content)

            if COMPRESS_OUTPUT:
                content = compress_code(content)

            out.write(f"\n/* FILE: {relative_path} */\n")
            out.write(content)
            out.write("\n")

def main():
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    output_dir = script_dir / OUTPUT_FOLDER

    files = collect_files(project_root)
    write_output(files, project_root, output_dir)

if __name__ == "__main__":
    main()