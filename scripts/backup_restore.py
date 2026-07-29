#!/usr/bin/env python3
"""
JG Mart — Automated Backup & Restore Script
Backs up website data, localStorage exports, and critical files.
Supports timestamped backups, compression, and restore operations.

Usage:
    python backup_restore.py backup [--output-dir DIR] [--compress]
    python backup_restore.py restore --backup-file FILE [--dry-run]
    python backup_restore.py list
    python backup_restore.py verify --backup-file FILE

Examples:
    python backup_restore.py backup
    python backup_restore.py backup --output-dir ./backups --compress
    python backup_restore.py restore --backup-file backups/jgmart_backup_20260729_143022.tar.gz
    python backup_restore.py list
    python backup_restore.py verify --backup-file backups/jgmart_backup_20260729_143022.tar.gz
"""

import os
import sys
import json
import tarfile
import hashlib
import shutil
import argparse
from datetime import datetime
from pathlib import Path

# Configuration
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
BACKUP_DIR = PROJECT_ROOT / "backups"
CRITICAL_FILES = [
    "src/web/catalog/index.html",
    "src/web/catalog/admin.html",
    "src/web/catalog/images/",
    "src/web/catalog/sw.js",
    "src/web/catalog/manifest.json",
    "src/web/catalog/landing.html",
    "src/web/catalog/menu.html",
    "src/web/catalog/track.html",
    "src/web/catalog/zone.html",
    "src/web/catalog/myorders.html",
    "src/web/catalog/manifest.html",
    "src/web/catalog/healthcheck.html",
    "src/web/catalog/404.html",
    "src/web/catalog/order_intake.html",
    "src/pitch/",
    "src/launch/",
    "vercel.json",
    "netlify.toml",
    "README.md",
    "CHANGELOG.md",
]

CRITICAL_DIRS = [
    "src/web/catalog/images/",
    "src/pitch/",
    "src/launch/",
]

