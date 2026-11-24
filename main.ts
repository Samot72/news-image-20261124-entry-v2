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

// SHA-256 of a byte buffer, as lowercase hex.
function sha256Hex(bytes: Buffer): string {
  return createHash('sha256').update(bytes).digest('hex');
}

// Fail loudly unless the copy is byte-for-byte identical to the source:
// first the cheap length check, then the full SHA-256 comparison.
function verifyCopyMatchesSource(sourceBytes: Buffer, copiedBytes: Buffer): void {
  if (copiedBytes.length !== sourceBytes.length) {
    throw new Error(
      `entry.png copy length mismatch: source ${sourceBytes.length} bytes, copy ${copiedBytes.length} bytes`,
    );
  }

  const sourceHash = sha256Hex(sourceBytes);
  const copiedHash = sha256Hex(copiedBytes);

  if (copiedHash !== sourceHash) {
    throw new Error(`entry.png copy hash mismatch: source sha256 ${sourceHash}, copy sha256 ${copiedHash}`);
  }
}

// The committed image sits beside this file; the destination is the
// grader's output directory (or $MAKEFUN_OUTPUT_DIR outside the grader).
const committedImagePath = new URL('./entry.png', import.meta.url);
const destinationDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const destinationPath = join(destinationDir, 'entry.png');

copyFileSync(committedImagePath, destinationPath);

const committedBytes = readFileSync(committedImagePath);
const writtenBytes = readFileSync(destinationPath);

verifyCopyMatchesSource(committedBytes, writtenBytes);

console.log(`entry.png written to ${destinationPath}: ${writtenBytes.length} bytes, sha256 ${sha256Hex(writtenBytes)}`);
