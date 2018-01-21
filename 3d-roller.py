#Attempt to generate a countour map that will let point objects roll down it

import pygame
from pygame.locals import *
from noise import pnoise2
from time import time
import shelve
import Roller

#pygame.init()

screen_dimensions = (400,400)
screen = pygame.display.set_mode(screen_dimensions)

clock = pygame.time.Clock() #Initialize the clock

pygame.display.set_caption("Point rolling simulator") 

def limit_255(x):
	if abs(x) > 255:
		return 255
	return x

def colour_from_value(height):
	rgb = [0, 0, 0]
	colour = round(height*2000)
	for i in range(colour):
		if rgb[0] < 255:
			rgb[0] += 1
		elif rgb[1] < 255:
			rgb[1] += 1
		elif rgb[2] < 255:
			rgb[2] += 1
		else:
			rgb = [255, 255 ,255]

	colour = (rgb[0], rgb[1], rgb[2])
	return colour

def invert_colour(colour):
	return (255-colour[0], 255-colour[1], 255-colour[2])

def main():
	done = False
	rollers = []
	OCTAVES = 8
	
	#Generates heightmap
	print("Generating heightmap...")
	heightmap_gen_start_time = time()
	heightmap = []
	moisturemap = []
	MAP_SIZE = 0.5

	for i in range(screen_dimensions[0]):
		heightmap.append([])

	for i in heightmap:
		for j in range(screen_dimensions[1]):
			i.append([])

	
	for i in range(len(heightmap)):
		for j in range(len(heightmap[i])):
			heightmap[i][j] = pnoise2((i*MAP_SIZE)/screen_dimensions[0], (j*MAP_SIZE)/screen_dimensions[1], OCTAVES)*2

	heightmap_time_taken = time() - heightmap_gen_start_time
	print("Heightmap done. Took "+str(heightmap_time_taken)+" seconds.")
	del(heightmap_gen_start_time)
	del(heightmap_time_taken)

	#Renders heightmap and saves it into an image
	print("Rendering heightmap...")
	heightmap_render_start_time = time()

	for i in range(len(heightmap)):
		for j in range(len(heightmap[i])):
			height = heightmap[i][j]
			#colour *= 1000
			#colour = limit_255(colour)
			#colour = abs(colour)
			colour = colour_from_value(height)
			pygame.draw.line(screen, colour, (i, j), (i, j))

	loaded_map = shelve.open("maps/default_map")
	loaded_map["map"] = heightmap
	pygame.image.save(screen, "maps/default_map.png")
	loaded_map.close()

	heightmap_render_time_taken = time()-heightmap_render_start_time
	print("Rendering done. Took "+str(heightmap_render_time_taken)+" seconds.")
	del(heightmap_render_time_taken)
	del(heightmap_render_start_time)

	loaded_perlin = pygame.image.load("maps/default_map.png")

	while not done:
		events = pygame.event.get()

		for event in events:
			#Event handling
			if event.type == pygame.QUIT:
				done = True
			if event.type == pygame.KEYDOWN:
				if event.key == K_x:
					pass
			if event.type == pygame.KEYUP:
				if event.key == K_x:
					pass
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					#print("Left click at "+str(pygame.mouse.get_pos()))
					rollers.append(Roller.Roller(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))

		#Game logic below
		for roller in rollers:
			
			lowest_adjacent_height = heightmap[roller.get_x()][roller.get_y()]
			correct_offsets = (0, 0)
			for x_offset in range(-1, 2):
				for y_offset in range(-1, 2):
					if heightmap[roller.get_x(x_offset)][roller.get_y(y_offset)] < lowest_adjacent_height:
						lowest_adjacent_height = heightmap[roller.get_x(x_offset)][roller.get_y(y_offset)]
						correct_offsets = (x_offset, y_offset)

			roller.offset_pos(correct_offsets)

		#Drawing below
		screen.fill((255, 0, 255))
		screen.blit(loaded_perlin, (0, 0))

		for roller in rollers:
			pygame.draw.line(screen, invert_colour(screen.get_at(roller.get_pos())), (roller.get_x(), roller.get_y()), (roller.get_x(), roller.get_y()))

		pygame.display.flip() #Updates display
		clock.tick(60)

	pygame.quit() #Quits if all loops are exited

main()
