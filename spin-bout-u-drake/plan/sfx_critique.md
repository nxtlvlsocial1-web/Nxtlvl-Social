# Critique, round 1

| axis | score | basis |
|---|---|---|
| hook | 9.0 | first sound at 0.76s |
| sync | 9.4 | 52/56 sounds on their frame (peaks, arrivals, or first onsets for clicks) |
| coverage | n/a | not measured (pass --moments) |
| pacing | 7.8 | 9.2 weighted events per 10 s, longest silence 4.2 s |
| variety | 1.0 | 81 source recordings, 26 families in 82 sounds (runs and interface sounds not counted) |
| hierarchy | 10.0 | 21.6 dB between the loud and the quiet sounds |
| headroom | 10.0 | true peak -1.6 dBTP |
| loudness | 10.0 | final -14.7 LUFS (the author's own balance is kept) |
| balance | 7.0 | median event peak -12 dB vs the original around it, big sounds -9 dB (whole-track gap +8 LU) |
| mono | 10.0 | the SFX track loses 0.7 dB when folded to mono (0 = the channels agree, 3 = unrelated, 6+ = parts cancel); 0 of 92 sounds lose more than 6 dB; the film loses 0.1 LU in mono against 0.1 LU for the original (+0.0 added) |

**FIX**: lowest axis 1.0 (every axis must reach 8; ok to show)

Three worst problems, fix only these, re-render, run again:
1. variety: 13 takes of the same recording family 'swishes swish' (2.72s, 6.16s, 8.14s, 10.76s, 12.96s, 14.84s, 20.34s, 22.14s, 24.02s, 35.08s, 38.74s, 42.42s, 49.82s); mix in other sounds
2. sync: 'sticker' at 24.55s peaks -220 ms from the moment
3. sync: 'sticker' at 33.69s arrives -110 ms from the moment

Listen to these 5 moments, on headphones and then once on a phone speaker. This script cannot hear: they are the places where the numbers above are least certain, and none of them says that it sounds good:
  1.    0.76s  'glitch': the first sound of the film: the hook. Listen for: does it land with the picture at once, and is it clearly there under the music or the voice?
  2.    3.61s  'sticker': brought 6 dB up to the perceived level of its role; the quietest by perceived loudness among the sounds that are not ticks. Listen for: a thin recording lifted that far can turn harsh: is it clean? / can it be heard at all?
  3.   19.65s  'hit': the highest peak of the film (-2 dBFS before the master). Listen for: is it big without hurting on headphones, and does the music under it pump?
  4.   24.55s  'sticker': its peak sits -220 ms from the moment. Listen for: does it feel early or late against the picture?
  5.   35.58s  the busiest two seconds (14 sounds). Listen for: is every sound still distinct, or does it turn to mud?
  (--listen-out FILE.wav cuts them into one file of the film's own sound)

Still to judge by eye on review.png: character fit (each sound suits its picture), cleanliness (no mud in the low end under music/voice, nothing masks speech), taste (designed, not sprayed on).

---

# Critique, round 2

| axis | score | basis |
|---|---|---|
| hook | 9.0 | first sound at 0.76s |
| sync | 7.0 | 50/53 sounds on their frame (peaks, arrivals, or first onsets for clicks); 1 cue(s) missing from the track |
| coverage | n/a | not measured (pass --moments) |
| pacing | 7.9 | 9.1 weighted events per 10 s, longest silence 3.3 s |
| variety | 1.0 | 80 source recordings, 28 families in 81 sounds (runs and interface sounds not counted) |
| hierarchy | 10.0 | 19.4 dB between the loud and the quiet sounds |
| headroom | 10.0 | true peak -1.5 dBTP |
| loudness | 10.0 | final -14.7 LUFS (the author's own balance is kept) |
| balance | 7.0 | median event peak -12 dB vs the original around it, big sounds -8 dB (whole-track gap +9 LU) |
| mono | 10.0 | the SFX track loses 0.6 dB when folded to mono (0 = the channels agree, 3 = unrelated, 6+ = parts cancel); 0 of 88 sounds lose more than 6 dB; the film loses 0.2 LU in mono against 0.1 LU for the original (+0.1 added) |

**FIX**: lowest axis 1.0 (every axis must reach 8; ok to show)

Three worst problems, fix only these, re-render, run again:
1. variety: 10 takes of the same recording family 'paper stationery stationery' (2.03s, 3.61s, 13.43s, 24.55s, 26.41s, 28.23s, 33.69s, 51.63s, 55.29s, 59.03s); mix in other sounds
2. sync: 'sticker' at 24.55s arrives -240 ms from the moment
3. render: 'glitch' at 44.28s is missing from the SFX track (lost in the render): run mix.py again, report it if it repeats

Listen to these 5 moments, on headphones and then once on a phone speaker. This script cannot hear: they are the places where the numbers above are least certain, and none of them says that it sounds good:
  1.    0.76s  'glitch': the first sound of the film: the hook. Listen for: does it land with the picture at once, and is it clearly there under the music or the voice?
  2.    3.61s  'sticker': brought 6 dB up to the perceived level of its role; the quietest by perceived loudness among the sounds that are not ticks. Listen for: a thin recording lifted that far can turn harsh: is it clean? / can it be heard at all?
  3.   19.65s  'hit': the highest peak of the film (-2 dBFS before the master). Listen for: is it big without hurting on headphones, and does the music under it pump?
  4.   24.55s  'sticker': its arrival sits -240 ms from the moment. Listen for: does it feel early or late against the picture?
  5.   35.58s  the busiest two seconds (11 sounds). Listen for: is every sound still distinct, or does it turn to mud?
  (--listen-out FILE.wav cuts them into one file of the film's own sound)

Still to judge by eye on review.png: character fit (each sound suits its picture), cleanliness (no mud in the low end under music/voice, nothing masks speech), taste (designed, not sprayed on).

---

# Critique, round 3

| axis | score | basis |
|---|---|---|
| hook | 9.0 | first sound at 0.76s |
| sync | 7.0 | 57/57 sounds on their frame (peaks, arrivals, or first onsets for clicks); 1 cue(s) missing from the track |
| coverage | n/a | not measured (pass --moments) |
| pacing | 8.0 | 8.1 weighted events per 10 s, longest silence 3.3 s |
| variety | 1.0 | 76 source recordings, 31 families in 81 sounds (runs and interface sounds not counted) |
| hierarchy | 10.0 | 14.9 dB between the loud and the quiet sounds |
| headroom | 10.0 | true peak -1.5 dBTP |
| loudness | 10.0 | final -14.7 LUFS (the author's own balance is kept) |
| balance | 7.0 | median event peak -13 dB vs the original around it, big sounds -8 dB (whole-track gap +9 LU) |
| mono | 10.0 | the SFX track loses 0.6 dB when folded to mono (0 = the channels agree, 3 = unrelated, 6+ = parts cancel); 0 of 88 sounds lose more than 6 dB; the film loses 0.2 LU in mono against 0.1 LU for the original (+0.1 added) |

**FIX**: lowest axis 1.0 (every axis must reach 8; ok to show)

Three worst problems, fix only these, re-render, run again:
1. render: 'glitch' at 44.28s is missing from the SFX track (lost in the render): run mix.py again, report it if it repeats
2. variety: 7 takes of the same recording family 'audio glitch' (0.76s, 8.62s, 10.76s, 14.84s, 44.28s, 54.28s, 57.22s); mix in other sounds
3. balance: median sound is -13 dB under the original, weakest at 22.14s, 28.23s: raise gain_db there (sheet.py gain --db +N --between A B) and render with --no-match-layer: the layer match keeps the whole layer at the loudness of the sound it replaces and takes back a raise that is made on every cue

Listen to these 5 moments, on headphones and then once on a phone speaker. This script cannot hear: they are the places where the numbers above are least certain, and none of them says that it sounds good:
  1.    0.76s  'glitch': the first sound of the film: the hook. Listen for: does it land with the picture at once, and is it clearly there under the music or the voice?
  2.   14.84s  'glitch': brought 6 dB up to the perceived level of its role. Listen for: a thin recording lifted that far can turn harsh: is it clean?
  3.   16.36s  'camera': the quietest by perceived loudness among the sounds that are not ticks. Listen for: can it be heard at all?
  4.   19.65s  'hit': the highest peak of the film (-2 dBFS before the master). Listen for: is it big without hurting on headphones, and does the music under it pump?
  5.   35.58s  the busiest two seconds (11 sounds). Listen for: is every sound still distinct, or does it turn to mud?
  (--listen-out FILE.wav cuts them into one file of the film's own sound)

Still to judge by eye on review.png: character fit (each sound suits its picture), cleanliness (no mud in the low end under music/voice, nothing masks speech), taste (designed, not sprayed on).

---

# Critique, round 4

| axis | score | basis |
|---|---|---|
| hook | 9.0 | first sound at 0.76s |
| sync | 10.0 | 54/54 sounds on their frame (peaks, arrivals, or first onsets for clicks) |
| coverage | n/a | not measured (pass --moments) |
| pacing | 8.0 | 8.0 weighted events per 10 s, longest silence 3.3 s |
| variety | 1.0 | 70 source recordings, 32 families in 75 sounds (runs and interface sounds not counted) |
| hierarchy | 10.0 | 14.9 dB between the loud and the quiet sounds |
| headroom | 10.0 | true peak -1.6 dBTP |
| loudness | 10.0 | final -15.3 LUFS (the author's own balance is kept) |
| balance | 10.0 | median event peak -12 dB vs the original around it, big sounds -6 dB (whole-track gap +8 LU) |
| mono | 10.0 | the SFX track loses 0.6 dB when folded to mono (0 = the channels agree, 3 = unrelated, 6+ = parts cancel); 0 of 82 sounds lose more than 6 dB; the film loses 0.2 LU in mono against 0.1 LU for the original (+0.1 added) |

**FIX**: lowest axis 1.0 (every axis must reach 8; ok to show)

Three worst problems, fix only these, re-render, run again:
1. variety: 6 takes of the same recording family 'camera camera' (13.70s, 16.36s, 20.54s, 51.70s, 57.40s, 57.78s); mix in other sounds
2. hierarchy: 'hit' at 19.65s is 10 dB quieter (perceived level) than the other hit sounds: a thin recording, pick a fuller one (search.py --role hit --sheet) or raise it
3. pacing: two hit sounds 70 ms apart at 39.26s smear

Listen to these 4 moments, on headphones and then once on a phone speaker. This script cannot hear: they are the places where the numbers above are least certain, and none of them says that it sounds good:
  1.    0.76s  'glitch': the first sound of the film: the hook. Listen for: does it land with the picture at once, and is it clearly there under the music or the voice?
  2.   15.98s  'camera': brought 6 dB down to the perceived level of its role; also 'camera' at 16.36s: the quietest by perceived loudness among the sounds that are not ticks. Listen for: a sound brought down that far can get lost: does it still carry its moment? / can it be heard at all?
  3.   19.65s  'hit': the highest peak of the film (-2 dBFS before the master). Listen for: is it big without hurting on headphones, and does the music under it pump?
  4.   35.58s  the busiest two seconds (11 sounds). Listen for: is every sound still distinct, or does it turn to mud?
  (--listen-out FILE.wav cuts them into one file of the film's own sound)

Still to judge by eye on review.png: character fit (each sound suits its picture), cleanliness (no mud in the low end under music/voice, nothing masks speech), taste (designed, not sprayed on).

---

# Critique, round 5

| axis | score | basis |
|---|---|---|
| hook | 9.0 | first sound at 0.76s |
| sync | 10.0 | 53/53 sounds on their frame (peaks, arrivals, or first onsets for clicks) |
| coverage | n/a | not measured (pass --moments) |
| pacing | 9.0 | 7.4 weighted events per 10 s, longest silence 3.3 s |
| variety | 1.0 | 65 source recordings, 33 families in 70 sounds (runs and interface sounds not counted) |
| hierarchy | 10.0 | 14.4 dB between the loud and the quiet sounds |
| headroom | 10.0 | true peak -1.6 dBTP |
| loudness | 10.0 | final -15.3 LUFS (the author's own balance is kept) |
| balance | 10.0 | median event peak -12 dB vs the original around it, big sounds -6 dB (whole-track gap +7 LU) |
| mono | 10.0 | the SFX track loses 0.6 dB when folded to mono (0 = the channels agree, 3 = unrelated, 6+ = parts cancel); 0 of 77 sounds lose more than 6 dB; the film loses 0.2 LU in mono against 0.1 LU for the original (+0.1 added) |

**FIX**: lowest axis 1.0 (every axis must reach 8; ok to show)

Three worst problems, fix only these, re-render, run again:
1. variety: 5 takes of the same recording family 'rpg sound pack battle swing' (2.72s, 10.76s, 35.08s, 38.74s, 49.82s); mix in other sounds
2. pacing: two foley sounds 20 ms apart at 39.74s smear

Listen to these 5 moments, on headphones and then once on a phone speaker. This script cannot hear: they are the places where the numbers above are least certain, and none of them says that it sounds good:
  1.    0.76s  'glitch': the first sound of the film: the hook. Listen for: does it land with the picture at once, and is it clearly there under the music or the voice?
  2.   13.32s  'camera': the quietest by perceived loudness among the sounds that are not ticks. Listen for: can it be heard at all?
  3.   20.54s  'camera': brought 6 dB down to the perceived level of its role. Listen for: a sound brought down that far can get lost: does it still carry its moment?
  4.   32.79s  'hit': the highest peak of the film (-2 dBFS before the master). Listen for: is it big without hurting on headphones, and does the music under it pump?
  5.   35.58s  the busiest two seconds (11 sounds). Listen for: is every sound still distinct, or does it turn to mud?
  -> /home/user/Nxtlvl-Social/spin-bout-u-drake/cache/sfx/listen.wav: the 5 in this order, 3 s each

Still to judge by eye on review.png: character fit (each sound suits its picture), cleanliness (no mud in the low end under music/voice, nothing masks speech), taste (designed, not sprayed on).

---

# Critique, round 6

| axis | score | basis |
|---|---|---|
| hook | 9.0 | first sound at 0.76s |
| sync | 10.0 | 52/52 sounds on their frame (peaks, arrivals, or first onsets for clicks) |
| coverage | n/a | not measured (pass --moments) |
| pacing | 9.0 | 7.6 weighted events per 10 s, longest silence 3.3 s |
| variety | 1.0 | 65 source recordings, 35 families in 70 sounds (runs and interface sounds not counted) |
| hierarchy | 10.0 | 14.4 dB between the loud and the quiet sounds |
| headroom | 10.0 | true peak -1.6 dBTP |
| loudness | 10.0 | final -15.3 LUFS (the author's own balance is kept) |
| balance | 10.0 | median event peak -12 dB vs the original around it, big sounds -7 dB (whole-track gap +8 LU) |
| mono | 10.0 | the SFX track loses 0.5 dB when folded to mono (0 = the channels agree, 3 = unrelated, 6+ = parts cancel); 0 of 77 sounds lose more than 6 dB; the film loses 0.2 LU in mono against 0.1 LU for the original (+0.1 added) |

**FIX**: lowest axis 1.0 (every axis must reach 8; ok to show)

Three worst problems, fix only these, re-render, run again:
1. variety: 5 takes of the same recording family 'swishes swish' (6.16s, 12.96s, 20.34s, 38.74s, 42.42s); mix in other sounds
2. pacing: two foley sounds 100 ms apart at 39.74s smear

Listen to these 5 moments, on headphones and then once on a phone speaker. This script cannot hear: they are the places where the numbers above are least certain, and none of them says that it sounds good:
  1.    0.76s  'glitch': the first sound of the film: the hook. Listen for: does it land with the picture at once, and is it clearly there under the music or the voice?
  2.   13.32s  'camera': the quietest by perceived loudness among the sounds that are not ticks. Listen for: can it be heard at all?
  3.   14.84s  'swish': brought 6 dB up to the perceived level of its role. Listen for: a thin recording lifted that far can turn harsh: is it clean?
  4.   32.79s  'hit': the highest peak of the film (-2 dBFS before the master). Listen for: is it big without hurting on headphones, and does the music under it pump?
  5.   35.58s  the busiest two seconds (11 sounds). Listen for: is every sound still distinct, or does it turn to mud?
  -> /home/user/Nxtlvl-Social/spin-bout-u-drake/cache/sfx/listen.wav: the 5 in this order, 3 s each

Still to judge by eye on review.png: character fit (each sound suits its picture), cleanliness (no mud in the low end under music/voice, nothing masks speech), taste (designed, not sprayed on).

---

# Critique, round 7

| axis | score | basis |
|---|---|---|
| hook | 9.0 | first sound at 0.76s |
| sync | 10.0 | 50/50 sounds on their frame (peaks, arrivals, or first onsets for clicks) |
| coverage | n/a | not measured (pass --moments) |
| pacing | 10.0 | 7.8 weighted events per 10 s, longest silence 3.3 s |
| variety | 1.0 | 65 source recordings, 35 families in 70 sounds (runs and interface sounds not counted) |
| hierarchy | 10.0 | 14.4 dB between the loud and the quiet sounds |
| headroom | 10.0 | true peak -1.6 dBTP |
| loudness | 10.0 | final -15.3 LUFS (the author's own balance is kept) |
| balance | 10.0 | median event peak -12 dB vs the original around it, big sounds -7 dB (whole-track gap +8 LU) |
| mono | 10.0 | the SFX track loses 0.5 dB when folded to mono (0 = the channels agree, 3 = unrelated, 6+ = parts cancel); 0 of 77 sounds lose more than 6 dB; the film loses 0.2 LU in mono against 0.1 LU for the original (+0.1 added) |

**FIX**: lowest axis 1.0 (every axis must reach 8; ok to show)

Three worst problems, fix only these, re-render, run again:
1. variety: 4 takes of the same recording family 'audio glitch' (0.76s, 8.62s, 21.10s, 36.04s); mix in other sounds

Listen to these 5 moments, on headphones and then once on a phone speaker. This script cannot hear: they are the places where the numbers above are least certain, and none of them says that it sounds good:
  1.    0.76s  'glitch': the first sound of the film: the hook. Listen for: does it land with the picture at once, and is it clearly there under the music or the voice?
  2.   13.32s  'camera': the quietest by perceived loudness among the sounds that are not ticks. Listen for: can it be heard at all?
  3.   14.84s  'swish': brought 6 dB up to the perceived level of its role. Listen for: a thin recording lifted that far can turn harsh: is it clean?
  4.   32.79s  'hit': the highest peak of the film (-2 dBFS before the master). Listen for: is it big without hurting on headphones, and does the music under it pump?
  5.   35.58s  the busiest two seconds (11 sounds). Listen for: is every sound still distinct, or does it turn to mud?
  -> /home/user/Nxtlvl-Social/spin-bout-u-drake/cache/sfx/listen.wav: the 5 in this order, 3 s each

Still to judge by eye on review.png: character fit (each sound suits its picture), cleanliness (no mud in the low end under music/voice, nothing masks speech), taste (designed, not sprayed on).

---

# Critique, round 8

| axis | score | basis |
|---|---|---|
| hook | 9.0 | first sound at 0.76s |
| sync | 10.0 | 48/48 sounds on their frame (peaks, arrivals, or first onsets for clicks) |
| coverage | n/a | not measured (pass --moments) |
| pacing | 10.0 | 7.9 weighted events per 10 s, longest silence 3.3 s |
| variety | 1.0 | 65 source recordings, 35 families in 70 sounds (runs and interface sounds not counted) |
| hierarchy | 10.0 | 14.4 dB between the loud and the quiet sounds |
| headroom | 10.0 | true peak -1.6 dBTP |
| loudness | 10.0 | final -15.3 LUFS (the author's own balance is kept) |
| balance | 10.0 | median event peak -12 dB vs the original around it, big sounds -7 dB (whole-track gap +8 LU) |
| mono | 10.0 | the SFX track loses 0.5 dB when folded to mono (0 = the channels agree, 3 = unrelated, 6+ = parts cancel); 0 of 77 sounds lose more than 6 dB; the film loses 0.2 LU in mono against 0.1 LU for the original (+0.1 added) |

**FIX**: lowest axis 1.0 (every axis must reach 8; ok to show)

Three worst problems, fix only these, re-render, run again:
1. variety: 4 takes of the same recording family 'audio tick' (22.14s, 22.50s, 23.72s, 23.72s); mix in other sounds

Listen to these 5 moments, on headphones and then once on a phone speaker. This script cannot hear: they are the places where the numbers above are least certain, and none of them says that it sounds good:
  1.    0.76s  'glitch': the first sound of the film: the hook. Listen for: does it land with the picture at once, and is it clearly there under the music or the voice?
  2.    8.62s  'glitch': brought 6 dB down to the perceived level of its role. Listen for: a sound brought down that far can get lost: does it still carry its moment?
  3.   13.32s  'camera': the quietest by perceived loudness among the sounds that are not ticks. Listen for: can it be heard at all?
  4.   32.79s  'hit': the highest peak of the film (-2 dBFS before the master). Listen for: is it big without hurting on headphones, and does the music under it pump?
  5.   35.58s  the busiest two seconds (11 sounds). Listen for: is every sound still distinct, or does it turn to mud?
  -> /home/user/Nxtlvl-Social/spin-bout-u-drake/cache/sfx/listen.wav: the 5 in this order, 3 s each

Still to judge by eye on review.png: character fit (each sound suits its picture), cleanliness (no mud in the low end under music/voice, nothing masks speech), taste (designed, not sprayed on).

---

# Critique, round 9

| axis | score | basis |
|---|---|---|
| hook | 9.0 | first sound at 0.76s |
| sync | 10.0 | 47/47 sounds on their frame (peaks, arrivals, or first onsets for clicks) |
| coverage | n/a | not measured (pass --moments) |
| pacing | 10.0 | 7.9 weighted events per 10 s, longest silence 3.3 s |
| variety | 1.0 | 64 source recordings, 36 families in 69 sounds (runs and interface sounds not counted) |
| hierarchy | 10.0 | 14.4 dB between the loud and the quiet sounds |
| headroom | 10.0 | true peak -1.6 dBTP |
| loudness | 10.0 | final -15.3 LUFS (the author's own balance is kept) |
| balance | 10.0 | median event peak -12 dB vs the original around it, big sounds -7 dB (whole-track gap +7 LU) |
| mono | 10.0 | the SFX track loses 0.5 dB when folded to mono (0 = the channels agree, 3 = unrelated, 6+ = parts cancel); 0 of 76 sounds lose more than 6 dB; the film loses 0.2 LU in mono against 0.1 LU for the original (+0.1 added) |

**FIX**: lowest axis 1.0 (every axis must reach 8; ok to show)

Three worst problems, fix only these, re-render, run again:
1. variety: 4 takes of the same recording family 'qubodup megaswosh' (10.76s, 16.66s, 29.52s, 53.52s); mix in other sounds

Listen to these 5 moments, on headphones and then once on a phone speaker. This script cannot hear: they are the places where the numbers above are least certain, and none of them says that it sounds good:
  1.    0.76s  'glitch': the first sound of the film: the hook. Listen for: does it land with the picture at once, and is it clearly there under the music or the voice?
  2.    8.62s  'glitch': brought 6 dB down to the perceived level of its role. Listen for: a sound brought down that far can get lost: does it still carry its moment?
  3.   13.32s  'camera': the quietest by perceived loudness among the sounds that are not ticks. Listen for: can it be heard at all?
  4.   32.79s  'hit': the highest peak of the film (-2 dBFS before the master). Listen for: is it big without hurting on headphones, and does the music under it pump?
  5.   35.58s  the busiest two seconds (11 sounds). Listen for: is every sound still distinct, or does it turn to mud?
  -> /home/user/Nxtlvl-Social/spin-bout-u-drake/cache/sfx/listen.wav: the 5 in this order, 3 s each

Still to judge by eye on review.png: character fit (each sound suits its picture), cleanliness (no mud in the low end under music/voice, nothing masks speech), taste (designed, not sprayed on).

---

# Critique, round 10

| axis | score | basis |
|---|---|---|
| hook | 9.0 | first sound at 0.76s |
| sync | 10.0 | 48/48 sounds on their frame (peaks, arrivals, or first onsets for clicks) |
| coverage | n/a | not measured (pass --moments) |
| pacing | 10.0 | 7.9 weighted events per 10 s, longest silence 3.3 s |
| variety | 1.6 | 64 source recordings, 38 families in 69 sounds (runs and interface sounds not counted) |
| hierarchy | 10.0 | 14.4 dB between the loud and the quiet sounds |
| headroom | 10.0 | true peak -1.6 dBTP |
| loudness | 10.0 | final -15.3 LUFS (the author's own balance is kept) |
| balance | 10.0 | median event peak -12 dB vs the original around it, big sounds -7 dB (whole-track gap +7 LU) |
| mono | 10.0 | the SFX track loses 0.5 dB when folded to mono (0 = the channels agree, 3 = unrelated, 6+ = parts cancel); 0 of 76 sounds lose more than 6 dB; the film loses 0.2 LU in mono against 0.1 LU for the original (+0.1 added) |

**FIX**: lowest axis 1.6 (every axis must reach 8; ok to show)

Three worst problems, fix only these, re-render, run again:
1. variety: 4 takes of the same recording family 'paper stationery stationery' (2.03s, 24.55s, 48.43s, 59.03s); mix in other sounds

Listen to these 5 moments, on headphones and then once on a phone speaker. This script cannot hear: they are the places where the numbers above are least certain, and none of them says that it sounds good:
  1.    0.76s  'glitch': the first sound of the film: the hook. Listen for: does it land with the picture at once, and is it clearly there under the music or the voice?
  2.    8.62s  'glitch': brought 6 dB down to the perceived level of its role. Listen for: a sound brought down that far can get lost: does it still carry its moment?
  3.   13.32s  'camera': the quietest by perceived loudness among the sounds that are not ticks. Listen for: can it be heard at all?
  4.   32.79s  'hit': the highest peak of the film (-2 dBFS before the master). Listen for: is it big without hurting on headphones, and does the music under it pump?
  5.   35.58s  the busiest two seconds (11 sounds). Listen for: is every sound still distinct, or does it turn to mud?
  -> /home/user/Nxtlvl-Social/spin-bout-u-drake/cache/sfx/listen.wav: the 5 in this order, 3 s each

Still to judge by eye on review.png: character fit (each sound suits its picture), cleanliness (no mud in the low end under music/voice, nothing masks speech), taste (designed, not sprayed on).