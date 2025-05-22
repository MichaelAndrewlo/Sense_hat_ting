from sense_hat import SenseHat

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

class Enemy:
    def __init__(self, x, y):
        self.position = [x, y]

    def get_closest_player(self, players):
        def distance(p):
            dx = self.position[0] - p.position[0]
            dy = self.position[1] - p.position[1]
            return (dx**2 + dy**2) ** 0.5

        d1 = distance(players[0])
        d2 = distance(players[1])
        if d1 <= d2:
            return 0
        return 1

class Trap:
    def __init__(self, x, y):
        self.position = [x, y]
        self.turn = 3
        self.colour = (125, 125, 125)
        aoe = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                x_pos = check_position(x + dx)
                y_pos = check_position(y + dy)
                aoe.append([x_pos, y_pos])
        self.aoe = aoe

def spawn_trap(x, y, traps):   
    traps.append(Trap(x, y))
    
def ai_turn(players, enemies):
    for enemy in enemies:
        target = players[enemy.get_closest_player(players)]
        if enemy.position[0] < target.position[0]:
            enemy.position[0] += 1
        elif enemy.position[0] > target.position[0]:
            enemy.position[0] -= 1
        elif enemy.position[1] < target.position[1]:
            enemy.position[1] += 1
        elif enemy.position[1] > target.position[1]:
            enemy.position[1] -= 1

        enemy.position[0] = check_position(enemy.position[0])
        enemy.position[1] = check_position(enemy.position[1])

def check_position(position):
    return max(0, min(7, position))

def is_dead(players, enemies, traps):
    p1_enemy, p2_enemy = player_dies_by_enemy(players, enemies)
    p1_weapon, p2_weapon = player_dies_by_weapon(players)
    p1_trap, p2_trap = player_dies_by_trap(players, traps)

    handle_enemy_deaths(enemies, players, traps)

    result = check_and_score(players, p1_enemy, p2_enemy)
    if result[0]: 
        return result
    result = check_and_score(players, p1_weapon, p2_weapon)
    if result[0]: 
        return result
    result = check_and_score(players, p1_trap, p2_trap)
    if result[0]: 
        return result

    return False, ''


def check_and_score(players, p1_dead, p2_dead):
    if p1_dead and p2_dead:
        players[0].score += 1
        players[1].score += 1
        return True, 'draw'
    elif p1_dead:
        players[1].score += 3
        return True, '2'
    elif p2_dead:
        players[0].score += 3
        return True, '1'
    return False, ''


def player_dies_by_enemy(players, enemies):
    p1_hit = False
    p2_hit = False
    for enemy in enemies:
        if enemy.position == players[0].position:
            p1_hit = True
        if enemy.position == players[1].position:
            p2_hit = True
    return p1_hit, p2_hit

def player_dies_by_weapon(players):
    p1_hit = players[0].position == players[1].weapon
    p2_hit = players[1].position == players[0].weapon
    return p1_hit, p2_hit


def player_dies_by_trap(players, traps):
    p1_trap = False
    p2_trap = False
    for trap in traps:
        if trap.turn == 0:
            trap.colour = (255, 255, 255)
            for pos in trap.aoe:
                if pos == players[0].position:
                    p1_trap = True
                elif pos == players[1].position:
                    p2_trap = True
                if p1_trap or p2_trap:
                    traps.remove(trap)
                    break
        elif trap.turn > 0:
            trap.turn -= 1
    return p1_trap, p2_trap


def handle_enemy_deaths(enemies, players, traps):
    enemies_to_remove = []
    for enemy in enemies:
        for player in players:
            if enemy.position == player.weapon:
                enemies_to_remove.append(enemy)
    for trap in traps:
        if trap.turn == 0:
            for pos in trap.aoe:
                for enemy in enemies:
                    if enemy.position == pos and enemy not in enemies_to_remove:
                        enemies_to_remove.append(enemy)
                        traps.remove(trap)
    for enemy in enemies_to_remove:
        if enemy in enemies:
            enemies.remove(enemy)

def switch_player(player_turn):
    return 1 - player_turn

def run_game():
    sense = SenseHat()

    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)

    def update_display(players, enemies, traps):
        sense.clear()
        for enemy in enemies:
            sense.set_pixel(enemy.position[0], enemy.position[1], yellow)
        for trap in traps:
            for pos in trap.aoe:
                sense.set_pixel(pos[0], pos[1], trap.colour)
        sense.set_pixel(players[0].weapon[0], players[0].weapon[1], red)
        sense.set_pixel(players[1].weapon[0], players[1].weapon[1], red)
        sense.set_pixel(players[0].position[0], players[0].position[1], players[0].colour)
        sense.set_pixel(players[1].position[0], players[1].position[1], players[1].colour)  
        
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
        enemies = [Enemy(0, 7), Enemy(7, 0)]
        traps = []
        
        player_turn = 0
        winner = ''
        dead = False

        update_display(players, enemies, traps)

        while not dead:
            current_player = players[player_turn]
            other_player = players[1 - player_turn]

            event = sense.stick.wait_for_event()
            if event.action == 'pressed':0
                if event.direction == 'middle':
                    spawn_trap(current_player.position[0], current_player.position[1], traps)
                else:
                    original_position = current_player.position[:]
                    current_player.move(event.direction)
                    ai_turn(players, enemies)

                    if current_player.position == other_player.position:
                        current_player.position = original_position
                    else:
                        update_display(players, enemies, traps)
                        dead, winner = is_dead(players, enemies, traps)
                        if not dead:
                            player_turn = switch_player(player_turn)

        print("\n--- Round Over ---")
        print("Winner: " + str(winner))
        print("Score - Player 1: " + str(player1.score) + " | Player 2: " + str(player2.score))

        if input("Press Enter to play again or type 'exit' to quit: ").strip().lower() == 'exit':
            break

    print("\nFinal Scores:")
    print("Player 1: " + str(player1.score))
    print("Player 2: " + str(player2.score))
    print("Thanks for playing!")

if __name__ == "__main__":
    run_game()
