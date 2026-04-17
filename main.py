"""File for generating MD5 Hash"""
from freezegun import freeze_time
from uc3m_consulting.project_document import ProjectDocument

@freeze_time("2026/03/22 13:00:00")
def show_valid_hashes():
    """Shows expected hashes for the valid GE2b cases"""
    test_cases = [
        ("TC1", "a1b2c3d4e5f60718293a4b5c6d7e8f90", "Ab12Cd34.pdf"),
        ("TC2", "a1b2c3d4e5f60718293a4b5c6d7e8f90", "Ab12Cd34.docx"),
        ("TC3", "a1b2c3d4e5f60718293a4b5c6d7e8f90", "Ab12Cd34.xlsx"),
    ]

    for test_id, project_id, file_name in test_cases:
        obj = ProjectDocument(project_id, file_name)
        print(test_id, obj.document_signature)


if __name__ == '__main__':
    show_valid_hashes()
