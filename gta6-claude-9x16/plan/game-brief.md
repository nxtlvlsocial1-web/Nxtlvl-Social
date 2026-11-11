# Game Brief: Neon Drift District

## In your words
a top-down open-world city driving game at night. Neon streets, rain reflections, traffic, a few ramps and police lights in the distance. I drive a car around freely, drift around corners and hit a ramp for a jump. Original art and setting only - no references to any existing game. It must look great in a vertical screen recording: bold colours, big readable UI, a speedometer and a "DRIFT x2" combo counter that pops on screen.

1. Feel: Fast, arcadey, satisfying drifts. Not a simulator.
2. Look: Neon night city, rain, glowing signs, chunky low-poly / blocky style
3. Challenge: Easy to drive in the first 10 seconds
4. Goal: Free roam plus a short 'reach the rooftop ramp' challenge
5. Pickups: you pick
6. Slice or quick test: you pick

After play: Make these changes for a video recording:
1. Add a cinematic camera that follows the car slightly behind and above.
2. Make drift smoke, sparks and the ramp jump more dramatic.
3. Add an on-screen title card at start: "MY OPEN WORLD - BUILT BY CLAUDE".
4. Add a toggle (key H) that hides all UI except the speedometer.
Keep everything else the same.

**Pitch:** Tear through a rain-soaked neon city at night, chain drifts around corners for a growing DRIFT combo, and launch off the rooftop ramp.

**Genre:** top-down open-world city driving, arcade drift *(inferred (strong))*

**Controls:** arrow keys or WASD to drive and steer, Space (or Shift) held to drift, R to reset onto the road, Enter to start the rooftop challenge *(guessed)*; H hides all UI except the speedometer; C switches between the cinematic chase camera and the top-down camera *(guessed)*

**Question:** does drifting through neon streets and chaining combos feel fast and satisfying within the first 10 seconds? *(guessed)*

**Hooks:** the held drift that is easy to start and leave, scoring a "DRIFT xN" combo that pops big on screen; ramps that throw the car into the air over the wet neon streets.

**Intent:** no goal to reach *(provisional: free roam has none; the rooftop challenge is optional)*

## Look and references
- Look: chunky low-poly / blocky neon night city in the rain. Mood: electric, wet, fast. Camera and scale: 3D world, angled top-down that follows the car and leans ahead of it, framed for a tall portrait screen as well as wide. Shapes: blocky towers and boxy cars with bevel-free hard edges; ramps as bold striped wedges. Values: the player car and the HUD brightest; buildings dark with lit windows; the road near-black and glossy. Palette: road and buildings deep indigo/near-black (ground), hot magenta and cyan neon signs (accent), player car electric yellow-orange with white headlights (player), traffic in muted teal/maroon with red tail lights, police lights red/blue far off (threat, decorative). Shadows cool blue, lights warm. Detail: on the car, the signs and the road reflections; kept out of rooftops. Rules: flat-shaded low poly, no outlines, emissive neon. Signature: every neon sign and headlight smears a long coloured reflection streak on the wet road, and rain streaks slant through the light. Every figure drawn, no emoji, no plain circles.
- References: none named; original art and setting only (you said). The racing genre's saturated 90s arcade direction gives the bold colours *(guessed)*.
- View: 3D · Camera: angled top-down chase, about 55 degrees, follows and looks ahead with speed; works in portrait 9:16 and landscape *(inferred (strong))*

## First minute
The game opens on the car parked at a neon crossroads in the rain, a big speedometer at the bottom and a short hint "Hold UP to drive · SPACE to drift". The player presses up: the car leaps forward, the speed needle swings, rain streaks thicken. A wide corner comes up within a few seconds; holding Space while steering kicks the tail out with tyre smoke and sparks and "DRIFT x1" pops, chaining the next corner makes "DRIFT x2" pop bigger. A striped ramp sits on the main avenue: hitting it throws the car into the air with a slow-motion beat and a landing thump. A glowing marker on the skyline points to the rooftop ramp challenge.

## Challenge
Easy from the first second (you said): grippy steering, no fail state in free roam, traffic you can bump past. Real trouble comes with the rooftop ramp challenge (from about minute 1): reach the parking-garage spiral and the rooftop ramp within 60 seconds, weaving through traffic; a crash into a wall costs speed and seconds, falling off loses the run and R restarts it at the start line. Later: a best time to beat and more drift combo score.

## Core loop
- Drive the open streets, pick a corner, hold drift through it.
- A clean drift adds to the DRIFT combo; chaining corners within a few seconds multiplies it (x2, x3...), a crash or a long straight banks it into your score.
- Hit ramps for air time and bonus points; see the rooftop ramp on the skyline.
- Start the rooftop challenge, race the clock up the ramp, launch off the top; on landing see your time and best; go again or roam.
- Leads: racing leads handling, camera, the drift and the combo; the open world (action-adventure) leads structure: one open city with a landmark (the rooftop ramp) and a few ramps to find.

## Goal & fail state
- Free roam: a session feels complete when you have chained a big DRIFT combo and launched off the rooftop ramp.
- Rooftop challenge: reach the rooftop ramp and jump off it before the 60 s timer ends; running out of time or falling off ends the run, R restarts it.

## Features
- [x] Arcade car: quick smoothed steering, held drift that is easy to start and leave, brake to turn tighter
- [x] Open night city grid of blocks with neon signs, lit windows, wet reflective roads and rain
- [x] DRIFT xN combo counter that pops big on screen, plus a banked drift score
- [x] Big readable speedometer
- [x] A few street ramps with air time and a landing thump
- [x] Rooftop ramp challenge: a parking-garage ramp to the roof, a 60 s timer, a best time
- [x] Traffic cars driving the lanes (thin stand-in)
- [x] Police lights flashing in the distance (thin stand-in)
- [x] Quick reset (R) back onto the road facing the right way; landings come down straight
- [ ] Engine note that climbs with speed and drops on brake or slide; speed widens the view
- [x] A cinematic camera that follows the car slightly behind and above (C switches to the top-down view)
- [x] More dramatic drift smoke and sparks, and a more dramatic ramp jump
- [x] An on-screen title card at start: "MY OPEN WORLD - BUILT BY CLAUDE"
- [x] H hides all UI except the speedometer

## Your systems
- traffic · thin stand-in
- police lights in the distance · thin stand-in
- rain and wet reflections · in the slice
- ramps and jumps · in the slice
- drift combo counter · in the slice
- speedometer · in the slice
- rooftop ramp challenge · in the slice
- cinematic camera · in the slice
- title card at start · in the slice
- hide-the-UI toggle (H) · in the slice

## Keep
-

## Avoid
- References to any existing game: its name, art, characters, logos, map, music or UI (you said: original art and setting only)
- A simulator feel (you said: not a simulator)

## Out of scope
- Car upgrades and tuning: add it as a feature
- A career of cups: grow it
- Split-screen races: change it after play
- Online races and shared ghost replays: needs a server: not built yet
- A world map with markers and fast travel: grow it

## Build order
1. The slice: the drivable car with the drift and DRIFT combo in a small neon city block grid with rain, the speedometer, one street ramp, and the rooftop ramp challenge (60 s timer, falling off or time up ends the run, R restarts).
2. Traffic lanes and distant police lights.
3. More ramps, the engine note, speed effects, polish of reflections and rain.

---
**Kill condition:** if drifting still feels floaty or unreadable from above after two tuning rounds. *(guessed)*

**Who it's for / what they feel:** players who want a fast, flashy drive with no learning curve: the rush of a long neon drift. *(guessed)*

**Games you love / don't:** none named; original only.
