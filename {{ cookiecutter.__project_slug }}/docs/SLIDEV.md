# Slidev Presentations Guide

This guide covers how to work with Slidev presentations in {{ cookiecutter.project_name }}.

## What is Slidev?

[Slidev](https://sli.dev/) is a presentation tool for developers. It lets you create presentations using Markdown with features like:

- Code highlighting with line numbers
- Interactive components
- Export to PDF
- Presenter mode
- Live reload during development

## Getting Started

### List Presentations

To see all available presentations:

```bash
py-docs slidev list
```

### Create a New Presentation

```bash
py-docs slidev create my-presentation
```

This creates a new Slidev project in `slides/my-presentation/` with:
- `slides.md` - Main presentation file
- `package.json` - Node.js dependencies
- Basic configuration and examples

### Start a Presentation

```bash
py-docs slidev start my-presentation
```

Or, if you're in the presentation directory:

```bash
cd slides/my-presentation
py-docs slidev start
```

The presentation opens at `http://localhost:3030` with hot-reload enabled.

### Stop the Server

```bash
py-docs slidev stop
```

### Export to PDF

```bash
py-docs slidev export my-presentation
```

The PDF is saved as `slides-export.pdf` in the presentation directory.

## Presentation Structure

### Basic Slide

```markdown
---
theme: default
---

# My Presentation

First slide content

---

# Second Slide

More content here
```

### Using Pages

For complex presentations, split content into separate files:

```markdown
<!-- slides.md -->
---
src: ./pages/introduction.md
---

---
src: ./pages/features.md
---
```

### Frontmatter Configuration

Configure your presentation in the frontmatter:

```yaml
---
theme: seriph
title: My Presentation
info: |
  ## My Presentation
  Description here
drawings:
  persist: false
transition: slide-left
mdc: true
---
```

## Writing Slides

### Code Blocks

````markdown
```python
def hello():
    print("Hello, World!")
```
````

### Code Highlighting

Highlight specific lines:

````markdown
```python {2,4-6}
def fibonacci(n):
    if n <= 1:  # highlighted
        return n
    return (
        fibonacci(n-1) +  # highlighted
        fibonacci(n-2)    # highlighted
    )
```
````

### Click Animations

Use `<v-clicks>` for click-through animations:

```markdown
<v-clicks>

- First point (click to reveal)
- Second point (click to reveal)
- Third point (click to reveal)

</v-clicks>
```

### Two-Column Layout

```markdown
<div grid="~ cols-2 gap-4">
<div>

## Left Column

Content here

</div>
<div>

## Right Column

More content

</div>
</div>
```

### Images

Place images in the `public/` directory:

```markdown
![My Image](/my-image.png)
```

### Vue Components

Create custom components in `components/`:

```vue
<!-- components/MyComponent.vue -->
<template>
  <div class="my-component">
    <h3>{% raw %}{{ title }}{% endraw %}</h3>
    <p>{% raw %}{{ content }}{% endraw %}</p>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  content: String
})
</script>

<style scoped>
.my-component {
  padding: 1rem;
  border: 2px solid #42b983;
}
</style>
```

Use in slides:

```markdown
<MyComponent title="Hello" content="World" />
```

## Layouts

Slidev provides various layouts:

```markdown
---
layout: center
class: text-center
---

# Centered Content

---
layout: two-cols
---

# Left Column

::right::

# Right Column

---
layout: image-right
image: /my-image.png
---

# Content with Image

---
layout: end
---

# Thank You!
```

## Keyboard Shortcuts

When presenting:

- `Space` or `→` - Next slide
- `←` - Previous slide
- `f` - Fullscreen
- `o` - Overview mode
- `d` - Dark mode toggle
- `g` - Go to slide (type number)
- `Escape` - Exit fullscreen/overview

## Themes

Change themes in the frontmatter:

```yaml
---
theme: default  # or seriph, apple-basic, etc.
---
```

Available themes:
- `default` - Clean and minimal
- `seriph` - Elegant with nice transitions
- `apple-basic` - Apple-style presentation
- And many more on [Slidev Themes](https://sli.dev/themes/gallery.html)

## Best Practices

1. **Keep it Simple** - One main point per slide
2. **Use Visuals** - Images and diagrams over text
3. **Code Examples** - Use syntax highlighting
4. **Practice** - Use presenter mode to practice
5. **Export Early** - Test PDF export before presenting

## Troubleshooting

### Port Already in Use

If port 3030 is busy, stop the server:

```bash
py-docs slidev stop
```

### Dependencies Not Installed

Delete `node_modules` and restart:

```bash
cd slides/my-presentation
rm -rf node_modules
py-docs slidev start
```

### Export Fails

Ensure Chromium is installed in the Docker image. The setup includes this by default.

## Resources

- [Slidev Documentation](https://sli.dev/)
- [Markdown Syntax](https://sli.dev/guide/syntax.html)
- [Animations Guide](https://sli.dev/guide/animations.html)
- [Themes Gallery](https://sli.dev/themes/gallery.html)
- [Customization](https://sli.dev/custom/)

