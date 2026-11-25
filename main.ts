// main.ts -- entrypoint for the news-image-20261125 bounty.
// Node 22, standard library only.
//
// The entry image (entry.png, painted by render.py) sits next to this
// file. This program copies it into the output directory the grader
// provides, after confirming it is a whole PNG inside the competition's
// limits: at most 1 MiB and at most 1024x1024 pixels. It never touches
// the network, and every run writes exactly the same bytes.
//
// Run locally:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const PNG_SIGNATURE = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);
const MAX_FILE_BYTES = 1048576; // 1 MiB, the competition's gate
const MAX_SIDE = 1024;

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, 'entry.png');
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const target = join(outputDir, 'entry.png');

const image = readFileSync(source);
if (image.length < 24 || !image.subarray(0, 8).equals(PNG_SIGNATURE)) {
  throw new Error('entry.png does not start with the PNG signature');
}
if (image.length > MAX_FILE_BYTES) {
  throw new Error(
    `entry.png is ${image.length} bytes, over the 1 MiB limit`,
  );
}
// A PNG stores its pixel size in the IHDR chunk: width at offset 16,
// height at offset 20, both big-endian 32-bit.
const width = image.readUInt32BE(16);
const height = image.readUInt32BE(20);
if (width > MAX_SIDE || height > MAX_SIDE) {
  throw new Error(`entry.png is ${width}x${height}, over 1024x1024`);
}

mkdirSync(outputDir, { recursive: true });
copyFileSync(source, target);
console.log(`wrote ${target} (${width}x${height}, ${image.length} bytes)`);
