import os

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")


class TestUploadAPI:
    """Тесты для POST /upload-grades"""

    def test_upload_valid_csv(self, test_client, clean_db):
        """Загрузка валидного CSV файла"""
        file_path = os.path.join(FIXTURES_DIR, "valid_grades.csv")

        with open(file_path, 'rb') as f:
            response = test_client.post(
                "/upload-grades",
                files={"file": ("valid_grades.csv", f, "text/csv")}
            )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["records_loaded"] == 5
        assert data["students"] == 3

    def test_upload_csv_with_bom(self, test_client, clean_db):
        """Загрузка CSV с BOM"""
        file_path = os.path.join(FIXTURES_DIR, "with_bom.csv")

        with open(file_path, 'rb') as f:
            response = test_client.post(
                "/upload-grades",
                files={"file": ("with_bom.csv", f, "text/csv")}
            )

        assert response.status_code == 200
        data = response.json()
        assert data["records_loaded"] == 1
        assert data["students"] == 1

    def test_upload_invalid_csv(self, test_client, clean_db):
        """Загрузка невалидного CSV"""
        file_path = os.path.join(FIXTURES_DIR, "invalid_grades.csv")

        with open(file_path, 'rb') as f:
            response = test_client.post(
                "/upload-grades",
                files={"file": ("invalid_grades.csv", f, "text/csv")}
            )

        assert response.status_code == 400
        assert "Invalid" in response.json()["detail"]
