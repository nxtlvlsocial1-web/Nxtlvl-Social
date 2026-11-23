#!/bin/bash
# Kokoro local Hindi TTS, one wav per line of plan/vo_script.tsv.  usage: bash build/vo.sh <voice> <speed> <outdir>
set -e
cd "$(dirname "$0")/.."
V=${1:-hf_alpha}; SP=${2:-1.0}; OUT=${3:-assets/audio/vo}
mkdir -p "$OUT"
while IFS=$'\t' read -r id txt; do
  HYPERFRAMES_PYTHON=/root/.venvs/kokoro/bin/python npx --yes hyperframes@0.9.86 tts "$txt" --voice "$V" --speed "$SP" -o "$OUT/$id.wav" >/dev/null 2>&1
  printf "%s %s\n" "$id" "$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT/$id.wav")"
done < plan/vo_script.tsv
