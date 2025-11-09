# Installation

This guide will help you install and set up {{ cookiecutter.project_name }}.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python {{ cookiecutter.python_version }}** or higher
- **Docker** and **Docker Compose** (for running MkDocs and Slidev)
- **pyenv** and **pyenv-virtualenv** (recommended for Python version management)
- **Poetry** (Python package manager)

### Installing pyenv

=== "macOS"

    ```bash
    brew install pyenv pyenv-virtualenv
    ```

=== "Linux"

    ```bash
    curl https://pyenv.run | bash
    ```

=== "Windows"

    Use [pyenv-win](https://github.com/pyenv-win/pyenv-win)

### Installing Poetry

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Installing Docker

Visit [Docker's official website](https://www.docker.com/get-started) to download and install Docker Desktop for your operating system.

## Installation Steps

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd {{ cookiecutter.__project_slug }}
```

### 2. Set Up Python Environment

The project includes an automated setup script:

```bash
./scripts/setup_env.sh
```

This script will:

- Check for pyenv and pyenv-virtualenv
- Install Python {{ cookiecutter.python_version }} if needed
- Create a virtual environment named `{{ cookiecutter.__project_slug }}`
- Install Poetry
- Install all project dependencies

### 3. Activate the Virtual Environment

```bash
pyenv activate {{ cookiecutter.__project_slug }}
```

Or, if you're in the project directory:

```bash
pyenv local {{ cookiecutter.__project_slug }}
```

### 4. Verify Installation

```bash
# Check the CLI is available
{{ cookiecutter.__project_slug }} --help

# You should see the CLI commands
```

## Manual Installation

If you prefer to set up manually:

```bash
# Install Python version
pyenv install {{ cookiecutter.python_version }}

# Create virtual environment
pyenv virtualenv {{ cookiecutter.python_version }} {{ cookiecutter.__project_slug }}

# Activate environment
pyenv activate {{ cookiecutter.__project_slug }}

# Install Poetry
pip install poetry==2.1.3

# Install dependencies
poetry install
```

## Docker Setup

The project uses Docker for running MkDocs and Slidev. No additional Docker setup is required - the CLI will handle building images when needed.

## Troubleshooting

### Python Version Not Found

If pyenv can't find Python {{ cookiecutter.python_version }}:

```bash
pyenv install {{ cookiecutter.python_version }}
```

### Poetry Command Not Found

Ensure Poetry is in your PATH:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Docker Permission Errors

On Linux, you may need to add your user to the docker group:

```bash
sudo usermod -aG docker $USER
```

Then log out and back in.

## Next Steps

Now that you have {{ cookiecutter.project_name }} installed, check out the [Quick Start Guide](quickstart.md) to learn how to use it.

