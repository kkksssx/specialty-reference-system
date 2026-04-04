from knowledge_base import KnowledgeBase
from texts.messages import ROLE_INTRO_TEXTS, SECTION_FALLBACK_TEXT
from utils.formatters import format_admission_info, format_contacts, format_specialty_info

kb = KnowledgeBase()


def get_role_intro(role: str) -> str:
    return ROLE_INTRO_TEXTS.get(role, "Выберите нужный раздел.")


def get_common_menu_text() -> str:
    specialty = kb.get_specialty_info()
    return (
        f"📂 <b>Общая информация</b>\n\n"
        f"<b>Специальность:</b> {specialty.get('name', '—')}\n"
        f"<b>Код:</b> {specialty.get('code', '—')}\n\n"
        "Доступные сценарии поиска:\n"
        "<code>абитуриент: проходной балл</code>\n"
        "<code>студент: машинное обучение</code>\n"
        "<code>преподаватель: Шункевич</code>"
    )


def get_section_text(role: str, section: str) -> str:
    if role == "applicant":
        if section == "admissions_scores":
            return format_admission_info(kb.get_admission_summary())
        if section == "admissions_rules":
            admissions = kb.get_admission_summary()
            docs = admissions.get("required_documents", {}).get("general_required", [])
            return (
                "📝 <b>Документы для поступления</b>\n\n"
                + "\n".join(f"• {doc}" for doc in docs[:12])
            )
        if section == "common_about":
            return format_specialty_info(kb.get_specialty_info())
        if section == "graduates_career":
            grads = kb.get_graduates_summary()
            examples = grads.get("successful_graduates_examples", [])
            return (
                "💼 <b>Примеры выпускников</b>\n\n"
                + "\n".join(
                    f"• {item.get('full_name')} — {item.get('current_position')}"
                    for item in examples[:8]
                )
            )

    if role == "student":
        if section == "curriculum_plan":
            curriculum = kb.load("curriculum")
            meta = curriculum.get("metadata", {})
            return (
                "📚 <b>Учебный план</b>\n\n"
                f"<b>Специальность:</b> {meta.get('specialty', '—')}\n"
                f"<b>Код:</b> {meta.get('code', '—')}\n"
                f"<b>Кафедра:</b> {meta.get('department', '—')}\n"
                f"<b>Университет:</b> {meta.get('university', '—')}\n"
                f"<b>Форма обучения:</b> {meta.get('study_form', '—')}"
            )
        if section == "curriculum_subjects":
            curriculum = kb.load("curriculum")
            names = []
            for course in curriculum.get("courses", [])[:2]:
                for semester in course.get("semesters", [])[:2]:
                    for discipline in semester.get("disciplines", [])[:8]:
                        names.append(
                            f"• {discipline.get('name')} "
                            f"(курс {course.get('course_number')}, семестр {semester.get('semester_number')})"
                        )
            return "📘 <b>Дисциплины</b>\n\n" + ("\n".join(names[:15]) if names else "—")
        if section == "teachers_list":
            teachers = kb.load("teachers").get("teachers", [])
            return (
                "👨‍🏫 <b>Преподаватели</b>\n\n"
                + "\n".join(
                    f"• {t.get('full_name')} — {t.get('position')}"
                    for t in teachers[:15]
                )
            )
        if section == "science_events":
            science = kb.get_science_summary()
            conferences = science.get("conferences", [])
            return (
                "🔬 <b>Научные мероприятия</b>\n\n"
                + "\n".join(
                    f"• {c.get('year')} — {c.get('name')}"
                    for c in conferences[:10]
                )
            )

    if role == "teacher":
        if section == "teachers_staff":
            teachers = kb.load("teachers").get("teachers", [])
            return (
                "🏫 <b>Состав кафедры</b>\n\n"
                + "\n".join(
                    f"• {t.get('full_name')} — {t.get('position')}"
                    for t in teachers[:20]
                )
            )
        if section == "science_projects":
            common = kb.load("common")
            projects = common.get("research_projects", [])
            grants = common.get("research_grants", [])
            projects_text = "\n".join(f"• {p.get('name')}" for p in projects[:10])
            grants_text = "\n".join(f"• {g}" for g in grants[:10])

            return (
                "🔬 <b>Научная деятельность</b>\n\n"
                f"<b>Проекты:</b>\n{projects_text if projects_text else '—'}\n\n"
                f"<b>Гранты:</b>\n{grants_text if grants_text else '—'}"
            )
        if section == "curriculum_load":
            return (
                "📖 <b>Учебная нагрузка</b>\n\n"
                "Для просмотра нагрузки удобнее искать по преподавателю:\n"
                "<code>преподаватель: Шункевич</code>\n"
                "<code>преподаватель: Гракова</code>"
            )
        if section == "common_about":
            return format_specialty_info(kb.get_specialty_info())

    return SECTION_FALLBACK_TEXT


def get_contacts_text() -> str:
    return format_contacts(kb.get_contacts())