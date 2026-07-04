# Structural Health Monitoring academic website

This repository contains a static academic website for research, teaching, and the Structural Health Monitoring module.

The site is designed for local editing with Markdown and Python:

- edit normal pages in `docs/`;
- edit reusable course/publication metadata in `data/`;
- edit interactive lab logic in `src/shm_site/interactives/`;
- regenerate interactive pages with `python scripts/build_interactives.py`;
- preview the site with `mkdocs serve`.

## Local setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/build_interactives.py
mkdocs serve
```

MkDocs will print a local URL, usually `http://127.0.0.1:8000/`.

## Production build

```bash
python scripts/build_interactives.py
mkdocs build --strict
```

The static site is written to `site/`.

## GitHub Pages first

This repository includes a GitHub Actions workflow at `.github/workflows/deploy-pages.yml`.

After the project is pushed to GitHub:

1. Open the repository on GitHub.
2. Go to Settings > Pages.
3. Set Build and deployment > Source to GitHub Actions.
4. Push to the `main` branch, or run the `Deploy GitHub Pages` workflow manually.

The workflow installs Python dependencies, generates the interactive labs, runs `mkdocs build --strict`, uploads the `site/` artifact, and deploys it to GitHub Pages.

For a project repository, the first public URL will usually look like:

```text
https://YOUR-USERNAME.github.io/YOUR-REPOSITORY/
```

## Cloudflare Pages later

Connect the GitHub repository to Cloudflare Pages and use:

- build command: `pip install -r requirements.txt && python scripts/build_interactives.py && mkdocs build`
- build output directory: `site`

After the first deployment, add the custom domain in the Cloudflare Pages project settings.
