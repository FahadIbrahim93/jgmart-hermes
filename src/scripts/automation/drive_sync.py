#!/usr/bin/env python3
"""
JG Mart → Google Drive Sync Script
=====================================
Syncs the entire JG Mart - Hermes toolkit to Google Drive using rclone.

REQUIREMENTS:
    pip install rclone  (or: scoop install rclone / apt install rclone)

FIRST-TIME SETUP:
    1. Open terminal as administrator
    2. Run: rclone config
    3. Choose 'n' for new remote
    4. Name: 'jgmart-drive'
    5. Choose 'drive' for Google Drive
    6. Follow OAuth prompt (opens browser, login with your Google account)
    7. Leave everything default, choose 'y' for auto config
    8. Done.

USAGE:
    python drive_sync.py --upload      # Upload local → Google Drive
    python drive_sync.py --download    # Download Google Drive → local
    python drive_sync.py --status      # Check sync status
    python drive_sync.py --watch       # Continuous sync (every 5 min)
"""

import os
import sys
import subprocess
import time
from datetime import datetime
from pathlib import Path

# ─── CONFIG ───────────────────────────────────────────────────────────
LOCAL_DIR = Path(__file__).parent.resolve()
RCLONE_REMOTE = "jgmart-drive"
DRIVE_PATH = "JG Mart/JGC Mart - Hermes"
EXCLUDE = [
    "*.pyc",
    "__pycache__/",
    ".git/",
    "node_modules/",
    "launch_outputs/*.txt",  # Generated files, don't need backup
]
# ──────────────────────────────────────────────────────────────────────


def check_rclone():
    """Verify rclone is installed."""
    try:
        subprocess.run(["rclone", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.FileNotFoundError, subprocess.CalledProcessError):
        return False


def check_remote():
    """Check if the remote is configured."""
    result = subprocess.run(
        ["rclone", "listremotes"], capture_output=True, text=True
    )
    return RCLONE_REMOTE in result.stdout


def build_exclude_flags():
    flags = []
    for pattern in EXCLUDE:
        flags.extend(["--exclude", pattern])
    return flags


def sync_upload(dry_run=False):
    """Upload local changes to Google Drive."""
    cmd = [
        "rclone", "sync",
        str(LOCAL_DIR),
        f"{RCLONE_REMOTE}:{DRIVE_PATH}",
        "--progress",
        "--verbose",
        "--create-empty-dirs",
    ]
    if dry_run:
        cmd.append("--dry-run")
    cmd.extend(build_exclude_flags())

    print(f"\n{'='*60}")
    print(f"📤 SYNC: Local → Google Drive")
    print(f"   Local:  {LOCAL_DIR}")
    print(f"   Drive:  {RCLONE_REMOTE}:{DRIVE_PATH}")
    if dry_run:
        print(f"   Mode:   DRY RUN (no changes made)")
    print(f"{'='*60}\n")

    result = subprocess.run(cmd)
    if result.returncode == 0:
        print(f"\n✅ Sync complete at {datetime.now().strftime('%H:%M:%S')}")
    else:
        print(f"\n❌ Sync failed with code {result.returncode}")
    return result.returncode


def sync_download(dry_run=False):
    """Download Google Drive changes to local."""
    cmd = [
        "rclone", "sync",
        f"{RCLONE_REMOTE}:{DRIVE_PATH}",
        str(LOCAL_DIR),
        "--progress",
        "--verbose",
        "--create-empty-dirs",
    ]
    if dry_run:
        cmd.append("--dry-run")
    cmd.extend(build_exclude_flags())

    print(f"\n{'='*60}")
    print(f"📥 SYNC: Google Drive → Local")
    print(f"   Drive:  {RCLONE_REMOTE}:{DRIVE_PATH}")
    print(f"   Local:  {LOCAL_DIR}")
    if dry_run:
        print(f"   Mode:   DRY RUN (no changes made)")
    print(f"{'='*60}\n")

    result = subprocess.run(cmd)
    if result.returncode == 0:
        print(f"\n✅ Download complete at {datetime.now().strftime('%H:%M:%S')}")
    else:
        print(f"\n❌ Download failed with code {result.returncode}")
    return result.returncode


def show_status():
    """Show sync status: what differs between local and Drive."""
    cmd = [
        "rclone", "check",
        str(LOCAL_DIR),
        f"{RCLONE_REMOTE}:{DRIVE_PATH}",
        "--verbose",
    ]
    cmd.extend(build_exclude_flags())

    print(f"\n{'='*60}")
    print(f"📊 SYNC STATUS")
    print(f"{'='*60}\n")
    print("Comparing local ↔ Google Drive...\n")

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ Local and Drive are IN SYNC")
    else:
        print("⚠️  Differences found:")
        print(result.stdout[-2000:] if result.stdout else "  (check verbose output)")
    print(f"\nLast check: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


def watch_loop(interval=300):
    """Continuously sync every N seconds."""
    print(f"\n{'='*60}")
    print(f"👀 WATCH MODE — Syncing every {interval}s")
    print(f"   Press Ctrl+C to stop")
    print(f"{'='*60}\n")

    try:
        while True:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{now}] Syncing...", end=" ", flush=True)
            code = sync_upload()
            status = "✅" if code == 0 else "❌"
            print(f" {status}")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n\n🛑 Watch mode stopped.")


def setup_guide():
    """Print setup instructions."""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║           JG MART — GOOGLE DRIVE SYNC SETUP GUIDE                   ║
╚══════════════════════════════════════════════════════════════════════╝

STEP 1: Install rclone
────────────────────────────────────────────────────────────────────
  Windows (PowerShell as Admin):
    winget install rclone

  OR download from: https://rclone.org/downloads/

STEP 2: Configure Google Drive remote
────────────────────────────────────────────────────────────────────
  Open terminal/command prompt and run:
    rclone config

  Follow the prompts:
    n) New remote
    Name: jgmart-drive
    Type: drive (Google Drive)
    Client ID: (press Enter for default)
    Client Secret: (press Enter for default)
    Scope: 1 (Full access)
    Root Folder ID: (press Enter for default)
    Service Account File: (press Enter)
    Advanced config: n
    Auto config: y  (opens browser to login)
    ✅ Configure this as a team drive: n
    q) Quit config

