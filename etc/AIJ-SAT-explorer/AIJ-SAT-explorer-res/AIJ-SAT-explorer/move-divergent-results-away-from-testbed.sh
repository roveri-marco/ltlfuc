#!/bin/bash
EXCLUDED_TESTS_DIR='AIJ-SAT-explorer-res_REMOVED'
LOCAL_PREFIX="AIJ-SAT-explorer-res/"
DIVERGENT_FILE_STEMS=(
  'AIJ-SAT-explorer-res/AIJ-SAT-explorer/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/rozier/formulas/n2/P0.3/L70/P0.333333333333333N2L70_6.negated'
  'AIJ-SAT-explorer-res/AIJ-SAT-explorer/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/rozier/formulas/n2/P0.3/L80/P0.333333333333333N2L80_8'
  'AIJ-SAT-explorer-res/AIJ-SAT-explorer/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/rozier/formulas/n2/P0.3/L90/P0.333333333333333N2L90_3.negated'
  'AIJ-SAT-explorer-res/AIJ-SAT-explorer/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/rozier/formulas/n2/P0.5/L100/P0.5N2L100_1'
  'AIJ-SAT-explorer-res/AIJ-SAT-explorer/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/rozier/formulas/n2/P0.5/L30/P0.5N2L30_2'
  'AIJ-SAT-explorer-res/AIJ-SAT-explorer/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/rozier/formulas/n2/P0.5/L30/P0.5N2L30_8'
  'AIJ-SAT-explorer-res/AIJ-SAT-explorer/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/rozier/formulas/n2/P0.5/L40/P0.5N2L40_1'
  'AIJ-SAT-explorer-res/AIJ-SAT-explorer/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/rozier/formulas/n2/P0.5/L60/P0.5N2L60_2'
  'AIJ-SAT-explorer-res/AIJ-SAT-explorer/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/rozier/formulas/n2/P0.5/L90/P0.5N2L90_3'
  'AIJ-SAT-explorer-res/AIJ-SAT-explorer/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/rozier/formulas/n2/P0.7/L30/P0.7N2L30_6'
  'AIJ-SAT-explorer-res/AIJ-SAT-explorer/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/rozier/formulas/n2/P0.7/L40/P0.7N2L40_4.negated'
  'AIJ-SAT-explorer-res/AIJ-SAT-explorer/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/rozier/formulas/n2/P0.7/L60/P0.7N2L60_3'
  'AIJ-SAT-explorer-res/AIJ-SAT-explorer/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/rozier/formulas/n2/P0.95/L60/P0.95N2L60_1'
  'AIJ-SAT-explorer-res/AIJ-SAT-explorer/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/rozier/formulas/n2/P0.95/L90/P0.95N2L90_7'
  'AIJ-SAT-explorer-res/AIJ-SAT-explorer/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/rozier/formulas/n3/P0.3/L70/P0.333333333333333N3L70_10'
  'AIJ-SAT-explorer-res/AIJ-SAT-explorer/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/rozier/formulas/n3/P0.3/L80/P0.333333333333333N3L80_9.negated'
  'AIJ-SAT-explorer-res/AIJ-SAT-explorer/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/rozier/formulas/n3/P0.5/L100/P0.5N3L100_5.negated'
  'AIJ-SAT-explorer-res/AIJ-SAT-explorer/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/rozier/formulas/n3/P0.5/L60/P0.5N3L60_2'
  'AIJ-SAT-explorer-res/AIJ-SAT-explorer/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/rozier/formulas/n3/P0.5/L70/P0.5N3L70_2'
  'AIJ-SAT-explorer-res/AIJ-SAT-explorer/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/rozier/formulas/n3/P0.5/L80/P0.5N3L80_6'
  'AIJ-SAT-explorer-res/AIJ-SAT-explorer/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/rozier/formulas/n3/P0.7/L10/P0.7N3L10_9'
  'AIJ-SAT-explorer-res/AIJ-SAT-explorer/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/rozier/formulas/n3/P0.7/L30/P0.7N3L30_4.negated'
  'AIJ-SAT-explorer-res/AIJ-SAT-explorer/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/rozier/formulas/n4/P0.3/L40/P0.333333333333333N4L40_10'
  'AIJ-SAT-explorer-res/AIJ-SAT-explorer/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/rozier/formulas/n4/P0.3/L70/P0.333333333333333N4L70_5'
  'AIJ-SAT-explorer-res/AIJ-SAT-explorer/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/rozier/formulas/n4/P0.7/L100/P0.7N4L100_5'
  'AIJ-SAT-explorer-res/AIJ-SAT-explorer/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/rozier/formulas/n4/P0.95/L30/P0.95N4L30_5'
  'AIJ-SAT-explorer-res/AIJ-SAT-explorer/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/rozier/formulas/n5/P0.3/L10/P0.333333333333333N5L10_1'
  'AIJ-SAT-explorer-res/AIJ-SAT-explorer/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/rozier/formulas/n5/P0.3/L100/P0.333333333333333N5L100_7.negated'
  'AIJ-SAT-explorer-res/AIJ-SAT-explorer/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/rozier/formulas/n5/P0.3/L50/P0.333333333333333N5L50_9'
  'AIJ-SAT-explorer-res/AIJ-SAT-explorer/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/rozier/formulas/n5/P0.5/L70/P0.5N5L70_7.negated'
  'AIJ-SAT-explorer-res/AIJ-SAT-explorer/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/rozier/formulas/n5/P0.5/L80/P0.5N5L80_9.negated'
  'AIJ-SAT-explorer-res/AIJ-SAT-explorer/AIJ-artifact/LTL-as-LTLf/benchmarks/benchmarks/rozier/formulas/n5/P0.7/L20/P0.7N5L20_4'
  'AIJ-SAT-explorer-res/AIJ-SAT-explorer/AIJ-artifact/LTLf-specific/benchmarks/benchmarks_ltlf/LTLfRandomConjunction/V20/10/N12'
  'AIJ-SAT-explorer-res/AIJ-SAT-explorer/AIJ-artifact/LTLf-specific/benchmarks/benchmarks_ltlf/LTLfRandomConjunction/V20/10/N49'
  'AIJ-SAT-explorer-res/AIJ-SAT-explorer/AIJ-artifact/LTLf-specific/benchmarks/benchmarks_ltlf/LTLfRandomConjunction/V20/20/N10'
  'AIJ-SAT-explorer-res/AIJ-SAT-explorer/AIJ-artifact/LTLf-specific/benchmarks/benchmarks_ltlf/LTLfRandomConjunction/V20/20/N14'
  'AIJ-SAT-explorer-res/AIJ-SAT-explorer/AIJ-artifact/LTLf-specific/benchmarks/benchmarks_ltlf/LTLfRandomConjunction/V20/20/N22'
  'AIJ-SAT-explorer-res/AIJ-SAT-explorer/AIJ-artifact/LTLf-specific/benchmarks/benchmarks_ltlf/LTLfRandomConjunction/V20/20/N30'
  'AIJ-SAT-explorer-res/AIJ-SAT-explorer/AIJ-artifact/LTLf-specific/benchmarks/benchmarks_ltlf/LTLfRandomConjunction/V20/30/N43'
  'AIJ-SAT-explorer-res/AIJ-SAT-explorer/AIJ-artifact/LTLf-specific/benchmarks/benchmarks_ltlf/LTLfRandomConjunction/V20/30/N46'
)

