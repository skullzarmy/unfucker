# Unfucker

Unfucker is a Python utility for repairing corrupted or malformed text files. It currently supports JSON, XML, and TXT formats. It provides functionalities to automatically fix syntax errors, missing attributes, or encoding issues in these files.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Installation

As this package is not yet available on PyPI, you can install it locally by cloning the repository.

```bash
git clone https://github.com/skullzarmy/unfucker
cd unfucker
```

You can then either manually copy the file to your project directory or add the path to your PYTHONPATH environment variable.

## Dependencies

Make sure you install the required dependencies, if not already available:

-   chardet

Install using pip:

```bash
pip install chardet
```

## Usage

### Importing into a Script

To use Unfucker in a Python script, simply import the class and use it as follows:

```python
from Unfucker import Unfucker, unfuck

file_path = "path/to/your/file.json"
output_path = "path/to/save/fixed/file.json"

# Initialize the Unfucker
unfucker = Unfucker(file_path)

# Unfuck the file
fixed_content, error = unfucker.unfuck()

if fixed_content:
    # Save to a file or use fixed_content as you see fit
    unfucker.save_to_file(str(fixed_content), output_path, True)
else:
    print(f"Could not unfuck the file: {error}")
```

### Command-Line Interface

Alternatively, you can run the script from the command line:

```bash
python unfucker.py path/to/your/file.json -o path/to/save/fixed/file.json --overwrite
```

-   `path/to/your/file.json` is the path to the file you want to fix.
-   `-o path/to/save/fixed/file.json` specifies where to save the fixed content.
-   `--overwrite` allows you to overwrite the output file if it already exists.

## Running Tests

This project uses pytest for testing. To run the tests locally, you'll need to install pytest if you haven't already:

```bash
pip install pytest
```

Once pytest is installed, navigate to the project directory and run the following command:

```bash
pytest
```

This will discover and run all the test cases in the project. If everything is set up correctly, you should see output indicating the number of passed tests.

## Contributing to Unfucker Python Package

Hey there, awesome human! Interested in contributing to Unfucker? That's fuckin' great! 🎉 Before you dive into the code, make sure to read our [Contributing Guidelines](./CONTRIBUTING.md) and our rather entertaining [Code of Conduct](./CODE_OF_CONDUCT.md).

Whether it's submitting a bug report, proposing a new feature, or creating a pull request, every contribution is valuable and appreciated. 🙏

Let's build something badass together! 👩‍💻👨‍💻
