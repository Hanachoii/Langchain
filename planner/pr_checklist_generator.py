COMMON_PR_CHECKLIST = [
    "담당 기능이 정상 실행되는가?",
    "입력값과 출력값 형식이 명확한가?",
    "main.py 또는 다른 모듈과 연결 가능한 구조인가?",
    "불필요하게 다른 팀원 파일을 수정하지 않았는가?",
    "함수명과 변수명이 역할을 잘 드러내는가?",
    "긴 함수는 역할별로 분리했는가?",
    "핵심 로직에 주석 또는 docstring을 추가했는가?",
    "다음 팀원이 먼저 봐야 할 함수가 명확한가?"
]


def generate_pr_checklist(
    branch_name: str,
    changed_files: list[str],
    feature_name: str = "",
    custom_items: list[str] | None = None
) -> str:
    if custom_items is None:
        custom_items = []

    lines = []

    title_feature = feature_name if feature_name else branch_name

    lines.append(f"# PR 체크리스트: {title_feature}\n")

    lines.append("## 1. 변경 브랜치")
    lines.append(f"- `{branch_name}`")

    lines.append("\n## 2. 변경 파일")
    for file in changed_files:
        lines.append(f"- `{file}`")

    lines.append("\n## 3. 공통 확인 사항")
    for item in COMMON_PR_CHECKLIST:
        lines.append(f"- [ ] {item}")

    lines.append("\n## 4. 기능별 확인 사항")
    if custom_items:
        for item in custom_items:
            lines.append(f"- [ ] {item}")
    else:
        lines.append("- [ ] 이 기능의 입력/출력 형식이 다른 모듈과 연결 가능한가?")
        lines.append("- [ ] 이 기능에서 발생할 수 있는 예외 상황을 처리했는가?")

    lines.append("\n## 5. 리뷰어 확인 사항")
    lines.append("- 코드가 기능 요구사항을 만족하는가?")
    lines.append("- 다른 파일과 충돌 가능성은 없는가?")
    lines.append("- 인수인계 리포트 기준 위험 요소가 큰가?")
    lines.append("- 초보 팀원이 이해할 수 있는 구조인가?")

    return "\n".join(lines)