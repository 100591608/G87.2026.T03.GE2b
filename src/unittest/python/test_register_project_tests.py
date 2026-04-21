"""Class for testing the register_document method"""
import unittest
import csv
import json
import os
import hashlib
from unittest import TestCase
from os import remove, makedirs
from freezegun import freeze_time
from uc3m_consulting import (
    EnterpriseManager,
    EnterpriseManagementException
)

THIS_TEST_FILE = os.path.abspath(__file__)
TESTS_DIR = os.path.dirname(THIS_TEST_FILE)

JSON_FILES_PATH = os.path.join(TESTS_DIR, "json_files") + os.sep
GENERATED_INPUTS_PATH = os.path.join(JSON_FILES_PATH, "generated_inputs") + os.sep
ALL_DOCUMENTS_STORE_FILE = os.path.join(JSON_FILES_PATH, "all_documents.json")

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

    # pylint: disable=too-many-locals
    @freeze_time("2026/03/22 13:00:00")
    def test_parametrized_cases_tests(self):
        """Test cases read from test_cases_2026_method2.csv"""
        my_cases = JSON_FILES_PATH + "test_cases_2026_method2.csv"
        with open(my_cases, newline='', encoding='utf-8-sig') as csvfile:
            param_test_cases = csv.DictReader(csvfile, delimiter=',')
            mngr = EnterpriseManager()
            for row in param_test_cases:
                test_id = row["ID_TEST"]
                input_file = GENERATED_INPUTS_PATH + row["INPUT_FILE"]
                file_content = row["FILE_CONTENT"]
                result = row["RESULT"]
                valid = row["VALID"]

                if valid == "VALID":
                    with self.subTest("test_" + test_id):
                        self.write_input_file(input_file, file_content)

                        sha_256_output = mngr.register_document(input_file)
                        self.assertEqual(result, sha_256_output)

                        my_data = self.read_file()
                        input_data = json.loads(file_content)

                        found = False
                        for document in my_data:
                            if document["document_signature"] == sha_256_output:
                                found = True
                                self.assertEqual(document["project_id"], input_data["PROJECT_ID"])
                                self.assertEqual(document["file_name"], input_data["FILENAME"])
                                self.assertEqual(document["alg"], "SHA-256")
                                self.assertEqual(document["type"], "DOCUMENT")
                        self.assertTrue(found)

                else:
                    with self.subTest("test_" + test_id):
                        self.write_input_file(input_file, file_content)

                        if os.path.isfile(ALL_DOCUMENTS_STORE_FILE):
                            with open(ALL_DOCUMENTS_STORE_FILE, "r",
                                      encoding="utf-8", newline="") as file_org:
                                hash_original = hashlib.md5(str(file_org).encode()).hexdigest()
                        else:
                            hash_original = ""

                        with self.assertRaises(EnterpriseManagementException) as c_m:
                            mngr.register_document(input_file)
                        self.assertEqual(c_m.exception.message, result)

                        if os.path.isfile(ALL_DOCUMENTS_STORE_FILE):
                            with open(ALL_DOCUMENTS_STORE_FILE, "r",
                                      encoding="utf-8", newline="") as file:
                                hash_new = hashlib.md5(str(file).encode()).hexdigest()
                        else:
                            hash_new = ""
                        self.assertEqual(hash_new, hash_original)

                if os.path.exists(input_file):
                    remove(input_file)


if __name__ == '__main__':
    unittest.main()
