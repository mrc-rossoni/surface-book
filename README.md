# Surface Modeling for Engineering Applications - Course Book

This repository contains the course book and supporting Python code for the
Master-level course **Surface Modeling for Engineering Applications**.

The book is authored with MyST Markdown and published as a GitHub Pages site.
Laboratory notebooks can also be opened from the book and run in Google Colab.

## Repository Layout

- `myst.yml` configures the MyST project, table of contents, bibliography, and
  site theme.
- `book/` contains the course chapters, figures, bibliography, and glossary.
- `code/` contains notebooks and small Python helpers used by the labs.
- `.github/workflows/deploy_book.yml` builds and deploys the site to GitHub
  Pages.
- `requirements.txt` lists the Python dependencies needed for local execution
  and for the GitHub Actions build.

## Prerequisites

Install these tools before running the book locally:

- Python 3.11 or newer
- Node.js 20 or newer, including `npm`
- Git

## Start The Book Locally

1. Clone the repository and enter it.

```bash
git clone https://github.com/mrc-rossoni/surface-book.git
cd surface-book
```

2. Create a Python virtual environment.

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install Python dependencies.

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

4. Register the Jupyter kernel used when MyST executes code cells.

```bash
python -m ipykernel install --user --name python3 --display-name "Python 3 (ipykernel)"
```

5. Install the MyST command line tool.

```bash
npm install -g mystmd
```

6. Start the local preview server.

```bash
myst start
```

Open the localhost URL printed by MyST, usually `http://localhost:3000`. If that
port is already in use, MyST will print a different port.

7. Run the same HTML build used by GitHub Pages.

Windows PowerShell:

```powershell
$env:BASE_URL = "/surface-book"
myst build --execute --html
```

macOS/Linux:

```bash
BASE_URL=/surface-book myst build --execute --html
```

The generated site is written to `_build/html`.

## Running Notebooks In Colab

The book links selected notebooks with an "Open in Colab" badge. In Colab, run
the setup cell first when a notebook provides one. That cell installs the
repository dependencies and makes the local `code/` folder importable.

## GitHub Pages Workflow

The deployment workflow lives in `.github/workflows/deploy_book.yml`.

It runs whenever a commit is pushed to `main`.

### Build Job

The `build` job prepares the site artifact:

1. Checks out the repository with `actions/checkout`.
2. Installs Node.js 20 with `actions/setup-node`.
3. Installs Python 3.11 with `actions/setup-python`.
4. Upgrades `pip` and installs Python dependencies from `requirements.txt`.
5. Registers a `python3` Jupyter kernel so MyST can execute code cells.
6. Installs the MyST CLI globally with `npm install -g mystmd`.
7. Builds the site with:

```bash
BASE_URL=/surface-book myst build --execute --html
```

`BASE_URL=/surface-book` is required because the site is deployed as a GitHub
Pages project site under the repository name.

8. Prints a short debug listing of generated `index.html` files.
9. Uploads `_build/html` with `actions/upload-pages-artifact`.

### Deploy Job

The `deploy` job starts after the build artifact is ready. It uses
`actions/deploy-pages` to publish `_build/html` to GitHub Pages and exposes the
published URL through the `github-pages` environment.

## Updating Dependencies

When a chapter, notebook, or code cell needs a new Python package, add it to
`requirements.txt`. This keeps local execution, Colab setup, and the GitHub
Pages build aligned.
