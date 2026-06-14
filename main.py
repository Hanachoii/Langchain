from utils.code_loader import load_code
from analyzer.ast_analyzer import analyze_ast
from analyzer.style_extractor import extract_style_features
from analyzer.complexity_checker import check_complexity
from chains.review_chain import generate_review
import json


def main():
    # 1. 코드 불러오기
    code = load_code("sample_code.py")

    # 2. 코드 분석
    ast_result = analyze_ast(code)
    style_result = extract_style_features(code)
    complexity_result = check_complexity(code)

    # 3. 분석 결과 통합
    analysis_result = {
        "ast": ast_result,
        "style": style_result,
        "complexity": complexity_result,
    }

    analysis_result = json.dumps(
        analysis_result,
        indent=2,
        ensure_ascii=False
    )

    print(analysis_result)

    # 4. LangChain으로 리뷰 생성
    #review = generate_review(code, analysis_result)

    # 5. 결과 출력
    #print(review)


if __name__ == "__main__":
    main()