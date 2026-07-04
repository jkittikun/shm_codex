from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.offline import get_plotlyjs
from plotly.subplots import make_subplots


BRAND = {
    "violet": "#6B4CF0",
    "magenta": "#C24BE0",
    "cyan": "#19B6CC",
    "ink": "#18181F",
    "slate": "#5B5B6B",
    "line": "#E5E4EA",
}


@dataclass(frozen=True)
class LabPage:
    slug: str
    title: str
    summary: str
    figure: go.Figure
    notes: tuple[str, ...]


def damped_sine(
    time: np.ndarray,
    frequency_hz: float,
    damping_ratio: float,
    amplitude: float = 1.0,
    phase_rad: float = 0.0,
) -> np.ndarray:
    """Return a damped sinusoid using exp(-zeta * omega_n * t)."""
    if frequency_hz <= 0:
        raise ValueError("frequency_hz must be positive")
    if damping_ratio < 0:
        raise ValueError("damping_ratio must be non-negative")
    omega_n = 2.0 * np.pi * frequency_hz
    return amplitude * np.exp(-damping_ratio * omega_n * time) * np.sin(omega_n * time + phase_rad)


def single_sided_fft(signal: np.ndarray, sample_rate_hz: float) -> tuple[np.ndarray, np.ndarray]:
    """Return single-sided FFT frequency and amplitude arrays."""
    if sample_rate_hz <= 0:
        raise ValueError("sample_rate_hz must be positive")
    values = np.asarray(signal, dtype=float)
    if values.ndim != 1 or values.size < 2:
        raise ValueError("signal must be a one-dimensional array with at least two samples")

    centered = values - np.mean(values)
    frequency = np.fft.rfftfreq(centered.size, d=1.0 / sample_rate_hz)
    amplitude = np.abs(np.fft.rfft(centered)) * 2.0 / centered.size
    amplitude[0] *= 0.5
    if centered.size % 2 == 0:
        amplitude[-1] *= 0.5
    return frequency, amplitude


def shear_building_mode_shape(stories: int, mode: int) -> np.ndarray:
    """Return a normalized sine mode shape for a simple shear-building sketch."""
    if stories < 2:
        raise ValueError("stories must be at least 2")
    if mode < 1 or mode > stories:
        raise ValueError("mode must be between 1 and stories")
    floors = np.arange(1, stories + 1)
    shape = np.sin(mode * np.pi * floors / (stories + 1))
    return shape / np.max(np.abs(shape))


def strongest_sensor_floors(mode_shape: np.ndarray, count: int) -> np.ndarray:
    """Select floor numbers with the largest modal amplitudes."""
    if count < 1:
        raise ValueError("count must be at least 1")
    if count > mode_shape.size:
        raise ValueError("count cannot exceed number of floors")
    selected = np.argsort(np.abs(mode_shape))[-count:] + 1
    return np.sort(selected)


def _style_figure(fig: go.Figure, title: str) -> go.Figure:
    fig.update_layout(
        title={"text": title, "x": 0.02, "xanchor": "left"},
        font={"family": "IBM Plex Sans, Arial, sans-serif", "color": BRAND["ink"]},
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        margin={"l": 58, "r": 24, "t": 92, "b": 56},
        hovermode="x unified",
        legend={"orientation": "h", "y": 1.18, "x": 0.0},
    )
    fig.update_xaxes(gridcolor=BRAND["line"], zerolinecolor=BRAND["line"])
    fig.update_yaxes(gridcolor=BRAND["line"], zerolinecolor=BRAND["line"])
    return fig


def _visibility_steps(names: list[str], traces_per_step: int) -> list[dict]:
    steps = []
    trace_count = len(names) * traces_per_step
    for index, name in enumerate(names):
        visible = [False] * trace_count
        start = index * traces_per_step
        for offset in range(traces_per_step):
            visible[start + offset] = True
        steps.append({"label": name, "method": "update", "args": [{"visible": visible}]})
    return steps


