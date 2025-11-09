import os
import subprocess  # nosec B404
from pathlib import Path
from typing import List
import webbrowser

import click
import inquirer


def find_presentations(slides_root: Path) -> List[str]:
    """Find all presentations in the slides directory."""
    if not slides_root.exists() or not slides_root.is_dir():
        return []

    presentation_names: List[str] = []
    for entry in sorted(slides_root.iterdir()):
        if not entry.is_dir():
            continue

        package_json = entry / "package.json"
        slides_md = entry / "slides.md"

        if package_json.exists() or slides_md.exists():
            presentation_names.append(entry.name)

    return presentation_names


def _resolve_slides_root() -> Path:
    """Resolve the slides directory path from anywhere in the repo."""
    current = Path.cwd()
    while True:
        candidate = current / "slides"
        if candidate.exists() and candidate.is_dir():
            return candidate
        if current.parent == current:
            break
        current = current.parent

    # Fallback: use slides directory relative to CWD
    return (Path.cwd() / "slides").resolve()


def _resolve_build_dir() -> Path:
    """Resolve the .build directory path from anywhere in the repo."""
    current = Path.cwd()
    while True:
        candidate = current / ".build"
        if candidate.exists() and candidate.is_dir():
            return candidate
        if current.parent == current:
            break
        current = current.parent

    # Fallback
    return (Path.cwd() / ".build").resolve()


# ============================================================================
# MAIN CLI
# ============================================================================


@click.group()
def cli() -> None:
    """CLI to manage documentation and presentations."""


# ============================================================================
# SLIDEV COMMANDS
# ============================================================================


@click.group(name="slidev")
def slidev_cli() -> None:
    """Manage Slidev presentations with Docker."""


@slidev_cli.command(name="build")
def build_image() -> None:
    """Build the Slidev Docker image ({{ cookiecutter.__project_slug }}-slidev:latest)."""
    build_dir = _resolve_build_dir()
    dockerfile = build_dir / "slidev.Dockerfile"

    if not dockerfile.exists():
        raise click.ClickException(f"Dockerfile not found at '{dockerfile}'.")

    cmd = [
        "docker",
        "build",
        "-t",
        "{{ cookiecutter.__project_slug }}-slidev:latest",
        "-f",
        str(dockerfile),
        str(build_dir),
    ]

    click.echo("Building Docker image...")
    subprocess.run(cmd, check=True)  # nosec B603 B607
    click.echo("Image '{{ cookiecutter.__project_slug }}-slidev:latest' built successfully.")


@slidev_cli.command(name="list")
def list_presentations() -> None:
    """List available presentations (one per line)."""
    slides_root = _resolve_slides_root()
    presentations = find_presentations(slides_root)

    for name in presentations:
        click.echo(name)


@slidev_cli.command(name="start")
@click.argument("name", type=str, required=False)
def start_presentation(name: str) -> None:
    """Start a presentation with Docker and open browser.

    If no name is provided, tries to detect from current directory or shows interactive list.
    """
    slides_root = _resolve_slides_root()
    build_dir = _resolve_build_dir()

    # If no name provided, try to detect from current directory
    if not name:
        cwd = Path.cwd()
        # Check if we're in a presentation directory
        if (cwd / "slides.md").exists() or (cwd / "package.json").exists():
            # We're in the presentation directory
            name = cwd.name
        elif cwd.parent == slides_root:
            # We're in slides/<presentation>/
            name = cwd.name
        else:
            # Not in a presentation directory, show interactive list
            presentations = find_presentations(slides_root)

            if not presentations:
                raise click.ClickException(
                    f"No presentations found in '{slides_root}'.\n"
                    "Create one with: py-docs slidev create <name>"
                )

            questions = [
                inquirer.List(
                    "presentation",
                    message="Select presentation to start",
                    choices=presentations,
                ),
            ]
            answers = inquirer.prompt(questions)

            if not answers:
                raise click.ClickException("No presentation selected")

            name = answers["presentation"]

    presentation_dir = slides_root / name

    if not presentation_dir.exists():
        raise click.ClickException(
            f"Presentation '{name}' not found in '{slides_root}'."
        )

    compose_file = build_dir / "slidev-compose.yml"
    if not compose_file.exists():
        raise click.ClickException(
            f"docker-compose file not found at '{compose_file}'."
        )

    env = os.environ.copy()
    env["UID"] = str(os.getuid()) if hasattr(os, "getuid") else env.get("UID", "1000")
    env["GID"] = str(os.getgid()) if hasattr(os, "getgid") else env.get("GID", "1000")
    env["PRESENTATION"] = name

    cmd = [
        "docker",
        "compose",
        "-f",
        str(compose_file),
        "up",
        "--build",
        "-d",
        "slidev",
    ]

    click.echo(f"Starting '{name}'...")
    subprocess.run(cmd, check=True, env=env, cwd=build_dir)  # nosec B603
    click.echo(f"Presentation '{name}' running at http://localhost:3030/")

    click.echo("Opening browser...")
    try:
        webbrowser.open("http://localhost:3030")
    except Exception:  # nosec B110
        pass


