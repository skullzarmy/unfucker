import unittest
import xml.etree.ElementTree as ET
from unittest.mock import patch, mock_open
from unfucker.unfucker import Unfucker
import generate_large_test_files

generate_large_test_files.generate_files()

class TestUnfucker(unittest.TestCase):
    
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data="dummy data")
    def test_save_to_file_overwrite(self, mock_file, mock_exists):
        mock_exists.return_value = True
        unfucker = Unfucker("dummy_path")  # Changed class name
        unfucker.save_to_file("unfucked_content", "dummy_output", True)
        mock_file.assert_any_call("dummy_output", 'w', encoding='utf-8')

    @patch('builtins.open', new_callable=mock_open, read_data='{"key": "value", "key2": "value2"}')
    def test_unfuck_json_valid(self, mock_file):
        unfucker = Unfucker("test_files/valid_json.json")  # Changed class name
        fixed_content, error = unfucker.unfuck()  # Changed method name
        self.assertIsNone(error)
        self.assertEqual(fixed_content, {'key': 'value', 'key2': 'value2'})

    @patch('builtins.open', new_callable=mock_open, read_data='<root><element>text</element></root>')
    def test_unfuck_xml_valid(self, mock_file):
        unfucker = Unfucker("test_files/valid_xml.xml")  # Changed class name
        fixed_content, error = unfucker.unfuck()  # Changed method name
        self.assertIsNone(error)
        self.assertTrue(ET.fromstring(fixed_content))

    def test_unfucker_unsupported_file_type(self):
        unfucker = Unfucker("test_files/unsupported.xyz")  # Changed class name
        fixed_content, error = unfucker.unfuck()  # Changed method name
        self.assertIsNone(fixed_content)
        self.assertIsNotNone(error)

    @patch('builtins.open', new_callable=mock_open, read_data='simple text')
    def test_unfuck_txt_valid(self, mock_file):
        unfucker = Unfucker("test_files/valid_txt.txt")  # Changed class name
        fixed_content, error = unfucker.unfuck()  # Changed method name
        self.assertIsNone(error)
        self.assertEqual(fixed_content, 'simple text')

    @patch('builtins.open', new_callable=mock_open, read_data='')
    def test_unfuck_json_empty(self, mock_file):
        unfucker = Unfucker("test_files/empty.json")  # Changed class name
        fixed_content, error = unfucker.unfuck()  # Changed method name
        self.assertIsNone(error)
        self.assertEqual(fixed_content, {})

    @patch('builtins.open', new_callable=mock_open, read_data='')
    def test_unfuck_xml_empty(self, mock_file):
        unfucker = Unfucker("test_files/empty.xml")  # Changed class name
        fixed_content, error = unfucker.unfuck()  # Changed method name
        self.assertIsNone(error)
        self.assertEqual(fixed_content, '')

    @patch('builtins.open', new_callable=mock_open, read_data='{not a valid json}')
    def test_unfuck_json_invalid(self, mock_file):
        unfucker = Unfucker("test_files/invalid_json.json")  # Changed class name
        fixed_content, error = unfucker.unfuck()  # Changed method name
        self.assertIsNotNone(error)
        self.assertIsNone(fixed_content)

    @patch('builtins.open', new_callable=mock_open, read_data='<root><invalid></root>')
    def test_unfuck_xml_invalid(self, mock_file):
        unfucker = Unfucker("test_files/invalid_xml.xml")  # Changed class name
        fixed_content, error = unfucker.unfuck()  # Changed method name
        self.assertIsNotNone(error)
        self.assertIsNone(fixed_content)

    @patch('builtins.open', new_callable=mock_open, read_data='large dummy json')
    def test_unfuck_json_large(self, mock_file):
        unfucker = Unfucker("test_files/large_json.json")
        fixed_content, error = unfucker.unfuck()
        self.assertIsNone(error)
        self.assertEqual(fixed_content, 'large dummy json')  # Assuming the content is valid

    @patch('builtins.open', new_callable=mock_open, read_data='<root><large>content</large></root>')
    def test_unfuck_xml_large(self, mock_file):
        unfucker = Unfucker("test_files/large_xml.xml")
        fixed_content, error = unfucker.unfuck()
        self.assertIsNone(error)
        self.assertTrue(ET.fromstring(fixed_content))

    @patch('builtins.open', new_callable=mock_open, read_data='non utf 8 content')
    def test_unfuck_txt_non_utf8(self, mock_file):
        unfucker = Unfucker("test_files/non_utf8.txt")
        fixed_content, error = unfucker.unfuck()
        self.assertIsNone(error)
        self.assertEqual(fixed_content, 'non utf 8 content')

    # Further tests can be added to test various edge cases and corrupted file scenarios.

if __name__ == "__main__":
    unittest.main()
