"""Class for testing the register_document method"""
import unittest
import csv
import json
import os
import hashlib
from unittest import TestCase
from unittest.mock import patch, PropertyMock
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

    @staticmethod
    def get_file_hash():
        """Get hash of all_documents.json"""
        if os.path.isfile(ALL_DOCUMENTS_STORE_FILE):
            with open(ALL_DOCUMENTS_STORE_FILE, "r", encoding="utf-8", newline="") as file:
                return hashlib.md5(str(file).encode()).hexdigest()
        return ""

    @staticmethod
    def create_store_file():
        """Create empty all_documents.json file"""
        with open(ALL_DOCUMENTS_STORE_FILE, "w", encoding="utf-8", newline="") as file:
            json.dump([], file, indent=2)

    @freeze_time("2026/03/22 13:00:00")
    def test_TC80(self):
        """Path 1_2_5_7_9_10_11_13_15_17_18_19_21_22_24_25_26_end"""
        input_file = GENERATED_INPUTS_PATH + "tc80_valid_existing_store.json"
        file_content = """{
  "PROJECT_ID": "a1b2c3d4e5f60718293a4b5c6d7e8f90",
  "FILENAME": "Ab12Cd34.pdf"
}"""
        self.write_input_file(input_file, file_content)
        self.create_store_file()

        mngr = EnterpriseManager()
        sha_256_output = mngr.register_document(input_file)
        self.assertEqual(
            "699f631976b25795e55646d860d4cc94c17c830864f97d56b8921ab2e09765ff",
            sha_256_output
        )

        my_data = self.read_file()
        input_data = json.loads(file_content)

        found = False
        for document in my_data:
            if document["document_signature"] == sha_256_output:
                found = True
                self.assertEqual(document["project_id"], input_data["PROJECT_ID"])
                self.assertEqual(document["file_name"], input_data["FILENAME"])
                self.assertEqual(document["alg"], "SHA-256")
        self.assertTrue(found)

        if os.path.exists(input_file):
            remove(input_file)

    @freeze_time("2026/03/22 13:00:00")
    def test_TC81(self):
        """Path 1_3_end"""
        input_file = GENERATED_INPUTS_PATH + "tc81_missing_file.json"

        mngr = EnterpriseManager()
        hash_original = self.get_file_hash()

        with self.assertRaises(EnterpriseManagementException) as c_m:
            mngr.register_document(input_file)
        self.assertEqual(c_m.exception.message, "Input file not found")

        hash_new = self.get_file_hash()
        self.assertEqual(hash_new, hash_original)

    @freeze_time("2026/03/22 13:00:00")
    def test_TC82(self):
        """Path 1_4_end"""
        input_file = GENERATED_INPUTS_PATH + "tc82_invalid_json.json"
        file_content = """{
  "PROJECT_ID": "a1b2c3d4e5f60718293a4b5c6d7e8f90",
  "FILENAME": "Ab12Cd34.pdf"
"""
        self.write_input_file(input_file, file_content)

        mngr = EnterpriseManager()
        hash_original = self.get_file_hash()

        with self.assertRaises(EnterpriseManagementException) as c_m:
            mngr.register_document(input_file)
        self.assertEqual(c_m.exception.message, "The file is not JSON formatted")

        hash_new = self.get_file_hash()
        self.assertEqual(hash_new, hash_original)

        if os.path.exists(input_file):
            remove(input_file)

    @freeze_time("2026/03/22 13:00:00")
    def test_TC83(self):
        """Path 1_2_5_6_end"""
        input_file = GENERATED_INPUTS_PATH + "tc83_not_dict.json"
        file_content = """[
  "a1b2c3d4e5f60718293a4b5c6d7e8f90",
  "Ab12Cd34.pdf"
]"""
        self.write_input_file(input_file, file_content)

        mngr = EnterpriseManager()
        hash_original = self.get_file_hash()

        with self.assertRaises(EnterpriseManagementException) as c_m:
            mngr.register_document(input_file)
        self.assertEqual(c_m.exception.message, "The file is not JSON formatted")

        hash_new = self.get_file_hash()
        self.assertEqual(hash_new, hash_original)

        if os.path.exists(input_file):
            remove(input_file)

    @freeze_time("2026/03/22 13:00:00")
    def test_TC84(self):
        """Path 1_2_5_7_8_end"""
        input_file = GENERATED_INPUTS_PATH + "tc84_wrong_structure.json"
        file_content = """{
  "PROJECT_ID": "a1b2c3d4e5f60718293a4b5c6d7e8f90",
  "NAME": "Ab12Cd34.pdf"
}"""
        self.write_input_file(input_file, file_content)

        mngr = EnterpriseManager()
        hash_original = self.get_file_hash()

        with self.assertRaises(EnterpriseManagementException) as c_m:
            mngr.register_document(input_file)
        self.assertEqual(c_m.exception.message, "JSON does not have the expected structure")

        hash_new = self.get_file_hash()
        self.assertEqual(hash_new, hash_original)

        if os.path.exists(input_file):
            remove(input_file)

    @freeze_time("2026/03/22 13:00:00")
    def test_TC85(self):
        """Path 1_2_5_7_9_10_12_end"""
        input_file = GENERATED_INPUTS_PATH + "tc85_project_id_not_string.json"
        file_content = """{
  "PROJECT_ID": 12345,
  "FILENAME": "Ab12Cd34.pdf"
}"""
        self.write_input_file(input_file, file_content)

        mngr = EnterpriseManager()
        hash_original = self.get_file_hash()

        with self.assertRaises(EnterpriseManagementException) as c_m:
            mngr.register_document(input_file)
        self.assertEqual(c_m.exception.message, "JSON data has no valid values")

        hash_new = self.get_file_hash()
        self.assertEqual(hash_new, hash_original)

        if os.path.exists(input_file):
            remove(input_file)

    @freeze_time("2026/03/22 13:00:00")
    def test_TC86(self):
        """Path 1_2_5_7_9_10_11_12_end"""
        input_file = GENERATED_INPUTS_PATH + "tc86_filename_not_string.json"
        file_content = """{
  "PROJECT_ID": "a1b2c3d4e5f60718293a4b5c6d7e8f90",
  "FILENAME": 12345
}"""
        self.write_input_file(input_file, file_content)

        mngr = EnterpriseManager()
        hash_original = self.get_file_hash()

        with self.assertRaises(EnterpriseManagementException) as c_m:
            mngr.register_document(input_file)
        self.assertEqual(c_m.exception.message, "JSON data has no valid values")

        hash_new = self.get_file_hash()
        self.assertEqual(hash_new, hash_original)

        if os.path.exists(input_file):
            remove(input_file)

    @freeze_time("2026/03/22 13:00:00")
    def test_TC87(self):
        """Path 1_2_5_7_9_10_11_13_14_end"""
        input_file = GENERATED_INPUTS_PATH + "tc87_invalid_project_id.json"
        file_content = """{
  "PROJECT_ID": "A1b2c3d4e5f60718293a4b5c6d7e8f90",
  "FILENAME": "Ab12Cd34.pdf"
}"""
        self.write_input_file(input_file, file_content)

        mngr = EnterpriseManager()
        hash_original = self.get_file_hash()

        with self.assertRaises(EnterpriseManagementException) as c_m:
            mngr.register_document(input_file)
        self.assertEqual(c_m.exception.message, "JSON data has no valid values")

        hash_new = self.get_file_hash()
        self.assertEqual(hash_new, hash_original)

        if os.path.exists(input_file):
            remove(input_file)



if __name__ == '__main__':
    unittest.main()
