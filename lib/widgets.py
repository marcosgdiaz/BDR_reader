# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 11:19:04 2021

@author: MGD
"""
from matplotlib.widgets import CheckButtons, TextBox
import matplotlib.pyplot as plt

_colors = ["white"] * 10

_legend = {
    "x": 0.02,
    "y": 0.88,
    "width": 0.24,
    "height": 0.07,
    "alpha": 1,
    "rect_width": 0.06,
    "margin": 0.09,
}

_buttons = {
    "x": 0.53,
    "y": 0.1,
    "width": 0.13,
    "height": 0.15,
}

_submit_box = {
    "x": 0.42,
    "y": 0.2,
    "width": 0.04,
    "height": 0.075,
    "separation": 0.1,
    "label_pad": 0.2,
}


def make_legend(dis):
    """Create check buttons to select or deselect the measurement."""

    labels, visibility = [], []
    for line in dis.lines_phase:
        visibility.append(line.get_visible())
        labels.append(line.get_label())

    rax = plt.axes(
        [
            _legend["x"],
            _legend["y"] - _legend["height"] * len(labels),
            _legend["width"],
            _legend["height"] * len(labels),
        ]
    )

    check = CheckButtons(rax, labels, visibility)

    for n, i in enumerate(check.rectangles):
        i.set_width(_legend["rect_width"])
        i.set_color(_colors[n])
        i.set_alpha(_legend["alpha"])

    for i in check.lines:
        for k in i:
            a = k.get_xdata()
            a[1] = a[0] + _legend["rect_width"]
            k.set_xdata(a)

    for i in check.labels:
        a = i.get_position()
        b = (_legend["rect_width"] + _legend["margin"], a[1])
        i.set_position(b)

    return check


def make_buttons():
    labels = ["Invert", "Bacteria area"]
    visibility = [True, False]
    rax = plt.axes(
        [_buttons["x"], _buttons["y"], _buttons["width"], _buttons["height"]]
    )
    check = CheckButtons(rax, labels, visibility)
    return check


def make_thresholds(up_th, lw_th):
    axbox_1 = plt.axes(
        [
            _submit_box["x"],
            _submit_box["y"],
            _submit_box["width"],
            _submit_box["height"],
        ]
    )
    text_box = TextBox(
        axbox_1, "Upper TH", initial=str(up_th), label_pad=_submit_box["label_pad"]
    )
    axbox_2 = plt.axes(
        [
            _submit_box["x"],
            _submit_box["y"] - _submit_box["separation"],
            _submit_box["width"],
            _submit_box["height"],
        ]
    )
    text_box_2 = TextBox(
        axbox_2, "Lower TH", initial=str(lw_th), label_pad=_submit_box["label_pad"]
    )

    return text_box, text_box_2
