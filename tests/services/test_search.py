import pytest
from unittest.mock import patch, MagicMock
import services.search as search_mod


@pytest.fixture
def mock_kb():
    kb = MagicMock()
    kb.search_text.return_value = [{"path": "x", "value": "результат", "relevance": 0.8}]
    kb.get_teacher_by_name.return_value = None
    kb.get_discipline_by_name.return_value = None
    return kb


@patch.object(search_mod, 'kb')
def test_search_applicant_keywords_routing(mock_kb):
    res = search_mod.search_for_applicant("Какие нужны баллы для поступления?")
    assert mock_kb.get_admission_summary.called
    # Проверяем, что сработал маршрутизатор по ключевым словам
    mock_kb.search_text.assert_not_called()


@patch.object(search_mod, 'kb')
def test_search_student_fallback(mock_kb):
    # Явно возвращаем None, чтобы условия if teacher: и if discipline: стали False
    mock_kb.get_teacher_by_name.return_value = None
    mock_kb.get_discipline_by_name.return_value = None
    mock_kb.search_text.return_value = []

    res = search_mod.search_for_student("произвольный запрос без совпадений")

    # Проверяем, что fallback-поиск вызвался ровно один раз с нужными параметрами
    mock_kb.search_text.assert_called_once_with(
        "произвольный запрос без совпадений",
        sections=["curriculum", "teachers", "science", "common"]
    )
    assert mock_kb.get_teacher_by_name.called
    assert mock_kb.get_discipline_by_name.called


@patch.object(search_mod, 'kb')
def test_search_everywhere_global(mock_kb):
    mock_kb.get_teacher_by_name.return_value = None
    mock_kb.get_discipline_by_name.return_value = None
    mock_kb.search_text.return_value = []

    search_mod.search_everywhere("тестовый запрос")
    mock_kb.search_text.assert_called_once_with("тестовый запрос")  # без sections -> поиск везде