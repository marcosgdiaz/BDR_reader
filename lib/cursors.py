# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 16:33:45 2021

@author: MGD
"""

import mplcursors


def make_cursor(lines, lines_amp):
    cursor = mplcursors.cursor(lines + lines_amp, highlight=True, hover=True)
    cursor.annotation_kwargs["bbox"] = None
    cursor.annotation_kwargs["arrowprops"] = None
    color = "black"
    cursor.highlight_kwargs.update(
        dict(
            color=color,
            markeredgecolor=color,
            linewidth=3,
            markeredgewidth=3,
            facecolor=color,
            edgecolor=color,
        )
    )

    pairs = dict(zip(lines_amp, lines))
    pairs.update(zip(lines_amp, lines))

    pairs2 = dict(zip(lines, lines_amp))
    pairs2.update(zip(lines, lines_amp))

    @cursor.connect("add")
    def on_add(sel):
        if sel.artist in pairs.keys():
            sel.extras.append(
                cursor.add_highlight(pairs[sel.artist], target=sel.target)
            )
            sel.annotation.set_text(None)
        else:
            sel.extras.append(
                cursor.add_highlight(pairs2[sel.artist], target=sel.target)
            )
            sel.annotation.set_text(None)
