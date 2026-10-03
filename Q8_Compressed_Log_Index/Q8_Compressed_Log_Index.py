import os
import re
import sys
import pickle
import zipfile
from collections import defaultdict
from typing import Dict, List, Set, Tuple

TOKEN_REGEX = re.compile(r"[a-zA-Z0-9]+")

def normalize_tokens(text: str) -> List[str]:
    return TOKEN_REGEX.findall(text.lower())

class LogIndexer:
    def __init__(self):
        self.index: Dict[str, List[str]] = defaultdict(list)
        self.total_files = 0
        self.total_lines = 0

    def build_index(self, folder_path: str, output_zip_path: str) -> Tuple[int, int, int]:
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Folder '{folder_path}' does not exist.")

        log_files: List[str] = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                if not file.endswith(".zip") and not file.endswith(".pkl"):
                    log_files.append(os.path.join(root, file))

        log_files.sort()
        self.total_files = len(log_files)
        self.total_lines = 0

        pkl_path = "index.pkl"

        for file_path in log_files:
            rel_name = os.path.basename(file_path)
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    for line_num, line in enumerate(f, 1):
                        self.total_lines += 1
                        tokens = set(normalize_tokens(line))
                        posting = f"{rel_name}:{line_num}"
                        for tok in tokens:
                            self.index[tok].append(posting)
            except Exception as e:
                pass

        unique_tokens_count = len(self.index)

        with open(pkl_path, "wb") as pkl_file:
            pickle.dump(dict(self.index), pkl_file)

        with zipfile.ZipFile(output_zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(pkl_path, arcname="index.pkl")
            for file_path in log_files:
                rel_name = os.path.basename(file_path)
                zipf.write(file_path, arcname=rel_name)

        if os.path.exists(pkl_path):
            os.remove(pkl_path)

        return self.total_files, self.total_lines, unique_tokens_count

    @staticmethod
    def search_index(source_path: str, query_tokens: List[str]) -> Dict[str, List[str]]:
        index: Dict[str, List[str]] = {}

        if source_path.endswith(".zip"):
            with zipfile.ZipFile(source_path, "r") as zipf:
                if "index.pkl" in zipf.namelist():
                    with zipf.open("index.pkl") as pkl_file:
                        index = pickle.load(pkl_file)
                else:
                    raise FileNotFoundError("index.pkl not found inside zip file.")
        elif source_path.endswith(".pkl"):
            with open(source_path, "rb") as pkl_file:
                index = pickle.load(pkl_file)
        else:
            raise ValueError("Search source must be a .zip or .pkl file")

        results: Dict[str, List[str]] = {}
        for token in query_tokens:
            norm_tok = token.lower()
            results[token] = index.get(norm_tok, [])
        return results

if __name__ == "__main__":
    if len(sys.argv) >= 4:
        mode = sys.argv[1].upper()
        if mode == "BUILD":
            folder = sys.argv[2]
            zip_out = sys.argv[3]
            indexer = LogIndexer()
            f_cnt, l_cnt, t_cnt = indexer.build_index(folder, zip_out)
            print(f"FILES {f_cnt}")
            print(f"LINES {l_cnt}")
            print(f"TOKENS {t_cnt}")
        elif mode == "SEARCH":
            src = sys.argv[2]
            tokens = sys.argv[3:]
            res = LogIndexer.search_index(src, tokens)
            for tok, matches in res.items():
                for m in matches:
                    print(f"{tok}:{m}")
