import pytest
from unittest.mock import patch, MagicMock
import services.navigation as menu_mod  # замените на фактическое имя модуля

@pytest.fixture
def mock_kb():
    kb = MagicMock()
    kb.get_specialty_info.return_value = {
        "name": "Искусственный интеллект", "code": "6-05-0611-03", "description": "Тестовое описание"
    }
    kb.get_department_info.return_value = {
        "name": "Кафедра ИИТ",
        "current_head": {"full_name": "Шункевич Д.В.", "degree": "к.т.н."},
        "history": [{"year": 1995, "event": "Основание"}, {"year": 1998, "event": "Переименование"}]
    }
    kb.load.return_value = {
        "achievements": [{"name": "Проект OSTIS", "year": 2010}],
        "research_areas": [{"name": "Семантические технологии"}],
        "student_research": {"description": "СНИЛ работает активно"},
        "postgraduate_specialty": {"code": "1.2.3", "name": "ИИ"}
    }
    return kb

@patch.object(menu_mod, 'kb')
def test_get_common_menu_text_structure(mock_kb):
    mock_kb.get_specialty_info.return_value = {"name": "ИИ", "code": "001"}
    mock_kb.get_department_info.return_value = {"name": "ИИТ", "current_head": {}, "history": []}
    mock_kb.load.return_value = {}

    result = menu_mod.get_common_menu_text()
    assert "🎓 Специальность" in result
    assert "🏫 Кафедра" in result
    assert "ИИ (001)" in result

@patch.object(menu_mod, 'kb')
def test_get_section_text_applicant_branches(mock_kb):
    mock_kb.get_admission_summary.return_value = {
        "scores": {}, "exams": [], "required_documents": {
            "general_required": ["Паспорт"], "additional_if_needed": [], "for_minors": {}, "identity_documents": {}
        }
    }
    res = menu_mod.get_section_text("applicant", "admissions_rules")
    assert "📝 Документы для поступления" in res
    assert "• Паспорт" in res

@patch.object(menu_mod, 'kb')
def test_get_section_text_unknown_fallback(mock_kb, monkeypatch):
    monkeypatch.setattr(menu_mod, "SECTION_FALLBACK_TEXT", "РАЗДЕЛ НЕ НАЙДЕН")
    res = menu_mod.get_section_text("student", "non_existent")
    assert "РАЗДЕЛ НЕ НАЙДЕН" in res