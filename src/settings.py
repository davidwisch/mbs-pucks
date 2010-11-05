"""
Config file for the multibody puck simulation.

Author: David Wischhusen
"""
import os

TIMESTEP = 0.05
TIMESTEPS = 500

NUMBER_OF_PUCKS = 20
PUCK_RADIUS = 3.35 #cm
PUCK_MASS = 4.8 #grams, this is not really used anywhere

TABLE_WIDTH = 98.7 #cm
TABLE_HEIGHT = 60.0 #cm
TABLE_SLANT = 5.0 #degrees
PADDLE_STRENGTH = 80.0 #scalar
BIN_SPACING = 6.7 #cm

PHYSICS_INCLUDE_GRAVITY = True
GRAVITY = 9.8 #m/s
PHYSICS_INCLUDE_FRICTION = True
FRICTION = 0.01 #[0,1]

OUTPUT_IMAGE_STEPS = 1
#relative to simulation.py script
OUTPUT_DIRECTORY = os.path.join('..', 'output')

GNUPLOT_COMMAND = "gnuplot"
