# Quick Start Guide

Get up and running with {{ cookiecutter.project_name }} in minutes!

## Overview

{{ cookiecutter.project_name }} provides two main tools:

1. **MkDocs** - For creating and managing documentation sites
2. **Slidev** - For creating and managing interactive presentations

Both are managed through a unified CLI interface.

## Using MkDocs

### Start the Documentation Server

```bash
py-docs mkdocs start
```

This command will:

- Start the MkDocs development server using Docker
- Open your browser to `http://localhost:8000`
- Watch for changes and auto-reload

### Stop the Documentation Server

```bash
py-docs mkdocs stop
```

### Build Static HTML

To build the documentation as static HTML files:

```bash
py-docs mkdocs build
```

The output will be in `mkdocs/site/`.

## Using Slidev

### List Available Presentations

```bash
py-docs slidev list
```

### Create a New Presentation

```bash
py-docs slidev create my-presentation
```

This creates a new Slidev project in `slides/my-presentation/`.

### Start a Presentation

```bash
py-docs slidev start my-presentation
```

Or, if you're in the presentation directory:

```bash
cd slides/my-presentation
py-docs slidev start
```

The presentation will open at `http://localhost:3030`.

### Stop the Presentation Server

```bash
py-docs slidev stop
```

### Export to PDF

```bash
py-docs slidev export my-presentation
```

The PDF will be saved as `slides/my-presentation/slides-export.pdf`.

## Working with Documentation

### Adding New Pages

1. Create a new Markdown file in `mkdocs/docs/`:

```bash
touch mkdocs/docs/my-new-page.md
```

2. Edit the file with your content:

```markdown
# My New Page

This is my new documentation page.

## Section 1

Content here...
```

3. Add it to the navigation in `mkdocs/mkdocs.yml`:

```yaml
nav:
  - Home: index.md
  - Getting Started:
      - Installation: getting_started/installation.md
      - Quick Start: getting_started/quickstart.md
  - My New Page: my-new-page.md
```

4. The changes will appear automatically if the server is running!

## Working with Presentations

### Editing Slides

Edit the `slides.md` file in your presentation directory:

```markdown
---
theme: default
---

# My First Slide

Content here

---

# My Second Slide

More content
```

Changes appear immediately in the browser when the server is running.

### Adding Slide Pages

For complex presentations, use the `pages/` directory:

```markdown
<!-- In slides.md -->
---
src: ./pages/my-slide.md
---
```

### Adding Assets

Place images and other assets in the `public/` directory:

```markdown
![My Image](/my-image.png)
```

## CLI Reference

### MkDocs Commands

| Command | Description |
|---------|-------------|
| `py-docs mkdocs start` | Start development server |
| `py-docs mkdocs stop` | Stop development server |
| `py-docs mkdocs build` | Build static HTML |

### Slidev Commands

| Command | Description |
|---------|-------------|
| `py-docs slidev list` | List presentations |
| `py-docs slidev create <name>` | Create new presentation |
| `py-docs slidev start [name]` | Start presentation server |
| `py-docs slidev stop` | Stop presentation server |
| `py-docs slidev export [name]` | Export to PDF |
| `py-docs slidev open` | Open browser to running server |
| `py-docs slidev build` | Build Docker image |

## Tips and Tricks

### Auto-detection

Many Slidev commands support auto-detection. If you're in a presentation directory, you don't need to specify the name:

```bash
cd slides/my-presentation
py-docs slidev start  # Auto-detects 'my-presentation'
```

### Interactive Selection

If you don't specify a presentation name, you'll get an interactive list to choose from:

```bash
py-docs slidev start
# Shows a list to select from
```

### Keyboard Shortcuts (Slidev)

When presenting:

- `Space` or `→` - Next slide
- `←` - Previous slide
- `f` - Fullscreen
- `o` - Overview mode
- `d` - Dark mode toggle
- `g` - Go to slide (type number)

## Next Steps

- Learn more about [MkDocs configuration](https://www.mkdocs.org/)
- Explore [Slidev features](https://sli.dev/)
- Check out the [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) documentation
- Read about [Markdown extensions](https://squidfunk.github.io/mkdocs-material/reference/)

