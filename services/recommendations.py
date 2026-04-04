from knowledge_base import KnowledgeBase

kb = KnowledgeBase()


def get_student_recommendations() -> str:
    grads = kb.get_graduates_summary()
    mapping = grads.get("discipline_competence_mapping", [])

    lines = []
    for item in mapping[:6]:
        discipline = item.get("discipline", "—")
        competencies = item.get("competencies", [])
        lines.append(
            f"• <b>{discipline}</b>\n"
            + "\n".join(f"  - {comp}" for comp in competencies[:3])
        )

    return (
        "🎯 <b>Рекомендации студенту по дисциплинам и компетенциям</b>\n\n"
        + "\n\n".join(lines)
    )