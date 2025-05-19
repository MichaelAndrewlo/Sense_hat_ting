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

  def ai(self, enemies, player1, player2):
    pl_x = player1.position[0]
    pl_y = player1.position[1]
    pl2_x = player2.position[0]
    pl2_y = player2.position[1]
    for enemy in enemies:
      dist = get_dist(enemy.position[0], enemy.position[1], pl_x, pl_y)
      dist2 = get_dist(enemy.position[0], enemy.position[1], pl2_x, pl2_y)
      if dist < dist2: 
        u_plx = pl_x 
        u_ply = pl_y 
      else:
        u_plx = pl2_x 
        u_ply = pl2_y 
      if enemy.position[0] < u_plx:  
        enemy.position[0] += 1  
      elif enemy.position[0] > u_plx:  
        enemy.position[0] -= 1  
      elif enemy.position[1] < u_ply:  
        enemy.position[1] += 1  
      else:  
        enemy.position[1] -= 1  

 def spawn_enemy(enemies, difficulty)
   if len(enemies) > 0:
     pass
   else:
     for i in range(difficulty):
       x = randint(0,7)
       y = randint(0,7)
       name = "enemy" + str(i)
       name = Enemy(x, y)
       enemies.append(name)

def enemy_kill(enemies, players):
  for t in range(len(enemies)):
    if enemies[t].position == players[0] or enemies[t].position == players[1].position

class Player:
    def __init__(self, x, y, wx, wy, s, colour):
        self.position = [x, y]
        self.weapon = [wx, wy]
        self.score = s
        self.colour = colour

    def move(self, direction):
        if direction == 'up':
            self.position[1] -= 1
        elif direction == 'down':
            self.position[1] += 1
        elif direction == 'left':
            self.position[0] -= 1
        elif direction == 'right':
            self.position[0] += 1
        self.position[0] = check_position(self.position[0])
        self.position[1] = check_position(self.position[1])
        self.fire_weapon(direction)

    def fire_weapon(self, direction):
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
        self.weapon[0] = check_position(self.weapon[0])
        self.weapon[1] = check_position(self.weapon[1])

def check_position(position):
    return max(0, min(7, position))
  
class Trap:
  def __init__(self, x, y, z):
    self.position = [x, y]
    self.time = z
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
    else:
      for i in self.aoe:
        if players[0].position == i and players[1].position == i:
          players[0].score += 1
          players[1].score += 1
          return True, 'draw'
        elif players[0].position == i:
          players[1].score += 3
          return True, '2'
        elif players[1].position == i:
          players[0].score += 3
          return True, '1'
        else:
          return False, ''

def spawn_trap(player, traps, traps_aoe):
  x = player.position[0]
  y = player.position[1]
  trap = Trap[x, y, 0]
  traps.append(trap)
  return traps


def is_dead(players, enemies):
  for enemy in enemies:
    p1_hit = players[0].position == players[1].weapon or players[0].position == enemies[enemy].position()
    p2_hit = players[1].position == players[0].weapon or players[1].position == enemies[enemy].position()
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

    def update_display(players):
        sense.clear()
        sense.set_pixel(players[0].position[0], players[0].position[1], players[0].colour)
        sense.set_pixel(players[1].position[0], players[1].position[1], players[1].colour)
        sense.set_pixel(players[0].weapon[0], players[0].weapon[1], red)
        sense.set_pixel(players[1].weapon[0], players[1].weapon[1], red)
        for aoe in trap1.aoe:
          sense.set_pixel(aoe[0], aoe[1], (255, 255, 255))
        sense.set_pixel(traps[0].position[0], traps[0].position[1], (255, 0, 0))
    
    player1 = Player(0, 0, 0, 2, 0, blue)
    player2 = Player(7, 7, 7, 5, 0, green)
    players = [player1, player2]
    action = 0
    enemy1 = Enemy(0, 7)
    enemy2 = Enemy(7, 0)
    enemies = [enemy1, enemy2]
    traps = []
    traps_aoe = []
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
        update_display(players)

        while not dead:
            action += 1
            if action % 4 == 0:
                enemy_1.ai(player1, player2)
            current_player = players[player_turn]
            other_player = players[1 - player_turn]

            event = sense.stick.wait_for_event()
            if event.action == 'pressed':
                original_position = current_player.position[:]
                current_player.move(event.direction)

                if current_player.position == other_player.position:
                    current_player.position = original_position
                    current_player.fire_weapon(event.direction)

                update_display(players)
                dead, winner = is_dead(players)


                if not dead:
                    player_turn = switch_player(player_turn)

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
