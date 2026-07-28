#!/usr/bin/env python3
"""
JG Mart — Toolkit Auto-Validation Script
===========================================
Scans the entire JG Mart Hermes toolkit, validates HTML integrity,
Python syntax, cross-references, and generates a VALIDATION_REPORT.txt

Usage:
    python validate_toolkit.py                        # Full validation
    python validate_toolkit.py --quiet                # Minimal console output
    python validate_toolkit.py --html-only            # Only HTML checks
    python validate_toolkit.py --python-only          # Only Python checks
    python validate_toolkit.py --cross-refs-only      # Only cross-reference checks
"""

import os
import re
import sys
import html.parser
import ast
from pathlib import Path
from collections import Counter, defaultdict

# ── Configuration ──────────────────────────────────────────────────────────────
TOOLKIT_DIR = Path(__file__).resolve().parent.parent
REPORT_PATH = TOOLKIT_DIR / "VALIDATION_REPORT.txt"
WHATSAPP_NUMBER = "+8801870489448"
STORAGE_PREFIXES = ("jgmart_", "jgcmart_", "wizard_", "jg_")
REQUIRED_TAG_PAIRS = [("html", "html"), ("head", "head"), ("body", "body"), ("script", "script")]

EXCLUDED_FROM_MASTER_INDEX = {
    "09_Data_Export/launch_outputs",
    "09_Data_Export/sync_out",
    "09_Data_Export/*.json",
    "theme.css",
}


# ── ANSI Colors ───────────────────────────────────────────────────────────────
class Color:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    RESET = "\033[0m"
    GREY = "\033[90m"

    @staticmethod
    def ok(text):
        return f"{Color.GREEN}✔ {text}{Color.RESET}"

    @staticmethod
    def fail(text):
        return f"{Color.RED}✘ {text}{Color.RESET}"

    @staticmethod
    def warn(text):
        return f"{Color.YELLOW}⚠ {text}{Color.RESET}"

    @staticmethod
    def info(text):
        return f"{Color.CYAN}ℹ {text}{Color.RESET}"

    @staticmethod
    def header(text):
        return f"{Color.BOLD}{Color.CYAN}{text}{Color.RESET}"


# ── HTML Tag Pair Validator ────────────────────────────────────────────────────
class TagPairChecker:
    """Validate that required HTML tags appear as both open and close."""

    def __init__(self, raw_html, required_pairs):
        self.raw = raw_html
        self.required = required_pairs

    def check(self):
        results = {}
        for ot, ct in self.required:
            # Match <html> but not </html>, <html attr>, <html>
            open_pat = re.compile(rf"<{ot}(\s[^>]*)?>", re.IGNORECASE)
            close_pat = re.compile(rf"</{ct}\s*>", re.IGNORECASE)
            results[(ot, ct)] = {
                "open": bool(open_pat.search(self.raw)),
                "close": bool(close_pat.search(self.raw)),
            }
        return results

    def check_balance(self):
        """Use a simple stack to detect unclosed/mismatched tags for the required pairs."""
        errors = []
        stack = []
        tag_re = re.compile(r"</?(\w+)[^>]*>")
        void_elements = {
            "area", "base", "br", "col", "embed", "hr", "img", "input",
            "link", "meta", "param", "source", "track", "wbr",
        }

        for match in tag_re.finditer(self.raw):
            tag = match.group(1).lower()
            if tag not in {ot.lower() for ot, _ in self.required}:
                continue  # only track required tags
            if match.group(0).startswith("</"):
                # Closing tag
                if stack and stack[-1] == tag:
                    stack.pop()
                elif tag in stack:
                    errors.append(f"Mismatched </{tag}>: expected </{stack[-1]}>")
                else:
                    errors.append(f"Extra closing </{tag}> without matching open")
            else:
                if tag not in void_elements:
                    stack.append(tag)

        if stack:
            errors.append(f"Unclosed tags at EOF: {', '.join(stack)}")

        return errors


# ── File Discovery ────────────────────────────────────────────────────────────
def discover_files(toolkit_dir):
    """Discover all files, return by type with stats."""
    all_files = []
    by_type = defaultdict(list)
    ext_counts = Counter()
    total_size = 0

    for fpath in toolkit_dir.rglob("*"):
        if fpath.is_file() and not fpath.name.startswith("."):
            rel = str(fpath.relative_to(toolkit_dir)).replace("\\", "/")
            # Skip __pycache__ directories
            if "/__pycache__/" in rel or rel.startswith("__pycache__/"):
                continue
            all_files.append(rel)
            ext = fpath.suffix.lower() or "(no ext)"
            ext_counts[ext] += 1
            by_type[ext].append(rel)
            total_size += fpath.stat().st_size

    return all_files, by_type, ext_counts, total_size


