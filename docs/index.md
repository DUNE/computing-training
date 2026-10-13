---
title: DUNE Computing Training
hide:
  - navigation
  - toc
---

<section class="dt-hero" markdown>
# DUNE computing training

Self-paced tutorials for new collaborators: from your first login to the DUNE machines, through running LArSoft, to submitting jobs and analysing data. DUNE Software and Computing maintains the core lessons, and the HEP Software Foundation (HSF) lessons fill in the general skills.

<div class="dt-hero__actions" markdown>
[Start with Computing Basics](https://dune.github.io/computing-basics/){ .md-button .md-button--primary }
[Get help on Slack](https://dunescience.slack.com/archives/C02TJDHUQPR){ .md-button }
</div>
</section>

## Start here { #start-here }

Work through these three DUNE lessons in order. Each one builds on the last.

{{ path_cards(learning_path) }}

<p class="dt-subhead">New to the shell, git or Python? Do these first:</p>

{{ prereq_pills(before_you_start) }}

## Find a tutorial { #catalog }

{{ card_count(sections) }} more tutorials and references, from DUNE and from the wider HEP community. Use the filters to narrow them down.

{{ filter_bar(sections) }}

{% for section in sections %}
<h3 class="dt-section" id="{{ section.id }}">{{ section.title }}</h3>

<p class="dt-section__intro">{{ section.intro }}</p>

{{ card_grid(section) }}
{% endfor %}

## Getting help { #help }

<div class="dt-help" markdown>
<div markdown>
**Slack.** Ask in [#computing_training_basics](https://dunescience.slack.com/archives/C02TJDHUQPR) on the DUNE Slack. The training team and other learners answer there.
</div>
<div markdown>
**Email.** Write to [dune-computing-training@fnal.gov](mailto:dune-computing-training@fnal.gov).
</div>
<div markdown>
**Found a problem in a lesson?** Open an issue on that lesson's repository, linked from its card.
</div>
</div>

<p class="dt-footnote">Inspired by the <a href="https://hsf-training.org/training-center/">HSF Training Center</a>. Want your tutorial listed? See <a href="contributing/">Add a tutorial</a>.</p>
