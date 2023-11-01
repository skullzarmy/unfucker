import json
from xml.etree.ElementTree import Element, SubElement, ElementTree
import os

# Generate large JSON file (approximately 10MB)
def generate_large_json(filename):
    data = {"people": []}

    for i in range(145000):
        person = {
            "id": i,
            "name": f"Name_{i}",
            "email": f"email_{i}@example.com"
        }
        data["people"].append(person)

    with open(filename, "w") as f:
        json.dump(data, f)

# Generate large XML file (approximately 10MB)
def generate_large_xml(filename):
    root = Element("people")

    for i in range(100000):
        person = SubElement(root, "person")
        id_ = SubElement(person, "id")
        id_.text = str(i)
        name = SubElement(person, "name")
        name.text = f"Name_{i}"
        email = SubElement(person, "email")
        email.text = f"email_{i}@example.com"

    tree = ElementTree(root)
    tree.write(filename)

# Generate a non-UTF-8 text file (ISO-8859-1 encoded)
def generate_non_utf8_file(filename):
    with open(filename, "wb") as f:
        f.write(b"Hello, world! This is ISO-8859-1 encoded text: \xa1Hola!")

def generate_files():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    json_file_path = os.path.join(script_dir, "test_files", "large_json.json")
    xml_file_path = os.path.join(script_dir, "test_files", "large_xml.xml")
    txt_file_path = os.path.join(script_dir, "test_files", "non_utf8.txt")

    if not os.path.exists(json_file_path):
        generate_large_json(json_file_path)
    if not os.path.exists(xml_file_path):
        generate_large_xml(xml_file_path)
    if not os.path.exists(txt_file_path):
        generate_non_utf8_file(txt_file_path)


if __name__ == "__main__":
    generate_files()