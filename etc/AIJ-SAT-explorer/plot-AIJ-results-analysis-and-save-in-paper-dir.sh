#!/bin/bash
CUSTOM_PLOT_SCRIPT='/home/cdc08x/Code/LTLfUC/ltlfuc/etc/AIJ-SAT-explorer/run-AIJ-results-analysis.py'
# Download it from https://github.com/alexeyignatiev/mkplot (beware that I have customised the scripts here and there, hence mkplotalt.py and scatteralt.py)
MKPLOT_ALT_SCRIPT='/home/cdc08x/Code/LTLfUC/mkplot/mkplotalt.py'
MKPLOT_SCRIPT='/home/cdc08x/Code/LTLfUC/mkplot/mkplot.py'
TIMEOUT=600
PLOTS_DIR='/home/cdc08x/Code/LTLfUC/ltlfuc/etc/AIJ-SAT-explorer/AIJ-analysis-plots'
PAPER_DIR='/home/cdc08x/University/Pubs/declarative/ltlfuc/5fb28731dd8ae36628ce6a3f'
PLOT_SCRIPT='/home/cdc08x/Code/LTLfUC/ltlfuc/etc/AIJ-SAT-explorer/run-AIJ-results-analysis.py'

# Create plots and JSON inputs for mkplot.py (and the altered version thereof)
python3 "${PLOT_SCRIPT}"

# Create plots with mkplot.py
python "${MKPLOT_ALT_SCRIPT}" -l --legend program -p scatter \
  -t "${TIMEOUT}" -b pdf \
  --xmin "0.0001" --ymin "0.0001" --xmax 20000 --ymax 20000 \
  --save-to "${PLOTS_DIR}/AIJ-analysis-results-plot-scatter.pdf" "${PLOTS_DIR}/AIJ-analysis-results-aaltafuc_w_preproc.json" "${PLOTS_DIR}/AIJ-analysis-results-trppp_w_preproc.json" 

python "${MKPLOT_SCRIPT}" -l --legend program -p cactus \
   -t "${TIMEOUT}" --xlabel "\# solved instances" --ymin "0.0001" --ylog -b pdf \
   --save-to "${PLOTS_DIR}/AIJ-analysis-results-plot-cactus.pdf" "${PLOTS_DIR}/AIJ-analysis-results-aaltafuc.json" "${PLOTS_DIR}/AIJ-analysis-results-trppp.json" "${PLOTS_DIR}/AIJ-analysis-results-ltlfuc_sat.json" "${PLOTS_DIR}/AIJ-analysis-results-nusmvb.json" "${PLOTS_DIR}/AIJ-analysis-results-v_best.json"

# Crop figures and move them to the paper directory

pdfcrop "${PLOTS_DIR}/AIJ-analysis-results-plot-clauses_v_time.pdf" "${PAPER_DIR}/img/AIJ-analysis-results-plot-clauses_v_time.pdf"

pdfcrop "${PLOTS_DIR}/AIJ-analysis-results-plot-cactus.pdf" "${PAPER_DIR}/img/AIJ-analysis-results-plot-cactus.pdf"

pdfcrop "${PLOTS_DIR}/AIJ-analysis-results-plot-scatter.pdf" "${PAPER_DIR}/img/AIJ-analysis-results-plot-scatter.pdf"

pdfcrop "${PLOTS_DIR}/AIJ-analysis-results-plot-unsat-core-cardinality-scatter_AALTAF-v-TRPPP.pdf" \
 "${PAPER_DIR}/img/AIJ-analysis-results-plot-unsat-core-cardinality-scatter_AALTAF-v-TRPPP.pdf"

pdfcrop "${PLOTS_DIR}/AIJ-analysis-results-plot-unsat-core-cardinality-scatter_AALTAF-v-NuSMVS.pdf" \
 "${PAPER_DIR}/img/AIJ-analysis-results-plot-unsat-core-cardinality-scatter_AALTAF-v-NuSMVS.pdf"

pdfcrop "${PLOTS_DIR}/AIJ-analysis-results-plot-unsat-core-cardinality-scatter_NuSMVS-v-TRPPP.pdf" \
 "${PAPER_DIR}/img/AIJ-analysis-results-plot-unsat-core-cardinality-scatter_NuSMVS-v-TRPPP.pdf"

exit 0