@slidev_cli.command(name="stop")
def stop_presentation() -> None:
    """Stop the Slidev server."""
    build_dir = _resolve_build_dir()
    compose_file = build_dir / "slidev-compose.yml"

    if not compose_file.exists():
        raise click.ClickException(
            f"docker-compose file not found at '{compose_file}'."
        )

    env = os.environ.copy()
    env["UID"] = str(os.getuid()) if hasattr(os, "getuid") else env.get("UID", "1000")
    env["GID"] = str(os.getgid()) if hasattr(os, "getgid") else env.get("GID", "1000")

    cmd = ["docker", "compose", "-f", str(compose_file), "down"]

    subprocess.run(cmd, check=True, env=env, cwd=build_dir)  # nosec B603
    click.echo("Slidev server stopped.")


@slidev_cli.command(name="open")
def open_browser() -> None:
    """Open the presentation in browser (server must be running)."""
    click.echo("Opening browser at http://localhost:3030/")
    try:
        webbrowser.open("http://localhost:3030")
    except Exception as e:
        raise click.ClickException(f"Failed to open browser: {e}")


@slidev_cli.command(name="create")
@click.argument("name", type=str)
def create_presentation(name: str) -> None:
    """Create a new presentation using the official Slidev wizard (Docker-only)."""
    slides_root = _resolve_slides_root()
    slides_root.mkdir(parents=True, exist_ok=True)
    target_dir = slides_root / name

    if target_dir.exists():
        raise click.ClickException(
            f"Directory '{target_dir}' already exists. Use a different name."
        )

    # Ensure {{ cookiecutter.__project_slug }}-slidev image exists; build if missing
    try:
        subprocess.run(  # nosec B603 B607
            ["docker", "image", "inspect", "{{ cookiecutter.__project_slug }}-slidev:latest"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        build_dir = _resolve_build_dir()
        dockerfile = build_dir / "slidev.Dockerfile"
        if not dockerfile.exists():
            raise click.ClickException(f"Dockerfile not found at '{dockerfile}'.")
        click.echo(
            "Building Docker image '{{ cookiecutter.__project_slug }}-slidev:latest' (required for create)..."
        )
        subprocess.run(  # nosec B603 B607
            [
                "docker",
                "build",
                "-t",
                "{{ cookiecutter.__project_slug }}-slidev:latest",
                "-f",
                str(dockerfile),
                str(build_dir),
            ],
            check=True,
        )

    uid = str(os.getuid()) if hasattr(os, "getuid") else "1000"
    gid = str(os.getgid()) if hasattr(os, "getgid") else "1000"

    docker_cmd = [
        "docker",
        "run",
        "--rm",
        "--name",
        f"{{ cookiecutter.__project_slug }}-slidev-create-{name}",
        "--user",
        f"{uid}:{gid}",
        "-e",
        "HOME=/tmp",
        "-e",
        "NPM_CONFIG_CACHE=/tmp/.npm",
        "-v",
        f"{str(slides_root)}:/slidev",
        "-w",
        "/slidev",
        "{{ cookiecutter.__project_slug }}-slidev:latest",
        "sh",
        "-lc",
        f"npm create slidev@latest {name} -- --yes",
    ]

    click.echo(f"Creating presentation '{name}' using Docker...")
    click.echo("This may take a moment while dependencies are installed.\n")

    try:
        subprocess.run(docker_cmd, check=True)  # nosec B603
        click.echo(f"\nPresentation '{name}' created at {target_dir}")
        click.echo("\nNext step:")
        click.echo(f"   py-docs slidev start {name}")
    except subprocess.CalledProcessError as e:
        raise click.ClickException(
            f"Error creating presentation with Docker. Exit code: {e.returncode}"
        )


@slidev_cli.command(name="export")
@click.argument("name", type=str, required=False)
def export_presentation(name: str) -> None:
    """Export a presentation to PDF using Docker.

    If no name is provided, tries to detect from current directory or shows interactive list.
    """
    slides_root = _resolve_slides_root()
    build_dir = _resolve_build_dir()

    # If no name provided, try to detect from current directory
    if not name:
        cwd = Path.cwd()
        if (cwd / "slides.md").exists() or (cwd / "package.json").exists():
            name = cwd.name
        elif cwd.parent == slides_root:
            name = cwd.name
        else:
            # Not in a presentation directory, show interactive list
            presentations = find_presentations(slides_root)

            if not presentations:
                raise click.ClickException(
                    f"No presentations found in '{slides_root}'.\n"
                    "Create one with: py-docs slidev create <name>"
                )

            questions = [
                inquirer.List(
                    "presentation",
                    message="Select presentation to export",
                    choices=presentations,
                ),
            ]
            answers = inquirer.prompt(questions)

            if not answers:
                raise click.ClickException("No presentation selected")

            name = answers["presentation"]

    presentation_dir = slides_root / name

    if not presentation_dir.exists():
        raise click.ClickException(
            f"Presentation '{name}' not found in '{slides_root}'."
        )

    compose_file = build_dir / "slidev-compose.yml"
    if not compose_file.exists():
        raise click.ClickException(
            f"docker-compose file not found at '{compose_file}'."
        )

    env = os.environ.copy()
    env["UID"] = str(os.getuid()) if hasattr(os, "getuid") else env.get("UID", "1000")
    env["GID"] = str(os.getgid()) if hasattr(os, "getgid") else env.get("GID", "1000")
    env["PRESENTATION"] = name

    cmd = [
        "docker",
        "compose",
        "-f",
        str(compose_file),
        "run",
        "--rm",
        "slidev-export",
    ]

    click.echo(f"Exporting '{name}' to PDF...")
    subprocess.run(cmd, check=True, env=env, cwd=build_dir)  # nosec B603

    out_path = presentation_dir / "slides-export.pdf"
    click.echo(f"Exported: {out_path}")


# ============================================================================
# MKDOCS COMMANDS
# ============================================================================


@click.group(name="mkdocs")
def mkdocs_cli() -> None:
    """Manage MkDocs documentation with Docker."""


@mkdocs_cli.command(name="start")
def mkdocs_start() -> None:
    """Start MkDocs development server with Docker and open browser."""
    build_dir = _resolve_build_dir()
    compose_file = build_dir / "mkdocs-compose.yml"

    if not compose_file.exists():
        raise click.ClickException(
            f"docker-compose file not found at '{compose_file}'."
        )

    env = os.environ.copy()
    env["UID"] = str(os.getuid()) if hasattr(os, "getuid") else env.get("UID", "1000")
    env["GID"] = str(os.getgid()) if hasattr(os, "getgid") else env.get("GID", "1000")

    cmd = [
        "docker",
        "compose",
        "-f",
        str(compose_file),
        "up",
        "--build",
        "-d",
        "mkdocs-serve",
    ]

    click.echo("Starting MkDocs server...")
    subprocess.run(cmd, check=True, env=env, cwd=build_dir)  # nosec B603
    click.echo("MkDocs server running at http://localhost:8000/")

    click.echo("Opening browser...")
    try:
        webbrowser.open("http://localhost:8000")
    except Exception:  # nosec B110
        pass


@mkdocs_cli.command(name="stop")
def mkdocs_stop() -> None:
    """Stop the MkDocs server."""
    build_dir = _resolve_build_dir()
    compose_file = build_dir / "mkdocs-compose.yml"

    if not compose_file.exists():
        raise click.ClickException(
            f"docker-compose file not found at '{compose_file}'."
        )

    env = os.environ.copy()
    env["UID"] = str(os.getuid()) if hasattr(os, "getuid") else env.get("UID", "1000")
    env["GID"] = str(os.getgid()) if hasattr(os, "getgid") else env.get("GID", "1000")

    cmd = ["docker", "compose", "-f", str(compose_file), "down"]

    subprocess.run(cmd, check=True, env=env, cwd=build_dir)  # nosec B603
    click.echo("MkDocs server stopped.")


@mkdocs_cli.command(name="build")
def mkdocs_build() -> None:
    """Build static HTML documentation from MkDocs sources."""
    build_dir = _resolve_build_dir()
    compose_file = build_dir / "mkdocs-compose.yml"

    if not compose_file.exists():
        raise click.ClickException(
            f"docker-compose file not found at '{compose_file}'."
        )

    env = os.environ.copy()
    env["UID"] = str(os.getuid()) if hasattr(os, "getuid") else env.get("UID", "1000")
    env["GID"] = str(os.getgid()) if hasattr(os, "getgid") else env.get("GID", "1000")

    cmd = [
        "docker",
        "compose",
        "-f",
        str(compose_file),
        "run",
        "--rm",
        "mkdocs-build",
    ]

    click.echo("Building MkDocs documentation...")
    subprocess.run(cmd, check=True, env=env, cwd=build_dir)  # nosec B603
    click.echo("Documentation built successfully in mkdocs/site/")


# Register subcommands
cli.add_command(slidev_cli)
cli.add_command(mkdocs_cli)


if __name__ == "__main__":
    cli()