# Done before executing this script:
# cp "$HOME/Code/LTLfUC/ltlfuc/etc/AIJ-SAT-explorer/AIJ-SAT-explorer-res/AIJ-SAT-explorer/aaltafuc-done.txt" "$HOME/Code/LTLfUC/ltlfuc/etc/AIJ-SAT-explorer/AIJ-SAT-explorer-res/AIJ-SAT-explorer/aaltafuc-done_original.txt"
# cp "$HOME/Code/LTLfUC/ltlfuc/etc/AIJ-SAT-explorer/AIJ-SAT-explorer-res/AIJ-SAT-explorer/aaltafuc-error.txt" "$HOME/Code/LTLfUC/ltlfuc/etc/AIJ-SAT-explorer/AIJ-SAT-explorer-res/AIJ-SAT-explorer/aaltafuc-error_original.txt"
# cp "$HOME/Code/LTLfUC/ltlfuc/etc/AIJ-SAT-explorer/AIJ-SAT-explorer-res/AIJ-SAT-explorer/trppp-done.txt" "$HOME/Code/LTLfUC/ltlfuc/etc/AIJ-SAT-explorer/AIJ-SAT-explorer-res/AIJ-SAT-explorer/trppp-done_original.txt"
# cp "$HOME/Code/LTLfUC/ltlfuc/etc/AIJ-SAT-explorer/AIJ-SAT-explorer-res/AIJ-SAT-explorer/trppp-error.txt" "$HOME/Code/LTLfUC/ltlfuc/etc/AIJ-SAT-explorer/AIJ-SAT-explorer-res/AIJ-SAT-explorer/trppp-error_original.txt"

for f in ${DIVERGENT_FILE_STEMS[@]}
do
  destination_dir="${EXCLUDED_TESTS_DIR}/`dirname "${f}"`"
  mkdir -p "${destination_dir}"
  if [ -f "${f}.trpuc_out" ]; then
    echo "Moving ${f}.trpuc_out to ${destination_dir}"
    mv "${f}.trpuc_out" "${destination_dir}"
  fi
  if [ -f "${f}.trpuc" ]; then
    echo "Moving ${f}.trpuc to ${destination_dir}"
    mv "${f}.trpuc" "${destination_dir}"
  fi
  if [ -f "${f}.aaltafuc_out" ]; then
    echo "Moving ${f}.aaltafuc_out to ${destination_dir}"
    mv "${f}.aaltafuc_out" "${destination_dir}"
  fi
  if [ -f "${f}.aaltafuc" ]; then
    echo "Moving ${f}.aaltafuc to ${destination_dir}"
    mv "${f}.aaltafuc" "${destination_dir}"
  fi

  line_removal_pattern="${f#$LOCAL_PREFIX}"
  line_removal_pattern="${line_removal_pattern//\//.}"
  # echo sed -e "'/"${line_removal_pattern}"/d'" "AIJ-SAT-explorer-res/AIJ-SAT-explorer/aaltafuc-done.txt"
  sed -e "/${line_removal_pattern}/d" -i "AIJ-SAT-explorer-res/AIJ-SAT-explorer/aaltafuc-done.txt"
  sed -e "/${line_removal_pattern}/d" -i "AIJ-SAT-explorer-res/AIJ-SAT-explorer/aaltafuc-error.txt"
  sed -e "/${line_removal_pattern}/d" -i "AIJ-SAT-explorer-res/AIJ-SAT-explorer/trppp-done.txt"
  sed -e "/${line_removal_pattern}/d" -i "AIJ-SAT-explorer-res/AIJ-SAT-explorer/trppp-error.txt"
done
