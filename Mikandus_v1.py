from sense_hat import SenseHat

class Player:
    def __init__(self, x, y, wx, wy, s, colour, trap_free):
        self.position = [x, y]
        self.weapon = [wx, wy]
        self.score = s
        self.colour = colour
        self.trap_free = 2

    def move(self, direction, traps):
        if direction == 'up':
            self.position[1] -= 1
        elif direction == 'down':
            self.position[1] += 1
        elif direction == 'left':
            self.position[0] -= 1
        elif direction == 'right':
            self.position[0] += 1
        elif direction == 'middle' and self.trap_free > 0:
            spawn_trap(self, traps)
            self.trap_free -= 1
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

class Enemy(Player):
    def __init__(self, x, y):
        self.position = [x, y]

    def get_closest_player(self, players):
        player1_distance = ((self.position[0] - players[0].position[0]) ** 2 + (self.position[1] - players[0].position[1]) ** 2) ** 1/2
        player2_distance = ((self.position[0] - players[1].position[0]) ** 2 + (self.position[1] - players[1].position[1]) ** 2) ** 1/2
        closest = min(player1_distance, player2_distance)
        if player1_distance == closest and player2_distance == closest:
            return 0
        elif player1_distance == closest:
            return 0
        elif player2_distance == closest:
            return 1
class Trap:
  def __init__(self, x, y, z):
    self.position = [x, y]
    self.time = z
    self.col = (0, 50, 50)
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
  
  def trap_kill(self, players, enemies, traps):
    if self.time < 6:
      self.time += 1  
      return False, ''
    else:
      self.col = (255, 255, 255)
      if players[0].position in self.aoe and players[1].position in self.aoe:
        players[0].score += 1
        players[1].score += 1
        traps.remove(self)
        return True, 'draw'
      elif players[0].position in self.aoe:
        players[1].score += 3
        traps.remove(self)
        return True, '2'
      elif players[1].position in self.aoe:
        players[0].score += 3
        traps.remove(self)
        return True, '1'
      return False, ''
          
    def enemy_killed(self, enemies, traps):
        if self.time < 6:
            pass
        else:
            for enemy in enemies:
                if enemy.position in self.aoe:
                    enemies.remove(enemy)
                    traps.remove(self)

def spawn_trap(player, traps):
  x = player.position[0]
  y = player.position[1]
  trap = Trap(x, y, 0)
  traps.append(trap)
  return traps

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
    
def ai_turn(players, enemies):
    for enemy in enemies:
        closest_index = enemy.get_closest_player(players)
        if enemy.position[0] < players[closest_index].position[0]:
            enemy.position[0] += 1
        elif enemy.position[0] > players[closest_index].position[0]:
            enemy.position[0] -= 1
        elif enemy.position[1] < players[closest_index].position[1]:
            enemy.position[1] += 1
        elif enemy.position[1] > players[closest_index].position[1]:
            enemy.position[1] -= 1

        enemy.position[0] = check_position(enemy.position[0])
        enemy.position[1] = check_position(enemy.position[1])


def check_position(position):
    return max(0, min(7, position))

def is_dead(players, enemies):
    p1_hit_by_weapon = players[0].position == players[1].weapon
    p2_hit_by_weapon = players[1].position == players[0].weapon

    p1_hit_by_enemy = False
    p2_hit_by_enemy = False

    for enemy in enemies:
        if enemy.position == players[0].position:
            p1_hit_by_enemy = True
        if enemy.position == players[1].position:
            p2_hit_by_enemy = True

    enemies_to_remove = []
    for enemy in enemies:
        for player in players:
            if enemy.position == player.weapon:
                enemies_to_remove.append(enemy)

    for enemy in enemies_to_remove:
        enemies.remove(enemy)

    if p1_hit_by_enemy and p2_hit_by_enemy:
        players[0].score += 1
        players[1].score += 1
        return True, 'draw'

    if p1_hit_by_enemy:
        players[1].score += 3
        return True, '2'
    if p2_hit_by_enemy:
        players[0].score += 3
        return True, '1'

    if p1_hit_by_weapon and p2_hit_by_weapon:
        players[0].score += 1
        players[1].score += 1
        return True, 'draw'
    elif p1_hit_by_weapon:
        players[1].score += 3
        return True, '2'
    elif p2_hit_by_weapon:
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
    yellow = (255, 255, 0)

    def update_display(players, enemies):
        sense.clear()
        sense.set_pixel(players[0].position[0], players[0].position[1], players[0].colour)
        sense.set_pixel(players[1].position[0], players[1].position[1], players[1].colour)
        sense.set_pixel(players[0].weapon[0], players[0].weapon[1], red)
        sense.set_pixel(players[1].weapon[0], players[1].weapon[1], red)
        
        for enemy in enemies:
            sense.set_pixel(enemy.position[0], enemy.position[1], yellow)

    
    player1 = Player(0, 0, 0, 2, 0, blue)
    player2 = Player(7, 7, 7, 5, 0, green)
    players = [player1, player2]
    
    enemy1 = Enemy(0, 7)
    enemy2 = Enemy(7, 0)
    enemies = [enemy1, enemy2]
    
    while True:
        player1.position = [0, 0]
        player1.weapon = [0, 2]
        player2.position = [7, 7]
        player2.weapon = [7, 5]
        
        enemy1 = Enemy(0, 7)
        enemy2 = Enemy(7, 0)
        enemies = [enemy1, enemy2]
        
        player_turn = 0
        winner = ''
        dead = False

        update_display(players, enemies)

        while not dead:
            current_player = players[player_turn]
            other_player = players[1 - player_turn]

            event = sense.stick.wait_for_event()
            if event.action == 'pressed':
                original_position = current_player.position
                current_player.move(event.direction)
                ai_turn(players, enemies)

                if current_player.position == other_player.position:
                    current_player.position = original_position
                    current_player.fire_weapon(event.direction)
                else:
                    update_display(players, enemies)
                    dead, winner = is_dead(players, enemies)
                    if not dead:
                        player_turn = switch_player(player_turn)

        print("\n--- Round Over ---")
        print("Winner: " + str(winner))
        print("Score - Player 1: " + str(player1.score) + " | Player 2: " + str(player2.score))

        choice = input("Press Enter to play again or type 'exit' to quit: ").strip().lower()
        if choice == 'exit':
            break

    print("\nFinal Scores:")
    print("Player 1: " + str(player1.score))
    print("Player 2: " + str(player2.score))
    print("Thanks for playing!")

if __name__ == "__main__":
    run_game()