def signal_synthesis_lab() -> LabPage:
    sample_rate = 100.0
    time = np.arange(0.0, 12.0, 1.0 / sample_rate)
    losses = [0, 4, 8, 12, 16, 20]

    def response(loss_percent: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        loss = loss_percent / 100.0
        f1 = 2.6 * np.sqrt(1.0 - 0.85 * loss)
        f2 = 6.7 * np.sqrt(1.0 - 0.45 * loss)
        f3 = 10.8
        signal = (
            damped_sine(time, f1, 0.012, amplitude=1.0)
            + damped_sine(time, f2, 0.02, amplitude=0.38, phase_rad=0.4)
            + damped_sine(time, f3, 0.035, amplitude=0.18, phase_rad=1.1)
        )
        frequency, amplitude = single_sided_fft(signal, sample_rate)
        return signal, frequency, amplitude

    fig = make_subplots(rows=1, cols=2, subplot_titles=("Time response", "Frequency content"))
    frame_names = [f"{loss}%" for loss in losses]
    for index, loss in enumerate(losses):
        signal, frequency, amplitude = response(loss)
        visible = index == 0
        fig.add_trace(
            go.Scatter(
                x=time,
                y=signal,
                mode="lines",
                name="response",
                visible=visible,
                line={"color": BRAND["violet"], "width": 2},
                showlegend=index == 0,
            ),
            row=1,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                x=frequency,
                y=amplitude,
                mode="lines",
                name="FFT amplitude",
                visible=visible,
                line={"color": BRAND["magenta"], "width": 2},
                showlegend=index == 0,
            ),
            row=1,
            col=2,
        )
    fig.update_layout(
        sliders=[
            {
                "active": 0,
                "currentvalue": {"prefix": "Stiffness loss: "},
                "pad": {"t": 46},
                "steps": _visibility_steps(frame_names, traces_per_step=2),
            }
        ]
    )
    fig.update_xaxes(title_text="Time, s", row=1, col=1)
    fig.update_yaxes(title_text="Acceleration, normalized", row=1, col=1)
    fig.update_xaxes(title_text="Frequency, Hz", range=[0, 14], row=1, col=2)
    fig.update_yaxes(title_text="Amplitude", row=1, col=2)
    _style_figure(fig, "Vibration signal synthesis")
    return LabPage(
        slug="signal-synthesis",
        title="Vibration signal synthesis",
        summary="Move the stiffness-loss slider to see a synthetic response shift in time and frequency.",
        figure=fig,
        notes=(
            "Frequency shifts are exaggerated for teaching clarity.",
            "The response is generated from damped modal components.",
            "A lower first frequency is a common damage-sensitive feature, but interpretation needs context.",
        ),
    )


def fft_resolution_lab() -> LabPage:
    sample_rate = 80.0
    durations = [2, 4, 8, 12, 16, 20]

    def response(duration: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        time = np.arange(0.0, float(duration), 1.0 / sample_rate)
        signal = np.sin(2.0 * np.pi * 2.0 * time) + 0.72 * np.sin(2.0 * np.pi * 2.35 * time)
        frequency, amplitude = single_sided_fft(signal, sample_rate)
        return time, signal, frequency, amplitude

    fig = make_subplots(rows=1, cols=2, subplot_titles=("Signal window", "FFT estimate"))
    frame_names = [f"{duration}s" for duration in durations]
    for index, duration in enumerate(durations):
        time, signal, frequency, amplitude = response(duration)
        visible = index == 0
        fig.add_trace(
            go.Scatter(
                x=time,
                y=signal,
                mode="lines",
                name="signal",
                visible=visible,
                line={"color": BRAND["violet"], "width": 2},
                showlegend=index == 0,
            ),
            row=1,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                x=frequency,
                y=amplitude,
                mode="lines",
                name="spectrum",
                visible=visible,
                line={"color": BRAND["cyan"], "width": 2},
                showlegend=index == 0,
            ),
            row=1,
            col=2,
        )
    fig.update_layout(
        sliders=[
            {
                "active": 0,
                "currentvalue": {"prefix": "Record length: "},
                "pad": {"t": 46},
                "steps": _visibility_steps(frame_names, traces_per_step=2),
            }
        ]
    )
    fig.update_xaxes(title_text="Time, s", range=[0, max(durations)], row=1, col=1)
    fig.update_yaxes(title_text="Amplitude", row=1, col=1)
    fig.update_xaxes(title_text="Frequency, Hz", range=[0, 6], row=1, col=2)
    fig.update_yaxes(title_text="Single-sided amplitude", row=1, col=2)
    _style_figure(fig, "FFT frequency resolution")
    return LabPage(
        slug="fft-resolution",
        title="FFT frequency resolution",
        summary="Change the record length to see how closely spaced frequencies become easier to separate.",
        figure=fig,
        notes=(
            "Short records blur nearby frequency content.",
            "Sampling rate controls the highest observable frequency.",
            "Record duration controls the frequency spacing of FFT bins.",
        ),
    )


