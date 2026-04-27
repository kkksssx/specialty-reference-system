from typing import Any

from knowledge_base import KnowledgeBase

kb = KnowledgeBase()


def shorten_text(value: Any, limit: int = 350) -> str:
    text = str(value).replace("\n", " ").replace("\r", " ")
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "..."


def format_list(items: list[str], limit: int = 10) -> str:
    if not items:
        return "—"
    return "\n".join(f"• {item}" for item in items[:limit])


def format_search_results(query: str, results: list[dict], audience: str) -> str:
    if not query:
        return ""

    if not results:
        return (
            f"По запросу «{query}» ничего не найдено для {audience}.\n"
            "Попробуйте переформулировать запрос или использовать другие ключевые слова."
        )

    lines: list[str] = [f"🔎 Результаты поиска по запросу «{query}»:", ""]
    for index, result in enumerate(results[:5], start=1):
        section = result.get("section", "unknown")
        path = result.get("path", "unknown")
        item = shorten_text(result.get("item", ""))
        lines.append(
            f"{index}. Раздел: `{section}`\n"
            f"   Путь: `{path}`\n"
            f"   Фрагмент: {item}"
        )

    return "\n".join(lines)


def _format_teacher_common(teacher: dict, include_research: bool = False) -> str:
    taught_ids = teacher.get("taught_disciplines", [])
    taught_names = kb.get_discipline_names_by_ids(taught_ids)

    lines = [
        f"👨‍🏫 <b>{teacher.get('full_name', '') or '—'}</b>",
        "",
        f"<b>Должность:</b> {teacher.get('position', '') or '—'}",
        f"<b>Учёная степень:</b> {teacher.get('academic_degree', '') or '—'}",
        f"<b>Учёное звание:</b> {teacher.get('academic_title', '') or '—'}",
        f"<b>Email:</b> {teacher.get('email', '') or '—'}",
        f"<b>Преподаваемые дисциплины:</b>\n{format_list(taught_names, limit=50)}",
        f"<b>Профиль:</b> {teacher.get('profile_url', '') or '—'}",
    ]

    if include_research:
        research_interests = teacher.get("research_interests", [])
        lines.extend(
            [
                "",
                f"<b>Научные интересы:</b>\n{format_list(research_interests, limit=50)}",
            ]
        )

    return "\n".join(lines)


def format_teacher_card_for_student(teacher: dict) -> str:
    return _format_teacher_common(teacher, include_research=False)


def format_teacher_card_for_teacher(teacher: dict) -> str:
    return _format_teacher_common(teacher, include_research=True)


def format_teacher_short_button_text(teacher: dict) -> str:
    return teacher.get("full_name", "Преподаватель")


def format_discipline_card(discipline: dict, teacher: dict | None = None) -> str:
    teacher_text = teacher.get("full_name", "—") if teacher else "—"
    topic_names = [topic.get("name", "") for topic in discipline.get("topics", []) if topic.get("name")]
    resources = [
        f"{item.get('name', '')} ({item.get('type', '')})"
        for item in discipline.get("resources", [])
        if item.get("name")
    ]

    parts = [
        f"📘 <b>{discipline.get('name', '—')}</b>",
        "",
        f"<b>Курс:</b> {discipline.get('course_number', '—')}",
        f"<b>Семестр:</b> {discipline.get('semester_number', '—')}",
        f"<b>Часы:</b> {discipline.get('hours', '—')}",
        f"<b>Преподаватель:</b> {teacher_text}",
    ]

    description = discipline.get("description", "")
    if description:
        parts.extend(["", f"<b>Описание:</b> {description}"])

    parts.extend(
        [
            "",
            f"<b>Темы:</b>\n{format_list(topic_names, limit=20)}",
            "",
            f"<b>Материалы:</b>\n{format_list(resources, limit=20)}",
        ]
    )

    return "\n".join(parts)


def format_admission_scores(data: dict) -> str:
    years = data.get("admission_years", [])
    lines: list[str] = []

    for row in years[:3]:
        lines.append(
            f"{row.get('year', '—')} год:\n"
            f"• Бюджет: {row.get('passing_score_budget', '—')}\n"
            f"• Платно: {row.get('passing_score_paid', '—')}\n"
            f"• Целевой: {row.get('passing_score_goal', '—')}"
        )

    return "📊 Проходные баллы по годам\n\n" + ("\n\n".join(lines) if lines else "Нет данных.")


def format_admission_exams_and_duration(data: dict) -> str:
    exams = data.get("entrance_exams", [])
    duration = data.get("study_duration", "—")
    forms = data.get("study_forms", {})

    lines = [
        "📘 Вступительные испытания и срок обучения",
        "",
        "📚 Вступительные испытания:",
    ]

    if exams:
        for exam in exams:
            lines.append(f"• {exam}")
    else:
        lines.append("• Нет данных")

    lines.extend(
        [
            "",
            f"⏱ Срок обучения: {duration} года",
            "",
            "💺 Количество мест:",
            f"• Бюджет: {forms.get('budget_places', '—')}",
            f"• Платно: {forms.get('paid_places', '—')}",
        ]
    )

    return "\n".join(lines)


def format_contacts(contacts: dict) -> str:
    return (
        "📞 Контакты кафедры\n\n"
        f"{contacts.get('address', '')}\n"
        f"{contacts.get('building', '')}\n"
        f"<b>Email:</b> {contacts.get('email', '')}"
    )


def format_specialty_info(specialty: dict) -> str:
    return (
        f"🎓 <b>{specialty.get('name', '—')}</b>\n"
        f"Код специальности: {specialty.get('code', '—')}\n\n"
        f"{specialty.get('description', '')}\n\n"
        f"<b>Ключевые дисциплины:</b>\n"
        f"{format_list(specialty.get('main_disciplines', []), limit=10)}"
    )

def format_admission_info(data: dict) -> str:
    years = data.get("admission_years", [])
    exams = data.get("entrance_exams", [])
    duration = data.get("study_duration", "—")

    year_lines: list[str] = []
    for row in years[:3]:
        year_lines.append(
            f"{row.get('year', '—')} год: "
            f"бюджет {row.get('passing_score_budget', '—')}, "
            f"платно {row.get('passing_score_paid', '—')}, "
            f"целевой {row.get('passing_score_goal', '—')}"
        )

    return (
        "🎯 Поступление\n\n"
        + "📊 Проходные баллы:\n"
        + ("\n".join(year_lines) if year_lines else "Нет данных.\n")
        + "\n\n📚 Вступительные испытания:\n"
        + format_list(exams, limit=10)
        + f"\n\n⏱ Срок обучения: {duration} года"
    )