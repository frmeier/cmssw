#!/bin/bash

echo "Remove old alignment file..."
rm Alignments.db 

echo "Run scram..."
scramv1 b &> scram.out

echo "Run cmsRun..."
cmsRun test-misalign_cfg.py &> cmsrun.out

echo "Dump Alignments.db..."
echo '.dump' | sqlite3 Alignments.db > Alignments.dump

echo "Diff..."
diff Alignments.dump Alignments_ref.dump | grep ALIGNMENTS > Alignments.diff
grep "^<" Alignments.diff | wc
grep "^<" Alignments.diff | head
grep "^>" Alignments.diff | wc
grep "^>" Alignments.diff | head

echo "Finished."

