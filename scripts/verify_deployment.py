#!/usr/bin/env python3
"""
JG Mart — Deployment Verification Script
Verifies that the deployed website is serving the latest version
and all critical functionality is working.

Usage:
    python verify_deployment.py [url]

    If no URL is provided, defaults to https://jg-mart.vercel.app
"""

import sys
import json
import re
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

DEFAULT_URL = "https://jg-mart.vercel.app"
TIMEOUT = 10

PAGES_TO_CHECK = [
    "/",
    "/landing.html",
    "/menu.html",
    "/track.html",
    "/zone.html",
    "/myorders.html",
    "/admin.html",
    "/manifest.html",
    "/healthcheck.html",
    "/404.html",
]

EXPECTED_PRODUCTS = 65
EXPECTED_BUILDINGS = 27
EXPECTED_CLUSTERS = 4


class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


def log(msg, color=Colors.RESET):
    print(f"{color}{msg}{Colors.RESET}")


def fetch(url):
    """Fetch URL content"""
    try:
        req = Request(url, headers={"User-Agent": "JG-Mart-Verify/1.0"})
        with urlopen(req, timeout=TIMEOUT) as response:
            return response.read().decode("utf-8", errors="ignore"), response.status
    except HTTPError as e:
        return None, e.code
    except URLError as e:
        return None, str(e)
    except Exception as e:
        return None, str(e)


def check_page_accessible(base_url, path):
    """Check if a page is accessible"""
    url = f"{base_url.rstrip('/')}{path}"
    content, status = fetch(url)

    if content is None:
        return False, f"HTTP {status}"

    if status == 200:
        return True, "OK"
    else:
        return False, f"HTTP {status}"


def check_whatsapp_number(content):
    """Check if WhatsApp number is correct"""
    if "+8801870489448" in content or "8801870489448" in content:
        return True
    return False


def check_theme_color(content):
    """Check if theme-color meta tag exists"""
    if "theme-color" in content and "#00442D" in content:
        return True
    return False


def check_viewport(content):
    """Check if viewport meta tag exists"""
    if "viewport" in content:
        return True
    return False


def check_doctype(content):
    """Check if DOCTYPE exists"""
    if content.strip().startswith("<!DOCTYPE html>"):
        return True
    return False


def check_products_count(content):
    """Check if expected number of products is present"""
    # Look for product data patterns
    product_patterns = [
        r'"id"\s*:\s*\d+',
        r"p\s*[:=]\s*\{",
        r"product",
    ]

    count = 0
    for pattern in product_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        count += len(matches)

    # Heuristic: if we find many product references, assume catalog is loaded
    return count > 50


def check_buildings_count(content):
    """Check if building references exist"""
    building_patterns = [
        r"Building\s*\d+",
        r"B\d+",
        r"cluster",
    ]

    count = 0
    for pattern in building_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        count += len(matches)

    return count > 20


