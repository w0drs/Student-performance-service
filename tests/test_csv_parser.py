import pytest
import os
import logging
from src.service.upload_file import process_upload

logger = logging.getLogger(__name__)

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")


@pytest.mark.usefixtures("clean_db")
class TestUploadService:

    def test_process_upload_valid_csv(self):
        """Тест загрузки валидного CSV из файла"""
        file_path = os.path.join(FIXTURES_DIR, "valid_grades.csv")

        with open(file_path, 'rb') as f:
            content = f.read()

        result = process_upload(content)

        assert result["status"] == "ok"
        assert result["records_loaded"] == 5
        assert result["students"] == 3

    def test_process_upload_with_bom_csv(self):
        """Тест загрузки CSV с BOM"""
        file_path = os.path.join(FIXTURES_DIR, "with_bom.csv")

        with open(file_path, 'rb') as f:
            content = f.read()

        result = process_upload(content)

        assert result["status"] == "ok"
        assert result["records_loaded"] == 1
        assert result["students"] == 1

    def test_process_upload_empty_rows_csv(self):
        """Тест загрузки CSV с пустыми строками"""
        file_path = os.path.join(FIXTURES_DIR, "empty_rows.csv")

        with open(file_path, 'rb') as f:
            content = f.read()

        result = process_upload(content)

        assert result["status"] == "ok"
        assert result["records_loaded"] == 2
        assert result["students"] == 2

    def test_process_upload_invalid_csv(self):
        """Тест загрузки невалидного CSV"""
        file_path = os.path.join(FIXTURES_DIR, "invalid_grades.csv")

        with open(file_path, 'rb') as f:
            content = f.read()

        with pytest.raises(ValueError):
            process_upload(content)
