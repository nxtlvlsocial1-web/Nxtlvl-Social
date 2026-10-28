# 3 AM database horror short: caption, hashtags, alt text

Files: `renders/nxtlvl_horror-db_reels_9x16_v1.mp4` (the Reel) and `renders/nxtlvl_horror-db_reels_9x16_v1_cover.png`
(the cover, built by `build/cover.py`).

## Caption (paste as is)

Comment "BACKUP" and I'll send you the setup that saved him.

03:07 AM. A developer thought he was wiping the test database. He was connected to production. 1.2 million rows, gone. The backup job had been dead since March, and nobody checked.

Claude had taken a snapshot before he ever asked it to "clean things up".

What actually saved him:

1. Snapshot the database before any destructive command, every time
2. Make your terminal scream when you're connected to production
3. Check that your backup jobs ran, not just that they exist
4. Keep production access separate from your everyday account

Save this before your next late-night deploy, and send it to the dev on your team who works at 3 AM.

#claudeai #aiagents #softwareengineering #devops #coding

## Extra hashtags (optional)

Instagram now favours a few relevant hashtags over a long block, so the five above are the main set. For reach tests,
add some of these in the first comment:

#programming #developer #database #backup #aitools #techhorror #startup #webdevelopment #cybersecurity #claude
#automation #codinglife

## Alt text (Advanced settings → Accessibility)

3D horror short shot like CCTV footage. A narrator sets the scene: at 3:07 AM a developer alone in a dark office thinks
he is wiping the test database, but he is connected to production. He presses Enter and deletes 1.2 million rows. The
lights die row by row, the server room turns red because the backup stopped in March, two coral eyes open at the end of
the dead corridor, and his phone fills with alerts. In the blackout the eyes open on his monitor: Claude, his AI agent,
which had taken a snapshot before he said "clean things up". It restores everything, then revokes his production
access. Ends with "Comment BACKUP".

## Why it's written this way (SEO)

- Instagram search reads the caption, the alt text and the words on screen. The key phrases (Claude AI, AI agent,
  production database, backup, developer) are in the hook, the list and the alt text, in words people search for.
- The first line is the CTA keyword (house rule), so it shows before "more" on every phone; the hook follows on the
  next line.
- One CTA: the "BACKUP" comment keyword, said once at the top. It only works if an auto-DM for "BACKUP" is set up
  before the Reel goes live, with the setup to send (the snapshot and backup checklist).
- The numbered list gives the practical lesson from the story, so it gets saved and shared, and people who watch
  muted still get the value.
