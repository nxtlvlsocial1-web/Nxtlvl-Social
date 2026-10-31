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
          12: "stage", 15: "crowdmic", 17: "bugatti", 18: "selfie_b", 19: "fireup", 20: "back", 24: "jet", 26: "selfie_c",
          27: "barn", 28: "coat", 29: "purple"}   # the owner's photos and clean solo frames of Karan (build/cutouts.py)
PRINT = {7: "fire", 16: "fire", 25: "fire"}   # the fire-stage photo as a still print (its flames cannot be cut away)
# card footage (build/cards.py). v9: every print plays its own window (source, start, x of the subject, end), cut from a
# shot-by-shot breakdown of the owner's clips; no window is used twice or overlaps another, or the moments the clip-frame
# cut-outs come from (estate 1-4.6, tour 10.2-12.7, 49.2-51, 53.4-55.1). Playback stops at the window's end and holds.
SHOTS = {
    "e_table": ("estate", 5.2, .5, 8.4), "e_aimlow": ("estate", 12.9, .45, 14.2), "e_aim": ("estate", 15.0, .42, 16.8),
    "e_guns": ("estate", 18.4, .6, 20.0), "e_duo": ("estate", 20.4, .62, 22.0), "e_atcam": ("estate", 24.4, .5, 25.8),
    "e_pair": ("estate", 27.0, .62, 28.8), "e_polo": ("estate", 29.0, .5, 31.1), "e_teak": ("estate", 33.5, .62, 34.48),
    "e_tea2": ("estate", 37.2, .6, 38.04), "e_tea3": ("estate", 38.1, .6, 39.04), "e_tea4": ("estate", 40.7, .62, 41.64),
    "e_teaclose": ("estate", 41.8, .55, 43.36), "e_car": ("estate", 43.9, .3, 45.1),
    "t_group": ("tour", 0.1, .5, 1.29), "t_sign": ("tour", 1.4, .5, 3.21), "t_crowd": ("tour", 3.3, .5, 5.0),
    "t_hands": ("tour", 6.7, .5, 8.43), "t_hall": ("tour", 8.5, .55, 10.2), "t_spot": ("tour", 15.7, .45, 17.0),
    "t_crew": ("tour", 22.9, .5, 24.6), "t_redstage": ("tour", 28.2, .5, 29.8), "t_closemic": ("tour", 30.2, .6, 31.5),
    "t_corridor": ("tour", 32.4, .5, 33.49), "t_dancers": ("tour", 35.3, .5, 37.0), "t_spot2": ("tour", 37.4, .5, 39.0),
    "t_crowdk": ("tour", 42.3, .5, 44.0), "t_walk": ("tour", 44.4, .5, 46.4), "t_guitar": ("tour", 47.6, .6, 49.2),
    "t_spot3": ("tour", 51.1, .5, 52.2),
    # bright frames for the photo-filled keywords
    "f_tea": ("estate", 32.6, .5, 33.44), "f_smoke": ("tour", 21.2, .5, 22.7), "f_gun": ("estate", 22.4, .6, 24.0),
    "f_polo": ("estate", 35.3, .5, 36.7),
}
CARD1 = {0: "t_spot", 3: "e_aimlow", 4: "e_table", 5: "t_hall", 11: "e_teaclose", 12: "t_spot2", 13: "e_atcam", 14: "t_closemic",
         19: "t_crowdk", 21: "e_duo", 22: "t_walk", 23: "t_guitar", 26: "t_spot3", 30: "t_sign"}
# second print: R5's red duotone print, plus a small print in the cut-out scenes
CARD2 = {3: "t_group", 11: "e_tea3", 21: "e_guns", 1: "e_teak", 2: "t_crowd", 8: "e_car", 9: "t_hands", 10: "e_polo",
         15: "t_redstage", 17: "e_tea2", 18: "t_dancers", 20: "e_pair", 24: "t_corridor", 27: "e_tea4", 28: "t_crew", 29: "e_aim"}
FILL = {0: "f_tea", 12: "f_smoke", 19: "f_gun", 26: "f_polo"}
# single-frame transition flashes: frames from the music video's own verse (song 2:14-3:14), used nowhere else
TRANS_POOL = [f"mv_{k:02d}" for k in range(66)]


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
