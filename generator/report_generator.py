def generate_handoff_report(
    analysis_result: dict,
    handoff_score: dict,
    style_comparison: dict | None = None
) -> str:
    ast_result = analysis_result["ast"]
    style = analysis_result["style"]
    complexity = analysis_result["complexity"]

    lines = []

    lines.append("# AI 인수인계 리포트\n")

    lines.append("## 1. 코드 구조 요약")
    lines.append(f"- 함수 개수: {ast_result['function_count']}")
    lines.append(f"- 클래스 개수: {ast_result['class_count']}")
    lines.append(f"- import 개수: {ast_result['import_count']}")

    lines.append("\n## 2. 주요 함수")
    if ast_result["function_names"]:
        for name in ast_result["function_names"]:
            length = complexity["function_length"].get(name, "알 수 없음")
            lines.append(f"- `{name}`: 약 {length}줄")
    else:
        lines.append("- 함수가 정의되어 있지 않습니다.")

    lines.append("\n## 3. 주요 클래스")
    if ast_result["class_names"]:
        for name in ast_result["class_names"]:
            lines.append(f"- `{name}`")
    else:
        lines.append("- 클래스가 정의되어 있지 않습니다.")

    lines.append("\n## 4. 사용 모듈")
    if ast_result["import_names"]:
        for name in ast_result["import_names"]:
            lines.append(f"- `{name}`")
    else:
        lines.append("- import가 없습니다.")

    lines.append("\n## 5. 스타일/가독성 요약")
    lines.append(f"- 전체 줄 수: {style['total_lines']}")
    lines.append(f"- 주석 비율: {style['comment_ratio']:.2f}")
    lines.append(f"- snake_case 비율: {style['snake_case_ratio']:.2f}")
    lines.append(f"- 타입힌트 사용 여부: {style['uses_type_hint']}")
    lines.append(f"- docstring 사용 여부: {style['uses_docstring']}")

    lines.append("\n## 6. 복잡도 요약")
    lines.append(f"- 긴 함수 목록: {complexity['long_functions']}")
    lines.append(f"- if 개수: {complexity['if_count']}")
    lines.append(f"- loop 개수: {complexity['loop_count']}")
    lines.append(f"- try 개수: {complexity['try_count']}")
    lines.append(f"- 최대 중첩 깊이: {complexity['max_depth']}")

    lines.append("\n## 7. 인수인계 난이도")
    lines.append(f"- 점수: {handoff_score['handoff_score']}/100")
    lines.append(f"- 위험도: {handoff_score['handoff_risk_level']}")

    lines.append("\n## 8. 인수인계 위험 요인")
    if handoff_score["handoff_reasons"]:
        for reason in handoff_score["handoff_reasons"]:
            lines.append(f"- {reason}")
    else:
        lines.append("- 특별한 위험 요인이 크지 않습니다.")

    if style_comparison:
        lines.append("\n## 9. 팀 협업 기준 비교")
        lines.append(f"- 팀 기준 유사도: {style_comparison['similarity_score']}/100")
        lines.append(f"- 유사한 항목: {', '.join(style_comparison['matched_features'])}")
        lines.append(f"- 차이가 큰 항목: {', '.join(style_comparison['different_features'])}")

        lines.append("\n## 10. 개선 권장 사항")
        for rec in style_comparison["recommendations"]:
            lines.append(f"- {rec}")

    lines.append("\n## 11. 신규 팀원이 먼저 봐야 할 부분")
    if "main" in ast_result["function_names"]:
        lines.append("- `main()` 함수부터 확인하는 것을 권장합니다.")
    elif ast_result["function_names"]:
        lines.append(f"- `{ast_result['function_names'][0]}` 함수부터 확인하는 것을 권장합니다.")
    else:
        lines.append("- 함수로 분리되어 있지 않으므로 파일 상단부터 실행 흐름을 따라가야 합니다.")

    return "\n".join(lines)