"""
Engine that controls the evolution of pucks and calls functions responsible
for calling functions responsible for detecting collisions, etc.

Author: David Wischhusen
"""

import math
import copy
import random

import settings
import physics

from helpers.velocity import Velocity
from helpers.position import Position
from helpers import general


"""
Uses the slant of the table to calculate how the velocity will
be changed due to gravity
"""
def gravity_effect_velocity(velocity, dt):
	if not settings.PHYSICS_INCLUDE_GRAVITY:
		return velocity

	#settings.TABLE_SLANT is in degrees
	slant = math.radians(float(settings.TABLE_SLANT))

	vy = velocity.get_y() - (settings.GRAVITY*math.sin(slant)*dt)
	velocity.set_y(vy)

	return velocity

"""
Reduces the velocity of the puck according to the setting set in settings.py
"""
def friction_effect_velocity(velocity):
	if not settings.PHYSICS_INCLUDE_FRICTION:
		return velocity

	nvx = velocity.get_x() * ( 1 - settings.FRICTION )
	if not general.match_sign(nvx, velocity.get_x()):
		nvx = 0.0
	nvy = velocity.get_y() * ( 1 - settings.FRICTION )
	if not general.match_sign(nvy, velocity.get_y()):
		nvy = 0.0

	return Velocity(nvx, nvy)


"""
Moves the pucks [linearly] forward a single timestep and calls functions
to detect collisions with walls and other pucks
"""
def evolve_puck(puck, dt):
	#we want a copy to operate on (**python this by reference**)
	n_puck = copy.deepcopy(puck)

	#evolve the position based on current velocity
	pos_x = n_puck.get_x() + (n_puck.get_vx() * dt)
	pos_y = n_puck.get_y() + (n_puck.get_vy() * dt)
	n_puck.set_position(Position(pos_x, pos_y))

	#update the velocity (may be affected due to table slant)
	new_vel = physics.gravity_effect_velocity(n_puck.get_velocity(), dt)
	new_vel = physics.friction_effect_velocity(n_puck.get_velocity())
	n_puck.set_velocity(new_vel)

	return n_puck


"""
Detects if there is a collision between pucks, calculates the resultant velocities and
updates them
"""
def puck_collision(puck, pucks, dt, collision_log):
	for i in range(len(pucks)):
		if puck.get_name() == pucks[i].get_name():
			continue

		dist = physics.find_distance(pucks[i].get_position(), puck.get_position())
		if dist < (puck.get_radius() + pucks[i].get_radius()):
			if collision_log.has_collided(puck, pucks[i]):
				continue

			collision_log.log_collision(puck, pucks[i])

			x1 = puck.get_x()
			y1 = puck.get_y()
			x2 = pucks[i].get_x()
			y2 = pucks[i].get_y()
			v1x = puck.get_vx()
			v1y = puck.get_vy()
			v2x = pucks[i].get_vx()
			v2y = pucks[i].get_vy()
			r1 = puck.get_radius()
			r2 = pucks[i].get_radius()

			#relate velocity angles
			if v1x - v2x == 0: # yeah, I know this is cheap
				v1x += 0.00005
				v2x -= 0.00005
			Y_v = math.atan((v1y - v2y) / (v1x - v2x))
			#relate position angled
			if x2 - x1 == 0: #still cheap...
				x2 += 0.00005
				x1 -= 0.00005
			Y_xy = math.atan((y2 - y1) / (x2 - x1))
			#should we force d=2r at this point? - yes
			d = r1 + r2
			#impact angle
			alpha = math.asin((d * math.sin(Y_xy - Y_v)) / (r1 + r2))
			a = math.tan(Y_v + alpha)

			#all the pucks weigh the same, changing this would be easy but right
			#now this property is not stored in the pucks
			#mass_ratio = m2 / m1
			mass_ratio = 1.0

			dvx2 = 2 * (v1x - v2x + (a * (v1y - v2y)) ) / ((1 + a**2) * (1+mass_ratio))

			#post collision velocities
			v2x2 = v2x + dvx2
			v2y2 = v2y + (a * dvx2)
			v1x2 = v1x - (mass_ratio * dvx2)
			v1y2 = v1y - (a * mass_ratio * dvx2)

			puck.set_velocity(Velocity(v1x2, v1y2))
			pucks[i].set_velocity(Velocity(v2x2, v2y2))

			#Some of the pucks are sticking together, lets do something about it...
			#Could partially evolve them forward with their new velocities (done below)
			#Remember to keep the timestep low, will reduce the problem

			#start be evolving forward 1/2 timestep - could be done better, may not need to happen each time
			x12 = x1 + (puck.get_vx() * dt * 0.5)
			y12 = y1 + (puck.get_vy() * dt * 0.5)
			x22 = x2 + (pucks[i].get_vx() * dt * 0.5)
			y22 = y2 + (pucks[i].get_vy() * dt * 0.5)

			puck.set_position(Position(x12, y12))
			pucks[i].set_position(Position(x22, y22))


	return puck

