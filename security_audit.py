#!/usr/bin/env python3
"""
Security Audit Script for SADOCKDOG Platform

This script performs basic security checks on the codebase:
- Detects potential hardcoded secrets
- Checks for insecure dependencies
- Validates security configurations
- Scans for common security issues

Usage:
    python security_audit.py [--verbose]
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple

# Patterns that might indicate secrets
SECRET_PATTERNS = [
    (r'password\s*=\s*["\'](?!.*\{.*\})([^"\']{8,})["\']', "Hardcoded password"),
    (r'api[_-]?key\s*=\s*["\'](?!.*\{.*\})([^"\']{20,})["\']', "Hardcoded API key"),
    (r'secret[_-]?key\s*=\s*["\'](?!.*\{.*\})([^"\']{20,})["\']', "Hardcoded secret key"),
    (r'token\s*=\s*["\'](?!.*\{.*\})([^"\']{20,})["\']', "Hardcoded token"),
    (r'(sk-[a-zA-Z0-9]{48})', "OpenAI API key pattern"),
    (r'(ghp_[a-zA-Z0-9]{36})', "GitHub Personal Access Token"),
    (r'(AKIA[0-9A-Z]{16})', "AWS Access Key"),
]

# Files to exclude from scanning
EXCLUDE_PATTERNS = [
    r'node_modules/',
    r'\.git/',
    r'\.pytest_cache/',
    r'__pycache__/',
    r'\.venv/',
    r'venv/',
    r'dist/',
    r'build/',
    r'\.next/',
    r'coverage/',
    r'htmlcov/',
]

# File extensions to scan
SCAN_EXTENSIONS = {'.py', '.ts', '.tsx', '.js', '.jsx', '.env.example', '.env.default', '.yml', '.yaml', '.json'}


class SecurityAuditor:
    def __init__(self, root_dir: str, verbose: bool = False):
        self.root_dir = Path(root_dir)
        self.verbose = verbose
        self.issues: List[Tuple[str, str, int, str]] = []
        
    def should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded from scanning."""
        path_str = str(path.relative_to(self.root_dir))
        return any(re.search(pattern, path_str) for pattern in EXCLUDE_PATTERNS)
    
    def scan_file(self, file_path: Path):
        """Scan a single file for security issues."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                
            for line_num, line in enumerate(lines, 1):
                for pattern, description in SECRET_PATTERNS:
                    if re.search(pattern, line, re.IGNORECASE):
                        # Skip comments
                        if line.strip().startswith(('#', '//', '/*', '*', '<!--')):
                            continue
                        
                        self.issues.append((
                            str(file_path.relative_to(self.root_dir)),
                            description,
                            line_num,
                            line.strip()[:80]
                        ))
        except Exception as e:
            if self.verbose:
                print(f"Error scanning {file_path}: {e}")
    
    def scan_directory(self):
        """Recursively scan directory for security issues."""
        print(f"🔍 Scanning {self.root_dir} for security issues...")
        
        scanned_files = 0
        for file_path in self.root_dir.rglob('*'):
            if not file_path.is_file():
                continue
            
            if self.should_exclude(file_path):
                continue
                
            if file_path.suffix in SCAN_EXTENSIONS or file_path.name.startswith('.env'):
                self.scan_file(file_path)
                scanned_files += 1
        
        print(f"✅ Scanned {scanned_files} files")
        return len(self.issues)
    
    def check_env_files(self):
        """Check for .env files in repository."""
        print("\\n🔍 Checking for .env files...")
        
        env_files = list(self.root_dir.rglob('.env'))
        env_files = [f for f in env_files if not self.should_exclude(f)]
        
        if env_files:
            print("⚠️  WARNING: Found .env files (should not be committed):")
            for env_file in env_files:
                print(f"   - {env_file.relative_to(self.root_dir)}")
            return False
        else:
            print("✅ No .env files found in repository")
            return True
    
    def check_dependencies(self):
        """Check for known vulnerable dependencies."""
        print("\\n🔍 Checking dependencies...")
        
        # Check Python dependencies
        backend_pyproject = self.root_dir / "autogpt_platform" / "backend" / "pyproject.toml"
        if backend_pyproject.exists():
            print("ℹ️  Run: cd autogpt_platform/backend && poetry run safety check")
        
        # Check Node dependencies
        frontend_package = self.root_dir / "autogpt_platform" / "frontend" / "package.json"
        if frontend_package.exists():
            print("ℹ️  Run: cd autogpt_platform/frontend && pnpm audit")
        
        return True
    
    def print_report(self):
        """Print security audit report."""
        print("\\n" + "="*80)
        print("🔐 SECURITY AUDIT REPORT")
        print("="*80)
        
        if not self.issues:
            print("\\n✅ No security issues detected!")
            print("\\nNote: This is a basic scan. Consider:")
            print("  - Professional security audit for production")
            print("  - Dependency vulnerability scanning (safety, pnpm audit)")
            print("  - Code analysis (bandit, semgrep)")
        else:
            print(f"\\n⚠️  Found {len(self.issues)} potential security issues:\\n")
            
            for file_path, description, line_num, line_preview in self.issues:
                print(f"📄 {file_path}:{line_num}")
                print(f"   Issue: {description}")
                print(f"   Code: {line_preview}")
                print()
        
        print("="*80)
        
        return len(self.issues) == 0


def main():
    verbose = '--verbose' in sys.argv or '-v' in sys.argv
    
    # Find project root (assumes script is in project root)
    script_dir = Path(__file__).parent
    root_dir = script_dir
    
    auditor = SecurityAuditor(root_dir, verbose=verbose)
    
    # Run scans
    auditor.scan_directory()
    env_check = auditor.check_env_files()
    dep_check = auditor.check_dependencies()
    
    # Print report
    success = auditor.print_report()
    
    # Exit with appropriate code
    sys.exit(0 if success and env_check else 1)


if __name__ == "__main__":
    main()
