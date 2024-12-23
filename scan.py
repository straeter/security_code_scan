import argparse
import json
import os
from datetime import datetime

from tqdm import tqdm

from utils.gpt import llm


def get_prompt(code_chunk, results):
    previous_results = []
    for res in results[-3:]:
        previous_results.append(f"""
        "{res['title']}" at lines: {res['reference']}\n
        """)

    previous_str = f"""As we work with overlapping chunks, here are the last {len(previous_results)} security risks that were found in the previous chunk (so that you can avoid duplicates):\n
""" + "\n".join(
        previous_results) + "\n" + "These were the previous security risks, now continue with your evaluation." if previous_results else ""

    prompt = code_chunk + r"""
Above I have included a chunk of my flask python webapp code (including the line number at the start of each line). You should scan it for potential security risks of any kind.

""" + previous_str + r"""

Please format your response in the following json format:

{
    "1": {
    "title": "short description of the issue",
    "reference": "quote the lines that compose the security risk (including line numbers). If there are unrelated lines in between use \n ... \n to skip them",
    "reason": "explanation of the security risk in 1-10 sentences (depending on the complexity)",
    "level": "severity level (how dangerous, obvious and easy to exploit this risk is) from 1 (low risk) to 5 (high risk)"
    },
    "2": {
    "title": "...",
    "reference": "...",
    "reason": "...",
    "level": "..."
    }, ...
}

You can start now
"""
    return prompt


def scan_file(file_path: str, chunk_length: int = 200, overlap: int = 20):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for j, line in enumerate(lines):
        lines[j] = f"{j + 1}: {line}"

    all_results = []
    results = []

    for chunk_start in range(0, len(lines), chunk_length - overlap):

        chunk_end = min(chunk_start + chunk_length, len(lines))
        code_chunk = "".join(lines[chunk_start:chunk_end])

        if code_chunk.stript() == "":
            continue

        prompt = get_prompt(code_chunk, results)

        rsp_dict = llm.chat(
            prompt=prompt,
            json_mode=True
        )

        results = []
        for key, item in rsp_dict.items():
            result = item.copy()
            results.append(result)

        all_results.extend(results)

    return all_results


def scan_directory(directory: str, outfile: str, file_types: list):
    files_to_scan = [os.path.join(root, file) for root, _, files in os.walk(directory) for file in files if
                     any(file.endswith(ft) for ft in file_types)]

    scan_results = {}

    if os.path.exists(outfile):
        print(f"Loading previous scan results from {outfile}")
        with open(outfile, "r") as f:
            scan_results = json.load(f)
        scanned_files = list(scan_results.keys())
    else:
        scanned_files = []

    for file_path in tqdm(files_to_scan, desc="Scanning files"):
        if file_path not in scanned_files:
            print(f"Scanning {file_path}")
            scan_results[file_path] = scan_file(file_path)

        with open(outfile, "w") as f:
            json.dump(scan_results, f, indent=4)


def scan():
    parser = argparse.ArgumentParser(description="Scan source code for security issues.")
    parser.add_argument("directory", type=str, help="Directory to scan")
    parser.add_argument("--out-file", type=str, help="Name of file to save results to")
    parser.add_argument("--file-types", type=str, nargs="+", default=[".py"], help="File types to scan, e.g., .py .js")
    args = parser.parse_args()

    if not args.out_file:
        timestamp = datetime.now().strftime("%Y-%m-%d")
        outfile = f"security_scans/security_scan_results_{timestamp}.json"
        os.makedirs("security_scans", exist_ok=True)
    else:
        outfile = args.out_file

    scan_directory(args.directory, outfile, args.file_types)


if __name__ == "__main__":
    scan()
