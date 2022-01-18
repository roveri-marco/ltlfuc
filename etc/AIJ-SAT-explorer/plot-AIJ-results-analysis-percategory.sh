#!/bin/bash
#
# Notice that this file partially duplicates the contents of "plot-AIJ-results-analysis.sh" in this very same directory.
# However, it creates plots for the information stored in subfolders too. We use subfolders to separate test sets.
# See run-AIJ-results-analysis.py for more details.
#
CUSTOM_PLOT_SCRIPT="${HOME}/Code/LTLfUC/ltlfuc/etc/AIJ-SAT-explorer/run-AIJ-results-analysis.py"
# "mkplot" is a toolkit taken and adapted from https://github.com/alexeyignatiev/mkplot (scripts have been customised for these experiments, hence mkplotalt*.py and scatteralt*.py)
MKPLOT_FALSI_SCRIPT="${HOME}/Code/LTLfUC/ltlfuc/etc/AIJ-SAT-explorer/mkplot/mkplotaltfalsi.py"
MKPLOT_UNK_SCRIPT="${HOME}/Code/LTLfUC/ltlfuc/etc/AIJ-SAT-explorer/mkplot/mkplotaltunknown.py"
MKPLOT_FALSI_UNK_SCRIPT="${HOME}/Code/LTLfUC/ltlfuc/etc/AIJ-SAT-explorer/mkplot/mkplotaltfalsiunknown.py"
MKPLOT_SCRIPT="${HOME}/Code/LTLfUC/ltlfuc/etc/AIJ-SAT-explorer/mkplot/mkplot.py"
TIMEOUT=600 # 
PLOTS_DIR="${HOME}/Code/LTLfUC/ltlfuc/etc/AIJ-SAT-explorer/AIJ-analysis-plots"
PLOT_SCRIPT="${HOME}/Code/LTLfUC/ltlfuc/etc/AIJ-SAT-explorer/run-AIJ-results-analysis.py"

#### Create plots and JSON inputs for mkplot.py (and the altered version thereof)
# python3 "${PLOT_SCRIPT}"

#### Create plots with mkplot.py and variants thereof

for plots_dir in "$PLOTS_DIR/"*/ "$PLOTS_DIR/"
do
  echo "Plotting results in $plots_dir"

  ## Scatter plots
  python "${MKPLOT_FALSI_SCRIPT}" -l --legend program -p scatter \
    -t "${TIMEOUT}" -b pdf \
    --xmin "0.0001" --ymin "0.0001" --xmax 20000 --ymax 20000 \
    --save-to "${plots_dir}/AIJ-analysis-results-plot-scatter_AALTAF-v-TRPPP.pdf" "${plots_dir}/AIJ-analysis-results-aaltafuc_w_preproc.json" "${plots_dir}/AIJ-analysis-results-trppp_w_preproc.json"

  python "${MKPLOT_UNK_SCRIPT}" -l --legend program -p scatter \
    -t "${TIMEOUT}" -b pdf \
    --xmin "0.0001" --ymin "0.0001" --xmax 20000 --ymax 20000 \
    --save-to "${plots_dir}/AIJ-analysis-results-plot-scatter_AALTAF-v-NuSMVS.pdf" "${plots_dir}/AIJ-analysis-results-aaltafuc_w_preproc.json" "${plots_dir}/AIJ-analysis-results-ltlfuc_sat_w_preproc.json"

  python "${MKPLOT_SCRIPT}" -l --legend program -p scatter \
    -t "${TIMEOUT}" -b pdf \
    --xmin "0.0001" --ymin "0.0001" --xmax 20000 --ymax 20000 \
    --save-to "${plots_dir}/AIJ-analysis-results-plot-scatter_AALTAF-v-NuSMVB.pdf" "${plots_dir}/AIJ-analysis-results-aaltafuc.json" "${plots_dir}/AIJ-analysis-results-ltlfuc_bdd.json"

  python "${MKPLOT_UNK_SCRIPT}" -l --legend program -p scatter --reverse \
    -t "${TIMEOUT}" -b pdf \
    --xmin "0.0001" --ymin "0.0001" --xmax 20000 --ymax 20000 \
    --save-to "${plots_dir}/AIJ-analysis-results-plot-scatter_NuSMVB-v-NuSMVS.pdf" "${plots_dir}/AIJ-analysis-results-ltlfuc_bdd_w_preproc.json" "${plots_dir}/AIJ-analysis-results-ltlfuc_sat_w_preproc.json"

  python "${MKPLOT_FALSI_SCRIPT}" -l --legend program -p scatter --reverse \
    -t "${TIMEOUT}" -b pdf \
    --xmin "0.0001" --ymin "0.0001" --xmax 20000 --ymax 20000 \
    --save-to "${plots_dir}/AIJ-analysis-results-plot-scatter_NuSMVB-v-TRPPP.pdf" "${plots_dir}/AIJ-analysis-results-ltlfuc_bdd.json" "${plots_dir}/AIJ-analysis-results-trppp_w_preproc.json"

  python "${MKPLOT_FALSI_UNK_SCRIPT}" -l --legend program -p scatter \
    -t "${TIMEOUT}" -b pdf \
    --xmin "0.0001" --ymin "0.0001" --xmax 20000 --ymax 20000 \
    --save-to "${plots_dir}/AIJ-analysis-results-plot-scatter_NuSMVS-v-TRPPP.pdf" "${plots_dir}/AIJ-analysis-results-ltlfuc_sat_w_preproc.json" "${plots_dir}/AIJ-analysis-results-trppp_w_preproc.json"

  ## Cactus plots

  python "${MKPLOT_SCRIPT}" -l --legend program -p cactus \
     -t "${TIMEOUT}" --xlabel "\# solved instances" \
     --lloc='lower right' --ymin "0.0001" --ylog -b pdf \
     --save-to "${plots_dir}/AIJ-analysis-results-plot-cactus.pdf" "${plots_dir}/AIJ-analysis-results-aaltafuc.json" "${plots_dir}/AIJ-analysis-results-trppp.json" "${plots_dir}/AIJ-analysis-results-ltlfuc_sat.json" "${plots_dir}/AIJ-analysis-results-ltlfuc_bdd.json" "${plots_dir}/AIJ-analysis-results-v_best.json"

  python "${MKPLOT_SCRIPT}" -l --legend program -p cactus \
     -t "${TIMEOUT}" --xlabel "\# solved instances" \
     --lloc='lower right' --ymin "0.0001" --ylog -b pdf \
     --save-to "${plots_dir}/AIJ-analysis-results-plot-cactus_returned-uc-only.pdf" "${plots_dir}/AIJ-analysis-results-aaltafuc.json" "${plots_dir}/AIJ-analysis-results-trppp_w_preproc.json" "${plots_dir}/AIJ-analysis-results-ltlfuc_sat_w_preproc.json" "${plots_dir}/AIJ-analysis-results-ltlfuc_bdd.json" "${plots_dir}/AIJ-analysis-results-v_best.json"
done

# ZIP contents
zip -r 'AIJ-SAT-analysis-plots.zip' AIJ-analysis-plots/*.json AIJ-analysis-plots/*.pdf AIJ-analysis-plots/*/

exit 0
