"""The scene plan for the v3 edit, shared by build/cards.py and build/generate.py.

Each lyric line is one scene built with one of the nine scene recipes read off the owner's YouMotion reference
(Video "COUNTRY STREETS ... RIDE YOUR OWN ROAD"), in the reference's own order, with the hit lines on the photo-filled
keyword recipe:
  R1 cut-out on red torn paper, black label slams in big then settles, red word types on, blue marker circle, small
     print paragraph, black stars, one invert flash               (reference 0.0-2.6 s, COUNTRY STREETS)
  R2 dark photo, black label types on, white flash, the keyword huge and filled with a photo, camera zooms into it and
     back out, a white label under it                              (2.7-5.0 s, OLD ROOTS / NEW / RHYTHM)
  R3 red-and-black label types on close up over crumpled grey paper, pull out to a cut-out on a dark red block, the
     keyword in red 3D letters on torn white paper, the keyword ghosted large behind   (5.3-7.8 s, COUNTRY / SOUL)
  R4 invert flash, a big stamped word types on over a red outline frame, a cut-out, the keyword in white 3D letters on
     torn black paper, pull out                                    (8.0-10.6 s, CITY / FLOW)
  R5 photo print over red torn paper, big stamped word, a second print, black label typed and circled, a red duotone
     print, invert flash                                           (10.7-13.4 s, ROAD / THE BEAT)
  R6 tilted print, torn black paper, white label, the keyword in red letters circled with red stars, a blue arc
                                                                   (13.4-15.0 s, URBAN / SHIFT)
  R7 small red word types on above a big white paper label, a print below, a black torn chunk   (15.0-16.0 s, DRIVE PAPER)
  R8 invert flash on a cut-out, red torn paper, red-on-white label, relayout: big stamped word over a black label
     with a red block, the cut-out smaller                         (16.0-18.4 s, ROLLING / BEATS THROUGH)
  R9 black/white split frame, type only between torn grey scraps: red-on-white label, red box label, white 3D word,
     the keyword huge stamped and circled                          (18.5-21.2 s, RIDE YOUR OWN ROAD)
  END white flash, ASHKE on white tape with grid lines, the blue circle draws round it   (21.3-24 s, the logo)
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# The edit is the section itself (song 2:14 to 3:14); OFFSET would shift it (v5 used 0.74 for a 35 s cut).
OFFSET, DUR, NLINES = 0.0, 60.0, 33     # v6: back to the full minute from 2:14
W = json.load(open(os.path.join(ROOT, "plan", "words_scribe.json")))
for _w in W:
    _w["s"] -= OFFSET
    _w["e"] -= OFFSET
FIRST = [3, 7, 11, 16, 22, 28, 32, 36, 41, 44, 51, 55, 62, 65, 72, 76, 81, 84, 89, 95, 101, 105, 110, 115, 120, 123, 129,
         132, 138, 142, 146, 149, 154]

# line -> recipe; -1 is the intro (title), 31-32 the ending
RECIPE = {-1: "R1", 0: "R2", 1: "R3", 2: "R4", 3: "R5", 4: "R6", 5: "R7", 6: "R8", 7: "R9", 8: "R1", 9: "R3", 10: "R4",
          11: "R5", 12: "R2", 13: "R6", 14: "R7", 15: "R8", 16: "R9", 17: "R1", 18: "R3", 19: "R2", 20: "R4", 21: "R5",
          22: "R6", 23: "R7", 24: "R8", 25: "R9", 26: "R2", 27: "R1", 28: "R3", 29: "R4", 30: "R6", 31: "END", 32: "END"}
# cut-out stickers (build/cutouts.py) for the cut-out recipes
CUTOUT = {-1: "coat", 0: "profile", 1: "jet", 2: "selfie_a", 6: "redmic", 8: "point", 9: "suit", 10: "arms",
          12: "stage", 15: "crowdmic", 17: "bugatti", 18: "selfie_b", 19: "profile", 20: "back", 24: "point", 26: "selfie_c",
          27: "coat", 28: "suit", 29: "jet"}   # the owner's photos and clean solo frames of Karan (build/cutouts.py)
PRINT = {7: "fire", 16: "fire", 25: "fire"}   # the fire-stage photo as a still print (its flames cannot be cut away)
# card footage (build/cards.py): Karan-only shots (source, start time, x of Karan as a fraction)
SHOTS = {"K1": ("estate", 1.4, .5), "K2": ("estate", 13.0, .5), "K3": ("estate", 15.2, .42), "K4": ("estate", 42.6, .5),
         "K5": ("tour", 44.4, .5), "K6": ("tour", 41.4, .45), "K7": ("tour", 10.4, .5), "K8": ("tour", 49.0, .5),
         "K9": ("tour", 2.0, .5), "K10": ("tour", 31.0, .6), "K11": ("tour", 51.0, .5), "K13": ("estate", 13.8, .5),
         "K14": ("tour", 50.2, .5), "K15": ("tour", 10.3, .5), "K16": ("tour", 16.0, .45),
         "K17": ("estate", 43.3, .5), "K18": ("tour", 54.0, .5), "K19": ("tour", 31.2, .6), "K20": ("estate", 2.6, .52),
         "K21": ("tour", 11.6, .5), "K22": ("tour", 45.0, .5)}
CARD1 = {0: "K5", 3: "K2", 4: "K4", 5: "K11", 11: "K3", 12: "K16", 13: "K1", 14: "K10", 19: "K18", 21: "K13", 22: "K7",
         23: "K8", 26: "K14", 30: "K9"}
# second print: R5's red duotone print, plus a small print in the cut-out and type scenes for more footage
CARD2 = {3: "K15", 11: "K8", 21: "K11", 1: "K17", 2: "K19", 8: "K20", 9: "K21", 10: "K22", 15: "K6", 17: "K17",
         18: "K19", 20: "K20", 24: "K21", 27: "K22", 28: "K6", 29: "K18"}
# the photo that fills the giant keyword in R2 scenes
FILL = {0: "K13", 12: "K11", 19: "K2", 26: "K8"}
TRANS_POOL = ["K3", "K11", "K1", "K6", "K4", "K5", "K13", "K10", "K7", "K14"]


def line_times(li):
    a = W[FIRST[li]]["s"] - .06
    b = (W[FIRST[li + 1]]["s"] - .06) if li + 1 < NLINES else DUR
    return a, b


def scenes():
    out = [(0.0, line_times(0)[0], -1)]
    for li in range(NLINES):
        a, b = line_times(li)
        out.append((a, b, li))
    return out
