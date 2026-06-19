import re
import ast

def extract_style_features(code: str) -> dict:
    lines = code.splitlines()

    total_lines = len(lines)

    comment_lines = 0
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('#'):
            comment_lines += 1
    comment_ratio = comment_lines / total_lines if total_lines else 0

    tree = ast.parse(code)

    variable_names = []
    function_names = []

    use_type_hint = False
    use_docstring = False

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_names.append(node.name)

            for arg in node.args.args:
                if arg.annotation is not None:
                    use_type_hint = True
            if node.returns is not None:
                use_type_hint = True
            if ast.get_docstring(node) is not None:
                use_docstring = True

        elif isinstance(node, ast.Name):
            if isinstance(node.ctx, ast.Store):
                variable_names.append(node.id)

    pattern = r"^[a-z_][a-z0-9_]*$"
    all_names = variable_names + function_names
    snake_case_lines = sum(1 for name in all_names if re.match(pattern, name))
    snake_case_ratio = snake_case_lines / len(all_names) if all_names else 0

    return {
        'total_lines': total_lines,
        'comment_lines': comment_lines,
        'comment_ratio': comment_ratio,
        'variable_names': variable_names,
        'function_names': function_names,
        'snake_case_ratio': snake_case_ratio,
        'uses_type_hint': use_type_hint,
        'uses_docstring': use_docstring
    }