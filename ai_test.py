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
    
