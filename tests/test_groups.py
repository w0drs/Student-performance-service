import pytest
from src.db import groups_db

@pytest.mark.usefixtures("clean_db")
class TestGroupsDB:
    def test_create_group(self):
        """Тест создания группы"""
        group_id = groups_db.create_group("101Б")

        assert group_id > 0

    def test_get_group_by_name(self):
        """Тест поиска группы по имени"""
        expected_id = groups_db.create_group("102Б")
        found_id = groups_db.get_group_id_by_name("102Б")

        assert found_id == expected_id

    def test_get_group_not_found(self):
        """Тест поиска несуществующей группы"""
        group_id = groups_db.get_group_id_by_name("НеСуществует")

        assert group_id is None
