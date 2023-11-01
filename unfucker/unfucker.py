import os
import sys
import argparse
import mimetypes
import json
import re
import logging
from typing import Any, Optional, Tuple
from xml.etree.ElementTree import fromstring, ParseError
import chardet  # For encoding detection

logging.basicConfig(level=logging.INFO)

class Unfucker:
    """Class for fixing corrupted or malformed text files."""

    def __init__(self, file_path: str, max_iterations: int = 10):
        self.file_path = file_path
        self.file_type = self._identify_file_type()
        self.max_iterations = max_iterations

    def _identify_file_type(self) -> str:
        mime_type, _ = mimetypes.guess_type(self.file_path)
        
        if mime_type == 'application/json':
            return 'json'
        elif mime_type == 'application/xml':
            return 'xml'

        _, file_extension = os.path.splitext(self.file_path)
        return file_extension.lower()[1:]

    def save_to_file(self, content: Any, file_path: str, overwrite: bool) -> None:
        if os.path.exists(file_path) and not overwrite:
            logging.error("File already exists. Use --overwrite to overwrite the existing file.")
            return

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        logging.info(f"Saved unfucked content to {file_path}")

    def _retry_open_file(self, num_retries: int = 3) -> Tuple[Optional[str], Optional[str]]:
        for i in range(num_retries):
            try:
                with open(self.file_path, 'r') as f:
                    return f.read(), None
            except Exception as e:
                logging.warning(f"Could not read file on attempt {i + 1}: {e}")

        return None, "Reached maximum retry attempts for reading the file"

    def unfuck(self) -> Tuple[Optional[Any], Optional[str]]:
        if self.file_type == "txt":
            # Special case for text files, we do not read the content here
            unfuck_func = self._unfuck_txt
            if unfuck_func:
                return unfuck_func(None)
        else:
            # For other file types, we attempt to read the file first
            file_content, err = self._retry_open_file()
            if err:
                logging.exception("Could not read file")
                return None, err

            unfuck_func = getattr(self, f'_unfuck_{self.file_type}', None)
            if unfuck_func:
                return unfuck_func(file_content)

        logging.warning(f"File type {self.file_type} not supported")
        return None, f"File type {self.file_type} not supported"

    def _unfuck_json(self, file_content: str) -> Tuple[Optional[Any], Optional[str]]:
        if not file_content.strip():
            logging.error("JSON file is empty.")
            return None, "JSON file is empty."
            
        try:
            valid_json = json.loads(file_content)
            return valid_json, None
        except json.JSONDecodeError as e:
            logging.warning(f"Initial JSON validation failed. Error: {str(e)}")
            logging.warning(f"File content starts with: {file_content[:100]}")
            logging.warning(f"File content ends with: {file_content[-100:]}")
            logging.warning(f"File content length: {len(file_content)}")
            pass

        previous_id = id(file_content)

        for _ in range(self.max_iterations):

            # Remove comments
            file_content = re.sub(r'//.*?\n', '\n', file_content)
            file_content = re.sub(r'/\*.*?\*/', '', file_content, flags=re.DOTALL)

            # Handle escape characters
            file_content = re.sub(r'(?<!\\)\\(?!["\\/bfnrtu])', r'\\\\', file_content)

            # Insert missing commas between objects and arrays
            file_content = re.sub(r'(\}\s*\{)', r'}, {', file_content)
            file_content = re.sub(r'(\]\s*\[)', r'], [', file_content)

            # Insert missing commas between key-value pairs
            file_content = re.sub(r'(":\s*[^,\s\]\}]+)(\s*["\{\[])', r'\1, \2', file_content)

            # Regular expression-based corrections
            file_content = re.sub(r',\s*}', '}', file_content)
            file_content = re.sub(r',\s*]', ']', file_content)
            file_content = re.sub(r'([{,]\s*)(")?([a-zA-Z_][a-zA-Z_0-9]*)(")?\s*:', r'\1"\3":', file_content)
            file_content = re.sub(r':\s*([^"\d\[\]{},\s]+)([,\]})])', r': "\1"\2', file_content)

            # Bracket/Brace corrections
            open_braces = file_content.count('{')
            close_braces = file_content.count('}')
            open_brackets = file_content.count('[')
            close_brackets = file_content.count(']')
            file_content += '}' * (open_braces - close_braces)
            file_content += ']' * (open_brackets - close_brackets)

            # Check for changes in the content
            if id(file_content) == previous_id:
                break
            previous_id = id(file_content)

            try:
                fixed_content = json.loads(file_content)
                return fixed_content, None
            except json.JSONDecodeError:
                logging.warning("JSONDecodeError encountered")
                continue

        logging.error(f"Could not unfuck JSON after {MAX_ITERATIONS} iterations.")
        return None, f"Could not unfuck JSON after {MAX_ITERATIONS} iterations."

    
    def _unfuck_xml(self, file_content: str) -> Tuple[Optional[Any], Optional[str]]:
        if not file_content.strip():
            logging.error("XML file is empty.")
            return None, "XML file is empty."

        try:
            fromstring(file_content)
            return file_content, None
        except ParseError:
            pass

        for _ in range(self.max_iterations):

            orig_content = file_content

            # Remove invalid characters
            file_content = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', file_content)

            # Fix missing attribute quotes
            file_content = re.sub(r'(<\w+ \w+)=([^\s>]+)', r'\1="\2"', file_content)

            # Unescape entities
            file_content = file_content.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')

            # Fix unclosed tags
            file_content = re.sub(r'<(\w+)(.*?)(?<!/)>', r'<\1\2>', file_content)

            stack = []
            new_content = []
            last_pos = 0

            for match in re.finditer(r'<(/?)(\w+)', file_content):
                tag = match.group(2)
                is_closing = bool(match.group(1))

                new_content.append(file_content[last_pos:match.start()])

                if is_closing:
                    if stack and stack[-1] == tag:
                        new_content.append(file_content[match.start():match.end() + 1])
                        stack.pop()
                    else:
                        # Extra closing tag; skip it
                        pass
                else:
                    new_content.append(file_content[match.start():match.end() + 1])
                    if not file_content[match.end():].startswith('/'):
                        stack.append(tag)

                last_pos = match.end() + 1

            new_content.append(file_content[last_pos:])

            # Add missing closing tags
            for tag in reversed(stack):
                new_content.append(f'</{tag}>')

            file_content = ''.join(new_content)

            if file_content == orig_content:
                break

            try:
                fromstring(file_content)
                return file_content, None
            except ParseError:
                logging.warning("XML ParseError encountered")
                continue

        logging.error(f"Could not unfuck XML after {MAX_ITERATIONS} iterations.")
        return None, f"Could not unfuck XML after {MAX_ITERATIONS} iterations."

    def _unfuck_txt(self, _: str) -> Tuple[Optional[Any], Optional[str]]:
        # Step 1: Detect encoding
        try:
            with open(self.file_path, 'rb') as f:
                result = chardet.detect(f.read())
            encoding_type = result['encoding']
        except Exception as e:
            return None, f"Could not detect file encoding: {e}"

        # If chardet couldn't detect the encoding, use utf-8 as a fallback
        if encoding_type is None:
            encoding_type = 'utf-8'

        # Step 2: Read and decode file content
        decoded_content = []
        try:
            with open(self.file_path, 'rb') as f:
                while True:
                    char = f.read(1)
                    if not char:
                        break
                    try:
                        decoded_char = char.decode(encoding_type)
                        decoded_content.append(decoded_char)
                    except UnicodeDecodeError:
                        decoded_content.append('?')  # Replace the offending character
        except Exception as e:
            return None, f"Unknown error occurred: {e}"

        # Step 3: Text Cleaning
        file_content = "".join(decoded_content)
        file_content = ''.join(filter(lambda x: x in set(
            "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]_^`{|}~ \t\n\r"), file_content))

        return file_content, None

