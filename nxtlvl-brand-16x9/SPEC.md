GOAL:    A café owner watching the website hero thinks "that is my shop" and books the free call.
OUTPUT:  HyperFrames, 1920 x 1080, 30 fps, MP4 (H.264 + AAC), autoplays on the site with sound off, so every beat reads without audio.
TIME:    32 s x 30 = 960 frames; 120 BPM = 15 frames a beat, 60 a bar; 16 bars. Layout changes on bars, hits on beats.
LOOK:    ground #05030C with violet light: two radial glows (rgba(61,7,137,.55) top-left 1100 px, rgba(125,24,252,.38) bottom-right 1200 px, blur 90 px), a blurred ribbon at 560 px, 15 fixed stars; no linear gradient across the frame.
         ink #F5F2FF; muted #9F97BE; one accent #7D18FC (lift #A95CFF, pale #D8BBFF) used on exactly one word, one chip or one button per shot.
         display Archivo 800 (wdth 112) 120-150 px, tracking -0.035em; emphasised phrase Instrument Serif 400 in #A95CFF, upright; UI and body Instrument Sans 500/600, 24-34 px; nothing readable under 24 px.
         medium: product UI as tinted glass surfaces: rgba(17,12,34,.86) fill, 2 px rgba(169,124,255,.32) border, 24 px radius, shadow 0 40px 90px -30px rgba(0,0,0,.9); chips are pills 1.5 px border; the one solid element per shot is violet #7D18FC.
         light and depth: one 900 px violet bloom behind the hero surface at 20-35 %, soft shadows only, no grain, no vignette.
OBJECTS: post card (4:5, 520 x 650, a photo tile with warm chai gradient, headline, tag pill, logo corner); brand-kit chips (three 54 px swatches #7D18FC #A95CFF #FFC46B + a font chip "Archivo");
         brand cursor (white arrow 56 px with violet shadow, enters from off-screen, decelerates, lands 6 px off target);
         phone (kit .nx-phone 380 x 780, black body, dynamic island) showing a 9:16 reel: gradient scene, bold caption words, progress bar, like and comment counters;
         browser window (1180 x 700, 18 px radius, three traffic dots, URL pill "nxtlvlsocial.ai") showing the real site hero: star mark, nav, headline, violet button;
         calendar (7 x 5 grid of 54 px cells, post dots #A95CFF, reel dots #FFC46B), flow rail (Scheduled > Published > Replied > Enquiry), toasts (kit .nx-toast scaled 1.6), counter;
         the Shooting Star mark (assets/shooting-star.svg) and the wordmark PNG; CTA pill "Book a free call" with arrow disc.
MOTION:  enter power4.out / expo.out 12-18 frames; move power2.inOut 15-20 frames; exit power3.in 6-9 frames (half the entrance); camera push power2.inOut over a whole bar.
         springs: UI pops back.out(1.6) (damping ~0.7), never on opacity; the end-card mark elastic.out(1, .5) once.
         staggers: chips 3 frames, words 2-3 frames, calendar dots 1 frame, toasts 12 frames. Hits are tl.set at the beat; the move into a hit starts 3-5 frames early.
         ambient: the hero surface drifts 6 px on a sine over a bar; glows breathe 4 %; nothing else floats.
SHOTS:   see STORYBOARD.md (six frames, one hero move each, reads with windows, sound per frame).
BANNED:  gradient text; glass as decoration (only product surfaces are glass); every element fading-and-sliding up; titles that keep drifting; particles as decoration (the strike burst is the one particle event); three equal cards in a row; the logo docked in a corner; any price; WhatsApp.
QA:      frames 15, 125, 200, 330, 480, 560, 690, 760, 840, 930: hero fills >= 40 % of the frame; one accent per shot; text >= 24 px; nothing cut at the edges; the end card still at 930 with mark + wordmark + CTA + URL.
