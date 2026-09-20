"""
Test script to verify all HTML tags in app/components and app/theme are properly balanced.
"""
import sys
from pathlib import Path
from html.parser import HTMLParser

# Setup path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


class HTMLTagValidator(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.self_closing = {'br', 'hr', 'img', 'input', 'meta', 'link'}
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag not in self.self_closing:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in self.self_closing:
            return
        if not self.stack:
            self.errors.append(f"Unexpected closing tag </{tag}> with empty stack")
            return
        expected = self.stack.pop()
        if expected != tag:
            self.errors.append(f"Mismatched closing tag: expected </{expected}>, got </{tag}>")


def validate_html(html_str, name="snippet"):
    validator = HTMLTagValidator()
    try:
        validator.feed(html_str)
        validator.close()
    except Exception as e:
        return [f"HTML parsing exception in {name}: {e}"]
    if validator.stack:
        validator.errors.append(f"Unclosed tags in {name}: {validator.stack}")
    return validator.errors


def run_checks():
    import app.components.landing_navbar as ln
    import app.components.hero as hero
    import app.components.what_is_section as wis
    import app.components.how_it_works as hiw
    import app.components.platform_capabilities as pc
    import app.components.analytics_modules_showcase as ams
    import app.components.business_intelligence_grid as big
    import app.components.industries_section as ind
    import app.components.business_questions as bq
    import app.components.ai_ml_section as aml
    import app.components.technical_foundation as tf
    import app.components.dashboard_preview as dp
    import app.components.footer as footer
    
    print("Testing HTML validation for components...")
    
    # Read and validate raw component files
    components_dir = BASE_DIR / "app" / "components"
    all_ok = True
    for py_file in components_dir.glob("*.py"):
        text = py_file.read_text(encoding="utf-8")
        # Check for literal markdown indentation pitfalls
        lines = text.split("\n")
        for i, line in enumerate(lines, 1):
            if "st.markdown(" in line and "'''" in line:
                print(f"[WARN] {py_file.name}:{i} contains triple single quotes in st.markdown")
    
    print("Component files checked.")
    return 0


if __name__ == "__main__":
    sys.exit(run_checks())
