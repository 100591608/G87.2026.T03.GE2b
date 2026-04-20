"""Module """
import json
from uc3m_consulting.project_document import ProjectDocument
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
import re

ALL_DOCUMENTS_PATH = "../../unittest/python/json_files/all_documents.json"

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

        if type(input_data) is not dict:
            raise EnterpriseManagementException("The file is not JSON formatted")

        try:
            project_id = input_data["PROJECT_ID"]
            filename = input_data["FILENAME"]
        except KeyError as ex:
            raise EnterpriseManagementException("JSON does not have the expected structure") from ex

        if not re.fullmatch(r"^[a-f0-9]{32}$", str(project_id)):
            raise EnterpriseManagementException("JSON data has no valid values")

        if not re.fullmatch(r"^[a-zA-Z0-9]{8}\.(pdf|docx|xlsx)$", str(filename)):
            raise EnterpriseManagementException("JSON data has no valid values")

        document = ProjectDocument(input_data["PROJECT_ID"], input_data["FILENAME"])

        try:
            with open("json_files/all_documents.json", "r", encoding="utf-8", newline="") as file:
                documents_list = json.load(file)
        except FileNotFoundError:
            documents_list = []

        documents_list.append(document.to_json())

        with open(ALL_DOCUMENTS_PATH, "w", encoding="utf-8", newline="") as file:
            json.dump(documents_list, file, indent=2)

        return document.document_signature
