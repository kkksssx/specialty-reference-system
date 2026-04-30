import pytest
from unittest.mock import patch, MagicMock
import services.recommendations as rec_mod


@pytest.fixture
def mock_kb():
    kb = MagicMock()
    kb.get_graduates_summary.return_value = {
        "discipline_competence_mapping": [
            {"discipline": "Базы знаний", "competencies": ["C1", "C2", "C3", "C4"]},
            {"discipline": "Машинное обучение", "competencies": ["C5", "C6"]},
            {"discipline": "Нейросети", "competencies": ["C7"]},
        ]
    }
    return kb


@patch.object(rec_mod, 'kb')
def test_recommendations_format_and_limit(mock_kb):
    # Передаём больше 6 элементов, проверяем обрезку
    big_mapping = [{"discipline": f"Дисциплина {i}", "competencies": [f"Комп {i}"]} for i in range(10)]
    mock_kb.get_graduates_summary.return_value = {"discipline_competence_mapping": big_mapping}

    result = rec_mod.get_student_recommendations()

    assert "🎯 <b>Рекомендации студенту" in result
    assert result.count("<b>Дисциплина") == 6  # ограничение [:6]
    assert "Дисциплина 0" in result
    assert "Дисциплина 9" not in result  # элементы 7-9 отсекаются


@patch.object(rec_mod, 'kb')
def test_recommendations_empty_mapping(mock_kb):
    mock_kb.get_graduates_summary.return_value = {"discipline_competence_mapping": []}
    result = rec_mod.get_student_recommendations()
    assert "🎯 <b>Рекомендации студенту" in result
    assert "• <b>—" not in result  # цикл не выполнится, список пуст