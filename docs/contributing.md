# Add a tutorial

Every card on the [training catalog](index.md) comes from one file, [`data/modules.yml`](https://github.com/DUNE/training/blob/main/data/modules.yml). To list a tutorial, add an entry to the right section of that file and open a pull request. You do not need to edit any page.

## A card entry

```yaml
- title: WAFFLES
  url: https://waffles.readthedocs.io/
  repo: https://github.com/DUNE/waffles
  logo: waffles-logo.png
  provider: dune
  level: intermediate
  description: >-
    Analyse photon detector waveforms from ProtoDUNE with this Python
    framework and its examples.
```

| Field | Required | Values |
|---|---|---|
| `title` | yes | Card heading |
| `url` | yes | Where the title links: the rendered site if there is one, otherwise the repository |
| `description` | yes | One or two sentences on what the learner does |
| `logo` | one of `logo` or `icon` | The project's own logo, added to `docs/images/logos/`. SVG is best; a PNG should be at least 300 px wide. Record where it came from in `LOGOS.md` |
| `icon` | one of `logo` or `icon` | A [Lucide icon](https://lucide.dev/icons/) name, such as `atom` or `database`, for projects with no logo |

Database documentation uses `db-stack-1.svg`, `db-stack-2.svg` or `db-stack-3.svg` as its logo. The number of filled discs matches the level: 1 for beginner, 2 for intermediate, 3 for advanced.
| `provider` | yes | `dune`, `hsf` or `carpentries` |
| `level` | yes | `prerequisite`, `beginner`, `intermediate` or `advanced` |
| `repo` | no | Source repository. Shown as a separate link when it differs from `url` |
| `video` | no | Link to recordings |
| `status` | no | `beta`, `in-development` or `coming-soon`. Leave it out for stable material |

The build checks these fields. A missing required field, an unknown level or a logo file or icon name that does not exist stops the build with a message naming the card.

## What belongs here

- Tutorials and lessons that someone can work through on their own.
- Reference documentation for DUNE tools that new collaborators need.
- General HEP lessons, mostly from the [HSF Training Center](https://hsf-training.org/training-center/), that DUNE newcomers find useful.

Analysis code without a guide or example is better listed in the relevant working group's pages.

## Preview your change

```bash
uv venv ~/venvs/dune-training
UV_PROJECT_ENVIRONMENT=~/venvs/dune-training uv sync --locked
UV_PROJECT_ENVIRONMENT=~/venvs/dune-training uv run --locked zensical serve
```

Then open <http://localhost:8000/training/>.
