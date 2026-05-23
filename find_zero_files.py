import os

def find_zero_byte_files(directory):
    for root, dirs, files in os.walk(directory):
        if '.venv' in root or '.git' in root or '.gemini' in root:
            continue
        for file in files:
            filepath = os.path.join(root, file)
            try:
                if os.path.getsize(filepath) == 0:
                    print(f"Zero-byte file: {filepath}")
            except OSError:
                pass

if __name__ == "__main__":
    find_zero_byte_files(".")
