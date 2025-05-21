from sense_hat import SenseHat
from time import sleep
from random import randint

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

  def ai(self, player1, player2, enemies):
    pl_x = player1.position[0]
    pl_y = player1.position[1]
    pl2_x = player2.position[0]
    pl2_y = player2.position[1]
    dist = get_dist(self.position[0], self.position[1], pl_x, pl_y)
    dist2 = get_dist(self.position[0], self.position[1], pl2_x, pl2_y)
    if dist < dist2: 
      u_plx = pl_x 
      u_ply = pl_y 
    else:
      u_plx = pl2_x 
      u_ply = pl2_y 
    if self.position[0] < u_plx:  
      self.position[0] += 1  
    elif self.position[0] > u_plx:  
      self.position[0] -= 1  
    elif self.position[1] < u_ply:  
      self.position[1] += 1  
    else:  
      self.position[1] -= 1  
        
  def spawn_enemy(enemies, difficulty):
   if len(enemies) > 0:
     pass
   else:
     for i in range(difficulty):
       x = randint(0,7)
       y = randint(0,7)
       name = "enemy" + str(i)
       name = Enemy(x, y)
       enemies.append(name)
  
def enemy_killed(enemies, players):
  for player in players:
    for enemy in enemies:
      if enemy.position == player.weapon:
        enemies.remove(enemy)
        return enemies

class Player:
    def __init__(self, x, y, wx, wy, s, colour):
        self.position = [x, y]
        self.weapon = [wx, wy]
        self.score = s
        self.colour = colour

    def move(self, direction, traps, enemies):
        if direction == 'up':
            self.position[1] -= 1
        elif direction == 'down':
            self.position[1] += 1
        elif direction == 'left':
            self.position[0] -= 1
        elif direction == 'right':
            self.position[0] += 1
        if direction == 'middle':
          traps = spawn_trap(self, traps)
        self.position[0] = check_position(self.position[0])
        self.position[1] = check_position(self.position[1])
        self.fire_weapon(direction, enemies)

    def fire_weapon(self, direction, enemies):
        if direction == 'up':
            self.weapon[0] = self.position[0]
            self.weapon[1] = self.position[1] - 2
        elif direction == 'down':
            self.weapon[0] = self.position[0]
            self.weapon[1] = self.position[1] + 2
        elif direction == 'left':
            self.weapon[0] = self.position[0] - 2
            self.weapon[1] = self.position[1]
        elif direction == 'right':
            self.weapon[0] = self.position[0] + 2
            self.weapon[1] = self.position[1]
        for enemy in enemies:
          if enemy.position == self.weapon:
            enemies.remove(enemy)
        self.weapon[0] = check_position(self.weapon[0])
        self.weapon[1] = check_position(self.weapon[1])

def check_position(position):
    return max(0, min(7, position))
  
class Trap:
  def __init__(self, x, y, z, col):
    self.position = [x, y]
    self.time = z
    self.col = col
    aoe = []
    for i in range(-1, 2):
      for x in range(-1, 2):
        x_pos = self.position[0] + i
        y_pos = self.position[1] + x
        x_pos = check_position(x_pos)
        y_pos = check_position(y_pos)
        coords = [x_pos, y_pos]
        aoe.append(coords)
    self.aoe = aoe
  
  def trap_kill(self, players):
    if self.time < 6:
      self.time += 1  
      self.col = (125, 125, 125)
      return False, ''
    else:
      self.col = (255, 255, 255)
      if players[0].position in self.aoe and players[1].position in self.aoe:
        players[0].score += 1
        players[1].score += 1
        return True, 'draw'
      elif players[0].position in self.aoe:
        players[1].score += 3
        return True, '2'
      elif players[1].position in self.aoe:
        players[0].score += 3
        return True, '1'
      else:
        return False, ''

def spawn_trap(player, traps):
  x = player.position[0]
  y = player.position[1]
  trap = Trap(x, y, 0, (0, 0, 0))
  traps.append(trap)
  return traps


def is_dead(players, enemies):
  p1_dead = False
  p2_dead = False
  if len(enemies) != 0:
    for enemy in enemies:
      p1_hit = players[0].position == players[1].weapon or players[0].position == enemy.position or p1_dead
      p2_hit = players[1].position == players[0].weapon or players[1].position == enemy.position or p2_dead
      if p1_hit:
        p1_dead = True
      if p2_hit:
        p2_dead = True
  elif len(enemies) == 0:
    p1_hit = players[0].position == players[1].weapon
    p2_hit = players[1].position == players[0].weapon
  if p1_hit and p2_hit:
      players[0].score += 1
      players[1].score += 1
      return True, 'draw'
  elif p1_hit:
      players[1].score += 3
      return True, '2'
  elif p2_hit:
      players[0].score += 3
      return True, '1'
  return False, ''

def switch_player(player_turn):
    return 1 - player_turn

def run_game():
    sense = SenseHat()

    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    scores = [0, 0]

    def update_display(players, enemies):
        sense.clear()
        if len(traps) > 0:
          for trap in traps:
            for aoe in trap.aoe:
              sense.set_pixel(aoe[0], aoe[1], trap.col)
            sense.set_pixel(traps[0].position[0], traps[0].position[1], (255, 0, 0))
        sense.set_pixel(players[0].position[0], players[0].position[1], players[0].colour)
        sense.set_pixel(players[1].position[0], players[1].position[1], players[1].colour)
        sense.set_pixel(players[0].weapon[0], players[0].weapon[1], red)
        sense.set_pixel(players[1].weapon[0], players[1].weapon[1], red)
        for enemy in enemies:
          sense.set_pixel(enemy.position[0], enemy.position[1], 255, 255, 0)
    
    player1 = Player(0, 0, 0, 2, 0, blue)
    player2 = Player(7, 7, 7, 5, 0, green)
    players = [player1, player2]
    action = 0
    enemy1 = Enemy(0, 7)
    enemy2 = Enemy(7, 0)
    enemies = [enemy1, enemy2]
    traps = []
    while True:
        player1.position = [0, 0]
        player1.weapon = [0, 2]
        player2.position = [7, 7]
        player2.weapon = [7, 5]
        player_turn = 0
        action = 0
        winner = ''
        dead = False

        sense.clear()
        update_display(players, enemies)

        while not dead:
            action += 1
            if action % 4 == 0:
              for enemy in enemies:
                enemy.ai(player1, player2, enemies)
            current_player = players[player_turn]
            other_player = players[1 - player_turn]

            event = sense.stick.wait_for_event()
            if event.action == 'pressed':
                original_position = current_player.position[:]
                current_player.move(event.direction, traps, enemies)

                if current_player.position == other_player.position:
                    current_player.position = original_position
                    current_player.fire_weapon(event.direction, traps, enemies)
                    
                dead, winner = is_dead(players, enemies)
                if len(traps) != 0:
                  for trap in traps:
                    dead, winner = trap.trap_kill(players)
                    
                    
                if not dead:
                  player_turn = switch_player(player_turn)
                update_display(players, enemies)

        print("\n--- Round Over ---")
        print("Winner: " + str(winner))
        print("Score - Player 1: " + str(player1.score) + " | Player 2: " + str(player2.score))

        choice = input("Press Enter to play again or type 'exit' to quit: ").strip().lower()
        if choice == 'exit':
            break

    print("\nFinal Scores:")
    print("Player 1: " + str(player1.score()))
    print("Player 2: " + str(player2.score()))
    print("Thanks for playing!")

if __name__ == "__main__":
    run_game()
