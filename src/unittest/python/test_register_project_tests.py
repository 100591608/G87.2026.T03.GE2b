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

class MyTestCase(unittest.TestCase):
    """class for testing the register_order method"""
    def test_something( self ):
        """dummy test"""
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
