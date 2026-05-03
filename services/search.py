from knowledge_base import KnowledgeBase
from texts.messages import UNKNOWN_TEXT
from utils.formatters import (
    format_admission_info,
    format_discipline_card,
    format_teacher_card_for_student,
    format_teacher_card_for_teacher,
)

kb = KnowledgeBase()


def format_documents_info(data: dict) -> str:
    required = data.get("required_documents", {})
    general_required = required.get("general_required", [])
    for_minors = required.get("for_minors", {})
    identity_documents = required.get("identity_documents", {})
    additional_if_needed = required.get("additional_if_needed", [])
    foreign_documents_note = required.get("foreign_documents_note", "")

    parts = ["📄 <b>Документы для поступления</b>\n"]

    if general_required:
        parts.append("Основные документы:")
        parts.extend(f"• {item}" for item in general_required)

    if identity_documents:
        note = identity_documents.get("note", "")
        types = identity_documents.get("types", [])
        if note:
            parts.append(f"\n🪪 {note}")
        if types:
            parts.extend(f"• {item}" for item in types)

    if for_minors:
        rule = for_minors.get("rule", "")
        docs = for_minors.get("documents", [])
        if rule:
            parts.append(f"\n👶 <b>Для несовершеннолетних:</b>\n{rule}")
        if docs:
            parts.extend(f"• {item}" for item in docs)

    if additional_if_needed:
        parts.append("\n📎 Дополнительно, при необходимости:")
        parts.extend(f"• {item}" for item in additional_if_needed[:8])

    if foreign_documents_note:
        parts.append(f"\n🌍 {foreign_documents_note}")

    return "\n".join(parts)


def search_teacher(query: str) -> str:
    query = query.strip()
    if not query:
        return UNKNOWN_TEXT

    teacher = kb.get_teacher_by_name(query)
    if teacher:
        return format_teacher_card_for_teacher(teacher)

    return UNKNOWN_TEXT


def search_discipline(query: str) -> str:
    query = query.strip()
    if not query:
        return UNKNOWN_TEXT

    discipline = kb.get_discipline_by_name(query)
    if discipline:
        teacher = kb.get_teacher_by_id(discipline.get("teacher_id", ""))
        return format_discipline_card(discipline, teacher)

    return UNKNOWN_TEXT


def search_for_applicant(query: str) -> str:
    query_l = query.lower().strip()
    if not query_l:
        return UNKNOWN_TEXT

    admissions = kb.get_admission_summary()

    # 1. Сначала документы
    if any(word in query_l for word in ["документ", "документы", "справка", "паспорт", "аттестат"]):
        return format_documents_info(admissions)

    # 2. Потом проходные баллы и поступление
    if any(word in query_l for word in ["балл", "проход", "поступ", "экзам", "цт", "цэ"]):
        return format_admission_info(admissions)

    # 3. Карьера
    if any(word in query_l for word in ["карьер", "выпуск", "стажиров", "компан"]):
        graduates = kb.get_graduates_summary()
        prospects = graduates.get("graduates", {}).get("career_prospects", {})
        positions = prospects.get("possible_positions", [])[:8]
        companies = prospects.get("partner_companies", [])[:8]

        if not positions and not companies:
            return UNKNOWN_TEXT

        parts = ["🚀 Карьера выпускников\n"]

        if positions:
            parts.append("Возможные позиции:")
            parts.extend(f"• {item}" for item in positions)

        if companies:
            parts.append("\nКомпании-партнёры:")
            parts.extend(f"• {item}" for item in companies)

        return "\n".join(parts)

    return UNKNOWN_TEXT


def search_for_student(query: str) -> str:
    query_l = query.lower().strip()
    if not query_l:
        return UNKNOWN_TEXT

    teacher = kb.get_teacher_by_name(query_l)
    if teacher:
        return format_teacher_card_for_student(teacher)

    discipline = kb.get_discipline_by_name(query_l)
    if discipline:
        teacher_obj = kb.get_teacher_by_id(discipline.get("teacher_id", ""))
        return format_discipline_card(discipline, teacher_obj)

    return UNKNOWN_TEXT


def search_everywhere(query: str) -> str:
    query = query.strip()
    if not query:
        return UNKNOWN_TEXT

    teacher = kb.get_teacher_by_name(query)
    if teacher:
        return format_teacher_card_for_student(teacher)

    discipline = kb.get_discipline_by_name(query)
    if discipline:
        teacher_obj = kb.get_teacher_by_id(discipline.get("teacher_id", ""))
        return format_discipline_card(discipline, teacher_obj)

    return UNKNOWN_TEXT