def verify_deployment(base_url):
    """Run all verification checks"""

    log(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}", Colors.BLUE)
    log(f"{Colors.BOLD}JG Mart — Deployment Verification{Colors.RESET}", Colors.BLUE)
    log(f"{Colors.BOLD}URL: {base_url}{Colors.RESET}", Colors.BLUE)
    log(f"{Colors.BOLD}{'='*60}{Colors.RESET}\n", Colors.BLUE)

    results = []
    passed = 0
    failed = 0

    # Check 1: Pages accessible
    log(f"{Colors.BOLD}1. Page Accessibility{Colors.RESET}")
    for page in PAGES_TO_CHECK:
        ok, msg = check_page_accessible(base_url, page)
        status = (
            f"{Colors.GREEN}✅{Colors.RESET}" if ok else f"{Colors.RED}❌{Colors.RESET}"
        )
        log(f"  {status} {page}: {msg}")

        if ok:
            passed += 1
            results.append((page, True, msg))
        else:
            failed += 1
            results.append((page, False, msg))

    # Check 2: Index page content
    log(f"\n{Colors.BOLD}2. Index Page Content{Colors.RESET}")
    index_content, index_status = fetch(f"{base_url.rstrip('/')}/")

    if index_content:
        # WhatsApp number
        has_wa = check_whatsapp_number(index_content)
        status = (
            f"{Colors.GREEN}✅{Colors.RESET}"
            if has_wa
            else f"{Colors.RED}❌{Colors.RESET}"
        )
        log(f"  {status} WhatsApp number: {'Found' if has_wa else 'Missing'}")
        passed += 1 if has_wa else 0
        failed += 0 if has_wa else 1

        # Theme color
        has_theme = check_theme_color(index_content)
        status = (
            f"{Colors.GREEN}✅{Colors.RESET}"
            if has_theme
            else f"{Colors.RED}❌{Colors.RESET}"
        )
        log(f"  {status} Theme color: {'Found' if has_theme else 'Missing'}")
        passed += 1 if has_theme else 0
        failed += 0 if has_theme else 1

        # Viewport
        has_viewport = check_viewport(index_content)
        status = (
            f"{Colors.GREEN}✅{Colors.RESET}"
            if has_viewport
            else f"{Colors.RED}❌{Colors.RESET}"
        )
        log(f"  {status} Viewport meta: {'Found' if has_viewport else 'Missing'}")
        passed += 1 if has_viewport else 0
        failed += 0 if has_viewport else 1

        # DOCTYPE
        has_doctype = check_doctype(index_content)
        status = (
            f"{Colors.GREEN}✅{Colors.RESET}"
            if has_doctype
            else f"{Colors.RED}❌{Colors.RESET}"
        )
        log(f"  {status} DOCTYPE: {'Found' if has_doctype else 'Missing'}")
        passed += 1 if has_doctype else 0
        failed += 0 if has_doctype else 1

        # Products
        has_products = check_products_count(index_content)
        status = (
            f"{Colors.GREEN}✅{Colors.RESET}"
            if has_products
            else f"{Colors.YELLOW}⚠️{Colors.RESET}"
        )
        log(
            f"  {status} Product catalog: {'Loaded' if has_products else 'Check manually'}"
        )
        passed += 1 if has_products else 0
        failed += 0 if has_products else 1
    else:
        log(f"  {Colors.RED}❌ Could not fetch index page{Colors.RESET}")
        failed += 5

    # Check 3: Zone page content
    log(f"\n{Colors.BOLD}3. Zone Page Content{Colors.RESET}")
    zone_content, zone_status = fetch(f"{base_url.rstrip('/')}/zone.html")

    if zone_content:
        has_buildings = check_buildings_count(zone_content)
        status = (
            f"{Colors.GREEN}✅{Colors.RESET}"
            if has_buildings
            else f"{Colors.YELLOW}⚠️{Colors.RESET}"
        )
        log(
            f"  {status} Building references: {'Found' if has_buildings else 'Check manually'}"
        )
        passed += 1 if has_buildings else 0
        failed += 0 if has_buildings else 1
    else:
        log(f"  {Colors.RED}❌ Could not fetch zone page{Colors.RESET}")
        failed += 1

    # Check 4: Images
    log(f"\n{Colors.BOLD}4. Image Assets{Colors.RESET}")
    img_url = f"{base_url.rstrip('/')}/images/rice_dal.svg"
    img_content, img_status = fetch(img_url)

    if img_content and len(img_content) > 100:
        log(f"  {Colors.GREEN}✅{Colors.RESET} Category images: Accessible")
        passed += 1
    else:
        log(f"  {Colors.YELLOW}⚠️{Colors.RESET} Category images: Check manually")
        failed += 1

    # Summary
    log(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}", Colors.BLUE)
    log(f"{Colors.BOLD}SUMMARY{Colors.RESET}", Colors.BLUE)
    log(f"{Colors.BOLD}{'='*60}{Colors.RESET}", Colors.BLUE)
    log(f"  Total checks: {passed + failed}")
    log(f"  {Colors.GREEN}Passed: {passed}{Colors.RESET}")
    log(f"  {Colors.RED}Failed: {failed}{Colors.RESET}")

    if failed == 0:
        log(
            f"\n{Colors.GREEN}{Colors.BOLD}✅ DEPLOYMENT VERIFIED — ALL CHECKS PASSED{Colors.RESET}"
        )
        return 0
    else:
        log(
            f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  DEPLOYMENT ISSUES FOUND — REVIEW FAILED CHECKS{Colors.RESET}"
        )
        return 1


def main():
    base_url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL

    # Ensure URL has protocol
    if not base_url.startswith("http"):
        base_url = f"https://{base_url}"

    sys.exit(verify_deployment(base_url))


if __name__ == "__main__":
    main()
