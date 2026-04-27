from knowledge_base import KnowledgeBase
from texts.messages import ROLE_INTRO_TEXTS, SECTION_FALLBACK_TEXT
from utils.formatters import (
    format_admission_exams_and_duration,
    format_admission_scores,
    format_contacts,
    format_specialty_info,
)

kb = KnowledgeBase()


def get_role_intro(role: str) -> str:
    return ROLE_INTRO_TEXTS.get(role, "")


def get_common_menu_text() -> str:
    specialty = kb.get_specialty_info()
    department = kb.get_department_info()
    common = kb.load("common")

    achievements = common.get("achievements", [])
    research_areas = common.get("research_areas", [])
    student_research = common.get("student_research", {})
    postgraduate = common.get("postgraduate_specialty", {})

    lines: list[str] = []

    lines.append("🎓 Специальность")
    lines.append(f"{specialty.get('name', '')} ({specialty.get('code', '')})")
    lines.append("")

    desc = specialty.get("description")
    if desc:
        lines.append(desc)
        lines.append("")

    lines.append("🏫 Кафедра")
    lines.append(department.get("name", ""))

    head = department.get("current_head", {})
    if head:
        lines.append(f"Заведующий: {head.get('full_name', '')} ({head.get('degree', '')})")
    lines.append("")

    history = department.get("history", [])
    if history:
        lines.append("📜 История кафедры (ключевые вехи):")
        for item in history[-5:]:
            lines.append(f"• {item.get('year', '')}: {item.get('event', '')}")
        lines.append("")

    if achievements:
        lines.append("🏆 Достижения и крупные проекты:")
        for item in achievements[:5]:
            lines.append(f"• {item.get('name', '')} ({item.get('year', '')})")
        lines.append("")

    if research_areas:
        lines.append("🔬 Научные направления кафедры:")
        for item in research_areas[:6]:
            lines.append(f"• {item.get('name', '')}")
        lines.append("")

    if student_research:
        lines.append("👩‍🔬 Студенческая научная работа:")
        lines.append(student_research.get("description", ""))
        lines.append("")

    if postgraduate:
        lines.append("🎓 Аспирантура:")
        lines.append(f"{postgraduate.get('code', '')} — {postgraduate.get('name', '')}")

    return "\n".join(lines).strip()