STEP 3: Test the connection
────────────────────────────────────────────────────────────────────
    rclone ls jgmart-drive:

STEP 4: Run the sync
────────────────────────────────────────────────────────────────────
    python drive_sync.py --dry-run    # Preview changes
    python drive_sync.py --upload     # Upload everything
    python drive_sync.py --watch      # Keep syncing

TIPS:
  • Run --dry-run first to see what would change
  • Use --watch for continuous backup while working
  • Excluded files: __pycache__, .git, generated launch_outputs
    """)


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python drive_sync.py --upload     Upload local → Drive")
        print("  python drive_sync.py --download   Download Drive → local")
        print("  python drive_sync.py --dry-run    Preview upload changes")
        print("  python drive_sync.py --status     Check sync status")
        print("  python drive_sync.py --watch      Continuous sync (every 5 min)")
        print("  python drive_sync.py --setup      Show detailed setup guide")
        sys.exit(1)

    if not check_rclone():
        print("❌ rclone not found. Install it first:")
        print("   Windows: winget install rclone")
        print("   Or: python drive_sync.py --setup")
        sys.exit(1)

    if not check_remote():
        print(f"❌ Remote '{RCLONE_REMOTE}' not configured.")
        print("   Run: rclone config  (then create a new drive remote)")
        print("   Or: python drive_sync.py --setup")
        sys.exit(1)

    arg = sys.argv[1]
    if arg == "--upload":
        sys.exit(sync_upload(dry_run=False))
    elif arg == "--dry-run":
        sys.exit(sync_upload(dry_run=True))
    elif arg == "--download":
        sys.exit(sync_download(dry_run=False))
    elif arg == "--status":
        show_status()
    elif arg == "--watch":
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 300
        watch_loop(interval)
    elif arg == "--setup":
        setup_guide()
    else:
        print(f"Unknown option: {arg}")


if __name__ == "__main__":
    main()