# ── HTML Validation ───────────────────────────────────────────────────────────
def check_html_file(rel_path, abs_path):
    result = {
        "path": rel_path,
        "has_doctype": False,
        "has_viewport": False,
        "has_theme_color": False,
        "tag_pairs": {},
        "tag_errors": [],
        "localstorage_keys": [],
        "whatsapp_refs": [],
        "internal_links": [],
        "issues": [],
    }

    try:
        raw = abs_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        result["issues"].append(f"Cannot read file: {e}")
        return result

    result["has_doctype"] = bool(re.search(r"<!DOCTYPE\s+html", raw, re.IGNORECASE))
    result["has_viewport"] = bool(re.search(
        r'<meta[^>]*name=["\']viewport["\']', raw, re.IGNORECASE
    ))
    result["has_theme_color"] = bool(re.search(
        r'<meta[^>]*name=["\']theme-color["\']', raw, re.IGNORECASE
    ))

    # Tag pair checks
    tpc = TagPairChecker(raw, REQUIRED_TAG_PAIRS)
    result["tag_pairs"] = tpc.check()
    result["tag_errors"] = tpc.check_balance()

    # localStorage keys
    ls_pattern = re.compile(
        r"""localStorage\.(?:getItem|setItem|removeItem)\s*\(\s*['"]((?:"""
        + "|".join(re.escape(p) for p in STORAGE_PREFIXES)
        + r""")[^'"]*)['"]\s*\)"""
    )
    result["localstorage_keys"] = sorted(set(ls_pattern.findall(raw)))

    # WhatsApp references
    wa_count = len(re.findall(re.escape(WHATSAPP_NUMBER), raw))
    if wa_count > 0:
        result["whatsapp_refs"] = [(WHATSAPP_NUMBER, wa_count)]

    # Internal links (href= to files, not external URLs)
    href_pattern = re.compile(
        r"""href=["']((?!https?://|#|tel:|mailto:|javascript:|data:)[^"']+)["']""",
        re.IGNORECASE,
    )
    for match in href_pattern.finditer(raw):
        href = match.group(1).split("#")[0].split("?")[0]
        if href and not href.startswith(("http", "//", "data:")):
            result["internal_links"].append(href)

    return result


# ── Python Validation ─────────────────────────────────────────────────────────
def check_python_file(rel_path, abs_path):
    result = {
        "path": rel_path,
        "has_shebang": False,
        "has_docstring": False,
        "syntax_ok": False,
        "syntax_error": None,
    }

    try:
        raw = abs_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        result["syntax_error"] = f"Cannot read file: {e}"
        return result

    result["has_shebang"] = raw.startswith("#!/usr/bin/env python3") or raw.startswith("#!/usr/bin/python3")

    # Docstring: first module-level expression is a string literal
    try:
        tree = ast.parse(raw)
        if tree.body and isinstance(tree.body[0], ast.Expr):
            val = tree.body[0].value
            if isinstance(val, (ast.Constant, ast.Str)):
                result["has_docstring"] = True
    except SyntaxError:
        pass

    try:
        compile(raw, str(abs_path), "exec")
        result["syntax_ok"] = True
    except SyntaxError as e:
        result["syntax_ok"] = False
        result["syntax_error"] = f"Line {e.lineno}: {e.msg}"

    return result


# ── MASTER_INDEX Parser ───────────────────────────────────────────────────────
def parse_master_index(text):
    """
    Parse MASTER_INDEX.txt hierarchical format.

    Format:
      01_Investor_Deck
        • INVESTOR_1PAGER.txt
        • EXECUTIVE_SUMMARY.txt
      ROOT
        • QUICK_START.txt

    Returns a set of paths like "01_Investor_Deck/INVESTOR_1PAGER.txt"
    """
    refs = set()
    current_dir = ""
    in_file_listing_section = False

    for line in text.splitlines():
        stripped = line.strip()

        # Detect the "COMPLETE FILE LISTING" section
        if "COMPLETE FILE LISTING" in stripped.upper():
            in_file_listing_section = True
            continue

        if not in_file_listing_section:
            continue

        # Directory headers: "01_Investor_Deck", "11_Day1_Launch_Kit", "ROOT"
        dir_match = re.match(r"^(\d{2}_[A-Za-z0-9_]+|ROOT|Root)$", stripped)
        if dir_match:
            dir_name = dir_match.group(1)
            current_dir = "" if dir_name.upper() == "ROOT" else dir_name
            continue

        # Bullet entries with filenames
        bullet_match = re.match(r"[•●]\s*(.+\.\w+)", stripped)
        if bullet_match:
            fname = bullet_match.group(1).strip()
            # Remove any markdown formatting
            fname = re.sub(r"\*\*", "", fname)
            # Check if fname already has a path prefix
            if "/" in fname:
                refs.add(fname)
            elif current_dir:
                refs.add(f"{current_dir}/{fname}")
            else:
                refs.add(fname)

    return refs