def get_section_text(role: str, section: str) -> str:
    if role == "applicant":
        if section == "admissions_scores":
            return format_admission_scores(kb.get_admission_summary())

        if section == "admissions_exams":
            return format_admission_exams_and_duration(kb.get_admission_summary())

        if section == "admissions_rules":
            data = kb.get_admission_summary()
            docs = data.get("required_documents", {})

            general = docs.get("general_required", [])
            additional = docs.get("additional_if_needed", [])
            minors = docs.get("for_minors", {})
            identity = docs.get("identity_documents", {})
            foreign_note = docs.get("foreign_documents_note", "")

            parts: list[str] = ["📝 Документы для поступления", ""]

            if general:
                parts.append("Основные документы:")
                for item in general:
                    parts.append(f"• {item}")
                parts.append("")

            if additional:
                parts.append("Дополнительные (при необходимости):")
                for item in additional:
                    parts.append(f"• {item}")
                parts.append("")

            if minors:
                parts.append("Для несовершеннолетних:")
                rule = minors.get("rule")
                if rule:
                    parts.append(f"• {rule}")
                for item in minors.get("documents", []):
                    parts.append(f"• {item}")
                parts.append("")

            if identity:
                note = identity.get("note")
                if note:
                    parts.append(note)
                for item in identity.get("types", []):
                    parts.append(f"• {item}")
                parts.append("")

            if foreign_note:
                parts.append(f"🌐 {foreign_note}")

            return "\n".join(parts).strip()

        if section == "graduates_career":
            grads_all = kb.get_graduates_summary()
            grads = grads_all.get("graduates", {})
            prospects = grads.get("career_prospects", {})
            internships = grads.get("internships", [])
            examples = grads_all.get("successful_graduates_examples", [])

            lines: list[str] = ["🚀 Карьера выпускников", ""]

            positions = prospects.get("possible_positions", [])
            companies = prospects.get("partner_companies", [])

            if positions:
                lines.append("Возможные позиции:")
                for item in positions:
                    lines.append(f"• {item}")
                lines.append("")

            if companies:
                lines.append("Компании-партнёры и места работы:")
                for item in companies:
                    lines.append(f"• {item}")
                lines.append("")

            if internships:
                lines.append("Примеры стажировок:")
                for item in internships:
                    lines.append(
                        f"• {item.get('company', '')}: {item.get('name', '')} ({item.get('type', '')})"
                    )
                lines.append("")

            if examples:
                lines.append("Истории выпускников:")
                for item in examples:
                    lines.append(
                        f"• {item.get('full_name', '')} — {item.get('current_position', '')}"
                    )

            return "\n".join(lines).strip()

        if section == "common_about":
            return format_specialty_info(kb.get_specialty_info())

        return SECTION_FALLBACK_TEXT

    if role == "student":
        if section == "curriculum_plan":
            curriculum = kb.load("curriculum")
            meta = curriculum.get("metadata", {})
            courses = curriculum.get("courses", [])

            lines: list[str] = [
                "📚 Учебный план специальности",
                "",
                f"Специальность: {meta.get('specialty', '—')} ({meta.get('code', '—')})",
                f"Кафедра: {meta.get('department', '—')}",
                f"Университет: {meta.get('university', '—')}",
                f"Форма обучения: {meta.get('study_form', '—')}",
                "",
                "Структура по курсам:",
            ]

            for course in courses:
                course_number = course.get("course_number")
                semesters = course.get("semesters", [])
                lines.append(f"• {course_number} курс:")
                for semester in semesters:
                    semester_number = semester.get("semester_number")
                    discipline_count = len(semester.get("disciplines", []))
                    lines.append(f"  - {semester_number} семестр: {discipline_count} дисциплин")

            return "\n".join(lines).strip()

        if section == "curriculum_subjects":
            return "Выберите курс, затем семестр, затем дисциплину."

        if section == "teachers_list":
            return "Выберите преподавателя из списка кнопок."

        if section == "science_events":
            science = kb.get_science_summary()
            conferences = science.get("conferences", [])
            publications = science.get("publications", [])

            common = kb.load("common")
            research_areas = common.get("research_areas", [])
            projects = common.get("research_projects", [])

            lines: list[str] = ["🔬 Наука и конференции", ""]

            if conferences:
                lines.append("Конференции:")
                for item in conferences[:5]:
                    lines.append(f"• {item.get('year', '')}: {item.get('name', '')}")
                lines.append("")

            if publications:
                lines.append("Публикации:")
                for item in publications[:5]:
                    lines.append(f"• {item.get('year', '')}: {item.get('title', '')}")
                lines.append("")

            if research_areas:
                lines.append("Научные направления:")
                for item in research_areas[:5]:
                    lines.append(f"• {item.get('name', '')}")
                lines.append("")

            if projects:
                lines.append("Проекты:")
                for item in projects[:4]:
                    lines.append(f"• {item.get('name', '')}")

            return "\n".join(lines).strip()

        return SECTION_FALLBACK_TEXT

    if role == "teacher":
        if section == "teachers_staff":
            return ""

        if section == "science_projects":
            common = kb.load("common")
            projects = common.get("research_projects", [])
            grants = common.get("research_grants", [])

            lines: list[str] = ["🔬 Научные проекты и гранты", ""]

            if projects:
                lines.append("Проекты:")
                for item in projects[:10]:
                    lines.append(f"• {item.get('name', '')}")
                lines.append("")

            if grants:
                lines.append("Гранты:")
                for item in grants[:10]:
                    lines.append(f"• {item}")

            return "\n".join(lines).strip()

        if section == "curriculum_load":
            curriculum = kb.load("curriculum")
            teachers_data = kb.load("teachers")
            teacher_map = {
                teacher.get("id"): teacher.get("full_name", "Неизвестный преподаватель")
                for teacher in teachers_data.get("teachers", [])
            }

            grouped: dict[str, list[str]] = {}

            for course in curriculum.get("courses", []):
                course_number = course.get("course_number")
                for semester in course.get("semesters", []):
                    semester_number = semester.get("semester_number")
                    for discipline in semester.get("disciplines", []):
                        teacher_id = discipline.get("teacher_id", "")
                        teacher_name = teacher_map.get(teacher_id, "Неизвестный преподаватель")
                        grouped.setdefault(teacher_name, []).append(
                            f"• {discipline.get('name', '')} — курс {course_number}, семестр {semester_number}, часов {discipline.get('hours', '—')}"
                        )

            lines: list[str] = ["📚 Учебная нагрузка преподавателей", ""]
            for teacher_name, items in list(grouped.items())[:10]:
                lines.append(f"{teacher_name}:")
                lines.extend(items[:6])
                lines.append("")

            return "\n".join(lines).strip()

        if section == "common_about":
            return format_specialty_info(kb.get_specialty_info())

        return SECTION_FALLBACK_TEXT

    return SECTION_FALLBACK_TEXT


def get_contacts_text() -> str:
    return format_contacts(kb.get_contacts())