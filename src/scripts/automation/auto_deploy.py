#!/usr/bin/env python3
"""
JG Mart — Auto-Deploy Script
=============================
One-command deploy of web apps to Vercel or Netlify.

USAGE:
    python auto_deploy.py --dashboard --vercel    # Deploy dashboard to Vercel
    python auto_deploy.py --catalog --netlify     # Deploy catalog to Netlify
    python auto_deploy.py --all --vercel          # Deploy everything to Vercel
    python auto_deploy.py --list                  # Show what can be deployed
    python auto_deploy.py --setup                 # Install deploy tools
"""

import os
import sys
import subprocess
import shutil
import tempfile
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

APPS = {
    "dashboard": {
        "dir": BASE_DIR / "05_Tech_Dashboard",
        "files": ["index.html", "README.txt", "sample_data.json"],
        "description": "KPI Dashboard (Chart.js, Tailwind, localStorage)",
    },
    "catalog": {
        "dir": BASE_DIR / "06_Web_Catalog",
        "files": [
            "index.html", "catalog_data.json", "manifest.json",
            "order_intake.html", "README.txt",
        ],
        "description": "Customer Catalog + Order Intake (47 products, WhatsApp)",
    },
}


def check_vercel():
    return shutil.which("vercel") is not None


def check_netlify():
    return shutil.which("netlify") is not None


def list_apps():
    print("\n📦 JG Mart — Deployable Applications\n")
    for name, info in APPS.items():
        print(f"  {name}:")
        print(f"    📁 {info['dir'].name}/")
        print(f"    ℹ️  {info['description']}")
        print(f"    📄 Files: {', '.join(info['files'])}\n")


def setup_tools():
    print("🔧 Installing deploy tools...\n")

    if not check_vercel():
        print("  Installing Vercel CLI...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "vercel"],
            capture_output=True,
        )
        # Try npm if pip fails
        if not check_vercel():
            subprocess.run(["npm", "install", "-g", "vercel"], check=False)

    if not check_netlify():
        print("  Installing Netlify CLI...")
        subprocess.run(["npm", "install", "-g", "netlify-cli"], check=False)

    print("\n  ✅ Setup complete!")
    print("  NOTE: You still need to run `vercel login` or `netlify login` once.")


def deploy_vercel(app_name):
    info = APPS.get(app_name)
    if not info:
        print(f"❌ Unknown app: {app_name}")
        return 1

    print(f"\n{'='*60}")
    print(f"🚀 Deploying {app_name} to Vercel...")
    print(f"{'='*60}\n")

    if not check_vercel():
        print("❌ Vercel CLI not found. Run: python auto_deploy.py --setup")
        return 1

    # Create a temporary vercel.json for static deployment
    os.chdir(info["dir"])
    vercel_json = {
        "version": 2,
        "builds": [{"src": "*.html", "use": "@vercel/static"}],
        "routes": [{"src": "/(.*)", "dest": "/$1"}],
    }

    import json
    with open("vercel.json", "w") as f:
        json.dump(vercel_json, f)

    result = subprocess.run(
        ["vercel", "--prod", "--yes", "--public"],
        cwd=info["dir"],
    )

    # Clean up
    Path(info["dir"] / "vercel.json").unlink(missing_ok=True)

    if result.returncode == 0:
        print(f"\n✅ {app_name} deployed to Vercel successfully!")
    else:
        print(f"\n❌ Deployment failed (code {result.returncode})")
    return result.returncode


def deploy_netlify(app_name):
    info = APPS.get(app_name)
    if not info:
        print(f"❌ Unknown app: {app_name}")
        return 1

    print(f"\n{'='*60}")
    print(f"🚀 Deploying {app_name} to Netlify...")
    print(f"{'='*60}\n")

    if not check_netlify():
        print("❌ Netlify CLI not found.")
        print("   Run: npm install -g netlify-cli")
        print("   Then: netlify login")
        return 1

    # Create netlify.toml for static deployment
    netlify_toml = """
[build]
  publish = "."

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
"""
    with open(info["dir"] / "netlify.toml", "w") as f:
        f.write(netlify_toml)

    result = subprocess.run(
        ["netlify", "deploy", "--prod", "--dir", str(info["dir"])],
    )

    Path(info["dir"] / "netlify.toml").unlink(missing_ok=True)

    if result.returncode == 0:
        print(f"\n✅ {app_name} deployed to Netlify successfully!")
    else:
        print(f"\n❌ Deployment failed (code {result.returncode})")
    return result.returncode


def main():
    if len(sys.argv) < 2:
        print("JG Mart — Auto-Deploy Tool\n")
        print("Usage:")
        print("  python auto_deploy.py --list                List deployable apps")
        print("  python auto_deploy.py --setup               Install deploy tools")
        print("  python auto_deploy.py --dashboard --vercel  Deploy dashboard")
        print("  python auto_deploy.py --catalog --netlify   Deploy catalog")
        print("  python auto_deploy.py --all --vercel       Deploy all to Vercel")
        sys.exit(1)

    args = sys.argv[1:]
    target = None
    platform = None

    if "--setup" in args:
        setup_tools()
        return

    if "--list" in args:
        list_apps()
        return

    if "--dashboard" in args:
        target = "dashboard"
    elif "--catalog" in args:
        target = "catalog"
    elif "--all" in args:
        target = "all"

    if "--vercel" in args:
        platform = "vercel"
    elif "--netlify" in args:
        platform = "netlify"

    if not target or not platform:
        print("❌ Specify both app (--dashboard/--catalog/--all)")
        print("   and platform (--vercel/--netlify)")
        sys.exit(1)

    if target == "all":
        for app in APPS:
            if platform == "vercel":
                deploy_vercel(app)
            else:
                deploy_netlify(app)
    else:
        if platform == "vercel":
            deploy_vercel(target)
        else:
            deploy_netlify(target)


if __name__ == "__main__":
    main()
