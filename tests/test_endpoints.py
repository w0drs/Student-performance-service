
class TestRootEndpoints:
    """Тесты корневых эндпоинтов"""

    def test_root(self, test_client):
        """Тест корневого эндпоинта"""
        response = test_client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "Student performance service"
        assert "endpoints" in data

    def test_health(self, test_client):
        """Тест health check"""
        response = test_client.get("/health")

        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
