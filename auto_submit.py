#!/usr/bin/env python3
"""
Auto-detect guide page updates and submit to Google Indexing API.
Called by cron: checks if any commits in last hour, if yes submits.
Runs via Windows cmd.exe to use the proxy.
"""
import subprocess, sys

REPO = "/home/wenjun/bubbpackage-guide"
BAT  = r"C:\Users\chaox\bubbpackage-seo\submit_index_auto.bat"

# Check for recent commits (last 60 min)
result = subprocess.run(
    ["git", "-C", REPO, "log", "--oneline", "--since=60 minutes ago"],
    capture_output=True, text=True
)

if not result.stdout.strip():
    print("No recent commits, skip.")
    sys.exit(0)

print(f"Recent commits found:\n{result.stdout.strip()}")

# Run submission via Windows (for proxy access)
# Use cmd.exe /c to run the bat non-interactively
subprocess.run(
    ["cmd.exe", "/c", BAT],
    cwd=r"C:\Users\chaox\bubbpackage-seo",
    timeout=120
)
print("Submission triggered.")