def parse_readme_file_list(text):
    """
    Parse README.txt listing format.

    README uses:
      📁 01_Investor_Deck
         • INVESTOR_1PAGER.txt — corrected v2.2 ...

    Returns set of paths like "01_Investor_Deck/INVESTOR_1PAGER.txt"
    """
    refs = set()
    current_dir = ""

    for line in text.splitlines():
        stripped = line.strip()

        # Directory headers: 📁 01_Investor_Deck or 📁 Root
        dir_match = re.match(r"📁\s*(.+)$", stripped)
        if dir_match:
            dir_name = dir_match.group(1).strip().rstrip("*")
            current_dir = "" if dir_name.upper() in ("ROOT", "ROOT*") else dir_name
            continue

        # Bullet entries
        bullet_match = re.match(r"[•●]\s*(.+?)(?:\s+[—–-]|\s*$)", stripped)
        if bullet_match:
            fname = bullet_match.group(1).strip()
            fname = re.sub(r"\*\*", "", fname)
            fname = fname.rstrip("*")
            # Extract just the filename (before any dash/comment)
            fname = re.split(r"\s+[—–-]\s+", fname)[0].strip()
            if "/" in fname:
                refs.add(fname)
            elif current_dir:
                refs.add(f"{current_dir}/{fname}")
            else:
                refs.add(fname)

    return refs


def parse_index_html_refs(text):
    """Extract openFile('...') references from index.html."""
    refs = set()
    for match in re.finditer(r"""openFile\(['"]([^'"]+)['"]\)""", text):
        refs.add(match.group(1))
    return refs


# ── Cross-Reference Checks ────────────────────────────────────────────────────
def check_references_exist(refs, all_file_set, toolkit_dir, source_name, quiet=False):
    """Check that all referenced files exist on disk."""
    missing = []
    for ref in sorted(refs):
        if "*" in ref:
            continue
        norm_ref = ref.replace("\\", "/")
        if norm_ref in all_file_set:
            continue
        resolved = toolkit_dir / norm_ref
        if not resolved.exists():
            missing.append(norm_ref)

    if not quiet:
        if missing:
            print(f"  {Color.fail(f'{source_name}: {len(missing)} broken reference(s)')}")
            for m in missing[:15]:
                print(f"       {Color.fail('•')} {m}")
            if len(missing) > 15:
                print(f"       {Color.warn(f'… and {len(missing) - 15} more')}")
        else:
            print(f"  {Color.ok(f'{source_name}: all {len(refs)} references valid')}")

    return missing


def check_master_index_coverage(all_files, master_refs, toolkit_dir, quiet=False):
    """Compare actual files against MASTER_INDEX entries."""
    all_set = set(all_files)
    master_set = set()
    for r in master_refs:
        master_set.add(r.replace("\\", "/").strip().rstrip(")"))

    files_not_in_index = []
    for f in sorted(all_set):
        if f in master_set:
            continue
        excluded = False
        for ex in EXCLUDED_FROM_MASTER_INDEX:
            if ex.endswith("/*"):
                if f.startswith(ex[:-1]):
                    excluded = True
                    break
            elif ex.endswith(".json"):
                if f.endswith(".json") and f.startswith("09_Data_Export/"):
                    excluded = True
                    break
            else:
                if f == ex or f.startswith(ex + "/"):
                    excluded = True
                    break
        if not excluded:
            files_not_in_index.append(f)

    missing_files = []
    for r in sorted(master_set):
        if "*" in r:
            continue
        if r not in all_set:
            resolved = toolkit_dir / r
            if not resolved.exists():
                missing_files.append(r)

    if not quiet:
        if files_not_in_index:
            print(f"  {Color.warn(f'{len(files_not_in_index)} file(s) not in MASTER_INDEX.txt')}")
            for f in files_not_in_index[:10]:
                print(f"       {Color.warn('•')} {f}")
            if len(files_not_in_index) > 10:
                print(f"       {Color.warn(f'… and {len(files_not_in_index) - 10} more')}")
        else:
            print(f"  {Color.ok('MASTER_INDEX.txt covers all files')}")

        if missing_files:
            print(f"  {Color.fail(f'{len(missing_files)} missing file(s) referenced in MASTER_INDEX.txt')}")
            for m in missing_files:
                print(f"       {Color.fail('•')} {m}")
        else:
            print(f"  {Color.ok('MASTER_INDEX.txt references valid files')}")

    return {
        "missing_files": missing_files,
        "files_not_in_index": files_not_in_index,
    }


