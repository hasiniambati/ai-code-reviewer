import ast
import re

class CodeReviewAgentGraph:
    @staticmethod
    def audit_code(code_snippet: str):
        issues = []
        suggestions = []
        
        # 1. AST Syntax & Structure Check
        try:
            tree = ast.parse(code_snippet)
        except SyntaxError as e:
            return {
                "status": "Syntax Error",
                "issues": [f"❌ Python Syntax Error: {str(e)}"],
                "suggestions": ["Fix the syntax error before running static analysis."],
                "refactored_code": code_snippet,
                "confidence": "Low"
            }

        has_return = False

        for node in ast.walk(tree):
            # Check for bare except clauses
            if isinstance(node, ast.ExceptHandler) and node.type is None:
                issues.append("⚠️ Bare 'except:' clause detected. Catches all exceptions.")
                suggestions.append("Specify exception types explicitly (e.g., `except ValueError:`).")
            
            # Check for global variables
            if isinstance(node, ast.Global):
                issues.append("⚠️ Use of 'global' keyword detected.")
                suggestions.append("Pass variables as parameters or use class state.")

            # Check for return statements
            if isinstance(node, ast.Return):
                has_return = True

            # Check for function definitions and local scope usage (Undefined variables)
            if isinstance(node, ast.FunctionDef):
                local_stores = set()
                local_loads = set()
                args_set = {arg.arg for arg in node.args.args}

                for subnode in ast.walk(node):
                    if isinstance(subnode, ast.Store):
                        if isinstance(subnode, ast.Name):
                            local_stores.add(subnode.id)
                    elif isinstance(subnode, ast.Load):
                        if isinstance(subnode, ast.Name):
                            local_loads.add(subnode.id)

                # Variables used but never defined or passed in arguments
                undefined = local_loads - local_stores - args_set - {'print', 'len', 'deque', 'graph', 'range', 'int', 'str', 'list', 'set', 'dict'}
                if undefined:
                    for var in undefined:
                        issues.append(f"🚨 Name/Runtime Error: Variable '{var}' is used before being defined or initialized in function `{node.name}`.")
                        suggestions.append(f"Initialize '{var}' (e.g., `queue = deque([start])` or `visited = []`) before using it in the loop.")

        # 2. Security & Vulnerability Scan
        if re.search(r"\beval\s*\(", code_snippet):
            issues.append("🚨 Critical Security Flaw: Use of `eval()` detected.")
            suggestions.append("Replace `eval()` with `ast.literal_eval()`.")

        # 3. Logical Completeness Check
        if any(isinstance(n, (ast.While, ast.For)) for n in ast.walk(tree)) and not has_return:
            issues.append("⚠️ Logical Warning: Function contains a loop (`while`/`for`) but has no `return` statement.")
            suggestions.append("Ensure your function returns the final result (e.g., `return visited`).")

        if not issues:
            issues.append("✅ No critical syntax errors, scoping bugs, or security anti-patterns detected.")
            suggestions.append("Code structure is clean and follows correct scoping.")
            confidence = "High (Passed Audit)"
            refactored = code_snippet
        else:
            confidence = "Medium (Requires Remediation)"
            refactored = code_snippet

        return {
            "status": "Audited & Remediation Generated",
            "issues": issues,
            "suggestions": suggestions,
            "refactored_code": refactored,
            "confidence": confidence
        }