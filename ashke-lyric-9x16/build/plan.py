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
W = json.load(open(os.path.join(ROOT, "plan", "words_scribe.json")))
FIRST = [3, 7, 11, 16, 22, 28, 32, 36, 41, 44, 51, 55, 62, 65, 72, 76, 81, 84, 89, 95, 101, 105, 110, 115, 120, 123, 129,
         132, 138, 142, 146, 149, 154]
DUR = 60.0

# line -> recipe; -1 is the intro (title), 31-32 the ending
RECIPE = {-1: "R1", 0: "R2", 1: "R3", 2: "R4", 3: "R5", 4: "R6", 5: "R7", 6: "R8", 7: "R9", 8: "R1", 9: "R3", 10: "R4",
          11: "R5", 12: "R2", 13: "R6", 14: "R7", 15: "R8", 16: "R9", 17: "R1", 18: "R3", 19: "R2", 20: "R4", 21: "R5",
          22: "R6", 23: "R7", 24: "R8", 25: "R9", 26: "R2", 27: "R1", 28: "R3", 29: "R4", 30: "R6", 31: "END", 32: "END"}
# cut-out stickers (build/cutouts.py) for the cut-out recipes
CUTOUT = {-1: "suit_a", 1: "plaid", 2: "selfie_a", 6: "aim", 8: "selfie_b", 9: "signing", 10: "point_up", 15: "suit_man",
          17: "arms_up", 18: "selfie_c", 20: "couch", 24: "red_jacket_b", 27: "red_jacket", 28: "suit_b", 29: "gun_close",
          0: "gun_up", 12: "plaid_tea", 19: "selfie_b", 26: "point_up"}   # R2: the cut-out behind the photo-filled keyword
# card footage (build/cards.py): source, start time, x of the subject (fraction); card 2 is R5's red print
SHOTS = {"E2": ("estate", 12.6, .5), "E3": ("estate", 18.3, .55), "E4": ("estate", 25.5, .6), "E5": ("estate", 30.5, .5),
         "E7": ("estate", 36.2, .5), "E9": ("estate", 42.6, .5), "E10": ("estate", 32.2, .3), "E11": ("estate", 40.5, .35),
         "E8": ("estate", 39.4, .6), "T1": ("tour", 3.5, .5), "T2": ("tour", 5.4, .6), "T3": ("tour", 16.0, .45),
         "T5": ("tour", 28.0, .45), "T6": ("tour", 31.0, .6), "T8": ("tour", 44.5, .5), "T10": ("tour", 48.0, .4),
         "T11": ("tour", 51.0, .5), "T12": ("tour", 54.0, .5), "T14": ("tour", 35.5, .45), "T7": ("tour", 42.0, .55)}
CARD1 = {0: "T8", 3: "E2", 4: "E9", 5: "T3", 11: "E3", 12: "T1", 13: "E7", 14: "T6", 19: "T5", 21: "E10", 22: "E4",
         23: "T12", 26: "T2", 30: "E5"}
CARD2 = {3: "T14", 11: "T11", 21: "T10"}
# the photo that fills the giant keyword in R2 scenes
FILL = {0: "E8", 12: "T2", 19: "E2", 26: "T11"}


def line_times(li):
    a = W[FIRST[li]]["s"] - .06
    b = (W[FIRST[li + 1]]["s"] - .06) if li + 1 < len(FIRST) else DUR
    return a, b


def scenes():
    out = [(0.0, line_times(0)[0], -1)]
    for li in range(len(FIRST)):
        a, b = line_times(li)
        out.append((a, b, li))
    return out