# ── Report Section Builders ───────────────────────────────────────────────────
def build_overview_section(fd, summary):
    lines = []
    lines.append("═══════════════════════════════════════════════════════════════════════════════")
    lines.append("1. OVERVIEW")
    lines.append("═══════════════════════════════════════════════════════════════════════════════")
    lines.append("")
    lines.append(f"  Total Files: {fd['total_files']}")
    lines.append(f"  Total Size:  {format_size(fd['total_size'])}")
    lines.append("")
    lines.append(f"  HTML Files:  {fd['ext_counts'].get('.html', 0)}")
    lines.append(f"  Python Files: {fd['ext_counts'].get('.py', 0)}")
    lines.append(f"  CSV Files:   {fd['ext_counts'].get('.csv', 0)}")
    lines.append(f"  TXT Files:   {fd['ext_counts'].get('.txt', 0)}")
    lines.append(f"  JSON Files:  {fd['ext_counts'].get('.json', 0)}")
    lines.append(f"  SVG Files:   {fd['ext_counts'].get('.svg', 0)}")
    lines.append(f"  XLSX Files:  {fd['ext_counts'].get('.xlsx', 0)}")
    lines.append(f"  BAT Files:   {fd['ext_counts'].get('.bat', 0)}")
    # Other
    other_exts = [k for k in fd['ext_counts'] if k not in ('.html','.py','.csv','.txt','.json','.svg','.xlsx','.bat')]
    other_total = sum(fd['ext_counts'][k] for k in other_exts)
    if other_total:
        lines.append(f"  Other:       {other_total} files ({', '.join(e.strip('.') for e in other_exts)})")
    lines.append("")
    return lines


def build_html_section(html_results):
    lines = []
    lines.append("═══════════════════════════════════════════════════════════════════════════════")
    lines.append("3. HTML VALIDATION")
    lines.append("═══════════════════════════════════════════════════════════════════════════════")
    lines.append("")

    for hr in html_results:
        issues = []
        status = "PASS"
        if not hr["has_doctype"]:
            issues.append("Missing DOCTYPE")
            status = "FAIL"
        if not hr["has_viewport"]:
            issues.append("Missing viewport meta")
            status = "FAIL"
        for (ot, ct), state in hr["tag_pairs"].items():
            if not state["open"]:
                issues.append(f"Missing <{ot}>")
                status = "FAIL"
            if not state["close"]:
                issues.append(f"Missing </{ct}>")
                status = "FAIL"
        if hr["tag_errors"]:
            issues.extend(hr["tag_errors"])
            status = "FAIL"
        if not hr["has_theme_color"]:
            issues.append("Missing theme-color meta")

        ls_keys = ", ".join(hr["localstorage_keys"]) or "(none)"
        wa_refs_list = [f"{num}x {num2}" for num2, num in hr["whatsapp_refs"]] or ["(none)"]
        wa_str = "; ".join(wa_refs_list)
        int_links = len(hr["internal_links"])

        lines.append(f"  [{status}] {hr['path']}")
        lines.append(f"         DOCTYPE:    {'✓' if hr['has_doctype'] else '✗'}")
        lines.append(f"         Viewport:   {'✓' if hr['has_viewport'] else '✗'}")
        lines.append(f"         Theme-Color: {'✓' if hr['has_theme_color'] else '✗'}")

        tag_str_parts = []
        for (ot, ct), st in hr["tag_pairs"].items():
            chk = chr(10003) if st["open"] and st["close"] else chr(10007)
            tag_str_parts.append(f"{ot}/{ct}={chk}")
        lines.append(f"         Tag Pairs:  {', '.join(tag_str_parts)}")
        lines.append(f"         localStorage: {ls_keys}")
        lines.append(f"         WhatsApp:    {wa_str}")
        lines.append(f"         Internal Links: {int_links}")
        if issues:
            lines.append(f"         ISSUES:")
            for iss in issues[:10]:
                lines.append(f"           • {iss}")
            if len(issues) > 10:
                lines.append(f"           … and {len(issues) - 10} more")
        lines.append("")

    return lines


def build_python_section(py_results):
    lines = []
    lines.append("═══════════════════════════════════════════════════════════════════════════════")
    lines.append("4. PYTHON VALIDATION")
    lines.append("═══════════════════════════════════════════════════════════════════════════════")
    lines.append("")

    for pr in py_results:
        ok = pr["syntax_ok"] and pr["has_shebang"] and pr["has_docstring"]
        status = "PASS" if ok else "FAIL"
        lines.append(f"  [{status}] {pr['path']}")
        lines.append(f"         Shebang:    {'✓' if pr['has_shebang'] else '✗'}")
        lines.append(f"         Docstring:  {'✓' if pr['has_docstring'] else '✗'}")
        if pr["syntax_ok"]:
            lines.append(f"         Syntax:     ✓")
        else:
            lines.append(f"         Syntax:     ✗ ({pr['syntax_error']})")
        lines.append("")

    return lines


