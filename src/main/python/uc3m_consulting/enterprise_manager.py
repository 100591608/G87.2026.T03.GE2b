"""Module """
import re
import os
import json
from uc3m_consulting.project_document import ProjectDocument
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException

THIS_FILE = os.path.abspath(__file__)
UC3M_DIR = os.path.dirname(THIS_FILE)
PROJECT_ROOT = os.path.abspath(os.path.join(UC3M_DIR, "..", "..", "..", ".."))

ALL_DOCUMENTS_PATH = os.path.join(
    PROJECT_ROOT,
    "src",
    "unittest",
    "python",
    "json_files",
    "all_documents.json"
)

class EnterpriseManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    @staticmethod
    def validate_cif(cif: str):
        """RETURNS TRUE IF THE IBAN RECEIVED IS VALID SPANISH IBAN,
        OR FALSE IN OTHER CASE"""
        return True

    def register_document(self, input_file: str):
        """Registers document in the Enterprise Manager"""
        try:
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                input_data = json.load(file)
        except FileNotFoundError as ex:
            raise EnterpriseManagementException("Input file not found") from ex
        except json.JSONDecodeError as ex:
            raise EnterpriseManagementException("The file is not JSON formatted") from ex

        if not isinstance(input_data, dict):
            raise EnterpriseManagementException("The file is not JSON formatted")

        if set(input_data.keys()) != {"PROJECT_ID", "FILENAME"}:
            raise EnterpriseManagementException("JSON does not have the expected structure")

        project_id = input_data["PROJECT_ID"]
        filename = input_data["FILENAME"]

        if not isinstance(project_id, str) or not isinstance(filename, str):
            raise EnterpriseManagementException("JSON data has no valid values")

        if not re.fullmatch(r"[a-f0-9]{32}$", project_id):
            raise EnterpriseManagementException("JSON data has no valid values")

        if not re.fullmatch(r"[a-zA-Z0-9]{8}\.(pdf|docx|xlsx)$", filename):
            raise EnterpriseManagementException("JSON data has no valid values")

        try:
            document = ProjectDocument(project_id, filename)
            document_signature = document.document_signature
        except Exception as ex:
            raise EnterpriseManagementException(
                "Internal processing error when getting the file_signature"
            ) from ex

        try:
            with open(ALL_DOCUMENTS_PATH, "r", encoding="utf-8", newline="") as file:
                documents_list = json.load(file)
        except FileNotFoundError:
            documents_list = []

        documents_list.append(document.to_json())

        with open(ALL_DOCUMENTS_PATH, "w", encoding="utf-8", newline="") as file:
            json.dump(documents_list, file, indent=2)

        return document_signature
