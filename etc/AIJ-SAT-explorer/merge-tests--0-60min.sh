#!/bin/bash
#
# This script merges test results obtained with a threshold of 10 minutes with those obtained with a threshold of 60 minutes.
#
ANALYSIS_RESULTS_DIR="$HOME/Code/LTLfUC/ltlfuc/etc/AIJ-SAT-explorer/AIJ-SAT-explorer-res/AIJ-SAT-explorer"
DIR_0_10="$ANALYSIS_RESULTS_DIR/0-10min-reports"
DIR_10_60="$ANALYSIS_RESULTS_DIR/10-60min-reports"
ERROR_FILENAME_TOKEN="-error"
SUCCESS_FILENAME_TOKEN="-done"
TO_60_FROM_10_FILENAME_TOKEN="-to60"
FILENAME_EXTENSION="txt"
TOOLS=("aaltafuc" "ltlfuc_bdd" "ltlfuc_sat" "trppp")


for tool in ${TOOLS[@]}; do
  # Create success files. Start with 0-to-10-minute ones
  if [ -f "${DIR_0_10}/${tool}${SUCCESS_FILENAME_TOKEN}.${FILENAME_EXTENSION}" ]; then
    echo "Copying ${DIR_0_10}/${tool}${SUCCESS_FILENAME_TOKEN}.${FILENAME_EXTENSION} to ${ANALYSIS_RESULTS_DIR}"
    cp "${DIR_0_10}/${tool}${SUCCESS_FILENAME_TOKEN}.${FILENAME_EXTENSION}" "${ANALYSIS_RESULTS_DIR}"
  else
    echo "Creating ${ANALYSIS_RESULTS_DIR}/${tool}${SUCCESS_FILENAME_TOKEN}.${FILENAME_EXTENSION}"
    echo -n "" > "${ANALYSIS_RESULTS_DIR}/${tool}${SUCCESS_FILENAME_TOKEN}.${FILENAME_EXTENSION}"
  fi
  # Append results obtained with runs of 10 to 60 minutes
  if [ -f "${DIR_10_60}/${tool}${SUCCESS_FILENAME_TOKEN}${TO_60_FROM_10_FILENAME_TOKEN}.${FILENAME_EXTENSION}" ]; then
    echo "Appending ${DIR_10_60}/${tool}${SUCCESS_FILENAME_TOKEN}${TO_60_FROM_10_FILENAME_TOKEN}.${FILENAME_EXTENSION} to ${ANALYSIS_RESULTS_DIR}/${tool}${SUCCESS_FILENAME_TOKEN}.${FILENAME_EXTENSION}"
    cat "${DIR_10_60}/${tool}${SUCCESS_FILENAME_TOKEN}${TO_60_FROM_10_FILENAME_TOKEN}.${FILENAME_EXTENSION}" >> "${ANALYSIS_RESULTS_DIR}/${tool}${SUCCESS_FILENAME_TOKEN}.${FILENAME_EXTENSION}"
  fi
  # Create error files. Start with 0-to-10-minute ones. They contain supersets of 10-to-60-minute ones.
  if [ -f "${DIR_0_10}/${tool}${ERROR_FILENAME_TOKEN}.${FILENAME_EXTENSION}" ]; then
    echo "Copying ${DIR_0_10}/${tool}${ERROR_FILENAME_TOKEN}.${FILENAME_EXTENSION} to ${ANALYSIS_RESULTS_DIR}"
    cp "${DIR_0_10}/${tool}${ERROR_FILENAME_TOKEN}.${FILENAME_EXTENSION}" "${ANALYSIS_RESULTS_DIR}"
  else
    echo "Creating ${ANALYSIS_RESULTS_DIR}/${tool}${ERROR_FILENAME_TOKEN}.${FILENAME_EXTENSION}"
    echo -n "" > "${ANALYSIS_RESULTS_DIR}/${tool}${ERROR_FILENAME_TOKEN}.${FILENAME_EXTENSION}"
  fi
  # Remove results obtained with a runtime from 0 to 60 minutes from error files
  echo "Cleaning ${ANALYSIS_RESULTS_DIR}/${tool}${ERROR_FILENAME_TOKEN}.${FILENAME_EXTENSION}"
  grep -v -x -f "${ANALYSIS_RESULTS_DIR}/${tool}${SUCCESS_FILENAME_TOKEN}.${FILENAME_EXTENSION}" "${ANALYSIS_RESULTS_DIR}/${tool}${ERROR_FILENAME_TOKEN}.${FILENAME_EXTENSION}" > "${ANALYSIS_RESULTS_DIR}/${tool}${ERROR_FILENAME_TOKEN}.${FILENAME_EXTENSION}.bak"
  mv "${ANALYSIS_RESULTS_DIR}/${tool}${ERROR_FILENAME_TOKEN}.${FILENAME_EXTENSION}.bak" "${ANALYSIS_RESULTS_DIR}/${tool}${ERROR_FILENAME_TOKEN}.${FILENAME_EXTENSION}"