def build_crossref_section(cr):
    lines = []
    lines.append("═══════════════════════════════════════════════════════════════════════════════")
    lines.append("5. CROSS-REFERENCE CHECKS")
    lines.append("═══════════════════════════════════════════════════════════════════════════════")
    lines.append("")

    # MASTER_INDEX
    mi = cr.get("master_index", {})
    lines.append("  5a. MASTER_INDEX.txt References")
    lines.append("  " + "─" * 50)
    lines.append(f"      Files referenced: {len(mi.get('referenced', []))}")
    if mi.get("missing_files"):
        lines.append(f"      MISSING files referenced:")
        for m in mi["missing_files"]:
            lines.append(f"        ✗ {m}")
    else:
        lines.append("      All referenced files exist ✓")
    if mi.get("files_not_in_index"):
        lines.append(f"      Files not listed in MASTER_INDEX:")
        for f in mi["files_not_in_index"][:20]:
            lines.append(f"        • {f}")
        if len(mi["files_not_in_index"]) > 20:
            lines.append(f"        … and {len(mi['files_not_in_index']) - 20} more")
    else:
        lines.append("      All files covered by MASTER_INDEX ✓")
    lines.append("")

    # README
    rd = cr.get("readme", {})
    lines.append("  5b. README.txt References")
    lines.append("  " + "─" * 50)
    lines.append(f"      Files referenced: {len(rd.get('referenced', []))}")
    if rd.get("missing"):
        lines.append(f"      MISSING references:")
        for m in rd["missing"]:
            lines.append(f"        ✗ {m}")
    else:
        lines.append("      All referenced files exist ✓")
    lines.append("")

    # index.html
    ix = cr.get("index_html", {})
    lines.append("  5c. index.html (Command Center) References")
    lines.append("  " + "─" * 50)
    lines.append(f"      Files referenced: {len(ix.get('referenced', []))}")
    if ix.get("missing"):
        lines.append(f"      MISSING references:")
        for m in ix["missing"]:
            lines.append(f"        ✗ {m}")
    else:
        lines.append("      All referenced files exist ✓")
    lines.append("")

    return lines


def build_ls_section(html_results, summary):
    lines = []
    lines.append("═══════════════════════════════════════════════════════════════════════════════")
    lines.append("6. LOCALSTORAGE KEYS ACROSS ALL HTML FILES")
    lines.append("═══════════════════════════════════════════════════════════════════════════════")
    lines.append("")

    all_ls = summary["localstorage_keys"]
    if all_ls:
        lines.append(f"  Total unique localStorage keys: {len(all_ls)}")
        lines.append("")
        for key in all_ls:
            files_using = []
            for hr in html_results:
                if key in hr["localstorage_keys"]:
                    files_using.append(str(hr["path"]))
            lines.append(f"  • {key}")
            for fu in files_using:
                lines.append(f"      → {fu}")
    else:
        lines.append("  No localStorage keys found.")
    lines.append("")

    return lines


def build_final_summary(s):
    lines = []
    lines.append("═══════════════════════════════════════════════════════════════════════════════")
    lines.append("7. FINAL SUMMARY")
    lines.append("═══════════════════════════════════════════════════════════════════════════════")
    lines.append("")

    lines.append(f"  Files Checked:        {s['total_files']}")
    lines.append(f"  Total Size:           {format_size(s['total_size'])}")
    lines.append("")

    if s["html_total"] > 0:
        lines.append(f"  HTML Valid:           {s['html_ok']}/{s['html_total']}")
        lines.append(f"  HTML With Issues:     {s['html_fail']}")
        if s["missing_doctype"]:
            lines.append(f"  Missing DOCTYPE:      {len(s['missing_doctype'])}")
            for md in s["missing_doctype"]:
                lines.append(f"                          • {md}")
        if s["missing_viewport"]:
            lines.append(f"  Missing Viewport:     {len(s['missing_viewport'])}")
            for mv in s["missing_viewport"]:
                lines.append(f"                          • {mv}")
    else:
        lines.append("  HTML:                 No HTML files checked")

    if s["python_total"] > 0:
        lines.append(f"  Python Valid:         {s['python_ok']}/{s['python_total']}")
        lines.append(f"  Python Warnings:      {s['python_warn']}")
        lines.append(f"  Python Failed:        {s['python_fail']}")
    else:
        lines.append("  Python:               No Python files checked")

    lines.append("")
    lines.append("  Cross-References:")
    lines.append(f"    MASTER_INDEX:       {len(s['master_missing_files'])} missing refs, "
                 f"{len(s['master_files_not_in_index'])} files not indexed")
    lines.append(f"    README:             {len(s['readme_missing'])} broken references")
    lines.append(f"    Command Center:     {len(s['index_missing'])} broken references")
    lines.append("")
    lines.append(f"  localStorage Keys:    {s['localstorage_key_count']} unique keys")
    lines.append("")

    total_issues = (
        s["html_fail"]
        + s["python_fail"]
        + len(s["master_missing_files"])
        + len(s["readme_missing"])
        + len(s["index_missing"])
    )
    if total_issues == 0:
        lines.append(f"  ╔══════════════════════════════════════════════════╗")
        lines.append(f"  ║  ALL CHECKS PASSED                              ║")
        lines.append(f"  ╚══════════════════════════════════════════════════╝")
    else:
        total_issues_str = f"{total_issues} ISSUE(S) FOUND — SEE DETAILS ABOVE"
        lines.append(f"  ╔══════════════════════════════════════════════════╗")
        lines.append(f"  ║  {total_issues_str:<46}║")
        lines.append(f"  ╚══════════════════════════════════════════════════╝")

    lines.append("")
    lines.append("═══════════════════════════════════════════════════════════════════════════════")
    lines.append("")
    lines.append("Document Owner: Fahad Ibrahim")
    lines.append(f"Version: Auto-Validation | "
                 f"{__import__('datetime').datetime.now().strftime('%B %Y')}")
    lines.append("")
    lines.append("Never GIVE UP on your HOPES.")
    lines.append("")

    return lines


