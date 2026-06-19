# analyzer/style_profiler.py

def create_collaboration_profile(all_analysis_results: list) -> dict:
    if not all_analysis_results:
        return {
            "error": "분석 결과 없음"
        }

    function_lengths = []

    for result in all_analysis_results:
        lengths = result["complexity"]["function_length"].values()
        function_lengths.extend(lengths)

    avg_function_length = (
        sum(function_lengths) / len(function_lengths)
        if function_lengths else 0
    )

    avg_comment_ratio = sum(
        r["style"]["comment_ratio"]
        for r in all_analysis_results
    ) / len(all_analysis_results)

    avg_snake_case_ratio = sum(
        r["style"]["snake_case_ratio"]
        for r in all_analysis_results
    ) / len(all_analysis_results)

    avg_max_depth = sum(
        r["complexity"]["max_depth"]
        for r in all_analysis_results
    ) / len(all_analysis_results)

    type_hint_ratio = sum(
        1
        for r in all_analysis_results
        if r["style"]["uses_type_hint"]
    ) / len(all_analysis_results)

    docstring_ratio = sum(
        1
        for r in all_analysis_results
        if r["style"]["uses_docstring"]
    ) / len(all_analysis_results)

    return {
        "profile_name": "team_collaboration_profile",

        "avg_function_length": avg_function_length,
        "avg_comment_ratio": avg_comment_ratio,
        "avg_snake_case_ratio": avg_snake_case_ratio,
        "avg_max_depth": avg_max_depth,

        "uses_type_hint_ratio": type_hint_ratio,
        "uses_docstring_ratio": docstring_ratio
    }