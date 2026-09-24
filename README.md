# Student release

This package is the **24 September 2026 classroom-draft release** of the ENV2301 e-book. The source remains intentionally editable: later versions can replace figures, revise chapters and add interactive material without changing the basic Quarto workflow.

# ENV2301: Methods & Techniques for Environmental Studies

## Ready-to-use student site

A complete browser build is included in `_site/`. Open `_site/index.html` to view the current classroom release locally. When the project is published through the included GitHub Actions workflow, Quarto will regenerate the site from the `.qmd` source files.

This folder is the editable source of the browser-based ENV2301 course book. The chapter files are Quarto Markdown (`.qmd`); the generated HTML in `_site/` is output and should not be edited directly.

## Open and edit in RStudio

1. Double-click `ENV2301_ebook.Rproj` (or use **File > Open Project** in RStudio).
2. Open any chapter `.qmd` file. Use **Visual** mode for ordinary prose editing or **Source** mode when you want to see the Quarto/Markdown syntax.
3. Save the `.qmd` file. Figures belong in `figures/` or `media/`; book-wide formatting is controlled by `_quarto.yml` and `styles.css`.

## Preview or render

If RStudio has Quarto available, use **Render** / **Preview** from the IDE. From the Terminal, the equivalent commands are:

```bash
quarto preview
```

for a live browser preview, or

```bash
quarto render
```

to render the complete book. The finished site is written to `_site/`.

If RStudio does not show Quarto rendering options, install or update Quarto from quarto.org and reopen the project.

## Publish to GitHub Pages

The repository includes `.github/workflows/publish.yml`. Once the project is in a GitHub repository with `main` as its default branch, pushes to `main` can render the book and publish `_site/` to the `gh-pages` branch. GitHub Pages then needs to be configured to serve from that branch. The public book URL can be linked from Canvas.


## GitHub Pages deployment note (24 September 2026)

This copy uses GitHub's current Pages Actions deployment workflow. In the GitHub repository, set **Settings > Pages > Build and deployment > Source** to **GitHub Actions**. A push to `main` will render the Quarto book and deploy the rendered `_site/` directory.