# ── Print helpers ─────────────────────────────────────────────────────────────
def print_html_result(hr):
    path_str = str(hr["path"])
    issues = []

    if not hr["has_doctype"]:
        issues.append("Missing DOCTYPE")
    if not hr["has_viewport"]:
        issues.append("Missing viewport meta")
    if not hr["has_theme_color"]:
        issues.append("Missing theme-color meta")

    for (ot, ct), state in hr["tag_pairs"].items():
        if not state["open"]:
            issues.append(f"Missing <{ot}>")
        if not state["close"]:
            issues.append(f"Missing </{ct}>")

    if hr["tag_errors"]:
        for err in hr["tag_errors"]:
            issues.append(err.strip())

    ls_count = len(hr["localstorage_keys"])
    link_count = len(hr["internal_links"])
    wa_count = sum(c for _, c in hr["whatsapp_refs"])

    status = Color.ok("OK") if not issues else Color.fail("FAIL")
    details = []
    if ls_count:
        details.append(f"lsKeys={ls_count}")
    if link_count:
        details.append(f"links={link_count}")
    if wa_count:
        details.append(f"WArefs={wa_count}")

    detail_str = f" [{', '.join(details)}]" if details else ""
    print(f"  {status} {path_str}{detail_str}")
    if issues:
        for iss in issues[:5]:
            print(f"       {Color.fail('•')} {iss}")
        if len(issues) > 5:
            print(f"       {Color.warn(f'… and {len(issues) - 5} more issues')}")


def print_python_result(pr):
    path_str = str(pr["path"])
    issues = []
    if not pr["has_shebang"]:
        issues.append("Missing shebang")
    if not pr["has_docstring"]:
        issues.append("Missing docstring")

    if pr["syntax_ok"] and not issues:
        print(f"  {Color.ok('OK')} {path_str}")
        print(f"       {Color.ok('Shebang + Docstring + Syntax OK')}")
    elif pr["syntax_ok"]:
        print(f"  {Color.warn('WARN')} {path_str}")
        if not pr["has_shebang"]:
            print(f"       {Color.warn('•')} Missing shebang line")
        if not pr["has_docstring"]:
            print(f"       {Color.warn('•')} Missing module docstring")
    else:
        print(f"  {Color.fail('FAIL')} {path_str}")
        print(f"       {Color.fail('•')} {pr['syntax_error']}")


def print_summary(s):
    print(f"  {Color.BOLD}FINAL RESULTS{Color.RESET}")
    print(f"  {'─' * 50}")

    print(f"  {Color.info('Files:')}       {s['total_files']} total, {format_size(s['total_size'])}")

    if s["html_total"] > 0:
        html_ok_val = s["html_ok"]
        html_total_val = s["html_total"]
        if s["html_fail"] == 0:
            print(f"  {Color.ok(f'HTML: {html_ok_val}/{html_total_val} passed')}")
        else:
            html_fail_val = s["html_fail"]
            print(f"  {Color.fail(f'HTML: {html_ok_val}/{html_total_val} passed, {html_fail_val} with issues')}")
    else:
        print(f"  {Color.warn('HTML: No HTML files checked')}")

    if s["python_total"] > 0:
        py_ok_val = s["python_ok"]
        py_warn_val = s["python_warn"]
        py_fail_val = s["python_fail"]
        py_total_val = s["python_total"]
        parts = [f"{Color.ok(str(py_ok_val))} passed"]
        if py_warn_val:
            parts.append(f"{Color.warn(str(py_warn_val))} warnings")
        if py_fail_val:
            parts.append(f"{Color.fail(str(py_fail_val))} failed")
        print(f"  {Color.info('Python:')}    {', '.join(parts)}/{py_total_val}")
    else:
        print(f"  {Color.warn('Python: No Python files checked')}")

    if s["localstorage_key_count"] > 0:
        print(f"  {Color.info('localStorage:')} {s['localstorage_key_count']} unique keys found")

    if s["missing_doctype"]:
        missing_dt_val = len(s["missing_doctype"])
        print(f"  {Color.fail(f'DOCTYPE: {missing_dt_val} file(s) missing')}")
    if s["missing_viewport"]:
        missing_vp_val = len(s["missing_viewport"])
        print(f"  {Color.fail(f'Viewport: {missing_vp_val} file(s) missing')}")

    cr_parts = []
    if s["master_missing_files"]:
        cr_parts.append(f"MASTER_INDEX missing {len(s['master_missing_files'])} files")
    if s["master_files_not_in_index"]:
        cr_parts.append(f"{len(s['master_files_not_in_index'])} files not in MASTER_INDEX")
    if s["readme_missing"]:
        cr_parts.append(f"README missing {len(s['readme_missing'])} refs")
    if s["index_missing"]:
        cr_parts.append(f"index.html missing {len(s['index_missing'])} refs")

    if cr_parts:
        print(f"  {Color.warn('Cross-refs:')} {'; '.join(cr_parts)}")
    else:
        print(f"  {Color.ok('Cross-refs: All references validated')}")


