#!/bin/bash
CUSTOM_PLOT_SCRIPT='/home/cdc08x/Code/LTLfUC/ltlfuc/etc/AIJ-SAT-explorer/run-AIJ-results-analysis.py'
# Download it from https://github.com/alexeyignatiev/mkplot (beware that I have customised the scripts here and there)
MKPLOT_SCRIPT='/home/cdc08x/Code/LTLfUC/mkplot/mkplot.py'
TIMEOUT=600
PLOTS_DIR='/home/cdc08x/Code/LTLfUC/ltlfuc/etc/AIJ-SAT-explorer/AIJ-analysis-plots'
PAPER_DIR='/home/cdc08x/University/Pubs/declarative/ltlfuc/5fb28731dd8ae36628ce6a3f'

python3 "${PLOT_SCRIPT_DIR}"

python "${MKPLOT_SCRIPT}" -l --legend program -p scatter \
  -t "${TIMEOUT}" -b pdf \
  --xmin "0.0001" --ymin "0.0001" --xmax 20000 --ymax 20000 \
  --save-to "${PLOTS_DIR}/AIJ-analysis-results-plot-scatter.pdf" "${PLOTS_DIR}/AIJ-analysis-results-aaltafuc_w_preproc.json" "${PLOTS_DIR}/AIJ-analysis-results-trppp_w_preproc.json" 

python "${MKPLOT_SCRIPT}" -l --legend program -p cactus \
   -t "${TIMEOUT}" --xlabel "Instances" --ymin "0.0001" --ylog -b pdf \
   --save-to "${PLOTS_DIR}/AIJ-analysis-results-plot-cactus.pdf" "${PLOTS_DIR}/AIJ-analysis-results-aaltafuc.json" "${PLOTS_DIR}/AIJ-analysis-results-trppp.json" "${PLOTS_DIR}/AIJ-analysis-results-nusmvb.json" "${PLOTS_DIR}/AIJ-analysis-results-nusmvs.json" "${PLOTS_DIR}/AIJ-analysis-results-v_best.json"
      
pdfcrop "${PLOTS_DIR}/AIJ-analysis-results-plot-clauses_v_time.pdf" "${PAPER_DIR}/img/AIJ-analysis-results-plot-clauses_v_time.pdf"

pdfcrop "${PLOTS_DIR}/AIJ-analysis-results-plot-cactus.pdf" "${PAPER_DIR}/img/AIJ-analysis-results-plot-cactus.pdf"

pdfcrop "${PLOTS_DIR}/AIJ-analysis-results-plot-scatter.pdf" "${PAPER_DIR}/img/AIJ-analysis-results-plot-scatter.pdf"


exit 0


python "${MKPLOT_SCRIPT}" -l --legend program -p cactus \
   -t "${TIMEOUT}" --xlabel "Instances" --ymin "0.0001" --ylog -b pdf \
   --save-to "${PLOTS_DIR}/AIJ-analysis-results-plot-cactus.pdf" "${PLOTS_DIR}/AIJ-analysis-results-nusmvb.json" "${PLOTS_DIR}/AIJ-analysis-results-nusmvs.json" 

