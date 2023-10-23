import unittest
import json
import xml.etree.ElementTree as ET
from unittest.mock import patch, mock_open
from unfucker import FileUnfucker, unfuck

class TestFileUnfucker(unittest.TestCase):
    
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data="dummy data")
    def test_save_to_file_overwrite(self, mock_file, mock_exists):
        mock_exists.return_value = True
        file_unfucker = FileUnfucker("dummy_path")
        file_unfucker.save_to_file("unfucked_content", "dummy_output", True)
        mock_file.assert_any_call("dummy_output", 'w', encoding='utf-8')

    @patch('builtins.open', new_callable=mock_open, read_data='{"key": "value", "key2": "value2"}')
    def test_unfuck_json_valid(self, mock_file):
        file_unfucker = FileUnfucker("test_files/valid_json.json")
        fixed_content, error = file_unfucker.unfuck()
        self.assertIsNone(error)
        self.assertEqual(fixed_content, {'key': 'value', 'key2': 'value2'})

    @patch('builtins.open', new_callable=mock_open, read_data='<root><element>text</element></root>')
    def test_unfuck_xml_valid(self, mock_file):
        file_unfucker = FileUnfucker("test_files/valid_xml.xml")
        fixed_content, error = file_unfucker.unfuck()
        self.assertIsNone(error)
        self.assertTrue(ET.fromstring(fixed_content))

    def test_unfucker_unsupported_file_type(self):
        file_unfucker = FileUnfucker("test_files/unsupported.xyz")
        fixed_content, error = file_unfucker.unfuck()
        self.assertIsNone(fixed_content)
        self.assertIsNotNone(error)

    @patch('builtins.open', new_callable=mock_open, read_data='simple text')
    def test_unfuck_txt_valid(self, mock_file):
        file_unfucker = FileUnfucker("test_files/valid_txt.txt")
        fixed_content, error = file_unfucker.unfuck()
        self.assertIsNone(error)
        self.assertEqual(fixed_content, 'simple text')

    # Add more tests here for various edge cases and corrupted file scenarios


if __name__ == "__main__":
    unittest.main()
