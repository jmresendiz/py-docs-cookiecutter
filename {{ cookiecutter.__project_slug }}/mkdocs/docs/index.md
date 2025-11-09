# Welcome to {{ cookiecutter.project_name }}

{{ cookiecutter.project_short_description }}

## Overview

This is the main documentation site for {{ cookiecutter.project_name }}. Here you'll find comprehensive guides, API references, and examples to help you get started and make the most of this project.

## Features

- **MkDocs Documentation**: Beautiful, searchable documentation with Material theme
- **Slidev Presentations**: Interactive presentation system for technical content
- **Python CLI**: Convenient command-line tools to manage both documentation and presentations

## Quick Links

- [Installation Guide](getting_started/installation.md) - Get started with {{ cookiecutter.project_name }}
- [Quick Start](getting_started/quickstart.md) - Your first steps with the project

## Project Structure

```
{{ cookiecutter.__project_slug }}/
├── mkdocs/              # Documentation source
│   ├── docs/           # Markdown documentation files
│   └── mkdocs.yml      # MkDocs configuration
├── slides/             # Slidev presentation projects (empty initially)
├── src/                # Python source code
│   └── {{ cookiecutter.__project_slug }}/
│       ├── __init__.py
│       └── cli.py      # CLI commands
└── .build/             # Docker infrastructure
```

## Getting Started

### Prerequisites

- Python {{ cookiecutter.python_version }}
- Docker (for running MkDocs and Slidev)
- Poetry (Python package manager)

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

### Using the CLI

The project includes a CLI tool for managing documentation and presentations:

```bash
# Start MkDocs server
py-docs mkdocs start

# List Slidev presentations
py-docs slidev list

# Start a Slidev presentation
py-docs slidev start <presentation-name>
```

## Documentation

This documentation is built with [MkDocs](https://www.mkdocs.org/) using the [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme.

To contribute to the documentation, edit the Markdown files in the `mkdocs/docs/` directory and submit a pull request.

## License

This project is licensed under the {{ cookiecutter.open_source_license }} license.

## Contact

For questions or support, please contact {{ cookiecutter.author_name }}.

