"""Module """
import json
from uc3m_consulting.project_document import ProjectDocument

ALL_DOCUMENTS_PATH = "../../unittest/python/json_files/all_documents.json"

class EnterpriseManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    @staticmethod
    def validate_cif(cif: str):
        """RETURNs TRUE IF THE IBAN RECEIVED IS VALID SPANISH IBAN,
        OR FALSE IN OTHER CASE"""
        return True

    def register_document(self, input_file: str):
        """Registers document in the Enterprise Manager"""
        with open(input_file, "r", encoding="utf-8", newline="") as file:
            input_data = json.load(file)

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