"""
Detects if a puck collides with a wall, calculates the change in velocity,
evolves the puck through the end of timestep if time remains after the
collision with the wall.
"""
def wall_collision(pos0, puck, dt):
	rad = puck.get_radius()

	posf = puck.get_position()

	#There's a lot of subtracting of the radius and other similar operations here.
	#This is because the interpolation of the impact point must be skewed because
	#the pucks arn't just a single point, they have a discrete width.

	#if we hit the top, reverse y-velocity
	if puck.get_y() + rad >= settings.TABLE_HEIGHT:
		#get the x coordinate of impact
		x_impact = physics.linear_interpolate_x(pos0, posf, settings.TABLE_HEIGHT - rad)
		impact_pos = Position(x_impact, settings.TABLE_HEIGHT - rad)
		time_to_impact = (impact_pos.get_y() - pos0.get_y()) / puck.get_vy()
		#how much time remains in the timestep
		time_remaining = dt - time_to_impact
		puck.set_vy(-1 * puck.get_vy())
		#set pucks new position including evolution from left over timestep
		puck.set_x(x_impact + (puck.get_vx() * time_remaining))
		puck.set_y((settings.TABLE_HEIGHT - rad) + (puck.get_vy() * time_remaining))

	#if we hit the right side, reverse the x-velocity
	elif puck.get_x() + rad >= settings.TABLE_WIDTH:
		#get the y coordinate of impact
		y_impact = physics.linear_interpolate_y(pos0, posf, settings.TABLE_WIDTH - rad)
		impact_pos = Position(settings.TABLE_WIDTH - rad, y_impact)
		time_to_impact = (impact_pos.get_x() - pos0.get_x()) / puck.get_vx()
		#how much time remains in the timestep
		time_remaining = dt - time_to_impact
		puck.set_vx(-1 * puck.get_vx())
		#set pucks new position including evolution from left over timestep
		puck.set_x((settings.TABLE_WIDTH - rad) + (puck.get_vx() * time_remaining))
		puck.set_y(y_impact + (puck.get_vy() * time_remaining))

	#if we hit the bottom, reverse y-velocity * make contact with paddle
	elif puck.get_y() - rad <= 0:
		#get the x coordinate of impact
		x_impact = physics.linear_interpolate_x(pos0, posf, rad)
		impact_pos = Position(x_impact, rad)
		time_to_impact = (impact_pos.get_y() - pos0.get_y()) / puck.get_vy()
		#how much time remains in the timestep
		time_remaining = dt - time_to_impact
		puck.set_vy((-1 * puck.get_vy()) + physics.paddle_impact())
		#set pucks new position including evolution from left over timestep
		puck.set_x(x_impact + (puck.get_vx() * time_remaining))
		puck.set_y(rad + (puck.get_vy() * time_remaining))

	#if we hit the left side, reverse the x-velocity
	elif puck.get_x() - rad <= 0:
		#get the y coordinate of impact
		y_impact = physics.linear_interpolate_y(pos0, posf, rad)
		impact_pos = Position(rad, y_impact)
		time_to_impact = (impact_pos.get_x() - pos0.get_x()) / puck.get_vx()
		#how much time remains in the timestep
		time_remaining = dt - time_to_impact
		puck.set_vx(-1 * puck.get_vx())
		#set pucks new position including evolution from left over timestep
		puck.set_x(rad + (puck.get_vx() * time_remaining))
		puck.set_y(y_impact + (puck.get_vy() * time_remaining))

	return puck

"""
Return the velocity modifier as the result of impact with the paddle
"""
def paddle_impact():
	if random.random() > 0.5:
		return 0.05 * settings.PADDLE_STRENGTH
	return 0.0

"""
Find the distance between two points
"""
def find_distance(point1, point2):
	dist = (point2.get_x()-point1.get_x())**2.0 + (point2.get_y() - point1.get_y())**2.0
	dist = math.sqrt(dist)

	return dist

"""
Find the slope between two points on a 2D plane
"""
def find_slope(pos1, pos2):
	return (pos2.get_y() - pos1.get_y()) / (pos2.get_x() - pos1.get_x())

"""
Simple function to calulate the b-intercept of a line
"""
def find_b_intercept(y, m, x):
	return y - (m * x)

"""
Linearly interpolate the x-position of a point, between two given points
corresponding to a given y-position.  Used to calculate the x coordinate
of an impact with the top or bottom of the table
"""
def linear_interpolate_x(pos1, pos2, y_coordinate):
	m = physics.find_slope(pos1, pos2)
	b = physics.find_b_intercept(pos2.get_y(), m, pos2.get_x())

	return (y_coordinate - b) / m

"""
Linearly interpolate the y-position of a point, between two given points
corresponding to a given x-position.  Used to calculate the y coordinate
of an impact with the left or right sides of the table
"""
def linear_interpolate_y(pos1, pos2, x_coordinate):
	m = physics.find_slope(pos1, pos2)
	b = physics.find_b_intercept(pos2.get_y(), m, pos2.get_x())

	return (m * x_coordinate) + b
