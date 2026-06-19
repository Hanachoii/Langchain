def split_roles(member_names: list[str], features: list[dict]) -> dict:
    """
    features 예시:
    [
        {
            "name": "코드 분석",
            "difficulty": "중간",
            "files": ["analyzer/ast_analyzer.py"]
        }
    ]
    """

    if not member_names:
        raise ValueError("팀원 이름이 필요합니다.")

    result = {member: [] for member in member_names}

    sorted_features = sorted(
        features,
        key=lambda x: x.get("difficulty", "중간"),
        reverse=True
    )

    for idx, feature in enumerate(sorted_features):
        member = member_names[idx % len(member_names)]
        result[member].append(feature)

    return result