# ── Utility ───────────────────────────────────────────────────────────────────
def format_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 ** 2:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / 1024 ** 2:.2f} MB"


# ── Summary Builder ───────────────────────────────────────────────────────────
def build_summary(results):
    s = {}
    fd = results["file_discovery"]
    s["total_files"] = fd["total_files"]
    s["total_size"] = fd["total_size"]
    s["ext_counts"] = fd["ext_counts"]

    html_ok = 0
    html_fail = 0
    all_ls_keys = set()
    missing_doctype_list = []
    missing_viewport_list = []

    for hr in results.get("html_results", []):
        issues = 0
        if not hr["has_doctype"]:
            issues += 1
            missing_doctype_list.append(str(hr["path"]))
        if not hr["has_viewport"]:
            issues += 1
            missing_viewport_list.append(str(hr["path"]))
        for (ot, ct), state in hr["tag_pairs"].items():
            if not state["open"] or not state["close"]:
                issues += 1
        if hr["tag_errors"]:
            issues += len(hr["tag_errors"])
        if issues:
            html_fail += 1
        else:
            html_ok += 1
        all_ls_keys.update(hr["localstorage_keys"])

    s["html_ok"] = html_ok
    s["html_fail"] = html_fail
    s["html_total"] = len(results.get("html_results", []))
    s["localstorage_keys"] = sorted(all_ls_keys)
    s["localstorage_key_count"] = len(all_ls_keys)
    s["missing_doctype"] = missing_doctype_list
    s["missing_viewport"] = missing_viewport_list

    py_ok = 0
    py_fail = 0
    py_warn = 0
    for pr in results.get("python_results", []):
        if pr["syntax_ok"] and pr["has_shebang"] and pr["has_docstring"]:
            py_ok += 1
        elif not pr["syntax_ok"]:
            py_fail += 1
        else:
            py_warn += 1
    s["python_ok"] = py_ok
    s["python_fail"] = py_fail
    s["python_warn"] = py_warn
    s["python_total"] = len(results.get("python_results", []))

    cr = results.get("cross_refs", {})
    s["master_missing_files"] = cr.get("master_index", {}).get("missing_files", [])
    s["master_files_not_in_index"] = cr.get("master_index", {}).get("files_not_in_index", [])
    s["readme_missing"] = cr.get("readme", {}).get("missing", [])
    s["index_missing"] = cr.get("index_html", {}).get("missing", [])

    return s


# ── Generate VALIDATION_REPORT.txt ────────────────────────────────────────────
def generate_report(results):
    fd = results["file_discovery"]
    summary = results["summary"]
    html_results = results.get("html_results", [])
    py_results = results.get("python_results", [])
    cr = results.get("cross_refs", {})

    now_str = __import__("datetime").datetime.now().strftime("%A, %B %d, %Y at %H:%M")

    lines = []
    lines.append("╔═══════════════════════════════════════════════════════════════════════════════╗")
    lines.append("║          JG MART — TOOLKIT VALIDATION REPORT (Auto-Generated)                ║")
    lines.append("╚═══════════════════════════════════════════════════════════════════════════════╝")
    lines.append("")
    lines.append(f"Generated: {now_str}")
    lines.append(f"Toolkit Path: {TOOLKIT_DIR}")
    lines.append("")

    lines.extend(build_overview_section(fd, summary))
    lines.extend(build_html_section(html_results))
    lines.extend(build_python_section(py_results))
    lines.extend(build_crossref_section(cr))
    lines.extend(build_ls_section(html_results, summary))
    lines.extend(build_final_summary(summary))

    return "\n".join(lines)


