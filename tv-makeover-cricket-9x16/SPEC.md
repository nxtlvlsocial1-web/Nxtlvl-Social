GOAL:    viewer laughs at the ad-billboard TV, follows the home run base by base, and comments "TV".
OUTPUT:  HyperFrames, 1080 x 1920, 30 fps
TIME:    34.19 s x 30 = 1026 frames; the voiceover is the clock (no music grid yet)
LOOK:    8-bit pixel art drawn on a 180 x 320 grid, every logical pixel = 6 x 6 px, nearest-neighbour,
         no anti-aliasing, no gradients except 2-colour ordered dither bands.
         Palette: night sky #0d1633 / #1b2a55 / #263a6b, lamp #fff6c8, grass #2f8f3a / #37a043,
         dirt #c07d45, chalk #f4f4f4, jumbotron #23262d, wall #e7b97f, floor #9b6440, couch #b5443b.
         Accent yellow #ffd447 only on the word that matters, the active base and the CTA.
         Type: Press Start 2P only. Captions 40 px, step labels 30 px, jumbotron heads 56-96 px.
         TV glass: a 2 px scanline every 6 px at 12% black over whatever the TV shows.
OBJECTS: TV (black bezel, stand), couch seen from behind, family of four (two adults, two kids) from
         behind, remote (black, red button), batter (red helmet, white jersey, grey pants),
         pitcher, bat, ball, bases + home plate, jumbotron with chasing bulbs, crowd, light towers,
         TV home screen (top bar, ad banners with "AD" badges, app tiles), terminal.
MOTION:  sprites move on whole logical pixels; sprint between bases 0.6 s power2.inOut;
         run cycle 2 frames at 12 fps; text pops per word 0.06 s apart, no slide;
         jumbotron content cuts on the action; zoom into the TV 0.4 s power3.in;
         pull back out 0.45 s power2.inOut.
SHOTS:   0.00-2.65  living room, TV covered in flashing ads; hook "YOUR TV IS A BILLBOARD?"
         2.40-3.05  dad raises remote, click, static
         3.05-3.45  zoom through the TV glass into the broadcast
         3.45-5.20  batter close-up: pitch, swing, CRACK on "OUT" (4.08), flash, ball rises
         5.20-7.65  stadium wide, ball arcs out, jumbotron "4 STEPS" / "MVP: CLAUDE"
         7.70-10.45 jumbotron "STEP 4 = HOME RUN!", batter drops bat, sprints to 1st
         10.45-14.2 1st: jumbotron home screen, launcher stamp on "swap", ad rows explode on "GONE"
         14.2-19.2  2nd: scattered icons snap into rounded tiles, dithered wallpaper fades in
         19.2-23.1  3rd: screen idles, drone landscape scrolls
         23.2-30.9  home: slide on "one command", fireworks; terminal deletes junk, SAFE, UNDO
         30.9-34.19 world dissolves around the jumbotron screen into the living room TV, now clean;
                    family cheers; CTA COMMENT "TV" held 2.7 s
BANNED:  glow/bloom, purple-blue gradients, everything centred and fading up, pills, frame borders
         as decoration, Apple logos or any real launcher/brand names, smooth (non-pixel) shapes.
QA:      0.0 hook readable with sound off; 4.1 flash + ball; 10.6 runner on 1st; 13.7 explosion;
         17.0 tiles neat; 21.0 landscape; 24.2 slide dust; 26.5 struck lines; 33.0 CTA + clean TV.
