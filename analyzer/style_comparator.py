FUNCTION_LENGTH_THRESHOLD = 5
COMMENT_THRESHOLD = 0.03
SNAKE_CASE_THRESHOLD = 0.05
DEPTH_THRESHOLD = 1


def get_current_avg_function_length(analysis_result: dict) -> float:
    function_lengths = analysis_result["complexity"]["function_length"]
    lengths = list(function_lengths.values())

    if not lengths:
        return 0

    return sum(lengths) / len(lengths)


def compare_with_collaboration_profile(
    analysis_result: dict,
    profile: dict
) -> dict:
    matched_features = []
    different_features = []
    recommendations = []

    current_avg_function_length = get_current_avg_function_length(analysis_result)
    current_comment_ratio = analysis_result["style"]["comment_ratio"]
    current_snake_case_ratio = analysis_result["style"]["snake_case_ratio"]
    current_uses_type_hint = analysis_result["style"]["uses_type_hint"]
    current_uses_docstring = analysis_result["style"]["uses_docstring"]
    current_max_depth = analysis_result["complexity"]["max_depth"]

    target_avg_function_length = profile["avg_function_length"]
    target_comment_ratio = profile["avg_comment_ratio"]
    target_snake_case_ratio = profile["avg_snake_case_ratio"]
    target_type_hint_ratio = profile["uses_type_hint_ratio"]
    target_docstring_ratio = profile["uses_docstring_ratio"]
    target_max_depth = profile["avg_max_depth"]

    similarity_score = 100

    function_length_diff = current_avg_function_length - target_avg_function_length
    comment_ratio_diff = current_comment_ratio - target_comment_ratio
    snake_case_diff = current_snake_case_ratio - target_snake_case_ratio
    depth_diff = current_max_depth - target_max_depth

    if current_avg_function_length == 0:
        different_features.append("함수 구조")
        recommendations.append(
            "함수로 분리되지 않은 코드는 인수인계가 어렵기 때문에 main(), load_data(), process_data()처럼 역할별 함수 분리를 권장합니다."
        )
        similarity_score -= 20
    elif abs(function_length_diff) <= FUNCTION_LENGTH_THRESHOLD:
        matched_features.append("함수 길이")
    else:
        different_features.append("함수 길이")
        recommendations.append(
            "팀 평균보다 함수 길이가 길어 이해 부담이 커질 수 있습니다. 긴 함수는 역할별로 분리하는 것이 좋습니다."
        )
        similarity_score -= 15

    if current_comment_ratio < target_comment_ratio - COMMENT_THRESHOLD:
        if current_uses_docstring:
            matched_features.append("주석/docstring 설명")
        else:
            different_features.append("주석/docstring 설명")
            recommendations.append(
                "주석과 docstring이 부족합니다. 핵심 로직과 수정 시 주의할 부분에 설명을 추가하는 것이 좋습니다."
            )
            similarity_score -= 10

    elif current_comment_ratio > target_comment_ratio + COMMENT_THRESHOLD:
        different_features.append("주석 비율")
        recommendations.append(
            "주석이 많은 편입니다. 코드가 이미 설명하는 내용보다 의도와 주의사항 중심으로 정리하는 것이 좋습니다."
        )
        similarity_score -= 5

    else:
        matched_features.append("주석 비율")


    if current_snake_case_ratio >= 0.8:
        matched_features.append("네이밍 규칙")
    else:
        different_features.append("네이밍 규칙")
        recommendations.append(
            "변수명과 함수명 규칙이 일관적이지 않습니다. snake_case 중심으로 통일하는 것이 좋습니다."
        )
        similarity_score -= 10


    if abs(depth_diff) <= DEPTH_THRESHOLD:
        matched_features.append("중첩 깊이")
    else:
        different_features.append("중첩 깊이")
        recommendations.append(
            "중첩 깊이가 깊어 흐름 파악이 어렵습니다. 조건문 내부 로직을 별도 함수로 분리하는 것이 좋습니다."
        )
        similarity_score -= 15

    if target_type_hint_ratio >= 0.5 and not current_uses_type_hint:
        different_features.append("타입힌트")
        recommendations.append(
            "팀 기준에서는 타입힌트를 사용하는 편입니다. 함수 인자와 반환값 타입을 명시하는 것이 좋습니다."
        )
        similarity_score -= 5
    else:
        matched_features.append("타입힌트")

    if target_docstring_ratio >= 0.5 and not current_uses_docstring:
        different_features.append("docstring")
        recommendations.append(
            "팀 기준에서는 docstring을 사용하는 편입니다. 주요 함수에 역할, 입력, 반환값 설명을 추가하는 것이 좋습니다."
        )
        similarity_score -= 5
    else:
        matched_features.append("docstring")

    similarity_score = max(0, similarity_score)

    return {
        "profile_name": profile.get("profile_name", "team_collaboration_profile"),
        "similarity_score": similarity_score,
        "matched_features": matched_features,
        "different_features": different_features,
        "recommendations": recommendations,
        "diff": {
            "function_length_diff": function_length_diff,
            "comment_ratio_diff": comment_ratio_diff,
            "snake_case_diff": snake_case_diff,
            "depth_diff": depth_diff,
        }
    }