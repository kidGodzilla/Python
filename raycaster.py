# original foamdino@gmail.com
from __future__ import division

import sys
from graphics import *
from math import *

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
l=[]

def cast():
    w=GraphWin('Raycaster', 512, 384)
    width, height = 512, 384    
    level = load_level()
    pos_x = 22
    pos_y = 12
    dir_x = -1
    dir_y = 0
    plane_x = 0
    plane_y = 0.66

    time = 0
    old_time = 0

    # main loop
    done = False
    gx=0
    for i in range(len(l)):
        l[i].undraw()
    while not done:
        for x in range(width):
            camera_x = 2 * x / float(width) - 1
            ray_pos_x = pos_x
            ray_pos_y = pos_y
            ray_dir_x = dir_x + plane_x * camera_x
            ray_dir_y = dir_y + plane_y * camera_x

            # which square of the map are we in?
            map_x = int(ray_pos_x)
            map_y = int(ray_pos_y)
            # length of a ray from current position to next x or next y-side
            side_dist_x = 0
            side_dist_y = 0

            # length of ray from one x or y side to next x or y side
            delta_dist_x = sqrt(1 + (ray_dir_y * ray_dir_y) / (ray_dir_x * ray_dir_x))

            # in C++ you can divide by zero with floats/doubles - I figure you can't do that in python. Sadface.
            if ray_dir_y == 0.0:
                delta_dist_y = sqrt(1+ sys.float_info.max)
            else:
                delta_dist_y = sqrt(1 + (ray_dir_x * ray_dir_x) / (ray_dir_y * ray_dir_y))

            hit = False #hit a wall?
            side = 0 #NS or EW wall?

            # calculate step and initial side_dist
            if ray_dir_x < 0:
                step_x = -1
                side_dist_x = (ray_pos_x - map_x) * delta_dist_x
            else:
                step_x = 1
                side_dist_x = (map_x + 1.0 - ray_pos_x) * delta_dist_x

            if ray_dir_y < 0:
                step_y = -1
                side_dist_y = (ray_pos_y - map_y) * delta_dist_y
            else:
                step_y = 1
                side_dist_y = (map_y +1.0 - ray_pos_y) * delta_dist_y

            # perform DDA calcs
            while not hit:
                #jump to next map square in either x or y direction
                if side_dist_x < side_dist_y:
                    side_dist_x += delta_dist_x
                    map_x += step_x
                    side = 0
                else:
                    side_dist_y += delta_dist_y
                    map_y += step_y
                    side = 1

                # check for hitting a wall
                if level[map_x][map_y] > 0:
                    hit = True

            # calc the distance projected on camera direction
            if side == 0:
                perp_wall_dist = fabs((map_x - ray_pos_x + (1 - step_x) / 2) / ray_dir_x)
            else:
                try:
                    perp_wall_dist = fabs((map_y - ray_pos_y + (1 - step_y) / 2) / ray_dir_y)
                except ZeroDivisionError:
                    perp_wall_dist = sys.float_info.max

            # calc height of line to draw on screen
            try:
                line_height = abs(int(height / perp_wall_dist))
            except ZeroDivisionError:
                line_height = height

            # calc lowest and highest pixel to fill in current stripe
            draw_start = (-line_height / 2) + (height / 2)
            if draw_start < 0:
                draw_start = 0

            draw_end = (line_height / 2) + (height / 2)
            if draw_end >= height:
                draw_end = height -1

            # choose color depending on number in map pos
            if level[map_x][map_y] == 1:
                colour = RED
            elif level[map_x][map_y] == 2:
                colour = GREEN
            elif level[map_x][map_y] == 3:
                colour = BLUE
            elif level[map_x][map_y] == 4:
                colour = WHITE
            elif level[map_x][map_y] == 5:
                colour = YELLOW
            else:
                colour = None

            # give a different colour for x/y sides
            if side == 1 and colour:
                colour = (colour[0]/2, colour[1]/2, colour[2]/2)

            # draw the pixels for this vertical strip (the actual meat comes down to just this!)
            if colour:
                l.append([])
                l[gx]=Line(Point(x,draw_start), Point(x,draw_end))
                l[gx].setFill(color_rgb(colour[0], colour[1], colour[2]))
                l[gx].draw(w)
                gx+=1

        #old_time = time
        #time = pygame.time.get_ticks()
        #frame_time = (time - old_time) / 1000.0
        #if frame_time == 0.0:
        #    frame_time = 1.0
        
        # display some text
        #text = font.render("fps: %s" % int(1.0 / frame_time), 1, (200,200,200))
        #textpos = text.get_rect()
        #textpos.centerx = screen.get_rect().centerx
        #background.blit(text, textpos)

        # move this into a function...
        #move_speed = frame_time * 5.0 # squares/sec
        move_speed = 1
        #rot_speed = frame_time * 3.0 # radians/sec
            
        # read kb state
        #pygame.event.pump()
        keys = w.checkKey()
        if keys:
            # move forward if there's no wall in front of you
            if keys=='Up':
                if level[int(pos_x + dir_x * move_speed)][int(pos_y)] == 0:
                    pos_x += dir_x * move_speed
                if level[int(pos_x)][int(pos_y + dir_y * move_speed)] == 0:
                    pos_y += dir_y * move_speed

            # move backwards if there's no wall behind you
            if keys=='Down':
                if level[int(pos_x - dir_x * move_speed)][int(pos_y)] == 0:
                    pos_x -= dir_x * move_speed
                if level[int(pos_x)][int(pos_y - dir_y * move_speed)] == 0:
                    pos_y -= dir_y * move_speed

            # strafe right if there's no wall to the right of you
            if keys=='left':
                if level[int(pos_x - plane_x * move_speed)][int(pos_y)] == 0:
                    pos_x -= plane_x * move_speed
                if level[int(pos_x)][int(pos_y - plane_y * move_speed)] == 0:
                    pos_y -= plane_y * move_speed

            # strafe left if there's no wall to the left of you
            if keys=='Right':
                if level[int(pos_x + plane_x * move_speed)][int(pos_y)] == 0:
                    pos_x += plane_x * move_speed
                if level[int(pos_x)][int(pos_y + plane_y * move_speed)] == 0:
                    pos_y += plane_y * move_speed
                    
                    
            # rotate right
            '''if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                # rotate camera plane and dir
                old_dir_x = dir_x
                dir_x = dir_x * cos(-rot_speed) - dir_y * sin(-rot_speed)
                dir_y = old_dir_x * sin(-rot_speed) + dir_y * cos(-rot_speed)
                old_plane_x = plane_x
                plane_x = plane_x * cos(-rot_speed) - plane_y * sin(-rot_speed)
                plane_y = old_plane_x * sin(-rot_speed) + plane_y * cos(-rot_speed)

            # rotate left
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                # rotate camera plane and dir
                old_dir_x = dir_x
                dir_x = dir_x * cos(rot_speed) - dir_y * sin(rot_speed)
                dir_y = old_dir_x * sin(rot_speed) + dir_y * cos(rot_speed)
                old_plane_x = plane_x
                plane_x = plane_x * cos(rot_speed) - plane_y * sin(rot_speed)
                plane_y = old_plane_x * sin(rot_speed) + plane_y * cos(rot_speed)

            # quit
            if keys[pygame.K_ESCAPE]:
                print "quit.."
                done = True

        screen.blit(background, (0,0))
        pygame.display.flip()
        background.fill(BLACK)
        '''    

def load_level():
    with open("level.txt") as fyle:
        level_array = [[int(x) for x in line.split()] for line in fyle]

    return level_array

if __name__ == "__main__":
    print("Starting up...")
    print("Press escape to quit.")
    cast()
