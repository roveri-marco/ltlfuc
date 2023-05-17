#!/bin/bash
ANALYSIS_RESULTS_DIR="$HOME/Code/LTLfUC/ltlfuc/etc/AIJ-SAT-explorer/AIJ-SAT-explorer-res/AIJ-SAT-explorer"
# LTLfUC_SAT-success-file renaming for pattern consistency
if [ -f "${ANALYSIS_RESULTS_DIR}/ltlfucsat-done.txt" ]; then
  mv "${ANALYSIS_RESULTS_DIR}/ltlfucsat-done.txt" "${ANALYSIS_RESULTS_DIR}/ltlfuc_sat-done.txt"
fi
# LTLfUC_SAT-error-file renaming for pattern consistency
if [ -f "${ANALYSIS_RESULTS_DIR}/ltlfucsat-done.txt" ]; then
  mv "${ANALYSIS_RESULTS_DIR}/ltlfucsat-error.txt" "${ANALYSIS_RESULTS_DIR}/ltlfuc_sat-error.txt"
fi
# Removing error entries from LTLfUC_SAT-error-file retained in LTLfUC_SAT-success-file
grep -v -x -f "${ANALYSIS_RESULTS_DIR}/ltlfuc_sat-error.txt" "${ANALYSIS_RESULTS_DIR}/ltlfuc_sat-done.txt" > "${ANALYSIS_RESULTS_DIR}/ltlfuc_sat-error.txt.clean"
mv "${ANALYSIS_RESULTS_DIR}/ltlfuc_sat-error.txt.clean" "${ANALYSIS_RESULTS_DIR}/ltlfuc_sat-done.txt"

# Anonymising files in which the developers’ names occur
grep -rl roveri | xargs sed -i -e 's:/home/mroveri:$HOME:g' -e 's:/home/marco.roveri:$HOME:g'
