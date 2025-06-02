import os
import sys
import json
import argparse

def read_exclude_list(path):
    if not path or not os.path.isfile(path):
        return set()
    with open(path, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())

def get_file_contents(file_path):
    if not os.path.isfile(file_path):
        return None
    if not os.access(file_path, os.R_OK):
        return None
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception:
        return None

def parse_directory_path(
    directory_path, 
    exclude_dirs=None, 
    exclude_files=None, 
    prefix="", 
    recursive=True
):
    '''
    Parse the directory path and return its contents as a nested dict.
    '''
    if not os.path.isdir(directory_path):
        return {}
    exclude_dirs = set(exclude_dirs or [])
    exclude_files = set(exclude_files or [])
    contents = {}
    try:
        entries = sorted(os.scandir(directory_path), key=lambda e: e.name)
        for entry in entries:
            # Exclude dirs/files by name or ending
            if entry.is_dir():
                if entry.name in exclude_dirs or entry.name.startswith("."):
                    continue
            if entry.is_file():
                if entry.name in exclude_files or any(entry.name.endswith(suffix) for suffix in exclude_files):
                    continue
                if entry.name.startswith("."):
                    continue
            if entry.is_dir() and recursive:
                contents[entry.name] = parse_directory_path(
                    entry.path, exclude_dirs, exclude_files, prefix, recursive
                )
            elif entry.is_file():
                content = get_file_contents(entry.path)
                if content is not None:
                    contents[entry.name] = content
    except Exception:
        pass
    return contents

def flatten_dict_with_paths(d, parent_path="", append_root=False):
    """
    Flattens a nested dictionary from parse_directory_path, prepending keys with their full path.
    The key will be the full path from the root directory.
    """
    flat = {}
    for k, v in d.items():
        current_path = os.path.join(parent_path, k) if parent_path else k
        if isinstance(v, dict):
            flat.update(flatten_dict_with_paths(v, current_path))
        else:
            # Use the full path as the key (normalized)
            flat[os.path.normpath(current_path)] = v
    if append_root:
        flat = {os.path.normpath(os.path.join("./", k)): v for k, v in flat.items()}
    return flat

def append_prefix(flat_dict, prefix):
    """
    Append the beginning of each key in the dict with the given prefix.
    """
    return {os.path.join(prefix, k): v for k, v in flat_dict.items()}


def save_dict_to_json(d, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)

def main():
    parser = argparse.ArgumentParser(description="Parse a project directory and output file contents as JSON.")
    parser.add_argument("directory", help="Path to the directory to parse.")
    parser.add_argument("-o", "--output", help="Output JSON file path.", default="file_contents.json")
    parser.add_argument("--append-prefix", help="Filepath prefix.", default="./")
    parser.add_argument("--exclude-dirs", help="Path to file with directory names to exclude.", default=None)
    parser.add_argument("--exclude-files", help="Path to file with file names or endings to exclude.", default=None)
    args = parser.parse_args()

    exclude_dirs = read_exclude_list(args.exclude_dirs) | set(["node_modules",".git", "__pycache__", ".idea", ".vscode"])
    exclude_files = read_exclude_list(args.exclude_files)

    nested = parse_directory_path(
        args.directory, 
        exclude_dirs=exclude_dirs, 
        exclude_files=exclude_files, 
        recursive=True
    )
    flat = flatten_dict_with_paths(nested, append_root=True)
    flat = append_prefix(flat, args.append_prefix)

    if args.output:
        save_dict_to_json(flat, args.output)
    else:
        for k, v in flat.items():
            print(f"{k}:\n{v[:80]}...\n{'-'*40}")

if __name__ == "__main__":
    main()