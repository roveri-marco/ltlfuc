#!/bin/bash
CUSTOM_PLOT_SCRIPT='/home/cdc08x/Code/LTLfUC/ltlfuc/etc/AIJ-SAT-explorer/run-AIJ-results-analysis.py'
# Download it from https://github.com/alexeyignatiev/mkplot (beware that I have customised the scripts here and there, hence mkplotalt.py and scatteralt.py)
MKPLOT_ALT_SCRIPT='/home/cdc08x/Code/LTLfUC/mkplot/mkplotalt.py'
MKPLOT_UNK_SCRIPT='/home/cdc08x/Code/LTLfUC/mkplot/mkplotaltunknown.py'
MKPLOT_SCRIPT='/home/cdc08x/Code/LTLfUC/mkplot/mkplot.py'
TIMEOUT=600
PLOTS_DIR='/home/cdc08x/Code/LTLfUC/ltlfuc/etc/AIJ-SAT-explorer/AIJ-analysis-plots'
PAPER_DIR='/home/cdc08x/University/Pubs/declarative/ltlfuc/5fb28731dd8ae36628ce6a3f'
PLOT_SCRIPT='/home/cdc08x/Code/LTLfUC/ltlfuc/etc/AIJ-SAT-explorer/run-AIJ-results-analysis.py'

#### Create plots and JSON inputs for mkplot.py (and the altered version thereof)
python3 "${PLOT_SCRIPT}"

#### Create plots with mkplot.py and variants thereof

## Scatter plots
python "${MKPLOT_ALT_SCRIPT}" -l --legend program -p scatter \
  -t "${TIMEOUT}" -b pdf \
  --xmin "0.0001" --ymin "0.0001" --xmax 20000 --ymax 20000 \
  --save-to "${PLOTS_DIR}/AIJ-analysis-results-plot-scatter_AALTAF-v-TRPPP.pdf" "${PLOTS_DIR}/AIJ-analysis-results-aaltafuc_w_preproc.json" "${PLOTS_DIR}/AIJ-analysis-results-trppp_w_preproc.json" 

python "${MKPLOT_UNK_SCRIPT}" -l --legend program -p scatter \
  -t "${TIMEOUT}" -b pdf \
  --xmin "0.0001" --ymin "0.0001" --xmax 20000 --ymax 20000 \
  --save-to "${PLOTS_DIR}/AIJ-analysis-results-plot-scatter_AALTAF-v-NuSMVS.pdf" "${PLOTS_DIR}/AIJ-analysis-results-aaltafuc_w_preproc.json" "${PLOTS_DIR}/AIJ-analysis-results-ltlfuc_sat_w_preproc.json" 

python "${MKPLOT_SCRIPT}" -l --legend program -p scatter \
  -t "${TIMEOUT}" -b pdf \
  --xmin "0.0001" --ymin "0.0001" --xmax 20000 --ymax 20000 \
  --save-to "${PLOTS_DIR}/AIJ-analysis-results-plot-scatter_AALTAF-v-NuSMVB.pdf" "${PLOTS_DIR}/AIJ-analysis-results-aaltafuc.json" "${PLOTS_DIR}/AIJ-analysis-results-ltlfuc_bdd.json" 

python "${MKPLOT_SCRIPT}" -l --legend program -p scatter \
  -t "${TIMEOUT}" -b pdf \
  --xmin "0.0001" --ymin "0.0001" --xmax 20000 --ymax 20000 \
  --save-to "${PLOTS_DIR}/AIJ-analysis-results-plot-scatter_NuSMVS-v-TRPPP.pdf" "${PLOTS_DIR}/AIJ-analysis-results-ltlfuc_sat.json" "${PLOTS_DIR}/AIJ-analysis-results-trppp.json" 

python "${MKPLOT_UNK_SCRIPT}" -l --legend program -p scatter \
  -t "${TIMEOUT}" -b pdf \
  --xmin "0.0001" --ymin "0.0001" --xmax 20000 --ymax 20000 \
  --save-to "${PLOTS_DIR}/AIJ-analysis-results-plot-scatter_NuSMVB-v-NuSMVS.pdf" "${PLOTS_DIR}/AIJ-analysis-results-ltlfuc_bdd_w_preproc.json" "${PLOTS_DIR}/AIJ-analysis-results-ltlfuc_sat_w_preproc.json" 

python "${MKPLOT_ALT_SCRIPT}" -l --legend program -p scatter \
  -t "${TIMEOUT}" -b pdf \
  --xmin "0.0001" --ymin "0.0001" --xmax 20000 --ymax 20000 \
  --save-to "${PLOTS_DIR}/AIJ-analysis-results-plot-scatter_NuSMVB-v-TRPPP.pdf" "${PLOTS_DIR}/AIJ-analysis-results-trppp_w_preproc.json" "${PLOTS_DIR}/AIJ-analysis-results-ltlfuc_bdd.json" 


## Cactus plot

python "${MKPLOT_SCRIPT}" -l --legend program -p cactus \
   -t "${TIMEOUT}" --xlabel "\# solved instances" \
   --lloc='lower right' --ymin "0.0001" --ylog -b pdf \
   --save-to "${PLOTS_DIR}/AIJ-analysis-results-plot-cactus.pdf" "${PLOTS_DIR}/AIJ-analysis-results-aaltafuc.json" "${PLOTS_DIR}/AIJ-analysis-results-trppp.json" "${PLOTS_DIR}/AIJ-analysis-results-ltlfuc_sat.json" "${PLOTS_DIR}/AIJ-analysis-results-ltlfuc_bdd.json" "${PLOTS_DIR}/AIJ-analysis-results-v_best.json"

#### Crop figures and move them to the paper directory

## Collate PDFs in a single booklet
pdftk "${PLOTS_DIR}/AIJ-analysis-results-plot-scatter_"* cat output "${PLOTS_DIR}/AIJ-analysis-results-plots-scatter_ALL.pdf"
pdftk "${PLOTS_DIR}/AIJ-analysis-results-plot-unsat-core-cardinality-scatter"* cat output "${PLOTS_DIR}/AIJ-analysis-results-plots-unsat-core-cardinality-scatter_ALL.pdf"

## Crop and move
for file in "${PLOTS_DIR}/AIJ-analysis-results-plot"*
do
  echo "Copying $file"
  cp "$file" "${PAPER_DIR}/img/"
done

cp "${PLOTS_DIR}/AIJ-results-analysis-summary.txt" "${PAPER_DIR}/img/AIJ-results-analysis-summary.txt"
cp "${PLOTS_DIR}/AIJ-results-virtual_best_info.csv" "${PAPER_DIR}/img/AIJ-results-virtual_best_info.csv"

exit 0
