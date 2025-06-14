import argparse
import sys
import json
import ast
import jedi
from pathlib import Path
from stdlib_list import stdlib_list


def OLDread_excluded_imports(exclude_path):
    '''
    Read excluded imports from a file.
    Args:
        exclude_path (str): Path to the file containing excluded imports.
    Returns:
        dict: A dictionary with excluded imports.
    '''

    if not exclude_path or not Path(exclude_path).is_file():
        return set()
    with open(exclude_path, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())
    
def read_excluded_imports(exclude_path):
    '''
    Read excluded imports from a file.
    Args:
        exclude_path (str): Path to the file containing excluded imports.
    Returns:
        tuple: (set of excluded imports, exclude_all_imports flag)
    '''
    if not exclude_path or not Path(exclude_path).is_file():
        return set(), False
    with open(exclude_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    exclude_all_imports = any(line.startswith("*") for line in lines)
    return set(lines), exclude_all_imports


def read_excluded_paths(exclude_paths_file):
    """
    Read excluded paths from a file.
    Each line should be a path (relative or absolute).
    """
    if not exclude_paths_file or not Path(exclude_paths_file).is_file():
        return set()
    with open(exclude_paths_file, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())


def get_ast_code_blocks(filepath, excluded_imports=None):
    '''
    Parse a Python file and extract code blocks (functions, classes, imports).
    Args:
        filepath (str): Path to the Python file.
        excluded_imports (set): Set of import names to exclude.
    Returns:
        dict: Dictionary with code block information.
    '''
    source = Path(filepath).read_text(encoding="utf-8")
    tree = ast.parse(source)
    results = {}
    for node in ast.walk(tree):
        # Exclude selected imports
        if isinstance(node, ast.Import):
            # Check all imported names
            skip = False
            for alias in node.names:
                if excluded_imports and (alias.name in excluded_imports or any(alias.name.startswith(ex + ".") for ex in excluded_imports)):
                    skip = True
                    break
            if skip:
                continue
            module = node.names[0].name
            name = module
            start = node.lineno
            end = node.lineno
            code = "\n".join(source.splitlines()[start - 1:end])
            results[name] = {
                "start": start,
                "end": end,
                "code": code,
                "type": "import",
                "docstring": None
            }
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            # Exclude if module or any imported name matches
            skip = False
            if excluded_imports and (module in excluded_imports or any(module.startswith(ex + ".") for ex in excluded_imports)):
                skip = True
            if not skip and excluded_imports:
                for alias in node.names:
                    full_import = f"{module}.{alias.name}" if module else alias.name
                    if full_import in excluded_imports or any(full_import.startswith(ex + ".") for ex in excluded_imports):
                        skip = True
                        break
            if skip:
                continue
            name = module
            start = node.lineno
            end = node.lineno
            code = "\n".join(source.splitlines()[start - 1:end])
            results[name] = {
                "start": start,
                "end": end,
                "code": code,
                "type": "import",
                "docstring": None
            }
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            name = node.name
            start = node.lineno
            end = max([n.lineno for n in ast.walk(node) if hasattr(n, "lineno")], default=start)
            code = "\n".join(source.splitlines()[start - 1:end])
            results[name] = {
                "start": start,
                "end": end,
                "code": code,
                "type": "class" if isinstance(node, ast.ClassDef) else "function",
                "docstring": ast.get_docstring(node)
            }
    return results


def OLDparse_file(filepath, excluded_imports=None):
    '''
    Parse a Python file and extract code blocks (functions, classes, imports).
    Args:
        filepath (str): Path to the Python file.
        excluded_imports (set): Set of import names to exclude.
    Returns:
        list: List of dictionaries containing code block information.
    '''
    source = Path(filepath).read_text(encoding="utf-8")
    tree = ast.parse(source)
    script = jedi.Script(code=source, path=str(filepath))
    blocks = []

    # Helper to check if an import should be excluded
    def is_excluded(name):
        return excluded_imports and (
            name in excluded_imports or any(name.startswith(ex + ".") for ex in excluded_imports)
        )

    module_docstring = ast.get_docstring(tree)
    if module_docstring:
        blocks.append({
            "file": str(filepath),
            "type": "module",
            "name": "__module__",
            "docstring": module_docstring,
            "start_line": 1,
            "code": "",
        })

    # Collect all blocks from AST
    for node in ast.walk(tree):
        """
        # uncomment these blocks if you want to include docstrings imports
        if isinstance(node, ast.Import):
            if any(is_excluded(alias.name) for alias in node.names):
                continue
            name = node.names[0].name
            code = source.splitlines()[node.lineno - 1]
            blocks.append({
                "file": str(filepath),
                "type": "import",
                "name": name,
                "docstring": None,
                "start_line": node.lineno,
                "code": code,
            })
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if is_excluded(module) or any(is_excluded(f"{module}.{alias.name}") for alias in node.names):
                continue
            code = source.splitlines()[node.lineno - 1]
            blocks.append({
                "file": str(filepath),
                "type": "import",
                "name": module,
                "docstring": None,
                "start_line": node.lineno,
                "code": code,
            })
            """
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            name = node.name
            start = node.lineno
            end = max([n.lineno for n in ast.walk(node) if hasattr(n, "lineno")], default=start)
            code = "\n".join(source.splitlines()[start - 1:end])
            dtype = "class" if isinstance(node, ast.ClassDef) else "function"
            docstring = ast.get_docstring(node)
            blocks.append({
                "file": str(filepath),
                "type": dtype,
                "name": name,  # will update to full_name below
                "docstring": docstring,
                "start_line": start,
                "code": code,
            })

    # Use Jedi to update names and docstrings for functions/classes
    jedi_defs = {d.name: d for d in script.get_names(all_scopes=True, definitions=True) if d.type in ("class", "function")}
    for block in blocks:
        if block["type"] in ("class", "function"):
            jedi_def = jedi_defs.get(block["name"])
            if jedi_def:
                block["name"] = jedi_def.full_name or block["name"]
                if not block["docstring"]:
                    block["docstring"] = jedi_def.docstring(raw=True)

    return blocks


def parse_file(filepath, excluded_imports=None, exclude_all_imports=False):
    """
    Parse a Python file and extract code blocks (functions, classes, imports).
    Args:
        filepath (str): Path to the Python file.
        excluded_imports (set): Set of import names to exclude.
        exclude_all_imports (bool): If True, exclude all imports.
    Returns:
        list: List of dictionaries containing code block information.
    """
    source = Path(filepath).read_text(encoding="utf-8")
    tree = ast.parse(source)
    script = jedi.Script(code=source, path=str(filepath))
    blocks = []

    def is_excluded(name):
        return excluded_imports and (
            name in excluded_imports or any(name.startswith(ex + ".") for ex in excluded_imports)
        )

    # Module-level docstring
    module_docstring = ast.get_docstring(tree)
    if module_docstring:
        blocks.append({
            "file": str(filepath),
            "type": "module",
            "name": "__module__",
            "docstring": module_docstring,
            "start_line": 1,
            "code": "",
        })

    # Collect all blocks from AST
    for node in ast.walk(tree):
        # Exclude all imports if flag is set
        if exclude_all_imports and isinstance(node, (ast.Import, ast.ImportFrom)):
            continue

        # Imports
        if isinstance(node, ast.Import):
            if any(is_excluded(alias.name) for alias in node.names):
                continue
            name = node.names[0].name
            code = source.splitlines()[node.lineno - 1]
            blocks.append({
                "file": str(filepath),
                "type": "import",
                "name": name,
                "docstring": None,
                "start_line": node.lineno,
                "code": code,
            })
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if is_excluded(module) or any(is_excluded(f"{module}.{alias.name}") for alias in node.names):
                continue
            code = source.splitlines()[node.lineno - 1]
            blocks.append({
                "file": str(filepath),
                "type": "import",
                "name": module,
                "docstring": None,
                "start_line": node.lineno,
                "code": code,
            })

        # Functions, Classes
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            name = node.name
            start = node.lineno
            end = max([n.lineno for n in ast.walk(node) if hasattr(n, "lineno")], default=start)
            code = "\n".join(source.splitlines()[start - 1:end])
            dtype = "class" if isinstance(node, ast.ClassDef) else "function"
            docstring = ast.get_docstring(node)
            blocks.append({
                "file": str(filepath),
                "type": dtype,
                "name": name,  # will update to full_name below
                "docstring": docstring,
                "start_line": start,
                "code": code,
            })

    # Use Jedi to update names and docstrings for functions/classes
    jedi_defs = {d.name: d for d in script.get_names(all_scopes=True, definitions=True) if d.type in ("class", "function")}
    for block in blocks:
        if block["type"] in ("class", "function"):
            jedi_def = jedi_defs.get(block["name"])
            if jedi_def:
                block["name"] = jedi_def.full_name or block["name"]
                if not block["docstring"]:
                    block["docstring"] = jedi_def.docstring(raw=True)

    return blocks


def iter_parsed_python_files(path, excluded_imports=None, recursive=True, excluded_paths=None, exclude_all_imports=False):
    """
    Walk through a directory and yield parsed code blocks for each .py file,
    skipping hidden directories and any paths in excluded_paths.

    Args:
        path (str or Path): Directory or file path to process.
        excluded_imports (set): Set of import names to exclude.
        recursive (bool): Whether to search directories recursively.
        excluded_paths (set): Set of paths (as strings) to exclude.
        exclude_all_imports (bool): If True, exclude all imports.

    Yields:
        (str, list): Tuple of file path and list of code blocks.
    """
    path = Path(path)
    excluded_paths = set(excluded_paths or [])

    def is_excluded_path(p):
        return any(str(p).startswith(str(Path(ex))) for ex in excluded_paths)

    if path.is_file() and path.suffix == ".py" and not is_excluded_path(path):
        yield str(path), parse_file(str(path), excluded_imports=excluded_imports, exclude_all_imports=exclude_all_imports)
    elif path.is_dir():
        for entry in path.iterdir():
            if entry.name.startswith('.'):
                continue  # Skip hidden files/directories
            if is_excluded_path(entry):
                continue
            if entry.is_file() and entry.suffix == ".py":
                yield str(entry), parse_file(str(entry), excluded_imports=excluded_imports, exclude_all_imports=exclude_all_imports)
            elif entry.is_dir() and recursive:
                yield from iter_parsed_python_files(
                    entry,
                    excluded_imports=excluded_imports,
                    recursive=recursive,
                    excluded_paths=excluded_paths,
                    exclude_all_imports=exclude_all_imports
                )


def print_code_blocks(code_blocks):
    for block in code_blocks:
        print(f"File: {block['file']}")
        print(f"Type: {block['type']}")
        print(f"Name: {block['name']}")
        print(f"Docstring: {block['docstring']}")
        print(f"Start Line: {block['start_line']}")
        print(f"Code:\n{block['code']}")
        print("-" * 40)

def code_block_to_string(code_block):
    return f"""
    File: {code_block['file']}
    Type: {code_block['type']}
    Name: {code_block['name']}
    Docstring: {code_block['docstring']}
    Start Line: {code_block['start_line']}
    Code:
    {code_block['code']}
    """

def format_code_blocks(code_blocks):
    """
    Format code blocks for better readability.
    """
    formatted_blocks = []
    for block in code_blocks:
        formatted_blocks.append(code_block_to_string(block))
    return formatted_blocks

def replace_filepath_prefix(blocks, old_prefix, new_prefix):
    """
    Replace the beginning of the file path in each code block.
    """
    for block in blocks:
        if block["file"].startswith(old_prefix):
            block["file"] = block["file"].replace(old_prefix, new_prefix, 1)
    return blocks

def save_code_blocks_to_json(code_blocks, output_path):
    """
    Save code blocks to a JSON file.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(code_blocks, f, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description="Parse Python code files and extract code blocks.")
    parser.add_argument("filepath", help="Path to a Python file or directory to parse.")
    parser.add_argument("-e", "--exclude", help="Path to file with excluded imports.", default=None)
    parser.add_argument("-o", "--output", help="Output JSON file path.", default="parsed_code_blocks.json")
    parser.add_argument("--replace-source", help="Filepath prefix to replace.", default=None)
    parser.add_argument("--replace-target", help="Replacement for filepath prefix.", default=None)
    args = parser.parse_args()

    if args.replace_source and not args.replace_target:
        args.replace_target = "."

    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    std_libs = set(stdlib_list(python_version))
    excluded_imports, exclude_all_imports = read_excluded_imports(args.exclude)
    excluded_imports = excluded_imports | std_libs

    all_blocks = []
    for _, code_blocks in iter_parsed_python_files(
            args.filepath,
            excluded_imports=excluded_imports,
            recursive=True,
            exclude_all_imports=exclude_all_imports
        ):
        # Only replace if both source and target are provided
        if args.replace_source is not None and args.replace_target is not None:
            code_blocks = replace_filepath_prefix(code_blocks, args.replace_source, args.replace_target)
        all_blocks.extend(code_blocks)

        if not args.output:
            for block in code_blocks:
                print(code_block_to_string(block))
                print("=" * 40)
    
    if args.output:
        save_code_blocks_to_json(all_blocks, args.output)


if __name__ == "__main__":
    main()