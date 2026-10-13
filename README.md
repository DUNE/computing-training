# DUNE Computing Training

Source for the DUNE training landing page at <https://dune.github.io/training/>. The page collects the DUNE Software and Computing lessons ([Computing Basics](https://dune.github.io/computing-basics/), [LArSoft Basics](https://dune.github.io/computing-basics-larsoft/), [Batch Computing](https://dune.github.io/computing-basics-batch/)), DUNE tool documentation, physics and analysis tutorials, and starter lessons from the [HSF Training Center](https://hsf-training.org/training-center/).

The site is built with [Zensical](https://zensical.org/), following the setup of [dune-phlex-project](https://github.com/DUNE/dune-phlex-project) and [dune-spack-project](https://github.com/DUNE/dune-spack-project).

## Add a tutorial

Add an entry to [`data/modules.yml`](data/modules.yml) and open a pull request. The [Add a tutorial](docs/contributing.md) page lists the fields. You do not need to touch any page or template.

## How it works

| File | Role |
|---|---|
| `data/modules.yml` | Every card: the Start-here path, the prerequisite links and the catalog sections |
| `main.py` | Zensical macros that turn the YAML into card HTML and check each entry |
| `docs/index.md` | The page layout, calling the macros |
| `docs/images/logos/` | Project logos shown on the cards. Sources are listed in [`LOGOS.md`](LOGOS.md) |
| `docs/stylesheets/extra.css` | DUNE colours (Okabe-Ito, from `dune_plot_style`) and card styles |
| `docs/javascripts/filters.js` | Level and provider filters |

## Build locally

Keep the Python environment outside the repository:

```bash
uv venv ~/venvs/dune-training
UV_PROJECT_ENVIRONMENT=~/venvs/dune-training uv sync --locked
PYTHONDONTWRITEBYTECODE=1 UV_PROJECT_ENVIRONMENT=~/venvs/dune-training uv run --locked zensical serve
```

`PYTHONDONTWRITEBYTECODE=1` stops Python from leaving a `__pycache__` folder in the repository when it imports `main.py`.

In CI, run `uv sync --locked` directly without the `UV_PROJECT_ENVIRONMENT` override.

## Help

Ask in `#computing_training_basics` on the DUNE Slack or write to dune-computing-training@fnal.gov.
