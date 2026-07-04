---
title: Interactive labs
description: Static Plotly labs generated from Python.
---

# Interactive labs

<p class="page-lead">
Each lab below is generated from Python and runs in the browser as static HTML. No server-side Python is required after deployment.
</p>

## Vibration signal synthesis

<iframe class="interactive-frame" title="Vibration signal synthesis lab" data-lab-src="../../generated/interactives/signal-synthesis.html"></iframe>

<a class="button button--small" href="#" data-lab-href="../../generated/interactives/signal-synthesis.html">Open full lab</a>

## FFT frequency resolution

<iframe class="interactive-frame" title="FFT frequency resolution lab" data-lab-src="../../generated/interactives/fft-resolution.html"></iframe>

<a class="button button--small" href="#" data-lab-href="../../generated/interactives/fft-resolution.html">Open full lab</a>

## Damping and free decay

<iframe class="interactive-frame" title="Damping and free decay lab" data-lab-src="../../generated/interactives/damping-decay.html"></iframe>

<a class="button button--small" href="#" data-lab-href="../../generated/interactives/damping-decay.html">Open full lab</a>

## Mode shape and sensor placement

<iframe class="interactive-frame" title="Mode shape and sensor placement lab" data-lab-src="../../generated/interactives/mode-shape-sensors.html"></iframe>

<a class="button button--small" href="#" data-lab-href="../../generated/interactives/mode-shape-sensors.html">Open full lab</a>

## Editing workflow

Update lab logic in `src/shm_site/interactives/labs.py`, then run:

```bash
python scripts/build_interactives.py
mkdocs serve
```
