#! /usr/bin/python2

import pygame
import sys
import time
import random
import datetime
import os

from pygame.locals import *
from time import gmtime, localtime

stop = False  # This is discripted at down
tpath = sys.path[0] + '/'  # Program's path

def main():
    pygame.init()  # Initualize Pygame
    size = width, height = 800, 600  # Set window size
    pygame.display.set_caption("The Tank")  # Set window caption
    icon = pygame.image.load(tpath + "/data/icon.png")  # Get window icon
    icon_rect = icon.get_rect()  # Get icon rectangle (geometry)
    icon_surface = pygame.Surface( (icon_rect.width, icon_rect.height) )  # Make a surface for the window icon
    icon_surface.blit(icon, icon_rect)  # blit the icon
    pygame.display.set_icon(icon_surface)  # Set the icon
    screen = pygame.display.set_mode(size)  # Run window
    
    screen.fill((255, 255, 255))  # Fill screen with white
    font0 = pygame.font.SysFont(None, 32)  # Set font for the start text
    start_text = font0.render("Press Return to start game or Q to exit", True, (0, 0, 0) )  # Set start text
    start_text_rect = start_text.get_rect()
    start_text_rect.centerx = screen.get_rect().centerx  # Set the text geometry to center of the window
    start_text_rect.centery = screen.get_rect().centery  #
    screen.blit(start_text, start_text_rect)  # blit the start text
    pygame.display.flip()  # Update display
    b = True  # Set keys
    while b:
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == KEYDOWN:
                if e.key == ord('q'):
                    pygame.quit()
                    sys.exit()
                elif e.key == K_RETURN:
                    b = False
    
    winners_file = tpath + ".ttwinners"
    
    # Tip: 20 is one second
    tank_speed = 20  # Set the tank's speed. Standard: 20
    enemy_speed = (0, 4)  # Set the enemy's speed. Standard: (0, 4)
    enemy_array = list()
    fire_speed = (0, -30)  # Set tank's fire speed. Standard: (0, -8)
    fire_array = list()
    efire_speed = (0, 8)  # Set enemy's fire speed. Standard: (0, 8)
    efire_array = list()
    efire_warray = list()
    #efire_time = 40  # Standard: 40 #### It's random now
    fexplote_array = list()
    fexplote_darray = list()
    fexplote_time = 5  # Set time for the fexplote (the tank explotion fire) time. Standard: 5
    eexplote_array = list()
    eexplote_darray = list()
    eexplote_time = 5  # Set time for the fexplote (the enemy explotion fire) time. Standard: 5
    harder = 200  # How long it will take to be harder. Standard: 200
    harder_s = harder
    speedup = 1 # Set the speed up number for everytime efire/enemy speeds up. Standard: 4
    
    # Get objects' images and set their rectangle value
    tank = pygame.image.load(tpath + "data/tank.png")
    tank_rect = tank.get_rect()
    enemy = pygame.image.load(tpath + "data/enemy.png")
    enemy_rect = enemy.get_rect()
    fire = pygame.image.load(tpath + "data/fire.png")
    fire_rect = fire.get_rect()
    efire = pygame.image.load(tpath + "data/enemy_fire.png")
    efire_rect = efire.get_rect()
    fexplote = pygame.image.load(tpath + "data/fire_explote.png")
    fexplote_rect = fexplote.get_rect()
    eexplote = pygame.image.load(tpath + "data/enemy_explote.png")
    eexplote_rect = eexplote.get_rect()
    
    tank_rect = tank_rect.move(( (width / 2) - (tank_rect[2] / 2), height - (tank_rect[3] * 2) ))  # Set tank to appear in the center of the area
    enemy_rect = enemy_rect.move(0, -enemy_rect[3])  # Set enemy rectangle to appear
    enemy_array.append( enemy_rect.move(random.randint(1, width - 1 - enemy_rect[2]), 0) )
    efire_array.append(random.randint(1, 80))
    
    waiter = 0
    waituntil = random.randint(5, 50)
    fire_times = 0
    lost = 3
    
    move = {'left': 0, 'right': 0, 'down': 0, 'up': 0}
    
    #time_start = time.strftime("%H:%M:%S", time.localtime())
    time_start_sec = time.time()
    time_stopped = 0.0
    
    stop = False
    
    nomod = pygame.key.get_mods()
    
    while True:
        fire_times -= 1
        harder -= 1
        
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == KEYDOWN:
                if e.key == ord('q'):
                    pygame.quit()
                    sys.exit()
                elif e.key == K_ESCAPE:
                    time_stopped_start = time.time()
                    font6 = pygame.font.SysFont(None, 32)
                    text_stop = font6.render("Press Return, Space or Escape to resume, Q to exit or R to start again", True, (0, 0, 0) )
                    text_stop_rect = text_stop.get_rect()
                    text_stop_rect.centerx = screen.get_rect().centerx
                    text_stop_rect.centery = screen.get_rect().centery
                    screen.fill((255, 255, 255))
                    screen.blit(text_stop, text_stop_rect)
                    pygame.display.flip()
                    b = True
                    while b:
                        time.sleep(0.05)
                        for e in pygame.event.get():
                            if e.type == QUIT:
                                pygame.quit()
                                sys.exit()
                            elif e.type == KEYDOWN:
                                if e.key == ord('q'):
                                    pygame.quit()
                                    sys.exit()
                                elif e.key == ord('r'):
                                    return 0
                                elif e.key == K_RETURN or e.key == K_ESCAPE or e.key == ord(' '):
                                    b = False
                                    time_stopped += time.time() - time_stopped_start
                                    break
                elif e.key == K_DOWN or e.key == ord('s'):
                    move['down'] += tank_speed
                elif e.key == K_UP or e.key == ord('w'):
                    move['up'] += tank_speed
                elif e.key == K_LEFT or e.key == ord('a'):
                    move['left'] += tank_speed
                elif e.key == K_RIGHT or e.key == ord('d'):
                    move['right'] += tank_speed
                elif e.key == ord(' '):
                    if fire_times <= 0:
                        fire_array.append( fire_rect.move( tank_rect.centerx - ( fire_rect.width / 2 ), tank_rect.top - fire_rect.height ) )
                        fire_times = 10
                elif e.key == ord('r'):
                    return 0
            elif e.type == KEYUP:
                if e.key == K_DOWN or e.key == ord('s'):
                    move['down'] = 0
                elif e.key == K_UP or e.key == ord('w'):
                    move['up'] = 0
                elif e.key == K_LEFT or e.key == ord('a'):
                    move['left'] = 0
                elif e.key == K_RIGHT or e.key == ord('d'):
                    move['right'] = 0
        
        #m = pygame.key.get_mods() - nomod
        #if m == KMOD_RCTRL or m == KMOD_LCTRL:
        #    move['right'] *= 2
        #    move['left'] *= 2
        #    move['down'] *= 2
        #    move['up'] *= 2
        
        if tank_rect.left <= 0:
            move['left'] = 0
        if tank_rect.right >= width:
            move['right'] = 0
        if tank_rect.top <= 0:
            move['up'] = 0
        if tank_rect.bottom >= height:
            move['down'] = 0
        
        tank_rect[0] += move['right']
        tank_rect[0] -= move['left']
        tank_rect[1] += move['down']
        tank_rect[1] -= move['up']
        
        if waiter == waituntil:
            enemy_array.append( enemy_rect.move(random.randint(1, width - 1 - enemy_rect[2]), 0) )
            efire_array.append(random.randint(1, 80))
            waituntil = random.randint(5, 50)
            waiter = 0
        else:
            waiter += 1
        
        for i in range(len(efire_array)):
            efire_array[i] -= 1
            if efire_array[i] == 0:
                efire_warray.append( efire_rect.move( enemy_array[i].centerx - (efire_rect.width / 2), enemy_array[i].bottom ) )
        
        b = True
        while b:
            b = False
            for i in range(len(enemy_array)):
                if enemy_array[i][1] >= height:
                    enemy_array.pop(i)
                    efire_array.pop(i)
                    lost -= 1
                    b = True
                    break
        
        b = True
        while b:
            b = False
            for i in range(len(fire_array)):
                if fire_array[i][1] <= 0:
                    fire_array.pop(i)
                    b = True
                    break
        
        b = True
        while b:
            b = False
            for f in range(len(fire_array)):
                for i in range(len(enemy_array)):
                    if ( enemy_array[i].bottom > fire_array[f].top and enemy_array[i].top < fire_array[f].bottom and enemy_array[i].left < fire_array[f].right and enemy_array[i].right > fire_array[f].left ):
                        eexplote_array.append(( enemy_array[i].centerx - eexplote_rect.centerx, enemy_array[i].centery - eexplote_rect.centery ))
                        eexplote_darray.append(eexplote_time)
                        enemy_array.pop(i)
                        efire_array.pop(i)
                        fire_array.pop(f)
                        b = True
                        break
                if b:
                    break
        
        b = True
        while b:
            b = False
            for i in range(len(enemy_array)):
                if ( enemy_array[i].bottom > tank_rect.top and enemy_array[i].top < tank_rect.bottom and enemy_array[i].left < tank_rect.right and enemy_array[i].right > tank_rect.left ) :
                    eexplote_array.append(( enemy_array[i].centerx - eexplote_rect.centerx, enemy_array[i].centery - eexplote_rect.centery ))
                    eexplote_darray.append(eexplote_time)
                    enemy_array.pop(i)
                    efire_array.pop(i)
                    lost -= 1
                    b = True
                    break
        
        b = True
        while b:
            b = False
            for i in range(len(efire_warray)):
                if efire_warray[i].top >= height:
                    efire_warray.pop(i)
                    b = True
                    break
        
        b = True
        while b:
            b = False
            for i in range(len(efire_warray)):
                if ( efire_warray[i].bottom > tank_rect.top and efire_warray[i].top < tank_rect.bottom and efire_warray[i].left < tank_rect.right and efire_warray[i].right > tank_rect.left ) :
                    fexplote_array.append(( efire_warray[i].left - (fexplote_rect.width - efire_warray[i].width), efire_warray[i].top - (fexplote_rect.height - efire_warray[i].height) ))
                    fexplote_darray.append(fexplote_time)
                    efire_warray.pop(i)
                    lost -= 1
                    b = True
                    break
        
        b = True
        while b:
            b = False
            for i in range(len(fexplote_darray)):
                if fexplote_darray[i] <= 0:
                    fexplote_darray.pop(i)
                    fexplote_array.pop(i)
                    b = True
                    break
        
        b = True
        while b:
            b = False
            for i in range(len(eexplote_darray)):
                if eexplote_darray[i] <= 0:
                    eexplote_darray.pop(i)
                    eexplote_array.pop(i)
                    b = True
                    break
        
        for i in range(len(fexplote_darray)):
            fexplote_darray[i] -= 1
        
        for i in range(len(eexplote_darray)):
            eexplote_darray[i] -= 1
        
        for i in range(len(efire_warray)):
            efire_warray[i] = efire_warray[i].move(efire_speed)
        
        for i in range(len(enemy_array)):
            enemy_array[i] = enemy_array[i].move(enemy_speed)
        
        for i in range(len(fire_array)):
            fire_array[i] = fire_array[i].move(fire_speed)
        
        if harder <= 0:
            r = random.randint(1, 2)
            if r == 1:
                enemy_speed = ( enemy_speed[0], enemy_speed[1] + speedup )
                if efire_speed[1] <= enemy_speed[1]:
                    efire_speed = ( efire_speed[0], enemy_speed[1] + speedup )
            elif r == 2:
                efire_speed = ( efire_speed[0], efire_speed[1] + speedup )
            harder = harder_s
        
        if lost > 0:
            font1 = pygame.font.SysFont(None, 32)
            lost_text = font1.render(str(lost), True, (255, 255, 255) )
            lost_text_rect = lost_text.get_rect()
            lost_text_rect.left = 20
            lost_text_rect.top = 20
            
            font7 = pygame.font.SysFont(None, 32)
            text_fs_time = font7.render( str( datetime.timedelta( seconds = int(time.time() - time_start_sec - time_stopped) )), True, (255, 255, 255) )
            text_fs_time_rect = text_fs_time.get_rect()
            text_fs_time_rect.right = width - 20
            text_fs_time_rect.top = 20
            
            screen.fill( (0, 0, 0) )
            for i in enemy_array:
                screen.blit(enemy, i)
            for i in fire_array:
                screen.blit(fire, i)
            for i in efire_warray:
                screen.blit(efire, i)
            for i in fexplote_array:
                screen.blit(fexplote, i)
            for i in eexplote_array:
                screen.blit(eexplote, i)
            screen.blit(tank, tank_rect)
            screen.blit(lost_text, lost_text_rect)
            screen.blit(text_fs_time, text_fs_time_rect)
            pygame.display.flip()
            #print(enemy_array)
            time.sleep(0.05)
        else:
            diff = time.time() - time_start_sec - time_stopped
            
            for i in range(256):
                for e in pygame.event.get():
                    if e.type == QUIT or ( e.type == KEYDOWN and ( e.key == K_ESCAPE or e.key == ord('q') ) ):
                        pygame.quit()
                        sys.exit()
                screen.fill( (i, i, i) )
                pygame.display.flip()
                time.sleep(0.006)
            
            winners = ""
            won = True
            if os.path.exists(winners_file):
              o = open(winners_file, 'r')
              winners = o.read() + "\n"
              o.close()
              for i in winners.split("\n"):
                if not i == '':
                  i = i.split(" ")[2]
                  if diff <= float(i.replace("\n", "").strip()):
                    won = False
            o = open(winners_file, 'w')
            win_text = ""#winners + time.strftime("%Y:%m:%d %H:%M:%S         ", time.localtime()) + str( int( float(diff) * 10 ) / 10.0 )
            o.write( winners + time.strftime("%Y:%m:%d %H:%M:%S ", time.localtime()) + str(diff) )
            o.flush()
            o.close()
            
            font2 = pygame.font.SysFont(None, 48)
            if won:
              text = font2.render("NEW RECORD!", True, (0, 0, 255) )
            else:
              text = font2.render("LOSER", True, (255, 0, 0) )
            text_rect = text.get_rect()
            text_rect.centerx = screen.get_rect().centerx
            text_rect.centery = screen.get_rect().centery
            
            #time_finish = time.strftime("%H:%M:%S", time.localtime())
            font3 = pygame.font.SysFont(None, 32)
            text_time = font3.render( str(datetime.timedelta( seconds = int(diff) )), True, (255, 0, 100) )
            text_time_rect = text_time.get_rect()
            text_time_rect.centerx = text_rect.centerx
            text_time_rect.top = text_rect.bottom + 10
            
            win_surf = pygame.Surface((230, height - 40))
            win_surf.fill((100, 0, 100))
            win_surf_rect = win_surf.get_rect()
            win_surf_rect = win_surf_rect.move((20, 20))
            font4 = pygame.font.SysFont(None, 24)
            text_win = font4.render(win_text, True, (0, 0, 0))
            text_win_rect = text_win.get_rect()
            text_win_rect.left = 10
            text_win_rect.centery = win_surf_rect.centery
            win_surf.blit(text_win, text_win_rect)
            
            font5 = pygame.font.SysFont(None, 24)
            text_return = font5.render("Press Return, Space or Escape to start again or Q to exit", True, (0, 0, 0))
            text_return_rect = text_return.get_rect()
            text_return_rect.centerx = text_time_rect.centerx
            text_return_rect.top = text_time_rect.bottom + 10
            
            screen.blit(text, text_rect)
            screen.blit(text_time, text_time_rect)
            #screen.blit(win_surf, win_surf_rect)
            screen.blit(text_return, text_return_rect)
            pygame.display.flip()
            while True:
              for e in pygame.event.get():
                if e.type == QUIT:
                  pygame.quit()
                  sys.exit()
                elif e.type == KEYDOWN:
                  if e.key == ord('q'):
                    pygame.quit()
                    sys.exit()
                  elif e.key == K_RETURN or e.key == ord(' ') or e.key == K_ESCAPE:
                    stop = True
                    return 0
                time.sleep(0.05)

if __name__ == '__main__':
  while True:
    main()
