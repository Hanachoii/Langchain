import json

from utils.code_loader import load_code
from utils.project_plan_storage import (
    save_project_plan,
    load_project_plan,
    find_feature_by_file
)

from analyzer.ast_analyzer import analyze_ast
from analyzer.style_extractor import extract_style_features
from analyzer.complexity_checker import check_complexity
from analyzer.style_comparator import compare_with_collaboration_profile

from generator.handoff_score import calculate_handoff_score
from generator.report_generator import generate_handoff_report

from chains.review_chain import generate_handoff_review

from planner.branch_planner import create_branch_plan
from planner.role_splitter import split_roles
from planner.pr_checklist_generator import generate_pr_checklist
from planner.project_structure_planner import generate_project_structure_plan

def analyze_code(code: str) -> dict:
    return {
        "ast": analyze_ast(code),
        "style": extract_style_features(code),
        "complexity": check_complexity(code),
    }


def load_profile(profile_path: str) -> dict:
    with open(profile_path, "r", encoding="utf-8") as file:
        return json.load(file)


def planning_mode():
    print("===== 프로젝트 시작 단계 =====")

    project_description = input("만들고 싶은 프로젝트를 설명하세요: ")
    member_input = input("팀원 이름을 쉼표로 입력하세요. 예: A,B,C: ")

    member_names = [
        name.strip()
        for name in member_input.split(",")
        if name.strip()
    ]

    if not member_names:
        print("팀원 이름이 필요합니다.")
        return

    structure = generate_project_structure_plan(
        project_description=project_description,
        member_count=len(member_names)
    )

    if "error" in structure:
        print("프로젝트 구조 생성 중 오류가 발생했습니다.")
        print(structure["raw_response"])
        return

    print("\n===== 프로젝트 요약 =====")
    print(structure["summary"])

    print("\n===== 추천 폴더 구조 =====")
    for folder in structure["folders"]:
        print(f"- {folder['path']}: {folder['purpose']}")

    features = structure["features"]

    print("\n===== 기능 분해 =====")
    for feature in features:
        print(f"\n[{feature['name']}]")
        print(f"- 설명: {feature['description']}")
        print(f"- 난이도: {feature['difficulty']}")
        print(f"- 관련 파일: {feature['files']}")
        print(f"- 선행 기능: {feature['dependencies']}")

    roles = split_roles(member_names, features)

    for member, tasks in roles.items():
        for task in tasks:
            task["owner"] = member

    assigned_features = []
    for tasks in roles.values():
        assigned_features.extend(tasks)

    branches = create_branch_plan(assigned_features)

    project_plan = {
        "project_description": project_description,
        "structure": structure,
        "features": features,
        "roles": roles,
        "branches": branches
    }

    save_project_plan(project_plan)

    print("\n===== 프로젝트 계획 저장 완료 =====")
    print("저장 위치: data/project_plan.json")

    print("\n===== 역할 분담 =====")
    for member, tasks in roles.items():
        print(f"\n[{member}]")
        for task in tasks:
            print(f"- {task['name']}")
            print(f"  난이도: {task['difficulty']}")
            print(f"  담당 파일: {task['files']}")

    print("\n===== 브랜치 전략 =====")
    for branch_name, branch_info in branches.items():
        print(f"\n[{branch_name}]")
        print(f"- 목적: {branch_info['purpose']}")
        print(f"- 규칙: {branch_info['rule']}")

        if "owner" in branch_info:
            print(f"- 담당자: {branch_info['owner']}")

        if "related_files" in branch_info:
            print(f"- 관련 파일: {branch_info['related_files']}")

    print("\n===== 브랜치별 PR 체크리스트 =====")
    for branch_name, branch_info in branches.items():
        if branch_name in ["main", "dev"]:
            continue

        checklist = generate_pr_checklist(
            branch_name=branch_name,
            changed_files=branch_info["related_files"],
            feature_name=branch_info["purpose"].replace(" 기능 개발", ""),
            custom_items=branch_info.get("pr_checklist", [])
        )

        print(f"\n--- {branch_name} ---")
        print(checklist)


def review_mode():
    print("===== 개발 코드 리뷰 단계 =====")

    code_path = input("리뷰할 코드 파일 경로를 입력하세요. 예: sample_code.py: ")

    project_plan = load_project_plan()
    feature_context = find_feature_by_file(code_path, project_plan)

    profile_path = input(
        "팀 협업 프로파일 경로를 입력하세요. 기본값: profiles/team_collaboration_profile.json: "
    )

    if not profile_path.strip():
        profile_path = "profiles/team_collaboration_profile.json"

    code = load_code(code_path)

    if code == "File not found":
        print("코드 파일을 찾을 수 없습니다.")
        return

    analysis_result = analyze_code(code)
    profile = load_profile(profile_path)

    style_comparison = compare_with_collaboration_profile(
        analysis_result,
        profile
    )

    handoff_score = calculate_handoff_score(
        analysis_result,
        style_comparison
    )

    handoff_report = generate_handoff_report(
        analysis_result,
        handoff_score,
        style_comparison
    )

    if feature_context:
        print("\n===== 프로젝트 연결 정보 =====")
        print(f"- 담당 기능: {feature_context['feature_name']}")
        print(f"- 브랜치: {feature_context['branch_name']}")
        print(f"- 담당자: {feature_context['owner']}")
        print(f"- 관련 파일: {feature_context['related_files']}")
    else:
        print("\n===== 프로젝트 연결 정보 =====")
        print("- 저장된 프로젝트 계획에서 이 파일과 연결된 기능을 찾지 못했습니다.")

    print("\n===== 인수인계 리포트 =====")
    print(handoff_report)

    use_llm = input("\nAI 리뷰도 생성할까요? (y/n): ")

    if use_llm.lower() == "y":
        review = generate_handoff_review(
            code=code,
            analysis_result=analysis_result,
            style_comparison=style_comparison,
            handoff_score=handoff_score,
            handoff_report=handoff_report
        )

        print("\n===== AI 리뷰 =====")
        print(review)


def main():
    print("===== AI 프로젝트 협업 도우미 =====")
    print("1. 프로젝트 시작 설계")
    print("2. 개발 코드 리뷰/인수인계 분석")

    mode = input("모드를 선택하세요 (1/2): ")

    if mode == "1":
        planning_mode()
    elif mode == "2":
        review_mode()
    else:
        print("올바른 모드를 선택하세요.")


if __name__ == "__main__":
    main()