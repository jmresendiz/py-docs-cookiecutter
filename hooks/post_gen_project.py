#!/usr/bin/env python3
"""Post-generation hook for {{ cookiecutter.project_name }} cookiecutter template."""

import os
import shutil
import subprocess
import sys

##############################################################################
# Utilities
##############################################################################

def remove(filepath):
    """Remove a file or directory."""
    if os.path.isfile(filepath):
        os.remove(filepath)
    elif os.path.isdir(filepath):
        shutil.rmtree(filepath)


def run_command(cmd, check=True):
    """Run a shell command."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=check,
            capture_output=True,
            text=True
        )
        if result.stdout:
            print(result.stdout)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        if e.stderr:
            print(f"Error: {e.stderr}", file=sys.stderr)
        return False


##############################################################################
# Cookiecutter clean-up
##############################################################################

# Directive flags
no_license = "{{cookiecutter.open_source_license}}" == "None"

# Remove license (if specified)
if no_license:
    remove("LICENSE")

##############################################################################
# Initialize project
##############################################################################

print("\n" + "="*70)
print("Setting up {{ cookiecutter.project_name }}")
print("="*70 + "\n")

# Initialize git repository
print("Initializing git repository...")
if run_command("git init"):
    print("✓ Git repository initialized")
    
    # Create initial commit
    run_command("git add .")
    run_command('git commit -m "chore: initial commit from cookiecutter"')
    print("✓ Initial commit created")
else:
    print("⚠ Git initialization failed (you may need to initialize manually)")

# Run setup_env.sh to set up Python environment
print("\nSetting up Python environment...")
print("This may take a few minutes...")
setup_script = os.path.join("scripts", "setup_env.sh")

if os.path.exists(setup_script):
    if run_command(f"bash {setup_script} --verbose"):
        print("✓ Python environment set up successfully")
    else:
        print("⚠ Environment setup encountered issues")
        print("  You can run './scripts/setup_env.sh' manually to complete setup")
else:
    print("⚠ Setup script not found")

print("\n" + "="*70)
print("{{ cookiecutter.project_name }} is ready!")
print("="*70)
print("\nNext steps:")
print("  1. Activate the environment:")
print("     pyenv activate {{ cookiecutter.__project_slug }}")
print("\n  2. Start the documentation server:")
print("     py-docs mkdocs start")
print("\n  3. List available presentations:")
print("     py-docs slidev list")
print("\n  4. Read the documentation:")
print("     - README.md - Project overview")
print("     - docs/USAGE.md - Usage guide")
print("     - docs/SLIDEV.md - Slidev guide")
print("\nHappy documenting! 📝\n")
