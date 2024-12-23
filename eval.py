import argparse
import json


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def scan_file(file_path, level=None, n_char=120):
    with open(file_path, "r") as f:
        scan_result = json.load(f)

    for file, content in scan_result.items():
        print(bcolors.WARNING + f"Scanning file {file}" + bcolors.ENDC)
        for item in content:
            if level and item["level"] != level:
                continue
            print(bcolors.FAIL + f"Level: {item['level']}" + bcolors.ENDC)
            print(bcolors.OKBLUE + f"Ref: {item['reference']}" + bcolors.ENDC)
            reason = item["reason"]
            print("Reason:")
            for i in range(0, len(reason), n_char):
                print(bcolors.OKGREEN + reason[i:i + n_char] + bcolors.ENDC)
            user_input = input("Press 'n' for next issue, 'f' if you fixed the issue, or 'b' to go to the next file: ")
            if user_input == "b":
                print("Skipping file...")
                break
            elif user_input == "f":
                content.remove(item)
                with open(file_path, "w") as f:
                    json.dump(scan_result, f, indent=4)
                print("Issue fixed and saved to file.")
            elif user_input == "n":
                print("Skipping issue...")
                continue
            else:
                print("Invalid input. Please try again.")
        print(f"Finished scanning file {file}")


def main():
    parser = argparse.ArgumentParser(description="Scan source code for security issues.")
    parser.add_argument("file", type=str, help="Directory to scan")
    parser.add_argument("--level", type=str, default="", help="only show issues of this level")
    args = parser.parse_args()

    scan_file(args.file, args.level)


if __name__ == "__main__":
    main()
