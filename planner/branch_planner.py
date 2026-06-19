import re


def to_branch_name(feature_name: str) -> str:
    name = feature_name.lower()
    name = re.sub(r"[^a-z0-9가-힣]+", "-", name)
    name = name.strip("-")
    return f"feature/{name}"


def create_branch_plan(features: list[dict]) -> dict:
    """
    features 예시:
    [
        {
            "name": "인수인계 리포트",
            "files": ["generator/handoff_score.py"],
            "owner": "A"
        }
    ]
    """

    branch_plan = {
        "main": {
            "purpose": "최종 안정 버전 관리",
            "rule": "직접 커밋하지 않고 dev에서 검증된 코드만 병합합니다."
        },
        "dev": {
            "purpose": "기능 통합 브랜치",
            "rule": "feature 브랜치 작업 완료 후 PR로 병합합니다."
        }
    }

    for feature in features:
        branch_name = to_branch_name(feature["name"])

        branch_plan[branch_name] = {
            "purpose": f"{feature['name']} 기능 개발",
            "owner": feature.get("owner", "미정"),
            "related_files": feature.get("files", []),
            "pr_checklist": feature.get("pr_checklist", []),
            "rule": "작업 완료 후 dev 브랜치로 PR을 생성합니다."
        }

    return branch_plan