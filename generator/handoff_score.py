def calculate_handoff_score(
    analysis_result: dict,
    style_comparison: dict | None = None
) -> dict:
    score = 100
    reasons = []

    ast_result = analysis_result["ast"]
    style = analysis_result["style"]
    complexity = analysis_result["complexity"]

    if ast_result["function_count"] == 0:
        score -= 20
        reasons.append("함수로 분리되어 있지 않아 실행 흐름을 처음부터 끝까지 따라가야 합니다.")

    if complexity["long_functions"]:
        penalty = min(len(complexity["long_functions"]) * 10, 20)
        score -= penalty
        reasons.append(
            f"긴 함수가 {len(complexity['long_functions'])}개 있어 특정 기능을 수정하기 어렵습니다."
        )

    if complexity["max_depth"] >= 4:
        score -= 15
        reasons.append("중첩 깊이가 깊어 조건/반복 흐름을 파악하기 어렵습니다.")

    if style["comment_ratio"] < 0.03 and not style["uses_docstring"]:
        score -= 10
        reasons.append("주석과 docstring이 부족해 코드 작성 의도와 수정 시 주의점을 파악하기 어렵습니다.")

    if style["snake_case_ratio"] < 0.7:
        score -= 10
        reasons.append("변수명/함수명 규칙이 일관적이지 않아 코드 역할을 추론하기 어렵습니다.")

    if not style["uses_type_hint"]:
        score -= 5
        reasons.append("타입힌트가 없어 함수 입력/출력 형태를 파악하기 어렵습니다.")

    if not style["uses_docstring"]:
        score -= 5
        reasons.append("docstring이 없어 함수의 역할과 사용법을 빠르게 이해하기 어렵습니다.")

    if style_comparison:
        if style_comparison["similarity_score"] < 60:
            score -= 10
            reasons.append("팀 협업 기준과 차이가 커서 다른 팀원이 이어서 작성하기 어려울 수 있습니다.")

    score = max(0, score)

    if score >= 80:
        risk_level = "낮음"
    elif score >= 60:
        risk_level = "보통"
    else:
        risk_level = "높음"

    return {
        "handoff_score": score,
        "handoff_risk_level": risk_level,
        "handoff_reasons": reasons,
    }