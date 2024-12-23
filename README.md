# security_code_scan
Use LLMs to scan your code for security issue.

The script goes through the files of your repo, scans them one by one and outputs the security issues found in a json file.

## How to use
1. Install the required packages
```bash
pip install -r requirements.txt
```
(optionally you can first create a virtual environment)

2. Create a .env file in the root folder with the following content (or copy/paste the content of the .env.example file)
```bash
OPENAI_API_KEY=<your_openai_api_key>
```

3. Run the following command to scan your code in your folder
```bash
python scan.py <path_to_folder> --out-file <output_file> --file-types <file_types>
```
- path_to_folder: the path to the folder you want to scan
- output_file: the path to the output file (otherwise will default to the current date)
- file_types: the file types you want to scan (default to .py)

The output will be saved in folder security_scans.

4. Run the following command to go through the issues one by one:
```bash
python eval.py <path_to_output_file> --level <level>
```
- path_to_output_file: the path to the output file with security scan results
- level: the level (1-5) of the issues you want to go through (default to None which means all levels)

## Format of the output file

The output file of the security scan is a json file with the following format:
```json
{
    "file_path": [
        {
            "title": "title of the issue",
            "reference": "problematic lines (with numbers)",
            "level": "level of security issue: 1 (low) - 5 (high)",
            "reason": "explanation of the issue"
        },
      ...
    ],
  ...
}
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

