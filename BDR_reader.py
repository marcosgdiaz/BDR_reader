# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 13:45:53 2020

@author: MGD
"""

import os
import sys

from tkinter import filedialog
from tkinter import Tk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

from lib.display_properties import DisplayProperties
from lib.BDR_lib import BDR_reader
from lib.cursors import make_cursor
from lib.widgets import make_buttons, make_legend, make_thresholds

currdir = os.getcwd()
root = Tk()
path = filedialog.askopenfilenames(
    filetypes=[("BDR Files", "*.bdr")], parent=root, title="Select BDR files"
)
root.destroy()
transitions = BDR_reader(path)

win_scale = (16.8, 9.6)
fig, ax = plt.subplots(1, 2, figsize=win_scale)

dis_input = {
    "axes_phase": ax[0],
    "axes_amp": ax[1],
    "marker_size": 3,
    "upper_th": float(sys.argv[1]) if len(sys.argv) == 3 else 2,
    "lower_th": float(sys.argv[2]) if len(sys.argv) == 3 else -2.43,
    "invert": True,
    "shaded": True,
}

# Initializing
dis = DisplayProperties(**dis_input)

dis.plotting(transitions)

dis.initialise_phase()

dis.initialise_amp()

dis.draw_th()

dis.update_text()

# Make data points selectable by hovering
make_cursor(dis.lines_phase, dis.lines_amp)

# Make checkbuttons with all plotted lines with correct visibility
check = make_legend(dis)


def func_buttons(event):
    for i, k in zip(dis.lines_phase, dis.lines_amp):
        if i.get_label() == event:
            i.set_visible(np.invert(i.get_visible()))
            k.set_visible(np.invert(k.get_visible()))
            break
    dis.update_text()
    plt.draw()


check.on_clicked(func_buttons)

#  Make check buttons for Invert and Filling options
check_2 = make_buttons()


def func(label):
    if label == "Bacteria area":
        [
            c.set_visible(np.invert(c.get_visible()))
            for c in ax[0].collections
            if isinstance(c, matplotlib.collections.PolyCollection)
        ]
        dis.invert_th(3)
    elif label == "Invert":
        dis.invert_th(1)
    plt.draw()


check_2.on_clicked(func)

# Make text boxes for thresholds
text_1, text_2 = make_thresholds(dis.upper_th, dis.lower_th)


def submit(text):
    up_threshold = float(text_1.text)
    lw_threshold = float(text_2.text)
    dis.update_th(up_threshold, lw_threshold)
    plt.draw()


text_1.on_submit(submit)
text_2.on_submit(submit)

plt.show()
