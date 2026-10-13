"""Macros that render the training catalog from data/modules.yml.

Zensical's built-in macros extension imports this module (module_name =
"main") and calls define_env once per page. docs/index.md passes the YAML
data in explicitly, e.g. ``{{ card_grid(section) }}``, so a missing or
misnamed data file fails the build instead of rendering an empty page.

A card shows the project's own logo when it has one (``logo``, a file in
docs/images/logos/). Cards without a logo fall back to an icon inlined from
the Lucide set that ships with Zensical, because Markdown icon shortcodes are
not expanded inside raw HTML.
"""

from __future__ import annotations

from functools import cache
from html import escape
from pathlib import Path

import zensical

ICON_DIR = Path(zensical.__file__).parent / "templates" / ".icons" / "lucide"
LOGO_DIR = Path(__file__).parent / "docs" / "images" / "logos"

PROVIDERS = {
    "dune": "DUNE",
    "hsf": "HSF",
    "carpentries": "Carpentries",
}
LEVELS = {
    "prerequisite": "Prerequisite",
    "beginner": "Beginner",
    "intermediate": "Intermediate",
    "advanced": "Advanced",
}
STATUSES = {
    "beta": "Beta",
    "in-development": "In development",
    "coming-soon": "Coming soon",
}
REQUIRED = ("title", "url", "description", "provider", "level")


@cache
def icon(name: str) -> str:
    path = ICON_DIR / f"{name}.svg"
    if not path.is_file():
        raise ValueError(f"Unknown Lucide icon '{name}' (looked in {ICON_DIR})")
    # One line, so the SVG never breaks out of the surrounding raw HTML block.
    svg = " ".join(path.read_text(encoding="utf-8").split())
    return svg.replace("<svg ", '<svg aria-hidden="true" focusable="false" ', 1)


def _check(card: dict) -> None:
    missing = [key for key in REQUIRED if not card.get(key)]
    if missing:
        raise ValueError(f"Card {card.get('title', card)!r} is missing {missing}")
    for key, allowed in (("provider", PROVIDERS), ("level", LEVELS)):
        if card[key] not in allowed:
            raise ValueError(f"Card {card['title']!r}: {key} must be one of {list(allowed)}")
    if not any(card.get(key) for key in ("logo", "icon", "emoji")):
        raise ValueError(f"Card {card['title']!r} needs a logo, an icon or an emoji")
    if card.get("status") and card["status"] not in STATUSES:
        raise ValueError(f"Card {card['title']!r}: status must be one of {list(STATUSES)}")


@cache
def logo(name: str) -> str:
    if not (LOGO_DIR / name).is_file():
        raise ValueError(f"Unknown logo '{name}' (looked in {LOGO_DIR})")
    # Decorative: the card title next to it already names the project.
    return f'<img src="images/logos/{escape(name)}" alt="" loading="lazy">'


def _media(card: dict, step: int | None = None) -> str:
    if step:
        if not card.get("emoji"):
            raise ValueError(f"Step {step} ({card['title']!r}) needs an emoji")
        return (
            '<div class="dt-card__media dt-card__media--step">'
            f'<span class="dt-step" aria-label="Step {step}">{step}</span>'
            f'<span class="dt-emoji" aria-hidden="true">{escape(card["emoji"])}</span></div>'
        )
    if card.get("logo"):
        return f'<div class="dt-card__media">{logo(card["logo"])}</div>'
    return f'<div class="dt-card__media dt-card__media--icon">{icon(card["icon"])}</div>'


def _meta(card: dict) -> str:
    parts = [PROVIDERS[card["provider"]], LEVELS[card["level"]]]
    if card.get("status"):
        parts.append(f'<em class="dt-status">{STATUSES[card["status"]]}</em>')
    if card.get("repo") and card["repo"] != card["url"]:
        parts.append(f'<a class="dt-card__link" href="{escape(card["repo"])}">Source</a>')
    if card.get("video"):
        parts.append(f'<a class="dt-card__link" href="{escape(card["video"])}">Videos</a>')
    return '<p class="dt-card__meta">' + '<span aria-hidden="true"> · </span>'.join(parts) + "</p>"


def _card(card: dict, step: int | None = None) -> str:
    _check(card)
    return (
        f'<article class="dt-card{" dt-card--step" if step else ""}" '
        f'data-provider="{card["provider"]}" data-level="{card["level"]}">'
        f"{_media(card, step)}"
        '<div class="dt-card__body">'
        f'<h3 class="dt-card__title"><a href="{escape(card["url"])}">{escape(card["title"])}</a></h3>'
        f'<p class="dt-card__desc">{escape(card["description"])}</p>'
        f"{_meta(card)}"
        "</div></article>"
    )


def define_env(env):
    @env.macro
    def path_cards(steps: list[dict]) -> str:
        """The numbered Start-here cards, joined by arrows."""
        arrow = f'<span class="dt-path__arrow">{icon("arrow-right")}</span>'
        cards = arrow.join(_card(step, step=step["step"]) for step in steps)
        return f'<div class="dt-path">{cards}</div>'

    @env.macro
    def prereq_pills(items: list[dict]) -> str:
        """A strip of pill links to prerequisite lessons."""
        pills = "".join(
            f'<a class="dt-pill" href="{escape(item["url"])}">'
            f'{logo(item["logo"]) if item.get("logo") else icon(item["icon"])}'
            f'<span>{escape(item["title"])}</span></a>'
            for item in items
        )
        return f'<div class="dt-pills">{pills}</div>'

    @env.macro
    def card_grid(section: dict) -> str:
        """One catalog section: a grid of filterable cards."""
        cards = "".join(_card(card) for card in section["cards"])
        return f'<div class="dt-grid" data-section="{escape(section["id"])}">{cards}</div>'

    @env.macro
    def filter_bar(sections: list[dict]) -> str:
        """Level and provider chips. docs/javascripts/filters.js wires them up."""
        cards = [card for section in sections for card in section["cards"]]
        levels = [key for key in LEVELS if any(c["level"] == key for c in cards)]
        providers = [key for key in PROVIDERS if any(c["provider"] == key for c in cards)]

        def group(name: str, label: str, keys: list[str], names: dict) -> str:
            chips = f'<button type="button" class="dt-chip" data-filter="{name}" data-value="" aria-pressed="true">All</button>'
            chips += "".join(
                f'<button type="button" class="dt-chip" data-filter="{name}" data-value="{key}" aria-pressed="false">{names[key]}</button>'
                for key in keys
            )
            return f'<div class="dt-filter__group" role="group" aria-label="{label}"><span class="dt-filter__label">{label}</span>{chips}</div>'

        return (
            '<div class="dt-filter" hidden>'
            + group("level", "Level", levels, LEVELS)
            + group("provider", "From", providers, PROVIDERS)
            + '<p class="dt-filter__empty" hidden>No tutorials match these filters.</p>'
            + "</div>"
        )

    @env.macro
    def card_count(sections: list[dict]) -> int:
        return sum(len(section["cards"]) for section in sections)
