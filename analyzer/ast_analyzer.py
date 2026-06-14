import ast

def analyze_ast(code: str) -> dict:
    tree = ast.parse(code)

    function_names = []
    class_names = []
    import_names = []

    for node in ast.walk(tree):

        if isinstance(node, ast.FunctionDef):
            function_names.append(node.name)
        elif isinstance(node, ast.ClassDef):
            class_names.append(node.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                import_names.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                import_names.append(alias.name)

    return {
        'function_count': len(function_names),
        'class_count': len(class_names),
        'import_count': len(import_names),
        'import_names': import_names,
        'function_names': function_names,
        'class_names': class_names,
    }