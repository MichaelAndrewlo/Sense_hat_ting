from time import sleep
player1 = [0, 0]
player2 = [7, 7]
def get_dist(x, y, x2, y2): 
  x_dist = x - x2 
  y_dist = y - y2 
  x_square = x_dist ** 2 
  y_square = y_dist ** 2 
  square = x_square + y_square 
  dist = square ** (1 / 2) 
  return dist 

class Enemy:
  def __init__(self, x, y):
    self.position = [x, y]

  def ai(self):
    dist = get_dist(self.position[0], self.position[1], player1[0], player1[1])
    dist2 = get_dist(self.position[0], self.position[1], player2[0], player2[1])
    pl_x = player1[0]
    pl_y = player1[1]
    pl2_x = player2[0]
    pl2_y = player2[1]
    if dist < dist2: 
      u_plx = pl_x 
      u_ply = pl_y 
    else:
      u_plx = pl2_x 
      u_ply = pl2_y 
    if self.position[0], < u_plx:  
      self.position[0], += 1  
    elif self.position[0], > u_plx:  
      self.position[0], -= 1  
    elif self.position[1], < u_ply:  
      self.position[1] += 1  
    else:  
      self.position[1] -= 1  

enemy1 = Enemy(6, 6)
while True:
  enemy1.ai()
  sleep(1)
