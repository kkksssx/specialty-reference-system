from typing import Any


def shorten_text(value: Any, limit: int = 350) -> str:
    text = str(value).replace("{", "").replace("}", "")
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "..."


def format_list(items: list[str], limit: int = 10) -> str:
    if not items:
        return "—"
    sliced = items[:limit]
    return "\n".join(f"• {item}" for item in sliced)


def format_search_results(query: str, results: list[dict], audience: str) -> str:
    if not query:
        return "Введите поисковый запрос."

    if not results:
        return (
            f"🔎 По запросу <b>{query}</b> ничего не найдено для {audience}.\n"
            "Попробуйте указать ФИО преподавателя, название дисциплины, научное направление или ключевое слово."
        )

    lines = [f"🔎 <b>Результаты по запросу:</b> {query}\n"]

    for index, result in enumerate(results[:5], start=1):
        section = result.get("section", "unknown")
        path = result.get("path", "")
        item = shorten_text(result.get("item", ""))
        lines.append(
            f"<b>{index}.</b> Раздел: <code>{section}</code>\n"
            f"Путь: <code>{path}</code>\n"
            f"Фрагмент: {item}\n"
        )

    return "\n".join(lines)


def format_teacher_card(teacher: dict, disciplines: list[dict]) -> str:
    full_name = teacher.get("full_name", "Неизвестно")
    position = teacher.get("position", "—")
    degree = teacher.get("academic_degree", "—")
    title = teacher.get("academic_title", "—")
    email = teacher.get("email", "—")
    interests = teacher.get("research_interests", [])
    profile_url = teacher.get("profile_url", "")

    discipline_lines = []
    for d in disciplines[:8]:
        discipline_lines.append(
            f"• {d.get('name')} — курс {d.get('course_number')}, семестр {d.get('semester_number')}"
        )

    text = (
        f"👨‍🏫 <b>{full_name}</b>\n\n"
        f"<b>Должность:</b> {position}\n"
        f"<b>Учёная степень:</b> {degree}\n"
        f"<b>Учёное звание:</b> {title}\n"
        f"<b>Email:</b> {email}\n\n"
        f"<b>Научные интересы:</b>\n{format_list(interests, limit=8)}\n\n"
        f"<b>Преподаваемые дисциплины:</b>\n"
        f"{chr(10).join(discipline_lines) if discipline_lines else '—'}"
    )

    if profile_url:
        text += f"\n\n<b>Профиль:</b> {profile_url}"

    return text


def format_discipline_card(discipline: dict, teacher: dict | None) -> str:
    name = discipline.get("name", "Неизвестная дисциплина")
    hours = discipline.get("hours", "—")
    topics = discipline.get("topics", [])
    resources = discipline.get("resources", [])
    course_number = discipline.get("course_number", "—")
    semester_number = discipline.get("semester_number", "—")

    teacher_text = "—"
    if teacher:
        teacher_text = teacher.get("full_name", "—")

    resources_text = "\n".join(
        f"• {item.get('name')} ({item.get('type')})"
        for item in resources[:8]
    ) if resources else "—"

    return (
        f"📘 <b>{name}</b>\n\n"
        f"<b>Курс:</b> {course_number}\n"
        f"<b>Семестр:</b> {semester_number}\n"
        f"<b>Часы:</b> {hours}\n"
        f"<b>Преподаватель:</b> {teacher_text}\n\n"
        f"<b>Темы:</b>\n{format_list(topics, limit=10)}\n\n"
        f"<b>Ресурсы:</b>\n{resources_text}"
    )


def format_admission_info(data: dict) -> str:
    years = data.get("admission_years", [])
    exams = data.get("entrance_exams", [])
    duration = data.get("study_duration", "—")

    year_lines = []
    for row in years[:3]:
        year_lines.append(
            f"• {row.get('year')}: бюджет {row.get('passing_score_budget')}, "
            f"платное {row.get('passing_score_paid')}, целевое {row.get('passing_score_goal')}"
        )

    return (
        f"🎓 <b>Информация для абитуриента</b>\n\n"
        f"<b>Вступительные испытания:</b>\n{format_list(exams, limit=10)}\n\n"
        f"<b>Срок обучения:</b> {duration} года\n\n"
        f"<b>Проходные баллы:</b>\n{chr(10).join(year_lines) if year_lines else '—'}"
    )


def format_contacts(contacts: dict) -> str:
    return (
        "📞 <b>Контакты</b>\n\n"
        f"<b>Адрес:</b> {contacts.get('address', '—')}\n"
        f"<b>Корпус:</b> {contacts.get('building', '—')}\n"
        f"<b>Email:</b> {contacts.get('email', '—')}"
    )


def format_specialty_info(specialty: dict) -> str:
    name = specialty.get("name", "—")
    code = specialty.get("code", "—")
    description = specialty.get("description", "—")
    disciplines = specialty.get("main_disciplines", [])

    return (
        f"ℹ️ <b>{name}</b>\n\n"
        f"<b>Код специальности:</b> {code}\n\n"
        f"{description}\n\n"
        f"<b>Основные дисциплины:</b>\n{format_list(disciplines, limit=10)}"
    )