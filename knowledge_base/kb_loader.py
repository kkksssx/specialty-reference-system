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

#Открывает JSON-файл и превращает его в Python-словарь/список
    def _read_json(self, path: Path) -> Any:
        if not path.exists():
            return {}
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

#Читает файл и сохраняет в кеш (потом берёт из кеша)
    def load(self, section: str) -> Any:
        if section in self._cache:
            return self._cache[section]

        path = self.files.get(section)
        if not path:
            return {}

        data = self._read_json(path)
        self._cache[section] = data
        return data

#Выгружает всё
    def load_all(self) -> dict[str, Any]:
        return {section: self.load(section) for section in self.files}

#Забывает всё из кеша
    def reload(self) -> None:
        self._cache.clear()

#Ну эта функция выгружает словарь(ключ - значение) для одного преподавателя, т.е.
#если написать kb.get_teacher_by_id("T001"), то выгрузит Шункевича
    def get_teacher_by_id(self, teacher_id: str) -> dict[str, Any] | None:
        teachers_data = self.load("teachers")
        for teacher in teachers_data.get("teachers", []):
            if teacher.get("id") == teacher_id:
                return teacher
        return None
    
#Выводит словарь именно по имени
    def get_teacher_by_name(self, query: str) -> dict[str, Any] | None:
        query_l = query.lower().strip()
        teachers_data = self.load("teachers")
        for teacher in teachers_data.get("teachers", []):
            if query_l in teacher.get("full_name", "").lower():
                return teacher
        return None

#ищет дисциплину по названию в учебном плане и добавляет к ней номер курса и семестра
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
    
#находит все дисциплины конкретного преподавателя во всём учебном плане и добавляет к каждой номер курса и семестра
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

#Поиск сразу по всем файлам
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

#ищет слово во всём содержимом объекта
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

#Выгружает контакты из common.json
    def get_contacts(self) -> dict[str, Any]:
        common = self.load("common")
        return common.get("contacts", {})

#Выгружает specialty из common.json
    def get_specialty_info(self) -> dict[str, Any]:
        common = self.load("common")
        return common.get("specialty", {})

#Выгружает department из common.json
    def get_department_info(self) -> dict[str, Any]:
        common = self.load("common")
        return common.get("department", {})
    