# ── Main Pipeline ─────────────────────────────────────────────────────────────
def run_validation(opts):
    toolkit_dir = TOOLKIT_DIR
    print(f"\n{Color.header('═' * 60)}")
    print(f"{Color.header('  JG MART — TOOLKIT AUTO-VALIDATION')}")
    print(f"{Color.header(f'  Toolkit: {toolkit_dir}')}")
    print(f"{Color.header('═' * 60)}\n")

    # ── Phase 1: File Discovery ───────────────────────────────────────────────
    print(f"{Color.header('▶ Phase 1: File Discovery')}")
    all_files, by_type, ext_counts, total_size = discover_files(toolkit_dir)

    fd = {
        "all_files": all_files,
        "by_type": dict(by_type),
        "ext_counts": dict(ext_counts),
        "total_size": total_size,
        "total_files": len(all_files),
    }

    type_summary_parts = []
    for ext in sorted(ext_counts, key=lambda e: -ext_counts[e]):
        type_summary_parts.append(f"{ext.upper().lstrip('.') or 'NO_EXT'}: {ext_counts[ext]}")
    print(f"  {Color.info('Total files:')} {len(all_files)}")
    print(f"  {Color.info('Total size:')}  {format_size(total_size)}")
    print(f"  {Color.info('By type:')}     {', '.join(type_summary_parts[:8])}"
          f"{' …' if len(type_summary_parts) > 8 else ''}")

    html_files = by_type.get(".html", [])
    py_files = by_type.get(".py", [])
    print(f"  {Color.info('HTML files:')}  {len(html_files)}")
    print(f"  {Color.info('Python files:')} {len(py_files)}\n")

    # ── Phase 2: HTML Validation ──────────────────────────────────────────────
    print(f"{Color.header('▶ Phase 2: HTML Validation')}")
    html_results = []
    if not opts.get("python_only"):
        for rel in html_files:
            abs_path = toolkit_dir / rel
            hr = check_html_file(rel, abs_path)
            html_results.append(hr)
            print_html_result(hr)
    else:
        print(f"  {Color.info('Skipped (--python-only)')}")
    print()

    # ── Phase 3: Python Validation ────────────────────────────────────────────
    print(f"{Color.header('▶ Phase 3: Python Validation')}")
    py_results = []
    if not opts.get("html_only"):
        for rel in py_files:
            abs_path = toolkit_dir / rel
            pr = check_python_file(rel, abs_path)
            py_results.append(pr)
            print_python_result(pr)
    else:
        print(f"  {Color.info('Skipped (--html-only)')}")
    print()

    # ── Phase 4: Cross-Reference Checks ───────────────────────────────────────
    print(f"{Color.header('▶ Phase 4: Cross-Reference Validation')}")
    cross_refs = {}
    if not opts.get("html_only") and not opts.get("python_only"):
        all_file_set = set(all_files)

        # MASTER_INDEX.txt
        mi_path = toolkit_dir / "MASTER_INDEX.txt"
        if mi_path.exists():
            mi_text = mi_path.read_text(encoding="utf-8", errors="replace")
            mi_refs = parse_master_index(mi_text)
            mi_result = check_master_index_coverage(all_files, mi_refs, toolkit_dir)
            cross_refs["master_index"] = {
                "referenced": sorted(mi_refs),
                "missing_files": mi_result["missing_files"],
                "files_not_in_index": mi_result["files_not_in_index"],
            }
        else:
            print(f"  {Color.fail('MASTER_INDEX.txt not found')}")
            cross_refs["master_index"] = {"referenced": [], "missing_files": [], "files_not_in_index": []}

        # README.txt
        readme_path = toolkit_dir / "README.txt"
        if readme_path.exists():
            readme_text = readme_path.read_text(encoding="utf-8", errors="replace")
            readme_refs = parse_readme_file_list(readme_text)
            readme_missing = check_references_exist(readme_refs, all_file_set, toolkit_dir, "README.txt")
            cross_refs["readme"] = {
                "referenced": sorted(readme_refs),
                "missing": readme_missing,
            }
        else:
            print(f"  {Color.fail('README.txt not found')}")
            cross_refs["readme"] = {"referenced": [], "missing": []}

        # index.html (Command Center)
        index_path = toolkit_dir / "index.html"
        if index_path.exists():
            index_text = index_path.read_text(encoding="utf-8", errors="replace")
            index_refs = parse_index_html_refs(index_text)
            index_missing = check_references_exist(index_refs, all_file_set, toolkit_dir, "index.html")
            cross_refs["index_html"] = {
                "referenced": sorted(index_refs),
                "missing": index_missing,
            }
        else:
            print(f"  {Color.fail('index.html not found')}")
            cross_refs["index_html"] = {"referenced": [], "missing": []}
    else:
        print(f"  {Color.info('Skipped (--html-only or --python-only)')}")
    print()

    # ── Phase 5: Summary ──────────────────────────────────────────────────────
    print(f"{Color.header('▶ Phase 5: Summary & Report')}")

    results = {
        "file_discovery": fd,
        "html_results": html_results,
        "python_results": py_results,
        "cross_refs": cross_refs,
    }
    summary = build_summary(results)
    results["summary"] = summary
    print_summary(summary)
    print()

    # Generate report
    report_text = generate_report(results)
    REPORT_PATH.write_text(report_text, encoding="utf-8")
    print(f"  {Color.ok(f'Report written to {REPORT_PATH}')}")
    print(f"  {Color.info(f'Report size: {len(report_text):,} chars')}\n")

    return results


# ── CLI Entry Point ───────────────────────────────────────────────────────────
def main():
    opts = {
        "html_only": "--html-only" in sys.argv,
        "python_only": "--python-only" in sys.argv,
        "cross_refs_only": "--cross-refs-only" in sys.argv,
        "quiet": "--quiet" in sys.argv,
    }

    try:
        run_validation(opts)
    except KeyboardInterrupt:
        print(f"\n  {Color.warn('Validation interrupted by user')}")
        sys.exit(1)
    except Exception as e:
        print(f"\n  {Color.fail(f'Validation error: {e}')}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
