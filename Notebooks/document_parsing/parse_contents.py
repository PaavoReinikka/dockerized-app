import os
import sys
import argparse

def read_exclude_list(path):
    if not path or not os.path.isfile(path):
        return set()
    with open(path, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())

def OLDprint_directory_contents(directory_path, prefix="", recursive=True, output_file=None, _acc=None, exclude_dirs=None, exclude_files=None):
    '''
    Recursively lists the contents of a directory in a tree-like format.
    Files are listed before directories at each level.
    Exclusion supports both exact names and suffixes for files.
    '''
    if _acc is None:
        _acc = []
    if exclude_dirs is None:
        exclude_dirs = set()
    if exclude_files is None:
        exclude_files = set()
    if not os.path.isdir(directory_path):
        msg = f"Error: The path '{directory_path}' is not a directory."
        print(msg)
        _acc.append(msg)
        if output_file:
            with open(output_file, "w") as f:
                f.write("\n".join(_acc) + "\n")
        return

    is_excluded_file = lambda name: any(name == excl or name.endswith(excl) for excl in exclude_files)

    try:
        entries = sorted(os.scandir(directory_path), key=lambda e: e.name)
        files = [
            e for e in entries
            if e.is_file() and not e.name.startswith(".") and not is_excluded_file(e.name)
        ]
        dirs = [
            e for e in entries
            if e.is_dir() and not e.name.startswith(".") and e.name not in exclude_dirs
        ]
        all_entries = files + dirs
        entries_count = len(all_entries)

        for index, entry in enumerate(all_entries):
            connector = "└── " if index == entries_count - 1 else "├── "
            line = f"{prefix}{connector}{entry.name}"
            print(line)
            _acc.append(line)

            if entry.is_dir() and recursive:
                new_prefix = prefix + ("    " if index == entries_count - 1 else "│   ")
                print_directory_contents(
                    entry.path, new_prefix, recursive, output_file, _acc, exclude_dirs, exclude_files
                )

    except FileNotFoundError:
        msg = f"Error: The directory '{directory_path}' does not exist."
        print(msg)
        _acc.append(msg)
    except PermissionError:
        msg = f"Error: Permission denied for accessing '{directory_path}'."
        print(msg)
        _acc.append(msg)
    if output_file:
        with open(output_file, "w") as f:
            f.write("\n".join(_acc) + "\n")

def print_directory_contents(directory_path, prefix="", recursive=True, output_file=None, _acc=None, exclude_dirs=None, exclude_files=None):
    '''
    Recursively lists the contents of a directory in a tree-like format.
    Files are listed before directories at each level.
    Exclusion supports both exact names and suffixes for files.
    '''
    if _acc is None:
        _acc = []
    if exclude_dirs is None:
        exclude_dirs = set()
    if exclude_files is None:
        exclude_files = set()
    if not os.path.isdir(directory_path):
        msg = f"Error: The path '{directory_path}' is not a directory."
        print(msg)
        _acc.append(msg)
        if output_file:
            with open(output_file, "w") as f:
                f.write("\n".join(_acc) + "\n")
        return

    def is_excluded_file(name):
        return (
            name.startswith(".") or
            any(name == excl or name.endswith(excl) for excl in exclude_files)
        )

    def is_excluded_dir(name):
        return (
            name.startswith(".") or
            name in exclude_dirs
        )

    try:
        entries = sorted(os.scandir(directory_path), key=lambda e: e.name)
        files = [
            e for e in entries
            if e.is_file() and not is_excluded_file(e.name)
        ]
        dirs = [
            e for e in entries
            if e.is_dir() and not is_excluded_dir(e.name)
        ]
        all_entries = files + dirs
        entries_count = len(all_entries)

        for index, entry in enumerate(all_entries):
            connector = "└── " if index == entries_count - 1 else "├── "
            line = f"{prefix}{connector}{entry.name}"
            print(line)
            _acc.append(line)

            if entry.is_dir() and recursive:
                new_prefix = prefix + ("    " if index == entries_count - 1 else "│   ")
                print_directory_contents(
                    entry.path, new_prefix, recursive, output_file, _acc, exclude_dirs, exclude_files
                )

    except FileNotFoundError:
        msg = f"Error: The directory '{directory_path}' does not exist."
        print(msg)
        _acc.append(msg)
    except PermissionError:
        msg = f"Error: Permission denied for accessing '{directory_path}'."
        print(msg)
        _acc.append(msg)
    if output_file:
        with open(output_file, "w") as f:
            f.write("\n".join(_acc) + "\n")

def main():
    parser = argparse.ArgumentParser(description="Print directory tree.")
    parser.add_argument("-d", "--directory", help="Path to the directory to list.", required=True)
    parser.add_argument("-r", "--recursive", action="store_true", help="Recursively list directory contents.")
    parser.add_argument("-o", "--output", help="Output file to save the result.", default=None)
    parser.add_argument("--exclude-dirs", help="Path to file with directory names to exclude.", default=None)
    parser.add_argument("--exclude-files", help="Path to file with file names to exclude.", default=None)
    args = parser.parse_args()

    exclude_dirs = read_exclude_list(args.exclude_dirs)
    exclude_files = read_exclude_list(args.exclude_files)

    print_directory_contents(
        args.directory,
        recursive=args.recursive,
        output_file=args.output,
        exclude_dirs=exclude_dirs,
        exclude_files=exclude_files
    )

if __name__ == "__main__":
    main()