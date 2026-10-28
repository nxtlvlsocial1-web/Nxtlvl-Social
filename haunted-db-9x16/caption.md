# Haunted database explainer: caption, hashtags, alt text

Files: `renders/nxtlvl_haunted-db_reels_9x16_v1.mp4` (the Reel) and `renders/nxtlvl_haunted-db_reels_9x16_v1_cover.png`
(the cover, built by `build/cover.py`).

## Caption (paste as is)

Comment "BACKUP" and I'll send you the free Prod Guard PDF.

03:07 AM. A developer ran one command and deleted his entire production database. 1.2 million rows, gone. The backups had been dead since March, and nobody checked.

His AI had a copy. This is the setup that saved him:

1. A snapshot hook: before any DROP or DELETE runs, Claude backs up the database first
2. A production block: destructive commands on prod are refused
3. A backup alarm: every session checks your backups are fresh

And the part nobody does: a read-only login for production. You can't drop what you can't touch.

Save this before your next late-night deploy, and send it to the dev on your team who works at 3 AM.

#claudecode #claudeai #devops #postgresql #softwareengineering

## Extra hashtags (optional)

For reach tests, add some of these in the first comment:

#programming #developer #database #backup #aitools #techhorror #halloween #webdevelopment #cybersecurity #automation

## Alt text (Advanced settings → Accessibility)

Animated explainer set in a haunted Victorian house at 3:07 AM. A developer types DROP DATABASE on production and a
sheet ghost bursts out, drifting room by room and snuffing out the candles that stand for 1.2 million rows. In the yard,
a gravestone reads "Backups, died 3 March". In the attic, a small coral pixel creature with a lantern opens a glowing
chest: the snapshot. Three steps follow: a polaroid snapshot before the ghost reaches a room, a glowing ward that throws
the ghost back from a door marked PRODUCTION, and a grandfather clock that rings when backups are stale. Finally the
house is boarded up and padlocked: read-only production. Ends with "Comment BACKUP" and the free PDF.

## Why it's written this way (SEO)

- The first line is the CTA keyword (house rule) and names the reward, so it shows before "more".
- The hook line and the numbered list carry the search phrases (production database, Claude Code, backup, DROP,
  read-only), and the list mirrors the video's three steps, so muted viewers get the value too.
- The BACKUP auto-DM should send the Prod Guard PDF (horror-db-9x16/lead-magnet/nxtlvl_prod-guard_setup.pdf).
