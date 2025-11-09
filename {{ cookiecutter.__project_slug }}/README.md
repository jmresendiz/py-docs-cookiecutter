# {{ cookiecutter.project_name }}

{{ cookiecutter.project_short_description }}

## Overview

This project combines **MkDocs** for documentation and **Slidev** for presentations, managed through a unified Python CLI with Docker infrastructure.

## Features

- 📝 **MkDocs Documentation** - Beautiful, searchable documentation with Material theme
- 🎨 **Slidev Presentations** - Interactive, markdown-based presentations
- 🛠️ **Python CLI** - Unified command-line interface for managing both
- 🐳 **Docker Integration** - Containerized environment for consistency

## Quick Start

### Prerequisites

- Python {{ cookiecutter.python_version }}
- Docker and Docker Compose
- pyenv and pyenv-virtualenv (recommended)

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd {{ cookiecutter.__project_slug }}

# Set up the environment
./scripts/setup_env.sh

# Activate the virtual environment
pyenv activate {{ cookiecutter.__project_slug }}
```

## Usage

### Documentation (MkDocs)

```bash
# Start the documentation server
py-docs mkdocs start

# Build static HTML
py-docs mkdocs build

# Stop the server
py-docs mkdocs stop
```

The documentation will be available at `http://localhost:8000`.

### Presentations (Slidev)

```bash
# List all presentations
py-docs slidev list

# Create a new presentation
py-docs slidev create my-presentation

# Start a presentation
py-docs slidev start my-presentation

# Export to PDF
py-docs slidev export my-presentation

# Stop the server
py-docs slidev stop
```

Presentations will be available at `http://localhost:3030`.

## Documentation

- [Installation Guide](docs/installation.md) - Detailed installation instructions
- [Usage Guide](docs/USAGE.md) - Complete usage documentation
- [Slidev Guide](docs/SLIDEV.md) - Working with Slidev presentations

## Project Structure

```
{{ cookiecutter.__project_slug }}/
├── mkdocs/              # MkDocs documentation
│   ├── docs/           # Markdown documentation files
│   └── mkdocs.yml      # MkDocs configuration
├── slides/             # Slidev presentations
│   └── example_presentation/
├── src/                # Python source code
│   └── {{ cookiecutter.__project_slug }}/
│       ├── __init__.py
│       └── cli.py      # CLI implementation
├── .build/             # Docker infrastructure
│   ├── slidev.Dockerfile
│   ├── slidev-compose.yml
│   ├── mkdocs.Dockerfile
│   └── mkdocs-compose.yml
└── scripts/            # Setup scripts
    └── setup_env.sh
```

## Contributing

Interested in contributing? Check out the [contributing guidelines](CONTRIBUTING.md). Please note that
this project is released with a [Code of Conduct](CONDUCT.md). By contributing to this project,
you agree to abide by its terms.

## License

`{{ cookiecutter.project_name }}` was created by {{ cookiecutter.author_name }}.
It is licensed under the terms of the {{ cookiecutter.open_source_license }} license.

## Credits

`{{ cookiecutter.project_name }}` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/)
and the `py-docs-cookiecutter` [template](https://github.com/ztocker/py-docs-cookiecutter).
