from sense_hat import SenseHat 
from random import randint 
from time import sleep 
sense = SenseHat() 
a = 255, 0, 0 # red 
b = 0, 255, 0 # green 
c = 0, 0, 255 # blue 
d = 255, 255, 0 # yellow 
e = 183, 183, 183 # gray 
f = 0, 0, 0 # nothing/ black 
g = 255, 0, 255 # pink/ magenta 
h = 255, 153, 0 # orange 
i = 255, 255, 255 # white 
enemy_positions = [] 
player_positions = [[0, 0, 0, 2],[7, 7, 7, 5]]
x_pos = 0 
y_pos = 0 
pl_x = 0 
pl_y = 0
pl2_x = 7
pl2_y = 7
action = 0 
z = 0 
w = 0 
j = 7
k = 7
score = 0 
dead = False 
col = a
col2 = h
difficulty = 0 
score = 0 
players = 1
player = 1
traps = [] 
  
  
def ai(t): 
  global enemy_positions
  global x_pos
  global y_pos
  pl_x = player_positions[0][0]
  pl_y = player_positions[0][1]
  get_xy(t, enemy_positions)
  org_x = x_pos 
  org_y = y_pos 
  if players == 1:
    u_plx = pl_x
    u_ply = pl_y
  if players >= 2:
    dist = get_dist(x_pos, y_pos, pl_x, pl_y)
    pl2_x = player_positions[1][0]
    pl2_y = player_positions[1][1]
    dist2 = get_dist(x_pos, y_pos, pl2_x, pl2_y)
    if dist < dist2:
      u_plx = pl_x
      u_ply = pl_y
    else:
      u_plx = pl2_x
      u_ply = pl2_y
  if x_pos < u_plx: 
    x_pos += 1 
  elif x_pos > u_plx: 
    x_pos -= 1 
  elif y_pos < u_ply: 
    y_pos += 1 
  else: 
    y_pos -= 1 
  coords = str(x_pos) + str(y_pos) 
  enemy_positions.pop(t) 
  for i in enemy_positions: 
    if coords == i: 
      coords = str(org_x) + str(org_y) 
  enemy_positions.insert(t, coords)
  sense.clear()
  
def check_pos(x1): 
  while x1 >= 8: 
    x1 -= 1 
  while x1 <= -1: 
    x1 += 1 
  return x1 
  
def get_dist(x, y, x2, y2):
  x_dist = x - x2
  y_dist = y - y2
  x_square = x_dist ** 2
  y_square = y_dist ** 2
  square = x_square + y_square
  dist = square ** (1 / 2)
  return dist
  
def get_xy(z, lists): 
  global x_pos 
  global y_pos 
  position = lists[z] 
  x_pos = int(position[0]) 
  y_pos = int(position[1]) 
  
def move(d, player):
  global player_positions
  x_pos = player_positions[player][0]
  y_pos = player_positions[player][1]
  if d == "up":
      y_pos-= 1
  elif d == "down":
      y_pos += 1
  elif d == "left":
      x_pos -= 1
  elif d == "right":
      x_pos += 1
  x_pos = check_pos(x_pos)
  y_pos = check_pos(y_pos)
  player_positions[player][0] = x_pos
  player_positions[player][1] = y_pos
  sense.clear()
  
def spawn_enemies(z):
  global enemy_positions
  for i in range(z):
    x = randint(0,7)
    y = randint(0,7)
    for i in range(len(enemy_positions)):
      get_xy(i, enemy_positions)
      while (x_pos == x and y_pos == y) or (x_pos == player_positions[0][0] and y_pos == player_positions[0][1]) or (x_pos == player_positions[1][0] and y_pos == player_positions[1][1]): 
        x = randint(0,7) 
        y = randint(0,7) 
    coords = str(x) + str(y) 
    enemy_positions.append(coords) 

def weapon():
    global player_positions
    x_pos = player_positions[player][0]
    y_pos = player_positions[player][1]
    wx_pos = player_positions[player][2]
    wy_pos = player_positions[player][3]
    if d == "up":
        wy_pos = y_pos - 2
    elif d == "down":
        wy_pos = y_pos + 2
    elif d == "left":
        wx_pos = x_pos - 2
    elif d == "right":
        wx_pos = x_pos + 2
    wx_pos = check_pos(wx_pos)
    wy_pos = check_pos(wy_pos)
    player_positions[player][2] = wx_pos
    player_positions[player][3] = wy_pos
    print(player_positions)
  
"""
def place_trap():
  

def trap():
  for i in range(len(traps)):
    get_xy(i, traps)
    trap_x = x_pos
    trap_y = y_pos
    trap = traps[i] 
    trap_time = int(trap[3])
    for x in range(len(enemy_positions)):
      get_xy(x, enemy_positions)
      if trap_time >= 3:
        if x_pos == trap_x + 1 or x_pos == trap_x - 1:
          if y_pos == trap_y + 1 or y_pos == trap_y - 1:
            trap_used = True
            enemy_positions.pop(x)
      if trap_used:
        traps.pop(i)
        trap_used = False
"""
if players == 1:
  while True:
    for i in range(len(enemy_positions)):
      get_xy(i, enemy_positions)
      if x_pos == player_positions[0][0] and y_pos == player_positions[0][1]:
        dead = True
    for event in sense.stick.get_events():
      if event.action == "pressed":
        move(event.direction, 0)
        weapon()
    if len(enemy_positions) == 0:
      difficulty += 1
      spawn_enemies(difficulty)
      sleep(0.2)
    if action % 5 == 0:
      for i in range(len(enemy_positions)):
        ai(i)
    if dead:
      break
    action += 1
    for i in range(len(enemy_positions)):
      get_xy(i, enemy_positions)
      sense.set_pixel(x_pos, y_pos, c)
    for i in range(len(enemy_positions)):
      get_xy(i, enemy_positions)
      if z == x_pos and w == y_pos:
        col = d
        break
      else:
        col = a
    sense.set_pixel(player_positions[0][0], player_positions[0][1], b)
    sense.set_pixel(z, w, col)
    sleep(0.1)

if players == 1:
  sense.show_message("Final score of: " + str(score) + ", thanks for playing", 0.05)
  
if players == 2:
  while True:
    if player == 1:
      for event in sense.stick.get_events():
        if event.action == "pressed":
          org_x = pl_x
          org_y = pl_y
          move(event.direction, player)
          weapon(pl_x, pl_y, event.direction)
          player = 2
          if pl_x == pl2_x and pl_y == pl2_y:
            pl_x = org_x
            pl_y = org_y
    elif player == 2:
      for event in sense.stick.get_events():
        if event.action == "pressed":
          org_2x = pl2_x
          org_2y = pl2_y
          move(event.direction, player)
          weapon2(pl2_x, pl2_y, event.direction)
          player = 1
          if pl2_x == pl_x and pl2_y == pl_y:
            pl2_x = org_2x
            pl2_y = org_2y
    
    sense.set_pixel(pl_x, pl_y, b)
    sense.set_pixel(pl2_x, pl2_y, c)
    sense.set_pixel(z, w, col)
    sense.set_pixel(j, k, col2)
