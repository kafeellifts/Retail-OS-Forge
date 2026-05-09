import re

with open("forge_app.py", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Remove Python docstrings (only those that start a line)
text = re.sub(r'(?m)^\s*\"\"\"[\s\S]*?\"\"\"\n', '', text)

# 2. Remove Python full-line comments
text = re.sub(r'(?m)^\s*#.*\n', '', text)

# 3. Remove CSS multi-line comments
text = re.sub(r'/\*[\s\S]*?\*/', '', text)

# 4. Remove HTML comments
text = re.sub(r'<!--[\s\S]*?-->', '', text)

# 5. Remove JS full-line comments
text = re.sub(r'(?m)^\s*//.*\n', '', text)

# 6. Remove JS inline comments that use // (specifically ones with ── or similar patterns to be safe, or just any // that isn't a URL)
text = re.sub(r'(?m)\s+//.*$', '', text)

# 7. Remove multiple blank lines
text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)

with open("forge_app.py", "w", encoding="utf-8") as f:
    f.write(text.strip() + "\n")
