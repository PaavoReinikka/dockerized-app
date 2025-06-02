ALTER TABLE code
ADD CONSTRAINT code_file_type_name_start_line_unique UNIQUE (file, type, name, start_line);
