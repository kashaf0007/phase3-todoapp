#!/usr/bin/env python3
"""
Security scanning script to detect hardcoded credentials in the codebase.
This script scans for potential security vulnerabilities related to hardcoded credentials.
"""

import os
import re
from pathlib import Path
from typing import List, Tuple


def scan_for_hardcoded_credentials(directory: str) -> List[Tuple[str, int, str]]:
    """
    Scans the specified directory for potential hardcoded credentials.
    
    Args:
        directory: The directory to scan
        
    Returns:
        List of tuples containing (file_path, line_number, line_content) for matches
    """
    suspicious_patterns = [
        r'password\s*[:=]\s*["\'][^"\']+["\']',
        r'DATABASE_URL\s*[:=]\s*["\'][^"\']*password=[^"\']*["\']',
        r'"[^"]*password[^"]*"\s*[:=]\s*["\'][^"\']+["\']',
        r"'[^']*password[^']*'\s*[:=]\s*['\"][^'\"]+['\"]",
        r'postgresql://[^:]+:[^@]+@',  # Connection string with password
        r'postgres://[^:]+:[^@]+@',    # Alternative connection string
    ]
    
    results = []
    
    for root, dirs, files in os.walk(directory):
        # Skip certain directories
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', '.venv', 'venv', 'node_modules']]
        
        for file in files:
            if file.endswith(('.py', '.js', '.ts', '.json', '.yaml', '.yml', '.env', '.txt')):
                file_path = Path(root) / file
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        
                    for line_num, line in enumerate(lines, 1):
                        for pattern in suspicious_patterns:
                            if re.search(pattern, line, re.IGNORECASE):
                                results.append((str(file_path), line_num, line.strip()))
                                
                except UnicodeDecodeError:
                    # Skip binary files
                    continue
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")
                    
    return results


def main():
    """
    Main function to run the security scan.
    """
    print("Scanning for hardcoded credentials...")
    
    # Scan the backend directory
    results = scan_for_hardcoded_credentials("backend/")
    
    if results:
        print("\n⚠️  Potential hardcoded credentials found:")
        print("-" * 50)
        for file_path, line_num, line_content in results:
            print(f"File: {file_path}:{line_num}")
            print(f"Line: {line_content}")
            print("-" * 50)
        print(f"\nFound {len(results)} potential issues.")
        return 1
    else:
        print("\n✅ No hardcoded credentials detected.")
        return 0


if __name__ == "__main__":
    exit(main())