def damping_decay_lab() -> LabPage:
    time = np.linspace(0.0, 14.0, 1400)
    frequency = 2.2
    damping_ratios = [0.005, 0.01, 0.02, 0.04, 0.06, 0.10]

    def response(zeta: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        displacement = damped_sine(time, frequency, zeta)
        envelope = np.exp(-zeta * 2.0 * np.pi * frequency * time)
        return displacement, envelope, -envelope

    fig = go.Figure()
    frame_names = [f"{zeta:.3f}" for zeta in damping_ratios]
    for index, zeta in enumerate(damping_ratios):
        displacement, upper, lower = response(zeta)
        visible = index == 0
        fig.add_trace(
            go.Scatter(
                x=time,
                y=displacement,
                mode="lines",
                name="free decay",
                visible=visible,
                line={"color": BRAND["violet"], "width": 2},
                showlegend=index == 0,
            )
        )
        fig.add_trace(
            go.Scatter(
                x=time,
                y=upper,
                mode="lines",
                name="envelope",
                visible=visible,
                line={"color": BRAND["magenta"], "dash": "dash"},
                showlegend=index == 0,
            )
        )
        fig.add_trace(
            go.Scatter(
                x=time,
                y=lower,
                mode="lines",
                visible=visible,
                showlegend=False,
                line={"color": BRAND["magenta"], "dash": "dash"},
            )
        )
    fig.update_layout(
        sliders=[
            {
                "active": 0,
                "currentvalue": {"prefix": "Damping ratio: "},
                "pad": {"t": 46},
                "steps": _visibility_steps(frame_names, traces_per_step=3),
            }
        ]
    )
    fig.update_xaxes(title_text="Time, s")
    fig.update_yaxes(title_text="Displacement, normalized")
    _style_figure(fig, "Damping and free decay")
    return LabPage(
        slug="damping-decay",
        title="Damping and free decay",
        summary="Adjust damping ratio to see how quickly a free-vibration response loses amplitude.",
        figure=fig,
        notes=(
            "The envelope follows exp(-zeta omega_n t).",
            "Small damping changes can be visible over several cycles.",
            "Real measurements need filtering and peak-picking care.",
        ),
    )


def mode_shape_sensor_lab() -> LabPage:
    stories = 6
    floors = np.arange(1, stories + 1)
    modes = [1, 2, 3, 4]
    sensor_count = 3

    fig = go.Figure()
    frame_names = [f"Mode {mode}" for mode in modes]
    for index, mode in enumerate(modes):
        shape = shear_building_mode_shape(stories, mode)
        sensors = strongest_sensor_floors(shape, sensor_count)
        visible = index == 0
        fig.add_trace(
            go.Scatter(
                x=shape,
                y=floors,
                mode="lines+markers",
                name="mode shape",
                visible=visible,
                line={"color": BRAND["violet"], "width": 3},
                marker={"size": 9},
                showlegend=index == 0,
            )
        )
        fig.add_trace(
            go.Scatter(
                x=shape[sensors - 1],
                y=sensors,
                mode="markers",
                name="suggested sensors",
                visible=visible,
                marker={"size": 15, "color": BRAND["magenta"], "line": {"color": "#FFFFFF", "width": 1.5}},
                showlegend=index == 0,
            )
        )
    fig.update_layout(
        sliders=[
            {
                "active": 0,
                "currentvalue": {"prefix": ""},
                "pad": {"t": 46},
                "steps": _visibility_steps(frame_names, traces_per_step=2),
            }
        ]
    )
    fig.update_xaxes(title_text="Normalized modal displacement", range=[-1.1, 1.1], zeroline=True)
    fig.update_yaxes(title_text="Floor", tickmode="array", tickvals=floors)
    _style_figure(fig, "Mode shape and sensor placement")
    return LabPage(
        slug="mode-shape-sensors",
        title="Mode shape and sensor placement",
        summary="Move between mode shapes and observe which floors carry the strongest modal response.",
        figure=fig,
        notes=(
            "This is a teaching sketch, not an optimal experimental design algorithm.",
            "Sensors are placed at the largest absolute modal amplitudes.",
            "Real placement also considers access, noise, redundancy, and target modes.",
        ),
    )


def build_all_labs() -> tuple[LabPage, ...]:
    return (
        signal_synthesis_lab(),
        fft_resolution_lab(),
        damping_decay_lab(),
        mode_shape_sensor_lab(),
    )


def write_lab_page(lab: LabPage, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    plotly_bundle = output_dir / "plotly.min.js"
    if not plotly_bundle.exists():
        plotly_bundle.write_text(get_plotlyjs(), encoding="utf-8")

    figure_html = lab.figure.to_html(
        full_html=False,
        include_plotlyjs="plotly.min.js",
        default_width="100%",
        default_height="460px",
        config={"responsive": True, "displaylogo": False},
    )
    notes_html = "\n".join(f"<p>{note}</p>" for note in lab.notes)
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{lab.title}</title>
  <link rel="stylesheet" href="../../assets/css/site.css">
</head>
<body class="lab-page">
  <main class="lab-container">
    <header class="lab-header">
      <p class="kj-label"><span class="gradient-dot"></span>Interactive SHM lab</p>
      <h1>{lab.title}</h1>
      <p>{lab.summary}</p>
    </header>
    {figure_html}
    <section class="lab-notes" aria-label="Lab notes">
      {notes_html}
    </section>
  </main>
</body>
</html>
"""
    destination = output_dir / f"{lab.slug}.html"
    destination.write_text(html, encoding="utf-8")
    return destination
