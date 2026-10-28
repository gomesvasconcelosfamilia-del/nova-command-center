#!/usr/bin/env python3
"""Public-site checks. No network, dependencies, credentials or private repo access."""
from html.parser import HTMLParser
from pathlib import Path
import re
import sys

class Audit(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []
        self.lang = None
        self.scripts = 0
        self.forms = 0
        self.external = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.lang = attrs.get("lang")
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
        if tag == "script":
            self.scripts += 1
        if tag == "form":
            self.forms += 1
        if tag in ("script", "img", "iframe", "link") and attrs.get("src", attrs.get("href", "")).startswith(("https://", "http://")):
            self.external.append(tag)

def main():
    path = Path("index.html")
    if not path.is_file():
        print("FAIL: missing index.html")
        return 1
    content = path.read_text(encoding="utf-8")
    audit = Audit()
    audit.feed(content)
    errors = []
    if audit.lang != "pt-PT":
        errors.append("Missing pt-PT language")
    if audit.scripts or audit.forms:
        errors.append("Public site unexpectedly contains script or form")
    if audit.external:
        errors.append("Unexpected remote assets")
    if any(link.startswith("#") and link[1:] not in audit.ids for link in audit.links):
        errors.append("Broken internal anchor")
    if re.search(r"(?i)github\.com/gomesvasconcelosfamilia-del/(?:novarawplugin|nova-operator|nova-bridge|ABLETON-NOVA-BRIDGE)", content):
        errors.append("Internal repository URL")
    if re.search(r"gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}", content):
        errors.append("Potential GitHub credential")
    if re.search(r"(?i)private-api|access_team_domain|github_token|admin_email", content):
        errors.append("Private configuration reference")
    print("Public site checks:", "PASS" if not errors else "FAIL")
    for error in errors:
        print(" -", error)
    return bool(errors)

if __name__ == "__main__":
    sys.exit(main())
