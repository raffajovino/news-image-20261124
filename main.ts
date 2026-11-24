// main.ts — entrypoint for news-image-20261124 ("THE WORLD IN ONE DAY").
//
// Regenerates entry.png from draw.py (deterministic: fixed fonts, no clock,
// no randomness, so two runs are byte-identical) and copies it to the
// output directory the grader reads. Before copying, it verifies the file
// is a real PNG and within the gate's 1 MiB limit, so a broken or oversized
// render fails loudly here instead of silently submitting bad bytes.
//
//   Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
//   /output:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { execFileSync } from 'node:child_process';
import { copyFileSync, readFileSync, statSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const MAX_BYTES = 1024 * 1024;

execFileSync('python3', [join(here, 'draw.py')], { stdio: 'inherit' });

const src = join(here, 'entry.png');
const head = readFileSync(src).subarray(0, 8);
if (!head.equals(PNG_MAGIC)) {
  throw new Error('entry.png is not a PNG (bad magic bytes)');
}
const size = statSync(src).size;
if (size > MAX_BYTES) {
  throw new Error(`entry.png is ${size} bytes, over the 1 MiB gate`);
}
console.log(`entry.png OK: ${size} bytes, PNG magic verified`);

copyFileSync(src, join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'));
