import unittest
import os
import json
import xml.etree.ElementTree as ET
from unfucker.unfucker import Unfucker
import generate_large_test_files

generate_large_test_files.generate_files()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_FILES_DIR = os.path.join(BASE_DIR, "test_files")

class TestUnfucker(unittest.TestCase):
    
    def test_save_to_file_overwrite(self):
        filepath = os.path.join(TEST_FILES_DIR, "dummy_output")
        unfucker = Unfucker(filepath)
        unfucker.save_to_file("unfucked_content", filepath, True)
        with open(filepath, 'r', encoding='utf-8') as f:
            self.assertEqual(f.read(), "unfucked_content")
        
    def test_unfuck_json_valid(self):
        filepath = os.path.join(TEST_FILES_DIR, "valid_json.json")
        unfucker = Unfucker(filepath)
        fixed_content, error = unfucker.unfuck()
        self.assertIsNone(error)

    def test_unfuck_xml_valid(self):
        filepath = os.path.join(TEST_FILES_DIR, "valid_xml.xml")
        unfucker = Unfucker(filepath)
        fixed_content, error = unfucker.unfuck()
        self.assertIsNone(error)
        self.assertTrue(ET.fromstring(fixed_content))

    def test_unfucker_unsupported_file_type(self):
        filepath = os.path.join(TEST_FILES_DIR, "unsupported.xyz")
        unfucker = Unfucker(filepath)
        fixed_content, error = unfucker.unfuck()
        self.assertIsNone(fixed_content)
        self.assertIsNotNone(error)

    def test_unfuck_txt_valid(self):
        filepath = os.path.join(TEST_FILES_DIR, "valid_txt.txt")
        unfucker = Unfucker(filepath)
        fixed_content, error = unfucker.unfuck()
        self.assertIsNone(error)

    def test_unfuck_json_empty(self):
        filepath = os.path.join(TEST_FILES_DIR, "empty.json")
        unfucker = Unfucker(filepath)
        fixed_content, error = unfucker.unfuck()
        self.assertEqual(error, 'JSON file is empty.')
        self.assertIsNone(fixed_content)

    def test_unfuck_xml_empty(self):
        filepath = os.path.join(TEST_FILES_DIR, "empty.xml")
        unfucker = Unfucker(filepath)
        fixed_content, error = unfucker.unfuck()
        self.assertEqual(error, 'XML file is empty.')
        self.assertIsNone(fixed_content)

    def test_unfuck_json_invalid(self):
        filepath = os.path.join(TEST_FILES_DIR, "invalid_json.json")
        unfucker = Unfucker(filepath)
        fixed_content, error = unfucker.unfuck()
        self.assertIsNone(error)

    def test_unfuck_xml_invalid(self):
        filepath = os.path.join(TEST_FILES_DIR, "invalid_xml.xml")
        unfucker = Unfucker(filepath)
        fixed_content, error = unfucker.unfuck()
        self.assertIsNone(error)

    def test_unfuck_json_large(self):
        filepath = os.path.join(TEST_FILES_DIR, "large_json.json")
        unfucker = Unfucker(filepath)
        fixed_content, error = unfucker.unfuck()
        self.assertIsNone(error)
        with open(filepath, 'r') as f:
            original_content = json.load(f)
        self.assertEqual(fixed_content, original_content)

    def test_unfuck_xml_large(self):
        filepath = os.path.join(TEST_FILES_DIR, "large_xml.xml")
        unfucker = Unfucker(filepath)
        fixed_content, error = unfucker.unfuck()
        self.assertIsNone(error)
        with open(filepath, 'r') as f:
            original_content = f.read()
        self.assertEqual(fixed_content, original_content)

    def test_unfuck_txt_non_utf8(self):
        filepath = os.path.join(TEST_FILES_DIR, "non_utf8.txt")
        unfucker = Unfucker(filepath)
        fixed_content, error = unfucker.unfuck()
        self.assertIsNone(error)

if __name__ == "__main__":
    unittest.main()
