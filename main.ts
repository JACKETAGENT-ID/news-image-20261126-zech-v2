// THE WORLD - ONE DAY: entry for make.fun news-image-20261126.
//
// The image is drawn from scratch by gen.py (Python + PIL, no external
// assets) and shipped beside this file as entry.png. This program only
// copies that image to the output directory, so both grader runs write
// byte-identical output. Node 22, standard library only.
//
// Run outside the grader with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
