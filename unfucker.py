import os
import argparse
import mimetypes
import re
import logging
from typing import Any, Optional, Tuple

logging.basicConfig(level=logging.INFO)

class Unfucker:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file_type = self._identify_file_type()

    def _identify_file_type(self) -> str:
        mime_type, _ = mimetypes.guess_type(self.file_path)
        
        if mime_type == 'application/json':
            return 'json'
        elif mime_type == 'application/xml':
            return 'xml'
        # Extend for more file types

        _, file_extension = os.path.splitext(self.file_path)
        return file_extension.lower()[1:]

    def save_to_file(self, content: Any, file_path: str, overwrite: bool) -> None:
        if os.path.exists(file_path) and not overwrite:
            logging.error("File already exists. Use --overwrite to overwrite the existing file.")
            return

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        logging.info(f"Saved unfucked content to {file_path}")

    def unfuck(self) -> Tuple[Optional[Any], Optional[str]]:
        try:
            with open(self.file_path, 'r') as f:
                file_content = f.read()
        except Exception as e:
            return None, f"Could not read file: {e}"

        unfuck_func = getattr(self, f'_unfuck_{self.file_type}', None)
        if unfuck_func:
            return unfuck_func(file_content)
        else:
            return None, f"File type {self.file_type} not supported"

    def _unfuck_json(self, file_content: str) -> Tuple[Optional[Any], Optional[str]]:
        import json

        # Replace missing or extra commas
        file_content = re.sub(r',\s*}', '}', file_content)
        file_content = re.sub(r',\s*]', ']', file_content)

        # Add missing closing brackets or braces
        open_braces = file_content.count('{')
        close_braces = file_content.count('}')
        open_brackets = file_content.count('[')
        close_brackets = file_content.count(']')

        file_content += '}' * (open_braces - close_braces)
        file_content += ']' * (open_brackets - close_brackets)

        # Quote unquoted keys
        file_content = re.sub(r'([{,]\s*)(")?([a-zA-Z_][a-zA-Z_0-9]*)(")?\s*:', r'\1"\3":', file_content)

        # Quote unquoted string values
        file_content = re.sub(r':\s*([^"\d\[\]{},\s]+)([,\]})])', r': "\1"\2', file_content)

        try:
            fixed_content = json.loads(file_content)
            return fixed_content, None
        except json.JSONDecodeError as e:
            return None, f"Could not unfuck JSON: {e}"

    def _unfuck_xml(self, file_content: str) -> Tuple[Optional[Any], Optional[str]]:
        import xml.etree.ElementTree as ET
        import re

        # Remove invalid characters
        file_content = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', file_content)

        # Fix missing attribute quotes
        file_content = re.sub(r'(<\w+ \w+)=([^\s>]+)', r'\1="\2"', file_content)

        # Fix mismatched or unclosed tags
        stack = []
        offset = 0
        for match in re.finditer(r'<(/?)(\w+)', file_content):
            tag = match.group(2)
            is_closing = bool(match.group(1))

            if is_closing:
                if stack and stack[-1] == tag:
                    stack.pop()
                else:
                    # Extra closing tag found; remove it
                    start, end = match.span()
                    file_content = file_content[:start + offset] + file_content[end + offset:]
                    offset -= (end - start)
            else:
                stack.append(tag)

        # Add missing closing tags at the end
        for tag in reversed(stack):
            file_content += f'</{tag}>'

        try:
            # Try parsing the modified XML string
            ET.fromstring(file_content)
            return file_content, None
        except ET.ParseError as e:
            return None, f"Could not unfuck XML: {e}"


    def _unfuck_txt(self, file_content: str) -> Tuple[Optional[Any], Optional[str]]:
        import chardet  # For encoding detection
        from collections import Counter

        # Step 1: Try to read the file in the standard way first
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
            return file_content, None
        except Exception as e:
            pass  # Continue to the next recovery steps

        # Step 2: Attempt binary read and per-line decoding with utf-8
        decoded_lines = []
        try:
            with open(self.file_path, 'rb') as f:
                lines = f.readlines()
            for line in lines:
                try:
                    decoded_line = line.decode('utf-8')
                    decoded_lines.append(decoded_line)
                except UnicodeDecodeError:
                    pass
        except Exception as e:
            return None, f"Could not read the binary file: {e}"

        # Step 3: If Step 2 fails, try to detect encoding and decode accordingly
        if not decoded_lines:
            with open(self.file_path, 'rb') as f:
                result = chardet.detect(f.read())
            try:
                encoding_type = result['encoding']
                with open(self.file_path, 'r', encoding=encoding_type) as f:
                    file_content = f.read()
                return file_content, None
            except Exception as e:
                return None, f"Failed to decode with detected encoding: {e}"

        # Check if decoded_lines is empty (all lines were corrupted)
        if not decoded_lines:
            return None, "The file appears to be irreparably fucked."

        # Step 4: Text Cleaning - Only applied if previous steps succeeded
        file_content = "".join(decoded_lines)

        # Remove duplicate lines
        file_content = "\n".join(dict.fromkeys(file_content.split("\n")))

        # Remove any non-printable characters
        file_content = ''.join(filter(lambda x: x in set(
            "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]_^`{|}~ \t\n\r"), file_content))

        return file_content, None



def unfuck(file_path: str, output_path: Optional[str], overwrite: bool):
    unfucker = Unfucker(file_path)
    fixed_content, error = unfucker.unfuck()

    if fixed_content is not None:
        if output_path:
            unfucker.save_to_file(str(fixed_content), output_path, overwrite)
        else:
            print(f"Unfucked content: {fixed_content}")
    else:
        logging.error(f"Error: {error}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Unfuck corrupted or malformed text files.")
    parser.add_argument("file_path", type=str, help="Path to the file to be unfucked")
    parser.add_argument("-o", "--output", type=str, help="Path to save the unfucked file", default=None)
    parser.add_argument("--overwrite", help="Overwrite the output file if it exists", action="store_true")
    
    args = parser.parse_args()
    unfuck(args.file_path, args.output, args.overwrite)
