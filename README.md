# gol_rule_switching

Implementation of the Game of Life with rule switching.

## About

This repo contains model and scripts used to run numerical experiments for Game
of Life with rule switching mechanisms. 

## Reproducing data

Scripts in this repo can be used to reproduce data ilustrattgin the behaviur of
the Game of Live cellular automata extended with the mechanisms for rule
switching. Additionally, the model can be used in asynchronouse and synhronouse
mode.

Compilation and code runing is controlled by file `Makefile` in the main
directory. This file should be modified to suit our NetLogo installation.
In the provided `Makefile` it is assume the NetLogo is installed in

    ~/Local/NetLogo/3.0.0

directory. It is also assumed that `java` and `javac` are in you PATH.

`Makefile` also uses GNU pararell for running Java programmes. 

### Fianl configurations

Sample configurations are produced using `GenerateExample.java` script. To compile this
file run

    make

in the main directory. This will also compile `CalculateMeanLiving.java`.

Examples are generated by issuing

    make genex

in the main directory. This will produce files `world*.csv` files, named according to the parameters defined in `CalculateMeanLiving.java` file.
 
Ploting of the resulting data is handled by `plot_world_example.py` script. Running

    plot_world_example.py word_data.csv

will produce PDF file for visualizing data from the CSV file `world_data.csv`. 

To plot all data from the generated examples run 

    for f in world*.csv ; do python plot_world_example.py $f ; done

**Note:** By default, world size is set to 2^6. Details are defined in `experiements.xml` file.

**Note:** Plots are saved in `plots` subdirectory.

### Realizations

Exlemplary realizations can be obtained by using `run.sh` script and
`experiments.xml` file. For each experiment defined in `experiments.xml` file,
make a symblic link to `run.sh`

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

### Average growth

Date for the average number of living cells are calculate by `CalculateMeanLiving.java` and can be obtained by running
    
    make calcmean

You need to compile `CalculateMeanLiving.java` first

**Note:** BY default, 500 realizations are used fo averaging. This value can be
modified in `CalculateMeanLiving.java` file. 

Ploting of the data is handled by `plot_living_average.py`.

**Note:** Data from this experiment are saved in `living_data_250steps_200runs.csv` file. This should be configures in `Makefile` and in the plotting script `plot_living_average.py`.