class BackupRestore:
    def __init__(self, output_dir=None, compress=True):
        self.output_dir = Path(output_dir) if output_dir else BACKUP_DIR
        self.compress = compress
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def get_backup_filename(self):
        """Generate backup filename with timestamp"""
        ext = "tar.gz" if self.compress else "tar"
        return f"jgmart_backup_{self.timestamp}.{ext}"
    
    def get_manifest_filename(self, backup_file):
        """Generate manifest filename for a backup"""
        return backup_file.with_suffix(backup_file.suffix + ".manifest.json")
    
    def calculate_file_hash(self, filepath):
        """Calculate SHA256 hash of a file"""
        sha256 = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except Exception as e:
            return None
    
    def create_backup(self):
        """Create a backup of critical files"""
        print(f"🔄 Creating backup...")
        print(f"   Source: {PROJECT_ROOT}")
        print(f"   Output: {self.output_dir}")
        print(f"   Timestamp: {self.timestamp}")
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        backup_file = self.output_dir / self.get_backup_filename()
        manifest = {
            "timestamp": self.timestamp,
            "created_at": datetime.now().isoformat(),
            "files": [],
            "total_files": 0,
            "total_size": 0,
            "compressed": self.compress,
        }
        
        try:
            if self.compress:
                # Create tar.gz archive
                with tarfile.open(backup_file, "w:gz") as tar:
                    for item in CRITICAL_FILES + CRITICAL_DIRS:
                        source = PROJECT_ROOT / item
                        if source.exists():
                            if source.is_file():
                                tar.add(source, arcname=item)
                                manifest["files"].append({
                                    "path": item,
                                    "type": "file",
                                    "size": source.stat().st_size,
                                    "hash": self.calculate_file_hash(source),
                                })
                                manifest["total_size"] += source.stat().st_size
                                manifest["total_files"] += 1
                                print(f"   ✅ Added: {item}")
                            elif source.is_dir():
                                for file in source.rglob("*"):
                                    if file.is_file():
                                        arcname = file.relative_to(PROJECT_ROOT)
                                        tar.add(file, arcname=arcname)
                                        manifest["files"].append({
                                            "path": str(arcname),
                                            "type": "file",
                                            "size": file.stat().st_size,
                                            "hash": self.calculate_file_hash(file),
                                        })
                                        manifest["total_size"] += file.stat().st_size
                                        manifest["total_files"] += 1
                                print(f"   ✅ Added directory: {item} ({manifest['total_files']} files)")
                        else:
                            print(f"   ⚠️  Skipped (not found): {item}")
            else:
                # Create uncompressed tar
                with tarfile.open(backup_file, "w") as tar:
                    for item in CRITICAL_FILES + CRITICAL_DIRS:
                        source = PROJECT_ROOT / item
                        if source.exists():
                            tar.add(source, arcname=item)
                            manifest["files"].append({
                                "path": item,
                                "type": "directory" if source.is_dir() else "file",
                                "size": source.stat().st_size if source.is_file() else 0,
                            })
                            manifest["total_files"] += 1
                            print(f"   ✅ Added: {item}")
                        else:
                            print(f"   ⚠️  Skipped (not found): {item}")
            
            # Save manifest
            manifest_file = self.get_manifest_filename(backup_file)
            with open(manifest_file, "w", encoding="utf-8") as f:
                json.dump(manifest, f, indent=2)
            
            # Print summary
            size_mb = manifest["total_size"] / (1024 * 1024)
            backup_size_mb = backup_file.stat().st_size / (1024 * 1024)
            
            print(f"\n✅ Backup created successfully!")
            print(f"   File: {backup_file.name}")
            print(f"   Size: {backup_size_mb:.2f} MB (compressed from {size_mb:.2f} MB)")
            print(f"   Files: {manifest['total_files']}")
            print(f"   Manifest: {manifest_file.name}")
            
            return backup_file
            
        except Exception as e:
            print(f"\n❌ Backup failed: {e}")
            return None
    
    def restore_backup(self, backup_file, dry_run=False):
        """Restore from a backup file"""
        backup_path = Path(backup_file)
        
        if not backup_path.exists():
            print(f"❌ Backup file not found: {backup_file}")
            return False
        
        print(f"🔄 Restoring from backup...")
        print(f"   Source: {backup_path.name}")
        print(f"   Target: {PROJECT_ROOT}")
        
        if dry_run:
            print(f"   ⚠️  DRY RUN — no files will be modified")
        
        try:
            # Load manifest if available
            manifest_file = self.get_manifest_filename(backup_path)
            manifest = None
            if manifest_file.exists():
                with open(manifest_file, "r", encoding="utf-8") as f:
                    manifest = json.load(f)
                print(f"   Manifest loaded: {manifest.get('total_files', 0)} files")
            
            # Extract backup
            with tarfile.open(backup_path, "r:*") as tar:
                members = tar.getmembers()
                
                if dry_run:
                    print(f"   Would restore {len(members)} files:")
                    for member in members[:10]:  # Show first 10
                        print(f"     - {member.name}")
                    if len(members) > 10:
                        print(f"     ... and {len(members) - 10} more")
                else:
                    # Extract all files
                    for member in members:
                        tar.extract(member, PROJECT_ROOT)
                        if manifest and manifest.get("verbose", False):
                            print(f"   ✅ Restored: {member.name}")
                    
                    print(f"\n✅ Restore complete!")
                    print(f"   Files restored: {len(members)}")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Restore failed: {e}")
            return False
    
    def list_backups(self):
        """List all available backups"""
        if not self.output_dir.exists():
            print(f"📁 No backups found (directory doesn't exist: {self.output_dir})")
            return []
        
        backups = sorted(self.output_dir.glob("jgmart_backup_*.tar.gz"), reverse=True)
        
        if not backups:
            print(f"📁 No backups found in {self.output_dir}")
            return []
        
        print(f"📦 Available backups ({len(backups)}):\n")
        
        for i, backup in enumerate(backups, 1):
            size_mb = backup.stat().st_size / (1024 * 1024)
            created = datetime.fromtimestamp(backup.stat().st_mtime)
            
            # Check for manifest
            manifest_file = self.get_manifest_filename(backup)
            manifest_info = ""
            if manifest_file.exists():
                try:
                    with open(manifest_file, "r", encoding="utf-8") as f:
                        manifest = json.load(f)
                    file_count = manifest.get("total_files", 0)
                    manifest_info = f" ({file_count} files)"
                except:
                    manifest_info = " (manifest error)"
            
            print(f"  {i}. {backup.name}")
            print(f"     Size: {size_mb:.2f} MB | Created: {created.strftime('%Y-%m-%d %H:%M:%S')}{manifest_info}")
            print()
        
        return backups
    
    def verify_backup(self, backup_file):
        """Verify integrity of a backup file"""
        backup_path = Path(backup_file)
        
        if not backup_path.exists():
            print(f"❌ Backup file not found: {backup_file}")
            return False
        
        print(f"🔍 Verifying backup: {backup_path.name}")
        
        try:
            # Check file size
            size_mb = backup_path.stat().st_size / (1024 * 1024)
            print(f"   Size: {size_mb:.2f} MB")
            
            if size_mb < 0.1:
                print(f"   ⚠️  Warning: Backup seems very small")
            
            # Check manifest
            manifest_file = self.get_manifest_filename(backup_path)
            if manifest_file.exists():
                with open(manifest_file, "r", encoding="utf-8") as f:
                    manifest = json.load(f)
                print(f"   Manifest: ✅ Found")
                print(f"   Files: {manifest.get('total_files', 0)}")
                print(f"   Created: {manifest.get('created_at', 'unknown')}")
                print(f"   Compressed: {manifest.get('compressed', 'unknown')}")
            else:
                print(f"   Manifest: ⚠️  Not found")
            
            # Try to open tar file
            with tarfile.open(backup_path, "r:*") as tar:
                members = tar.getmembers()
                print(f"   Archive: ✅ Valid tar file")
                print(f"   Entries: {len(members)}")
                
                # Show first few files
                print(f"   Sample files:")
                for member in members[:5]:
                    print(f"     - {member.name}")
                if len(members) > 5:
                    print(f"     ... and {len(members) - 5} more")
            
            print(f"\n✅ Backup verification complete")
            return True
            
        except Exception as e:
            print(f"\n❌ Backup verification failed: {e}")
            return False
    
    def cleanup_old_backups(self, keep=5):
        """Remove old backups, keeping only the most recent N"""
        if not self.output_dir.exists():
            return
        
        backups = sorted(self.output_dir.glob("jgmart_backup_*.tar.gz"), reverse=True)
        
        if len(backups) > keep:
            print(f"🧹 Cleaning up old backups (keeping {keep} most recent)...")
            
            for old_backup in backups[keep:]:
                try:
                    old_backup.unlink()
                    # Also remove manifest
                    manifest_file = self.get_manifest_filename(old_backup)
                    if manifest_file.exists():
                        manifest_file.unlink()
                    print(f"   🗑️  Removed: {old_backup.name}")
                except Exception as e:
                    print(f"   ⚠️  Failed to remove {old_backup.name}: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="JG Mart Backup & Restore Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python backup_restore.py backup
  python backup_restore.py backup --output-dir ./backups --compress
  python backup_restore.py restore --backup-file backups/jgmart_backup_20260729.tar.gz
  python backup_restore.py list
  python backup_restore.py verify --backup-file backups/jgmart_backup_20260729.tar.gz
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Backup command
    backup_parser = subparsers.add_parser("backup", help="Create a backup")
    backup_parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help=f"Output directory for backup (default: {BACKUP_DIR})"
    )
    backup_parser.add_argument(
        "--no-compress",
        action="store_true",
        help="Create uncompressed backup"
    )
    backup_parser.add_argument(
        "--cleanup",
        action="store_true",
        help="Remove old backups after creating new one"
    )
    backup_parser.add_argument(
        "--keep",
        type=int,
        default=5,
        help="Number of recent backups to keep (default: 5)"
    )
    
    # Restore command
    restore_parser = subparsers.add_parser("restore", help="Restore from backup")
    restore_parser.add_argument(
        "--backup-file",
        type=str,
        required=True,
        help="Path to backup file"
    )
    restore_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be restored without actually restoring"
    )
    
    # List command
    list_parser = subparsers.add_parser("list", help="List available backups")
    list_parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help=f"Backup directory to list (default: {BACKUP_DIR})"
    )
    
    # Verify command
    verify_parser = subparsers.add_parser("verify", help="Verify backup integrity")
    verify_parser.add_argument(
        "--backup-file",
        type=str,
        required=True,
        help="Path to backup file"
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute command
    if args.command == "backup":
        tool = BackupRestore(
            output_dir=args.output_dir,
            compress=not args.no_compress
        )
        backup_file = tool.create_backup()
        
        if backup_file and args.cleanup:
            tool.cleanup_old_backups(keep=args.keep)
        
        sys.exit(0 if backup_file else 1)
    
    elif args.command == "restore":
        tool = BackupRestore()
        success = tool.restore_backup(
            args.backup_file,
            dry_run=args.dry_run
        )
        sys.exit(0 if success else 1)
    
    elif args.command == "list":
        output_dir = args.output_dir if args.output_dir else str(BACKUP_DIR)
        tool = BackupRestore(output_dir=output_dir)
        backups = tool.list_backups()
        sys.exit(0 if backups else 1)
    
    elif args.command == "verify":
        tool = BackupRestore()
        success = tool.verify_backup(args.backup_file)
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