def unfuck(file_path: str, output_path: Optional[str], overwrite: bool, max_iterations: int):
    unfucker = Unfucker(file_path, max_iterations)
    fixed_content, error = unfucker.unfuck()

    if fixed_content is not None:
        serialized_content = json.dumps(fixed_content) if unfucker.file_type == 'json' else str(fixed_content)
        if output_path:
            unfucker.save_to_file(serialized_content, output_path, overwrite)
        else:
            print(f"Unfucked content: {serialized_content}")
    else:
        logging.error(f"Error: {error}")

def unfuck_entry():
    parser = argparse.ArgumentParser(description="Unfuck corrupted or malformed txt, XML, and JSON files.")
    parser.add_argument("file_path", type=str, help="Path to the file to be unfucked")
    parser.add_argument("-o", "--output", type=str, help="Path to save the unfucked file", default=None)
    parser.add_argument("--overwrite", help="Overwrite the output file if it exists", action="store_true")
    parser.add_argument("-p", "--passes", type=int, help="Maximum passes over file trying to unfuck it. Ignored in txt files. - - Default: 10.", default=10)
    # Open 'assets/unfucker.txt' and print it (ASCII art logo)
    try:
        with open('assets/unfucker.txt', 'r') as f:
            ascii_art = f.read()
            print(ascii_art)
    except FileNotFoundError:
        print("ASCII art logo not found.")
    if 'help' in sys.argv:
        parser.print_help()
        return
    args = parser.parse_args()
    unfuck(args.file_path, args.output, args.overwrite, args.passes)

if __name__ == "__main__":
    unfuck_entry()