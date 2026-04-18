"""Class for testing the register_document method"""
import unittest
import csv
import json
import os.path
import hashlib
from unittest import TestCase
from os import remove, makedirs
from freezegun import freeze_time
from uc3m_consulting import (
    EnterpriseManager,
    EnterpriseManagementException
)

JSON_FILES_PATH = "json_files/"
GENERATED_INPUTS_PATH = JSON_FILES_PATH + "generated_inputs/"
ALL_DOCUMENTS_STORE_FILE = JSON_FILES_PATH + "all_documents.json"

class TestRegisterDocumentTest(TestCase):
    """Class for testing register_document"""

    def setUp(self):
        """Create directories and JSON files """
        if not os.path.exists(GENERATED_INPUTS_PATH):
            makedirs(GENERATED_INPUTS_PATH)

        if os.path.exists(ALL_DOCUMENTS_STORE_FILE):
            remove(ALL_DOCUMENTS_STORE_FILE)

    @staticmethod
    def read_file():
        """Read all_documents.json"""
        my_file = ALL_DOCUMENTS_STORE_FILE
        try:
            with open(my_file, "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError as ex:
            raise EnterpriseManagementException("Wrong file or file path") from ex
        except json.JSONDecodeError as ex:
            raise EnterpriseManagementException("JSON Decode Error - Wrong JSON Format") from ex
        return data

    @staticmethod
    def write_input_file(input_file, file_content):
        """Writing to a file"""
        with open(input_file, "w", encoding="utf-8", newline="") as file:
            file.write(file_content)


if __name__ == '__main__':
    unittest.main()
