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

    def get_discipline_by_name(self, query: str) -> dict[str, Any] | None:
        query_l = query.lower().strip()
        curriculum = self.load("curriculum")

        for course in curriculum.get("courses", []):
            for semester in course.get("semesters", []):
                for discipline in semester.get("disciplines", []):
                    if query_l in discipline.get("name", "").lower():
                        result = discipline.copy()
                        result["course_number"] = course.get("course_number")
                        result["semester_number"] = semester.get("semester_number")
                        return result
        return None

    def get_disciplines_by_teacher(self, teacher_id: str) -> list[dict[str, Any]]:
        curriculum = self.load("curriculum")
        result = []

        for course in curriculum.get("courses", []):
            for semester in course.get("semesters", []):
                for discipline in semester.get("disciplines", []):
                    if discipline.get("teacher_id") == teacher_id:
                        row = discipline.copy()
                        row["course_number"] = course.get("course_number")
                        row["semester_number"] = semester.get("semester_number")
                        result.append(row)

        return result

    def search_text(self, query: str, sections: list[str] | None = None) -> list[dict[str, Any]]:
        query = query.strip().lower()
        if not query:
            return []

        target_sections = sections or list(self.files.keys())
        results: list[dict[str, Any]] = []

        for section in target_sections:
            data = self.load(section)
            self._search_in_object(
                obj=data,
                query=query,
                results=results,
                section=section,
                path=section,
            )

        unique: list[dict[str, Any]] = []
        seen: set[tuple[str, str, str]] = set()

        for item in results:
            key = (
                item.get("section", ""),
                item.get("path", ""),
                str(item.get("item", ""))[:200],
            )
            if key not in seen:
                seen.add(key)
                unique.append(item)

        return unique

    def _search_in_object(
        self,
        obj: Any,
        query: str,
        results: list[dict[str, Any]],
        section: str,
        path: str,
    ) -> None:
        if isinstance(obj, dict):
            text_parts = []
            for value in obj.values():
                if isinstance(value, (str, int, float, bool)):
                    text_parts.append(str(value))
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, (str, int, float, bool)):
                            text_parts.append(str(item))

            combined = " ".join(text_parts)
            if combined and query in combined.lower():
                results.append({
                    "section": section,
                    "path": path,
                    "item": obj,
                })

            for key, value in obj.items():
                self._search_in_object(value, query, results, section, f"{path}.{key}")

        elif isinstance(obj, list):
            for index, item in enumerate(obj):
                self._search_in_object(item, query, results, section, f"{path}[{index}]")

        elif isinstance(obj, (str, int, float, bool)):
            if query in str(obj).lower():
                results.append({
                    "section": section,
                    "path": path,
                    "item": obj,
                })

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