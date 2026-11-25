# SST: "The Journey Continues" (Instagram + Facebook Reels, 9:16, 59.3 s)

Client brief: `SST_The_Journey_Continues_Editor_Production_Brief.pdf` (8 pages). VO = the brief's master script, verbatim except one owner change (v2: "SST." is spoken as "Sports Science Technology.",
no "and", as the client asked on the earlier reel),
each line placed on the brief's time codes (Scene 02 at 0:07, 03 at 0:15, 04 at 0:29, 05 at 0:41, 06 at 0:51), with the
pauses it asks for after "behind the scenes", "whether you continue" and "the vision moves forward". On-screen text is
the brief's, scene by scene; English subtitles use the script's wording (the end card carries the last two lines).

Build: build/vo_cb.py + build/vo_pick.py + build/relabel.py (v2 voice: Chatterbox with the synthetic Kokoro am_puck
reference and the approved SST reel's emotion settings, recorded as whole passages per scene for a natural read, 3 takes
each, slip-free picked, then split back into sentences for timing), build/prep_shots.py (Pexels footage cut, cropped to the band and
graded: plan/edl.json), build/generate.py (composition), build/sfx_mix.py (mix).

## Post description (ready to paste)

The brief gives the social caption and the hashtags (section 07) and no CTA keyword, so it is used as written.

```
Behind every vision, there is a journey the world may never see.

Years of work. A purpose-driven initiative. And challenges that test the determination to keep moving forward.

A published account describes alleged digital interference, tracking and harassment connected to the journey of Sports Science Technology.

This is not just a story about obstacles. It is a reminder that meaningful progress demands resilience, patience and the courage to continue.

The work continues. The vision moves forward.

SST - The journey is far from over.

Music: "A Good Dream" by Jesse Keller, CC BY 3.0

#SportsScienceTechnology #SST #SportsTechnology #Innovation #Resilience
sports science technology, SST, sports technology, resilience, innovation in sport, sports science, perseverance, the journey continues, sports research, athlete performance technology
```

## For the client before publishing (the brief's own checklist)

- Confirm the VO and the allegation wording with SST before edit lock. The film keeps the brief's attribution exactly ("A
  published account describes alleged ..."), and the on-screen label reads "ALLEGATIONS DESCRIBED IN A PUBLISHED ACCOUNT".
  Nothing in the film presents them as verified findings. SST should check accuracy, attribution and legal suitability.
- Footage is symbolic stock (Pexels licence), not actual event footage: a performer at a desk, dark rooms, a blurred
  phone, sunrise. No identifiable alleged perpetrator, no fake evidence, messages, documents, police or news graphics,
  no readable screens (the phone shot is blurred past reading), no product or research details.
- The official SST logo is used exactly as supplied (brands/sports-science-technology/logo.jpg), unaltered, on a white card.

## Credits

- Footage: Pexels licence (footage/pexels/pexels.json lists every clip's page and file).
- Music: "A Good Dream" by Jesse Keller, Jamendo 1540856 via Openverse, CC BY 3.0 (credit line in the description).
- Sound effects: Openverse CC0 + OpenGameArt CC0 set, at low level (glitch ticks, soft notifications, one bass impact).
