import os
import chardet

def find_non_utf8_files(directory):
    non_utf8_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                result = chardet.detect(raw_data)
                if result['encoding'] != 'utf-8':
                    non_utf8_files.append((file_path, result['encoding']))
    return non_utf8_files

def convert_to_utf8(file_path, encoding):
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            content = f.read()
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Converted {file_path} from {encoding} to utf-8.")
    except Exception as e:
        print(f"Failed to convert {file_path}: {e}")

if __name__ == "__main__":
    directory = "."  # specify your project directory here
    non_utf8_files = find_non_utf8_files(directory)
    
    if non_utf8_files:
        print(f"Found {len(non_utf8_files)} non-UTF-8 encoded files.")
        for file_path, encoding in non_utf8_files:
            convert_to_utf8(file_path, encoding)
    else:
        print("All files are UTF-8 encoded.")
