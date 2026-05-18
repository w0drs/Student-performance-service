import os
import logging

logger = logging.getLogger(__name__)

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")

class TestAnalyticsAPI:
    """Тесты для GET эндпоинтов аналитики"""

    def test_more_than_3_twos(self, test_client, clean_db):
        """Тест студентов с >3 двойками"""
        file_path = os.path.join(FIXTURES_DIR, "grades_with_twos.csv")

        with open(file_path, 'rb') as f:
            response = test_client.post(
                "/upload-grades",
                files={"file": ("grades_with_twos.csv", f, "text/csv")}
            )
        assert response.status_code == 200

        logging.debug(f"\nUpload response: {response.json()}")

        response = test_client.get("/students/more-than-3-twos")

        logging.debug(f"Analytics response: {response.json()}")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["full_name"] == "Сергей Лучший"
        assert data[0]["count_twos"] == 4

    def test_more_than_3_twos_empty(self, test_client, clean_db):
        """Нет студентов с >3 двойками"""
        file_path = os.path.join(FIXTURES_DIR, "grades_no_twos.csv")

        with open(file_path, 'rb') as f:
            test_client.post(
                "/upload-grades",
                files={"file": ("grades_no_twos.csv", f, "text/csv")}
            )

        response = test_client.get("/students/more-than-3-twos")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0

    def test_less_than_5_twos(self, test_client, clean_db):
        """Тест студентов с <5 двойками"""
        file_path = os.path.join(FIXTURES_DIR, "grades_with_twos.csv")

        with open(file_path, 'rb') as f:
            test_client.post(
                "/upload-grades",
                files={"file": ("grades_with_twos.csv", f, "text/csv")}
            )

        response = test_client.get("/students/less-than-5-twos")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["full_name"] == "Сергей Лучший"
        assert data[0]["count_twos"] == 4
