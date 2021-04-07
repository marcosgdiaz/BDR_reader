# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 2021

@author: MGD
"""

import matplotlib.pyplot as plt
from matplotlib.collections import PathCollection
from matplotlib import rcParams
import numpy as np

fontsize = 16
rcParams["font.family"] = "serif"
rcParams["font.size"] = fontsize

_location = {
    "height": 0.64,
    "width": 0.74,
    "y_axis": 0.3,
    "x_axis_phase": 0.23,
    "x_axis_amp": 0.15,
    "x_text": 0.75,
    "y_text": 0.15,
}

_plot_param = {
    "amp_limits": (0, 35),
    "margins": (0, 0),
    "marker_size": 200,
    "shapes": ["^", "s", "o", "*", "d", "X"] * 2,
}

_visualization = {"fontsize": fontsize, "max_title_length": 30}

_fill_args = {"color": "blue", "alpha": 0.1, "interpolate": True}


class DisplayProperties:
    """Class in charge of initialiazing the axes."""

    # Default parameters
    axes_phase = None
    axes_amp = None
    marker_size = _plot_param["marker_size"]
    shapes = _plot_param["shapes"]
    upper_th = 0
    lower_th = 0
    invert = False
    shaded = False

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.box_text = plt.figtext(
            _location["x_text"],
            _location["y_text"],
            None,
            fontsize=_visualization["fontsize"],
        )
        self.lines_phase = self.axes_phase.collections
        self.lines_amp = self.axes_amp.collections

    def initialise_phase(self):
        """Initializing all the phase axes properties."""

        self.axes_phase.grid("on")
        chart_box = self.axes_phase.get_position()
        self.axes_phase.set_position(
            [
                chart_box.x0 + _location["x_axis_phase"],
                chart_box.y0 + _location["y_axis"],
                chart_box.width * _location["width"],
                chart_box.height * _location["height"],
            ]
        )

        self.axes_phase.set_xlabel("LF phase [rad]")
        self.axes_phase.set_ylabel("HF phase [rad]")
        self.axes_phase.margins(*_plot_param["margins"])
        self.axes_phase.set_ylim(-np.pi, np.pi)
        self.axes_phase.set_xlim(-np.pi, np.pi)

        y_low = [self.lower_th, self.lower_th]
        y_high = [self.upper_th, self.upper_th]
        lims = [-np.pi, np.pi]
        self.axes_phase.plot(lims, y_high, "k--")
        self.axes_phase.plot(lims, y_low, "k--")

    def initialise_amp(self):
        """Setting amplitude axes properties."""

        self.axes_amp.grid("on")
        chart_box = self.axes_amp.get_position()
        position = [
            chart_box.x0 + _location["x_axis_amp"],
            chart_box.y0 + _location["y_axis"],
            chart_box.width * _location["width"],
            chart_box.height * _location["height"],
        ]
        self.axes_amp.set_position(position)
        self.axes_amp.set_xlabel("LF amp [mV]")
        self.axes_amp.set_ylabel("HF amp [mV]")
        self.axes_amp.margins(*_plot_param["margins"])
        self.axes_amp.set_ylim(_plot_param["amp_limits"])
        self.axes_amp.set_xlim(_plot_param["amp_limits"])

    def invert_th(self, idx):
        """Defining bacteria region."""
        if idx == 1:
            self.invert = not self.invert
            self.draw_th()
            self.update_text()

        elif idx == 3:
            self.shaded = not self.shaded
            self.draw_th()

    def draw_th(self):
        """Plotting current thresholds on the axes."""

        self.axes_phase.lines[0].set_ydata([self.upper_th, self.upper_th])
        self.axes_phase.lines[1].set_ydata([self.lower_th, self.lower_th])
        if self.shaded:
            self.axes_phase.collections = [
                c for c in self.axes_phase.collections if isinstance(c, PathCollection)
            ]
            y_low = [self.lower_th, self.lower_th]
            y_high = [self.upper_th, self.upper_th]
            x_lims = [-np.pi, np.pi]
            if self.invert:
                self.axes_phase.fill_between(x_lims, y_high, np.pi, **_fill_args)
                self.axes_phase.fill_between(x_lims, y_low, -np.pi, **_fill_args)
            else:
                self.axes_phase.fill_between(x_lims, y_high, y_low, **_fill_args)

    def update_text(self):
        """Updating total count, bacteria count and particle count according
        to the threhsolds.
        """
        total_count = 0
        bac_count = 0
        part_count = 0
        for scatters in self.axes_phase.collections:
            if scatters.get_visible() and isinstance(scatters, PathCollection):
                data = scatters.get_offsets()[:, 1]
                total_count += len(data)
                if self.invert:
                    bac_count += len(
                        data[np.logical_or(data > self.upper_th, data < self.lower_th)]
                    )
                else:
                    bac_count += len(
                        data[
                            np.logical_and(data <= self.upper_th, data >= self.lower_th)
                        ]
                    )
        part_count = total_count - bac_count
        textstr = "\n".join(
            (
                (r"Total count = %i" % total_count),
                (r"Bacteria count = %i" % bac_count),
                (r"Particles count = %i" % part_count),
            )
        )
        self.box_text.set_text(textstr)

    def update_th(self, up_th, low_th):
        """Updating dead-alive threshold"""

        if up_th is not None:
            self.upper_th = up_th
            self.update_text()
            self.draw_th()
        if low_th is not None:
            self.lower_th = low_th
            self.update_text()
            self.draw_th()

    def plotting(self, transitions):
        """Plotting the transitions. Both amplitude and phase plot"""

        for n, i in enumerate(transitions):
            i.list2array()
            idx = i.site == b"site0"
            title = i.title[: _visualization["max_title_length"]]
            self.axes_phase.scatter(
                i.lf_phase[idx],
                i.hf_phase[idx],
                s=self.marker_size,
                color="black",
                marker=self.shapes[n],
                label=title,
            )

            self.axes_amp.scatter(
                i.lf_amp[idx] * 1e3,
                i.hf_amp[idx] * 1e3,
                s=self.marker_size,
                color="black",
                marker=self.shapes[n],
                label=title,
            )

        self.axes_phase.legend(
            bbox_to_anchor=(-0.25, 1),
            labelspacing=1,
            markerscale=2,
            borderpad=1,
            edgecolor="inherit",
        )
