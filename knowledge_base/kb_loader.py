import json
from pathlib import Path
from typing import Any


class KnowledgeBase:
    def __init__(self, base_path: str | Path | None = None) -> None:
        self.base_path = Path(base_path) if base_path else Path(__file__).resolve().parent
        self.files = {
            "common": self.base_path / "common.json",
            "admissions": self.base_path / "admissions.json",
            "curriculum": self.base_path / "curriculum.json",
            "teachers": self.base_path / "teachers.json",
            "graduates": self.base_path / "graduates.json",
            "science": self.base_path / "science.json",
        }
        self._cache: dict[str, Any] = {}

    def _read_json(self, path: Path) -> Any:
        if not path.exists():
            return {}
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    def load(self, section: str) -> Any:
        if section in self._cache:
            return self._cache[section]

        path = self.files.get(section)
        if not path:
            return {}

        data = self._read_json(path)
        self._cache[section] = data
        return data

    def load_all(self) -> dict[str, Any]:
        return {section: self.load(section) for section in self.files}

    def reload(self) -> None:
        self._cache.clear()

    def get_teacher_by_id(self, teacher_id: str) -> dict[str, Any] | None:
        teachers_data = self.load("teachers")
        for teacher in teachers_data.get("teachers", []):
            if teacher.get("id") == teacher_id:
                return teacher
        return None

    def get_teacher_by_name(self, query: str) -> dict[str, Any] | None:
        query_l = query.lower().strip()
        teachers_data = self.load("teachers")
        for teacher in teachers_data.get("teachers", []):
            if query_l in teacher.get("full_name", "").lower():
                return teacher
        return None

    def get_all_teachers(self) -> list[dict[str, Any]]:
        teachers_data = self.load("teachers")
        return teachers_data.get("teachers", [])

    def get_courses(self) -> list[dict[str, Any]]:
        curriculum = self.load("curriculum")
        return curriculum.get("courses", [])

    def get_semesters_by_course(self, course_number: int) -> list[dict[str, Any]]:
        curriculum = self.load("curriculum")
        for course in curriculum.get("courses", []):
            if course.get("course_number") == course_number:
                return course.get("semesters", [])
        return []

    def get_disciplines_by_course_and_semester(
        self,
        course_number: int,
        semester_number: int,
    ) -> list[dict[str, Any]]:
        curriculum = self.load("curriculum")
        result: list[dict[str, Any]] = []

        for course in curriculum.get("courses", []):
            if course.get("course_number") != course_number:
                continue

            for semester in course.get("semesters", []):
                if semester.get("semester_number") != semester_number:
                    continue

                for discipline in semester.get("disciplines", []):
                    row = discipline.copy()
                    row["course_number"] = course_number
                    row["semester_number"] = semester_number
                    result.append(row)

        return result

    def get_discipline_by_id(self, discipline_id: str) -> dict[str, Any] | None:
        curriculum = self.load("curriculum")

        for course in curriculum.get("courses", []):
            for semester in course.get("semesters", []):
                for discipline in semester.get("disciplines", []):
                    if discipline.get("id") == discipline_id:
                        row = discipline.copy()
                        row["course_number"] = course.get("course_number")
                        row["semester_number"] = semester.get("semester_number")
                        return row
        return None

    def get_discipline_name_by_id(self, discipline_id: str) -> str:
        discipline = self.get_discipline_by_id(discipline_id)
        if not discipline:
            return discipline_id
        return discipline.get("name", discipline_id)

    def get_discipline_names_by_ids(self, discipline_ids: list[str]) -> list[str]:
        return [self.get_discipline_name_by_id(discipline_id) for discipline_id in discipline_ids]

    def get_contacts(self) -> dict[str, Any]:
        common = self.load("common")
        return common.get("contacts", {})

    def get_specialty_info(self) -> dict[str, Any]:
        common = self.load("common")
        return common.get("specialty", {})

    def get_department_info(self) -> dict[str, Any]:
        common = self.load("common")
        return common.get("department", {})

    def get_admission_summary(self) -> dict[str, Any]:
        return self.load("admissions")

    def get_graduates_summary(self) -> dict[str, Any]:
        return self.load("graduates")

    def get_science_summary(self) -> dict[str, Any]:
        return self.load("science")