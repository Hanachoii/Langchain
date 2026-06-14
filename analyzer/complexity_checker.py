import ast

def check_complexity(code: str) -> dict:
    tree = ast.parse(code)

    function_lengths = {}
    long_functions = []

    if_count = 0
    loop_count = 0
    try_count = 0

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            lines = node.end_lineno - node.lineno + 1
            function_lengths[node.name] = lines
            if lines > 20:
                long_functions.append(node.name)
        elif isinstance(node, ast.If):
            if_count += 1
        elif isinstance(node, (ast.For, ast.While)):
            loop_count += 1
        elif isinstance(node, ast.Try):
            try_count += 1

    def calculate_max_depth(node, current_depth=0):
        if isinstance(node, (ast.If, ast.For, ast.While, ast.Try)):
            current_depth += 1
        max_depth = current_depth

        for child in ast.iter_child_nodes(node):
            child_depth = calculate_max_depth(child, current_depth)
            max_depth = max(max_depth, child_depth)

        return max_depth

    max_depth = calculate_max_depth(tree)


    return {
        'function_length': function_lengths,
        'long_functions': long_functions,
        'if_count': if_count,
        'loop_count': loop_count,
        'try_count': try_count,
        'max_depth': max_depth,
    }