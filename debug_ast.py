import sys
import os

# Add scripts directory to path to import analizador_ci
sys.path.append(os.path.join(os.path.dirname(__file__), "scripts"))
import analizador_ci

with open("test_vulnerable.py", "r", encoding="utf-8") as f:
    code = f.read()

extractor = analizador_ci.ASTFeatureExtractor()
features = extractor.extract(code)

print("AST Features:")
for k, v in features.items():
    print(f"{k}: {v}")

print("\nPath Traversal Findings:")
print(analizador_ci.detect_path_traversal_ast(code))

print("\nHeuristic Findings:")
print(analizador_ci.detect_heuristic_categories(code))
