from knowledge_base import KnowledgeBase
from utils.formatters import (
    format_admission_info,
    format_discipline_card,
    format_search_results,
    format_teacher_card_for_student,
    format_teacher_card_for_teacher,
)

kb = KnowledgeBase()


def search_for_applicant(query: str) -> str:
    query_l = query.lower().strip()

    if any(word in query_l for word in ["балл", "поступ", "экзам", "документ", "цт", "цэ"]):
        return format_admission_info(kb.get_admission_summary())

    if any(word in query_l for word in ["карьер", "выпуск", "стажиров", "компан"]):
        graduates = kb.get_graduates_summary()
        prospects = graduates.get("graduates", {}).get("career_prospects", {})
        positions = prospects.get("possible_positions", [])[:8]
        companies = prospects.get("partner_companies", [])[:8]

        return (
            "🚀 Карьера выпускников\n\n"
            "Возможные позиции:\n"
            + "\n".join(f"• {item}" for item in positions)
            + "\n\nКомпании-партнёры:\n"
            + "\n".join(f"• {item}" for item in companies)
        )

    results = kb.search_text(query, sections=["admissions", "common", "graduates"])
    return format_search_results(query, results, "абитуриента")


def search_for_student(query: str) -> str:
    teacher = kb.get_teacher_by_name(query)
    if teacher:
        return format_teacher_card_for_student(teacher)

    discipline = kb.get_discipline_by_name(query)
    if discipline:
        teacher_obj = kb.get_teacher_by_id(discipline.get("teacher_id", ""))
        return format_discipline_card(discipline, teacher_obj)

    results = kb.search_text(query, sections=["curriculum", "teachers", "science", "common"])
    return format_search_results(query, results, "студента")


def search_for_teacher(query: str) -> str:
    teacher = kb.get_teacher_by_name(query)
    if teacher:
        return format_teacher_card_for_teacher(teacher)

    discipline = kb.get_discipline_by_name(query)
    if discipline:
        teacher_obj = kb.get_teacher_by_id(discipline.get("teacher_id", ""))
        return format_discipline_card(discipline, teacher_obj)

    results = kb.search_text(query, sections=["teachers", "science", "curriculum", "common"])
    return format_search_results(query, results, "преподавателя")


def search_everywhere(query: str) -> str:
    teacher = kb.get_teacher_by_name(query)
    if teacher:
        return format_teacher_card_for_student(teacher)

    discipline = kb.get_discipline_by_name(query)
    if discipline:
        teacher_obj = kb.get_teacher_by_id(discipline.get("teacher_id", ""))
        return format_discipline_card(discipline, teacher_obj)

    results = kb.search_text(query)
    return format_search_results(query, results, "всех пользователей")