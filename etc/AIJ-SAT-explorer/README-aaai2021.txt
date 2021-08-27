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
  cd aaltafuc
  make

trp++
  cd trp++uc-v2.1-20150628
  make release

In order to compile these tools a standard environment for developing
C/C++ software is required: something along the lines of "make",
"g++", "bison", and "flex". TRP++ also requires the Boost C++
libraries and the "gengetopt". Moreover, python is also required.

The compilation has been succesfully performed within a Linux Ubuntu
20.04 LTS with standard development packages.

Once the tools have been compiled, to run the experiments it is needed
to edit the file config.py to change the variables

* AALTAFHOME to point to the directory where aalta-uc source code has been put:
   AALTAFHOME="../../../aaltaf-uc.src/"
* LTLFUCHOME to point to the root directory where the modified version of NuSMV has been put:
   LTLFUCHOME="../../../ltlfuc.src/"
* trpppBIN to point to the trp++uc executable
   trpppBIN="../../../trp++/bin/trp++uc"

Then, the script convert.py converts the aaltaf benchmarks specified
in the file AIJ-SoTA-aggregate-verification-results-UNSAT.txt to the
format accepted by the different tools. The files are already
generated, thus in principle it is not needed to execute this.

Then to run the different tools the following commands are provided:

     run-aaltaf.py
     run-trp.py
     run-ltlfuc_sat.py
     run-ltlfuc_bdd

To extract the results and the plots:

   run-results-analysis.py
