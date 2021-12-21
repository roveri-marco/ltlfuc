#!/bin/bash

bash "./plot-AIJ-results.analysis.sh"

PLOTS_DIR="${HOME}/Code/LTLfUC/ltlfuc/etc/AIJ-SAT-explorer/AIJ-analysis-plots"
PAPER_DIR="${HOME}/University/Pubs/declarative/ltlfuc/5fb28731dd8ae36628ce6a3f"

#### Crop figures and move them to the paper directory

## Collate PDFs in a single booklet
pdftk "${PLOTS_DIR}/AIJ-analysis-results-plot-scatter_"* cat output "${PLOTS_DIR}/AIJ-analysis-results-plots-scatter_ALL.pdf"
pdftk "${PLOTS_DIR}/AIJ-analysis-results-plot-unsat-core-cardinality-scatter"* cat output "${PLOTS_DIR}/AIJ-analysis-results-plots-unsat-core-cardinality-scatter_ALL.pdf"

## Crop and move
for file in "${PLOTS_DIR}/AIJ-analysis-results-plot"*
do
  echo "Copying $file"
  pdfcrop "$file" "${PAPER_DIR}/img/`basename ${file}`"
done

cp "${PLOTS_DIR}/AIJ-results-analysis-summary.txt" "${PAPER_DIR}/img/AIJ-results-analysis-summary.txt"
cp "${PLOTS_DIR}/AIJ-results-virtual_best_info.csv" "${PAPER_DIR}/img/AIJ-results-virtual_best_info.csv"

exit 0
