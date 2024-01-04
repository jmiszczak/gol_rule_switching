[![DOI](https://zenodo.org/badge/535613700.svg)](https://zenodo.org/badge/latestdoi/535613700)

# gol_rule_switching

Implementation of the Game of Life with rule switching.

## About

This repo contains model and scripts used to run numerical experiments for Game
of Life with rule switching mechanisms. The code was used in


J.A. Miszczak, *Rule switching mechanisms in the Game of Life with synchronous and asynchronous updating policy*, Physica Scripta, 98, 115210 (2023). DOI:[10.1088/1402-4896/acfc6c](https://doi.org/10.1088/1402-4896/acfc6c) arXiv:[2310.05979](https://arxiv.org/abs/2310.05979)

```
@article{miszczak2023rule,
	author = {Miszczak, J.A.},
	title = {Rule switching mechanisms in the Game of Life with synchronous and asynchronous updating policy},
	doi = {10.1088/1402-4896/acfc6c},
	journal = {Physica Scripta}, 
	volume = {98},
	number = {11},
	pages = {115210},
	year = {2023},
}

```

# Reproducing data

Scripts in this repo can be used to reproduce data illustrating the behaviour of
the Game of Live (GoL) cellular automata extended with the mechanisms for rule
switching. Additionally, the model can be used in asynchronous and synchronous
mode.

Code compilation and running is controlled by file `Makefile` in the main
directory. This file should be modified to suit our NetLogo installation. In the
provided `Makefile` it is assumed that NetLogo is installed in

    ~/Local/NetLogo/6.3.0

directory. It is also assumed that `java` and `javac` are in you `PATH`
environment variable.

`Makefile` also uses GNU parallel for running Java programmes. 

## Final configurations

Sample configurations are produced using `GenerateExample.java` script. To
compile this file run

    make

in the main directory. This will also compile `CalculateMeanLiving.java` and
`GenerateConfigurations.java`.

Examples are generated by issuing

    make genex

in the main directory. This will produce files `world*.csv` files, named according to the parameters defined in `CalculateMeanLiving.java` file.
 
Plotting of the resulting data is handled by `plot_world_example.py` script. Running

    python plot_world_example.py word_data.csv

will produce PDF file for visualizing data from the CSV file `world_data.csv`. 

To plot all data from the generated examples run 

    for f in world*.csv ; do python plot_world_example.py $f ; done

**Note:** By default, the world size is set to 2^6. Details are defined in
*`experiements.xml` file.

**Note:** Plots are saved in `plots` subdirectory.

## Realizations

Exemplary realizations can be obtained by using `run.sh` script and
`experiments.xml` file. For each experiment defined in `experiments.xml` file,
make a symbolic link to `run.sh`

    ln -s run.sh experiment-name.sh

Next, run

    bash experiment-name.sh

The resulting data will be saved in `experiment-name.csv` In the included
`experiments.xml` file there are defined two experiments:
`deterministic_realizations` and `random_realizations`

**Note:** The above commands can by run using
    
    make realizations

To plot data from the realizations run

    python plot_realizations.py

**Note:** Configure name of the data files in the plotting script.  

## Average growth

Data for the average number of living cells are calculated by
`CalculateMeanLiving.java` and can be obtained by running

    make calcmean

You need to compile `CalculateMeanLiving.java` first

**Note:** BY default, 200 realizations are used fo averaging. This value can be
modified in `CalculateMeanLiving.java` file by altering `steps` variable. 

Plotting of the data is handled by `plot_living_average.py`, which accepts one
argument with name of the data file.

**Note:** Data from this experiment are saved in
*`living_data_250steps_200runs.csv` file. This file is included in the
*repository. The name of the file used to save data should be configured in
*`Makefile` and in the plotting script `plot_living_average.py`.

## Mutual entropy

For the purpose of analysing the mutual entropy of the generated patters, it is
necessary to generate a number of final configurations. This data is generated
using `genfc` target in the Makefile,

    make gencf

You need to compile `GenerateConfigurations.java` before running this command.

Resulting `csv` files in `configurations` subdirectory. For each combination of
parameters 1000 files representing final configurations are generated. The names
of the resulting configurations can be saved in a shell variable using

    golTypes=$(for i in *_0001.csv ; do echo `echo $i | sed s/_0001.csv//g` ; done)

in the `configurations` directory. 

The calculation of the average mutual entropy is implemented in
`analyze_mutent.py` script. Using GNU parallel, the analysis results can be
obtained by running

    parallel ./analyze.py {} ::: $golTypes

in `configurations` subdirectory.

This will result in one `*.dat` file for each combination of parameters. To
obtain the file with all data run 

    bash postprocess_dat.sh 

script. This will produce `anayze_mutent.csv`, used by the plotting script
`plot_mutual_entropy.py` located in the main directory. 
