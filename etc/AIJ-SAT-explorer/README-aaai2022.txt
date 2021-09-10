This archive contains all the material to reproduce the experiments in
the associated paper. This material is provided as is, with the only
purpose to allow the reviewers to assess the code and to reproduce the
experiments.

In order to run the experiments:

enter the directory containing the modified version of NuSMV
(i.e. ltlfuc) and compile NuSMV with the respective instructions:

NuSMV:
  cd ltlfuc/NuSMV
  mkdir build
  cd build
  cmake ..
  make

aaltafuc:
  cd aaltaf-uc
  make
  cd ltlparser/ltlf2Andltlf
  make

trp++
  cd trp++
  make release

In order to compile these tools a standard environment for developing
C/C++ software is required: something along the lines of "make",
"g++", "bison", and "flex". TRP++ also requires the Boost C++
libraries and the "gengetopt". Moreover, python is also required.

The compilation has been succesfully performed within a Linux Ubuntu
20.04 LTS with standard development packages.

Once the tools have been compiled, to run the experiments it is needed
to edit the file config.py in the folder AIJ-SAT-explorer to change
the variables

* AALTAFHOME to point to the directory where aalta-uc source code has been put:
   AALTAFHOME="../aaltaf-uc.src/"
* LTLFUCHOME to point to the root directory where the modified version of NuSMV has been put:
   LTLFUCHOME="../ltlfuc.src/"
* trpppBIN to point to the trp++uc executable
   trpppBIN="../trp++/bin/trp++uc"

Then, the python script convert.py converts the aaltaf benchmarks
specified in the file AIJ-SoTA-aggregate-verification-results-UNSAT.txt
to the format accepted by the different tools. The files are already
generated, thus in principle it is not needed to execute this.

Then to run the different tools the following commands are provided:

     run-aaltaf.py
     run-trp.py
     run-ltlfuc_sat.py
     run-ltlfuc_bdd

These files upon termination write two files: toolname-done.txt and
toolname-error.txt containing respectively the names of the file
succeded/failed (e.g. due to timeout), example: ltlfucsat-done.txt and
ltlfucsat-error.txt. The output of each tool is stored in the file of
the benchmark followed by the suffix _tool_out in the same directory
of the source file.

To extract the results and generate the plots edit the file
"plot-AIJ-results-analysis-and-save-in-paper-dir.sh" to modify the
paths for the different python scripts/packages used and then run the
bash command

     plot-AIJ-results-analysis-and-save-in-paper-dir.sh

This will generate the plots and some statistics in th folder
AIJ-analysis-plots

It might be some paths needs to be adjusted to have the entire flow to run.
