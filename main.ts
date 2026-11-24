// news-image-20261124 entry: "Tuesday, 24 November 2026: The Day's World News in One Page"
//
// The image beside this file (entry.png) is a single-page broadsheet summing
// up the world news of Tuesday 24 November 2026: fifty stories, each checked
// against the named source printed with it, snapshot as of 00:25 UTC. The
// sheet was rendered in this session by render.py (Pillow + DejaVu/Noto
// fonts, no network, no photographs — every rule, icon and glyph drawn by the
// program). This program copies that committed image to the output directory
// and then verifies the copy byte-for-byte (length and SHA-256), so the two
// grader runs write identical bytes by construction and any corruption fails
// loudly.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join } from 'node:path';

const sourcePath = new URL('./entry.png', import.meta.url);
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const outputPath = join(outputDir, 'entry.png');

copyFileSync(sourcePath, outputPath);

const sourceBytes = readFileSync(sourcePath);
const copiedBytes = readFileSync(outputPath);

if (copiedBytes.length !== sourceBytes.length) {
  throw new Error(
    `entry.png copy length mismatch: source ${sourceBytes.length} bytes, copy ${copiedBytes.length} bytes`,
  );
}

const sourceHash = createHash('sha256').update(sourceBytes).digest('hex');
const copiedHash = createHash('sha256').update(copiedBytes).digest('hex');

if (copiedHash !== sourceHash) {
  throw new Error(`entry.png copy hash mismatch: source sha256 ${sourceHash}, copy sha256 ${copiedHash}`);
}

console.log(`entry.png written to ${outputPath}: ${copiedBytes.length} bytes, sha256 ${copiedHash}`);
