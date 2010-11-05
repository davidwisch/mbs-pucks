# A Multibody Puck Simulation

## About

This is a simulation of the multibody system from the Phy270 Lab class.  The simulation is of pucks on an airhockey table.  After the simulation is complete, the pucks positions overtime analyzed and placed in bins to determine various global propeties about the distribution.  Various aspects of the simulation are mutable including the evevation of the table, the dimentions of the table, as well as various puck properties.

## Dependencies

In order to run, the simulation needs a few packages to be installed.

**Python 2.6** is what the simulation was developed using.  Currently the simulation is **not** compatible with Python3 but should be backwards compatable at least a few version (I havent tested it though).

**Matplotlib** is used for generating [most] images and is therefore required.

**Gnuplot** is not required to run the simulation but is required to produce the heatmaps of puck distributions.

## Usage

### Settings File

In **src/settings.py** you'll find a number of configurable options.  Change these at will.  Some of the values don't make a lot of physical sense.  For instance, the **FRICTION** variable doesn't correspond to any accepted calculation of friction but still functions none the less.  This is discussed further later on.

### Running the simulation

You should run the simulation from the **src** directory.  There are a number of command line options that you can use to alter how the simulation is run and what output it produces.

You can get a full list of CLI params by running,

`python simulation.py --help`

Three of the possible CLI flags (--images, --files, --gigafile) are especially important.  You'll need to specify at least one of these.

* **-i, --images** will dump each timestep (or, every x timesteps (configurable in settings.py)) to an image file.  While this produces something interesting to look at, it's exceptionally slow compared to the other two options.
* **-f, --files** will dump every timestap (or every x timesteps) to their own data file
* **-g, --gigafile** will dump all timesteps (or every x timesteps) to a single file.  In order to generate the heatmap, you will need to specify this gigafile option.

### Statistics

The simulation performs some automatic statistics functions for you that roughly correspong to requirements from the original lab.  All statistics require that you specify the gigafile flag when running the simulation.

If the flag is specified, two graphs are produced (along with some other random files).  The first graph is essentially a histogram of the number of pucks in each bin (although it's not displayed as a histogram, it's displayed as a scatter plot).  The second file is a heatmap showing the concentration of pucks across all timesteps.
