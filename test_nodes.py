#!/usr/bin/env python3
"""Test all VAMDC nodes - check if they can migrate and start"""

import os
import subprocess
import sys
from pathlib import Path

NODES_DIR = Path("/home/user/NodeSoftware/nodes")
SKIP_NODES = ["vald", "ExampleNode"]  # Already tested

def test_node(node_dir):
    """Test a single node"""
    node_name = node_dir.name

    print(f"\n{'='*60}")
    print(f"Testing: {node_name}")
    print(f"{'='*60}")

    # Check if manage.py exists
    manage_py = node_dir / "manage.py"
    if not manage_py.exists():
        print(f"  ✗ No manage.py found - SKIP")
        return "skip", "No manage.py"

    # Change to node directory
    os.chdir(node_dir)

    # Check if settings.py exists
    settings_py = node_dir / "settings.py"
    if not settings_py.exists():
        # Try to find settings_default.py
        settings_default = node_dir / "settings_default.py"
        if settings_default.exists():
            print(f"  Creating settings.py symlink...")
            os.symlink("settings_default.py", "settings.py")
        else:
            print(f"  ✗ No settings.py or settings_default.py - NEEDS SETUP")
            return "needs_setup", "No settings file"

    # Check if STATIC_URL is set
    try:
        with open("settings.py" if settings_py.exists() else settings_py.readlink(), 'r') as f:
            content = f.read()
            if "STATIC_URL" not in content:
                print(f"  ! Adding STATIC_URL to settings...")
                with open(settings_py, 'a') as sf:
                    sf.write("\n# Required for staticfiles app\nSTATIC_URL = '/static/'\n")
    except Exception as e:
        print(f"  Warning: Could not check/add STATIC_URL: {e}")

    # Try migration
    print(f"  Running migrate...")
    try:
        result = subprocess.run(
            ["uv", "run", "python", "manage.py", "migrate"],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            print(f"  ✗ Migration failed:")
            print(f"    {result.stderr[:200]}")
            return "failed", f"Migration error: {result.stderr[:100]}"

        print(f"  ✓ Migration successful")

    except subprocess.TimeoutExpired:
        print(f"  ✗ Migration timeout")
        return "failed", "Migration timeout"
    except Exception as e:
        print(f"  ✗ Migration exception: {e}")
        return "failed", str(e)

    # Try server check
    print(f"  Running server check...")
    try:
        result = subprocess.run(
            ["uv", "run", "python", "manage.py", "check"],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            print(f"  ✗ Server check failed:")
            print(f"    {result.stderr[:200]}")
            return "failed", f"Check error: {result.stderr[:100]}"

        print(f"  ✓ Server check passed")
        print(f"  ✓✓ NODE WORKING ✓✓")
        return "passed", "OK"

    except subprocess.TimeoutExpired:
        print(f"  ✗ Check timeout")
        return "failed", "Check timeout"
    except Exception as e:
        print(f"  ✗ Check exception: {e}")
        return "failed", str(e)


def main():
    """Test all nodes"""

    results = {
        "passed": [],
        "failed": [],
        "needs_setup": [],
        "skip": []
    }

    # Get all node directories
    node_dirs = sorted([d for d in NODES_DIR.iterdir() if d.is_dir() and not d.name.startswith("__")])

    print(f"Found {len(node_dirs)} nodes to test")
    print(f"Skipping: {', '.join(SKIP_NODES)}")

    for node_dir in node_dirs:
        if node_dir.name in SKIP_NODES:
            print(f"\nSkipping {node_dir.name} (already tested)")
            continue

        status, message = test_node(node_dir)
        results[status].append((node_dir.name, message))

    # Print summary
    print(f"\n\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"✓ Passed:      {len(results['passed'])}")
    print(f"✗ Failed:      {len(results['failed'])}")
    print(f"! Needs Setup: {len(results['needs_setup'])}")
    print(f"- Skipped:     {len(results['skip'])}")

    if results['passed']:
        print(f"\n✓ PASSED ({len(results['passed'])}):")
        for node, _ in results['passed']:
            print(f"  - {node}")

    if results['failed']:
        print(f"\n✗ FAILED ({len(results['failed'])}):")
        for node, msg in results['failed']:
            print(f"  - {node}: {msg}")

    if results['needs_setup']:
        print(f"\n! NEEDS SETUP ({len(results['needs_setup'])}):")
        for node, msg in results['needs_setup']:
            print(f"  - {node}: {msg}")

    # Save detailed results
    with open("/home/user/NodeSoftware/NODE_TEST_RESULTS.md", "w") as f:
        f.write("# Node Test Results\n\n")
        f.write(f"Total nodes tested: {len(node_dirs) - len(SKIP_NODES)}\n\n")
        f.write(f"## Summary\n\n")
        f.write(f"- ✓ Passed: {len(results['passed'])}\n")
        f.write(f"- ✗ Failed: {len(results['failed'])}\n")
        f.write(f"- ! Needs Setup: {len(results['needs_setup'])}\n")
        f.write(f"- - Skipped: {len(results['skip'])}\n\n")

        for status_name, status_key in [("Passed", "passed"), ("Failed", "failed"),
                                        ("Needs Setup", "needs_setup"), ("Skipped", "skip")]:
            if results[status_key]:
                f.write(f"## {status_name}\n\n")
                for node, msg in results[status_key]:
                    f.write(f"- **{node}**: {msg}\n")
                f.write("\n")

    print(f"\nDetailed results saved to: NODE_TEST_RESULTS.md")

    return len(results['failed'])

if __name__ == "__main__":
    sys.exit(main())
