uv run parse_code.py ../../App/python-server/ --replace-source ../../App --replace-target ./App -o ../data/backend_code.txt -e ../data/exclude_imports.txt
uv run parse_contents.py -d ../../ -r --exclude-dirs ../data/exclude_dirs.txt --exclude-files ../data/exclude_files.txt -o ../data/project_structure.txt
uv run parse_files.py --exclude-dirs ../data/exclude_dirs.txt --exclude-files ../data/exclude_files.txt -o ../data/project_files.txt ../../ 

uv run update_database.py
