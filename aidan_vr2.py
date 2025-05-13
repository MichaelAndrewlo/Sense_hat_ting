from sense_hat import SenseHat
from time import sleep

sense = SenseHat()

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
player_colours = [blue, green]

class Player:
	def __init__(self, x, y, wx, wy, colour):
		self.position = [x, y]
		self.weapon = [wx, wy]
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

def check_position(position):
	while position > 7:
		position -= 1
	while position < 0:
		position += 1
	return position

def is_dead(players):
	global dead, winner
	p1_hit = players[0].get_position() == players[1].get_weapon()
	p2_hit = players[1].get_position() == players[0].get_weapon()
	if p1_hit and p2_hit:
		dead = True
		winner = 'draw'
	elif p1_hit:
		dead = True
		winner = '2'
	elif p2_hit:
		dead = True
		winner = '1'


def update_display(players):
	sense.clear()
	sense.set_pixel(players[0].get_position()[0], players[0].get_position()[1], players[0].colour)
	sense.set_pixel(players[1].get_position()[0], players[1].get_position()[1], players[1].colour)
	sense.set_pixel(players[0].get_weapon()[0], players[0].get_weapon()[1], red)
	sense.set_pixel(players[1].get_weapon()[0], players[1].get_weapon()[1], red)

def switch_player(player_turn):
	return 1 - player_turn

player1 = Player(0, 0, 0, 2, blue)
player2 = Player(7, 7, 7, 5, green)
players = [player1, player2]
player_turn = 0
dead = False
winner = ''

sense.clear()
update_display(players)
while not dead:	
	current_player = players[player_turn]
	other_player = players[1 - player_turn]
	is_dead(players)
	if dead:
		break
	for event in sense.stick.get_events():
		if event.action == 'pressed':
			original_position = current_player.get_position()
			current_player.move(event.direction)
		if current_player.get_position() == other_player.get_position():
			current_player.position = original_position
			continue
		current_player.fire_weapon(event.direction)
		sense.clear()
		update_display(players)
		player_turn = switch_player(player_turn)
		break

print(winner)
