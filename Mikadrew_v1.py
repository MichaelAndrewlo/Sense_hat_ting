from sense_hat import SenseHat
from time import sleep

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

  def ai(self, player1, player2):
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

    def get_position(self):
        return self.position

    def get_weapon(self):
        return self.weapon
    
    def get_score(self):
        return self.score

def check_position(position):
    return max(0, min(7, position))
  
class trap:
  def __init__(self, x, y, z):
    self.position = [x, y]
    self.time = z

  def aoe(self):
    aoe = []
    for i in range(-1, 1):
      for x in range(-1, 1):
        check_position(i)
        check_position(x)
        coords = [i, x]
        aoe.append(coords)
    return aoe
  
  def killzone(self, aoe, players):
    if self.time < 6:
      self.time += 1  
    else:
      for i in aoe:
        if players[0].get_position() == i and players[1].get_position() == i:
          players[0].score += 1
          players[1].score += 1
          return True, 'draw'
        elif players[0].get_position() == i:
          players[1].score += 3
          return True, '2'
        elif players[1].get_position() == i:
          players[0].score += 3
          return True, '1'
        else:
          return False, ''

def is_dead(players):
    p1_hit = players[0].get_position() == players[1].get_weapon()
    p2_hit = players[1].get_position() == players[0].get_weapon()
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
        sense.set_pixel(players[0].get_position()[0], players[0].get_position()[1], players[0].colour)
        sense.set_pixel(players[1].get_position()[0], players[1].get_position()[1], players[1].colour)
        sense.set_pixel(players[0].get_weapon()[0], players[0].get_weapon()[1], red)
        sense.set_pixel(players[1].get_weapon()[0], players[1].get_weapon()[1], red)
    
    player1 = Player(0, 0, 0, 2, 0, blue)
    player2 = Player(7, 7, 7, 5, 0, green)
    players = [player1, player2]
    action = 0
    enemy1 = Enemy(6, 6)
    
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
                original_position = current_player.get_position()[:]
                current_player.move(event.direction)

                if current_player.get_position() == other_player.get_position():
                    current_player.position = original_position
                    current_player.fire_weapon(event.direction)

                update_display(players)
                dead, winner = is_dead(players)


                if not dead:
                    player_turn = switch_player(player_turn)

        print("\n--- Round Over ---")
        print("Winner: " + str(winner))
        print("Score - Player 1: " + str(player1.get_score()) + " | Player 2: " + str(player2.get_score()))

        choice = input("Press Enter to play again or type 'exit' to quit: ").strip().lower()
        if choice == 'exit':
            break

    print("\nFinal Scores:")
    print("Player 1: " + str(player1.get_score()))
    print("Player 2: " + str(player2.get_score()))
    print("Thanks for playing!")

if __name__ == "__main__":
    run_game()
