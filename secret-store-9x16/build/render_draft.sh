#!/bin/bash
# draft render of secret-store-9x16 for review, fully detached; writes DONE or FAILED
cd /home/user/Nxtlvl-Social/secret-store-9x16 || exit 1
S=/tmp/secret-store-render; mkdir -p $S renders
rm -f renders/nxtlvl_secret-store_reels_9x16_draft.mp4 $S/draft.status
if HYPERFRAMES_RENDER_DETACHED=1 HYPERFRAMES_NO_TELEMETRY=1 HF_SEGMENTED_CAPTURE=true HF_SEGMENT_FRAMES=300 npx --yes hyperframes@0.8.203 render "$PWD" --quality draft --workers 4 --fps 30 -o renders/nxtlvl_secret-store_reels_9x16_draft.mp4 < <(sleep infinity) > $S/draft.log 2>&1; then
  echo DONE > $S/draft.status
else
  echo FAILED > $S/draft.status
fi