done

# exit 0
# DEBUG (comment the line above to unleash)
for tool in ${TOOLS[@]}; do
  # Check that tests are reported as successful only once
  sort "${ANALYSIS_RESULTS_DIR}/${tool}${SUCCESS_FILENAME_TOKEN}.${FILENAME_EXTENSION}" -o \
    "${ANALYSIS_RESULTS_DIR}/check-for-debug/${tool}${SUCCESS_FILENAME_TOKEN}-sorted.${FILENAME_EXTENSION}"
  sort "${ANALYSIS_RESULTS_DIR}/${tool}${SUCCESS_FILENAME_TOKEN}.${FILENAME_EXTENSION}" | uniq \
    -u > "${ANALYSIS_RESULTS_DIR}/check-for-debug/${tool}${SUCCESS_FILENAME_TOKEN}-unique.${FILENAME_EXTENSION}"
  echo "Checking uniqueness of results in ${ANALYSIS_RESULTS_DIR}/${tool}${SUCCESS_FILENAME_TOKEN}.${FILENAME_EXTENSION}"
  diff "${ANALYSIS_RESULTS_DIR}/check-for-debug/${tool}${SUCCESS_FILENAME_TOKEN}-sorted.${FILENAME_EXTENSION}" "${ANALYSIS_RESULTS_DIR}/check-for-debug/${tool}${SUCCESS_FILENAME_TOKEN}-unique.${FILENAME_EXTENSION}"
  echo

  # Check that generated error reports correpond to those left with runs from 10 to 60 minutes.
  sort "${ANALYSIS_RESULTS_DIR}/${tool}${ERROR_FILENAME_TOKEN}.${FILENAME_EXTENSION}" -o \
    "${ANALYSIS_RESULTS_DIR}/check-for-debug/${tool}${ERROR_FILENAME_TOKEN}-sorted.${FILENAME_EXTENSION}"
  sort "${DIR_10_60}/${tool}${ERROR_FILENAME_TOKEN}${TO_60_FROM_10_FILENAME_TOKEN}.${FILENAME_EXTENSION}" -o \
    "${ANALYSIS_RESULTS_DIR}/check-for-debug/${tool}${ERROR_FILENAME_TOKEN}${TO_60_FROM_10_FILENAME_TOKEN}-sorted.${FILENAME_EXTENSION}"
  echo "Checking correspondence of error terminations in ${ANALYSIS_RESULTS_DIR}/${tool}${ERROR_FILENAME_TOKEN}.${FILENAME_EXTENSION} and ${DIR_10_60}/${tool}${ERROR_FILENAME_TOKEN}${TO_60_FROM_10_FILENAME_TOKEN}.${FILENAME_EXTENSION}"
  diff "${ANALYSIS_RESULTS_DIR}/check-for-debug/${tool}${ERROR_FILENAME_TOKEN}-sorted.${FILENAME_EXTENSION}" \
    "${ANALYSIS_RESULTS_DIR}/check-for-debug/${tool}${ERROR_FILENAME_TOKEN}${TO_60_FROM_10_FILENAME_TOKEN}-sorted.${FILENAME_EXTENSION}"
  echo

done

exit 0