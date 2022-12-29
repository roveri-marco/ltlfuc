#!/bin/bash

bash "./plot-AIJ-results-analysis.sh"

PLOTS_DIR="${HOME}/Code/LTLfUC/ltlfuc/etc/AIJ-SAT-explorer/AIJ-analysis-plots"
PAPER_DIR="${HOME}/University/Pubs/declarative/ltlfuc/5fb28731dd8ae36628ce6a3f/src-j"

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

# Special treatment for category-based analysis plots
files_from=(
  "${PLOTS_DIR}/LTLf-specific_benchmarks_ltlf_LTLfRandomConjunction_V20/AIJ-analysis-results-plot-clauses_v_time.pdf"
  "${PLOTS_DIR}/LTLf-specific_benchmarks_ltlf_LTLfRandomConjunction_C100/AIJ-analysis-results-plot-clauses_v_time.pdf"
  "${PLOTS_DIR}/LTL-as-LTLf_schuppan_O1formula/AIJ-analysis-results-plot-clauses_v_time.pdf"
)
# Make sure the following array has the same length as $files_from
files_to=(
  "${PAPER_DIR}/img/LTLFRC20-AIJ-analysis-results-plot-clauses_v_time.pdf"
  "${PAPER_DIR}/img/LTLFRC100-AIJ-analysis-results-plot-clauses_v_time.pdf"
  "${PAPER_DIR}/img/SchuppanO1-AIJ-analysis-results-plot-clauses_v_time.pdf"
)
special_files_num=${#files_from[*]}
for (( i=0; i<=$(( $special_files_num -1 )); i++ ))
do
  echo "Copying ${files_from[i]} into ${files_to[i]}"
  pdfcrop "${files_from[i]}" "${files_to[i]}"
done

cp "${PLOTS_DIR}/AIJ-analysis-results-summary.txt" "${PAPER_DIR}/img/AIJ-analysis-results-summary.txt"
cp "${PLOTS_DIR}/AIJ-analysis-results-virtual-best-info.csv" "${PAPER_DIR}/img/AIJ-analysis-results-virtual-best-info.csv"

exit 0
