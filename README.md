# Unfucker

```
88        88                 ad88                           88
88        88                d8"                             88
88        88                88                              88
88        88  8b,dPPYba,  MM88MMM  88       88   ,adPPYba,  88   ,d8   ,adPPYba,  8b,dPPYba,
88        88  88P'   `"8a   88     88       88  a8"     ""  88 ,a8"   a8P_____88  88P'   "Y8
88        88  88       88   88     88       88  8b          8888[     8PP"""""""  88
Y8a.    .a8P  88       88   88     "8a,   ,a88  "8a,   ,aa  88`"Yba,  "8b,   ,aa  88
 `"Y8888Y"'   88       88   88      `"YbbdP'Y8   `"Ybbd8"'  88   `Y8a  `"Ybbd8"'  88




                                @@@@@@
                              .@. ..#*@
                              @&  ...*@
                              @. ....*@
                             @& .*,.**@
                             @. ....*/@
                      @@@@@@#@. ....*&@@**/@@@@@@@
                .@@@@@@@@***@@......*#..,***/*****@,
             .@#**(@@@#****&@@,#&@(.*&@  .......**@@
             @,. ..,*%  ...*@.  ,,.,*@@****%@@.,**@%
            @@  ...*@. ....*@. ....**@. ....**@*(@
           @@. ...**/ .....*@. ....,*@. ....,*@/@
          @#@.....*@.......*& ......*@. ....,*@*@,
          @&,....,*/......*/(.......*@*.....*#**@
          *@..............*,@......**..*....*%/@.
           ,@. ............................,*(@
             @@@@@@. .,.**................**@@
                  .@@/(@@@,. ..**&*. ...*@@,
                          @@@@@@@@&@@@@@%
 _     _        ___             _                                    ___ _ _
| |   | |      / __)           | |                                  / __|_) |
| |   | |____ | |__ _   _  ____| |  _    _   _  ___  _   _  ____   | |__ _| | ____  ___
| |   | |  _ \|  __) | | |/ ___) | / )  | | | |/ _ \| | | |/ ___)  |  __) | |/ _  )/___)
| |___| | | | | |  | |_| ( (___| |< (   | |_| | |_| | |_| | |      | |  | | ( (/ /|___ |
 \______|_| |_|_|   \____|\____)_| \_)   \__  |\___/ \____|_|      |_|  |_|_|\____|___/
                                        (____/

```

Unfucker is a Python utility for repairing corrupted or malformed text files. It currently supports JSON, XML, and TXT formats. It provides functionalities to automatically fix syntax errors, missing attributes, or encoding issues in these files.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Installation

Since this package is not yet available on PyPI, you can install it locally by cloning the repository and using pip. Follow the steps below:

1. Clone the repository:

```bash
git clone https://github.com/skullzarmy/unfucker.git
```

2. Navigate to the project directory:

```bash
cd unfucker
```

3. Install the package locally:

```bash
pip install -e .
```

By using pip install -e ., you're performing an "editable" install, which means changes to the source code will immediately affect the installed package without needing a reinstallation.

Now, you can import the package in your Python scripts without having to manipulate your PYTHONPATH.

## Dependencies

The project dependencies are listed in the requirements.txt file. To install them, run the following command:

```bash
pip install -r requirements.txt
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
unfucker path/to/your/file.json -o path/to/save/fixed/file.json --overwrite
```

```bash
python path/to/unfucker.py path/to/your/file.json -o path/to/save/fixed/file.json --overwrite
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
