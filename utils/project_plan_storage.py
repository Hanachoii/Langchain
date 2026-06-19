import json
from pathlib import Path


def save_project_plan(project_plan: dict, output_path: str = "data/project_plan.json") -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(project_plan, file, indent=2, ensure_ascii=False)


def load_project_plan(plan_path: str = "data/project_plan.json") -> dict:
    plan_path = Path(plan_path)

    if not plan_path.exists():
        return {}

    with open(plan_path, "r", encoding="utf-8") as file:
        return json.load(file)


def find_feature_by_file(file_path: str, project_plan: dict) -> dict:
    normalized_file_path = file_path.replace("\\", "/")

    for branch_name, branch_info in project_plan.get("branches", {}).items():
        related_files = branch_info.get("related_files", [])

        for related_file in related_files:
            normalized_related_file = related_file.replace("\\", "/")

            if normalized_file_path.endswith(normalized_related_file):
                return {
                    "feature_name": branch_info.get("purpose", "").replace(" 기능 개발", ""),
                    "branch_name": branch_name,
                    "owner": branch_info.get("owner", "미정"),
                    "related_files": related_files,
                    "rule": branch_info.get("rule", "")
                }

    return {}