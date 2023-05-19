#!/bin/bash
# "mkplot" is a toolkit taken and adapted from https://github.com/alexeyignatiev/mkplot (scripts have been customised for these experiments, hence mkplotalt*.py and scatteralt*.py)
MKPLOT_FALSI_SCRIPT="${HOME}/Code/LTLfUC/ltlfuc/etc/AIJ-SAT-explorer/mkplot/mkplotaltfalsi.py"
MKPLOT_UNK_SCRIPT="${HOME}/Code/LTLfUC/ltlfuc/etc/AIJ-SAT-explorer/mkplot/mkplotaltunknown.py"
MKPLOT_FALSI_UNK_SCRIPT="${HOME}/Code/LTLfUC/ltlfuc/etc/AIJ-SAT-explorer/mkplot/mkplotaltfalsiunknown.py"
MKPLOT_SCRIPT="${HOME}/Code/LTLfUC/ltlfuc/etc/AIJ-SAT-explorer/mkplot/mkplot.py"
TIMEOUT=3600 #
PLOTS_DIR="${HOME}/Code/LTLfUC/ltlfuc/etc/AIJ-SAT-explorer/AIJ-analysis-plots"
PLOT_SCRIPT="${HOME}/Code/LTLfUC/ltlfuc/etc/AIJ-SAT-explorer/run-AIJ-results-analysis.py"

#### Create plots and JSON inputs for mkplot.py (and the altered version thereof)
python3 "${PLOT_SCRIPT}"

#### Create plots with mkplot.py and variants thereof

## Scatter plots
python3 "${MKPLOT_FALSI_SCRIPT}" -l --legend program -p scatter \
  -t "${TIMEOUT}" -b pdf \
  --xmin "0.0001" --ymin "0.0001" --xmax 82000 --ymax 82000 \
  --save-to "${PLOTS_DIR}/AIJ-analysis-results-plot-scatter_AALTAF-v-TRPPP.pdf" "${PLOTS_DIR}/AIJ-analysis-results-aaltafuc_w_preproc.json" "${PLOTS_DIR}/AIJ-analysis-results-trppp_w_preproc.json" 

python3 "${MKPLOT_UNK_SCRIPT}" -l --legend program -p scatter \
  -t "${TIMEOUT}" -b pdf \
  --xmin "0.0001" --ymin "0.0001" --xmax 82000 --ymax 82000 \
  --save-to "${PLOTS_DIR}/AIJ-analysis-results-plot-scatter_AALTAF-v-NuSMVS.pdf" "${PLOTS_DIR}/AIJ-analysis-results-aaltafuc_w_preproc.json" "${PLOTS_DIR}/AIJ-analysis-results-ltlfuc_sat_w_preproc.json" 

python3 "${MKPLOT_SCRIPT}" -l --legend program -p scatter \
  -t "${TIMEOUT}" -b pdf \
  --xmin "0.0001" --ymin "0.0001" --xmax 82000 --ymax 82000 \
  --save-to "${PLOTS_DIR}/AIJ-analysis-results-plot-scatter_AALTAF-v-NuSMVB.pdf" "${PLOTS_DIR}/AIJ-analysis-results-aaltafuc.json" "${PLOTS_DIR}/AIJ-analysis-results-ltlfuc_bdd.json" 

python3 "${MKPLOT_UNK_SCRIPT}" -l --legend program -p scatter --reverse \
  -t "${TIMEOUT}" -b pdf \
  --xmin "0.0001" --ymin "0.0001" --xmax 82000 --ymax 82000 \
  --save-to "${PLOTS_DIR}/AIJ-analysis-results-plot-scatter_NuSMVB-v-NuSMVS.pdf" "${PLOTS_DIR}/AIJ-analysis-results-ltlfuc_bdd_w_preproc.json" "${PLOTS_DIR}/AIJ-analysis-results-ltlfuc_sat_w_preproc.json" 

python3 "${MKPLOT_FALSI_SCRIPT}" -l --legend program -p scatter --reverse \
  -t "${TIMEOUT}" -b pdf \
  --xmin "0.0001" --ymin "0.0001" --xmax 82000 --ymax 82000 \
  --save-to "${PLOTS_DIR}/AIJ-analysis-results-plot-scatter_NuSMVB-v-TRPPP.pdf" "${PLOTS_DIR}/AIJ-analysis-results-ltlfuc_bdd.json" "${PLOTS_DIR}/AIJ-analysis-results-trppp_w_preproc.json"

python3 "${MKPLOT_FALSI_UNK_SCRIPT}" -l --legend program -p scatter \
  -t "${TIMEOUT}" -b pdf \
  --xmin "0.0001" --ymin "0.0001" --xmax 82000 --ymax 82000 \
  --save-to "${PLOTS_DIR}/AIJ-analysis-results-plot-scatter_NuSMVS-v-TRPPP.pdf" "${PLOTS_DIR}/AIJ-analysis-results-ltlfuc_sat_w_preproc.json" "${PLOTS_DIR}/AIJ-analysis-results-trppp_w_preproc.json"

## Cactus plots

python3 "${MKPLOT_SCRIPT}" -l --legend program -p cactus \
   -t "${TIMEOUT}" --xlabel "\# solved instances" \
   --lloc='lower right' --ymin "0.0001" --ylog -b pdf \
   --save-to "${PLOTS_DIR}/AIJ-analysis-results-plot-cactus.pdf" "${PLOTS_DIR}/AIJ-analysis-results-aaltafuc.json" "${PLOTS_DIR}/AIJ-analysis-results-trppp.json" "${PLOTS_DIR}/AIJ-analysis-results-ltlfuc_sat.json" "${PLOTS_DIR}/AIJ-analysis-results-ltlfuc_bdd.json" "${PLOTS_DIR}/AIJ-analysis-results-v_best.json"

python3 "${MKPLOT_SCRIPT}" -l --legend program -p cactus \
   -t "${TIMEOUT}" --xlabel "\# solved instances" \
   --lloc='lower right' --ymin "0.0001" --ylog -b pdf \
   --save-to "${PLOTS_DIR}/AIJ-analysis-results-plot-cactus_returned-uc-only.pdf" "${PLOTS_DIR}/AIJ-analysis-results-aaltafuc.json" "${PLOTS_DIR}/AIJ-analysis-results-trppp_w_preproc.json" "${PLOTS_DIR}/AIJ-analysis-results-ltlfuc_sat_w_preproc.json" "${PLOTS_DIR}/AIJ-analysis-results-ltlfuc_bdd.json" "${PLOTS_DIR}/AIJ-analysis-results-v_best.json"
   
# ZIP contents
zip -q -r 'AIJ-SAT-analysis-plots.zip' AIJ-analysis-plots/*.json AIJ-analysis-plots/*.csv AIJ-analysis-plots/*.pdf AIJ-analysis-plots/*/

## Collate PDFs in a single booklet
pdftk "${PLOTS_DIR}/AIJ-analysis-results-plot-scatter_"* cat output "${PLOTS_DIR}/AIJ-analysis-results-plots-scatter_ALL.pdf"
pdftk "${PLOTS_DIR}/AIJ-analysis-results-plot-unsat-core-cardinality-scatter"* cat output "${PLOTS_DIR}/AIJ-analysis-results-plots-unsat-core-cardinality-scatter_ALL.pdf"

exit 0
