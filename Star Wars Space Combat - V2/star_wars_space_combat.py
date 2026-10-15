

# Import the random module for dice rolls
import copy
import random
from typing import List

# D2 roll function
def d2():
	return random.randint(1, 2)

# D4 roll function
def d4():
	return random.randint(1, 4)

# D6 roll function
def d6():
	return random.randint(1, 6)

# D8 roll function
def d8():
	return random.randint(1, 8)

# D10 roll function
def d10():
	return random.randint(1, 10)

# D12 roll function
def d12():
	return random.randint(1, 12)

# D20 roll function
def d20():
	return random.randint(1, 20)

# 3D vector class for positions and movements in space
class Vector3:
	def __init__(self, x=0, y=0, z=0):
		self.x = x
		self.y = y
		self.z = z

	def __add__(self, other):
		return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

	def __sub__(self, other):
		return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

	def __mul__(self, scalar):
		return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

	def __repr__(self):
		return f"Vector3({self.x}, {self.y}, {self.z})"

# Weapon class
class Weapon:
	def __init__(self, name, damage_die, number_of_die, damage_bonus=0):
			self.name = name
			self.number_of_die = number_of_die
			self.damage_die = damage_die
			self.damage_bonus = damage_bonus
	
	def roll_damage(self):
		total_damage = 0
		for _ in range(self.number_of_die):
			if self.damage_die == 2:
				total_damage += d2()
			elif self.damage_die == 4:
				total_damage += d4()
			elif self.damage_die == 6:
				total_damage += d6()
			elif self.damage_die == 8:
				total_damage += d8()
			elif self.damage_die == 10:
				total_damage += d10()
			elif self.damage_die == 12:
				total_damage += d12()
			elif self.damage_die == 20:
				total_damage += d20()
		total_damage += self.damage_bonus
		return total_damage

# X-Wing laser cannon weapon class
class XWingLaserCannon(Weapon):
	def __init__(self):
		super().__init__("Laser Cannon (X-Wing)", 10, 1)

# TIE Fighter laser cannon weapon class
# Slightly higher fire speed per cannon, and slightly higher explosive power per shot
class TIEFighterLaserCannon(Weapon):
	def __init__(self):
		super().__init__("Laser Cannon (TIE Fighter)", 12, 1, 1) 

# Shield class
class Shield:
	def __init__(self, name, description, shield_points, shield_regen_per_tick):
		self.name = name
		self.description = description
		self.shield_points = shield_points
		self.max_shield_points = shield_points
		self.shield_regen = shield_regen_per_tick

# X-Wing shield subclass
class XWingShield(Shield):
	def __init__(self):
		super().__init__("X-Wing Shield", "Standard X-Wing shield", 13, 1)


# Actor class representing any entity in the game world (e.g., starships)
class Actor:
	def __init__(self, name):
		self.name = name
		self.position = Vector3()

	def move(self, direction):
		self.position += direction

	def setPosition(self, position):
		self.position = position

	def getPosition(self):
		return self.position

# Unit class representing a generic unit in the game world
# ex. a group of starships
class Unit(Actor):
	def __init__(self, name, faction=None):
		super().__init__(name)
		self.faction = faction
		self.starships = []

	def addStarship(self, starship):
		self.starships.append(starship)

	def removeStarship(self, starship):
		if starship in self.starships:
			self.starships.remove(starship)

	def getStarships(self):
		return self.starships

	def addStarships(self, starships):
		for starship in starships:
			self.addStarship(starship)

	# Attack another unit with this unit's starships
	def attack(self, target_unit):
		simulateSingleCombatRoundOneSided(self.getStarships(), target_unit.getStarships())

	# Prints overview then lists the starships in the unit
	def __repr__(self):
		starship_list = "\n - ".join([repr(starship) for starship in self.starships])
		return f"<Unit name={self.name} faction={self.faction} starships={len(self.starships)}>\n - {starship_list}"


# Class representing a starship in Star Wars space combat
class Starship:
	def __init__(self, name, faction, hull_points, speed, evasion, weapons, shield = None):
		self.name = name
		self.is_destroyed = False
		self.faction = faction
		self.hull = hull_points
		self.speed = speed
		self.evasion = evasion
		self.weapons = weapons
		self.shield = shield

	def tick(self):
		self.tickChargeShields()

	# Check if the starship has an active shield
	def hasShield(self):
		return self.shield is not None and self.shield.shield_points > 0

	# Recharge the starship's shields to maximum
	def rechargeShields(self):
		if self.shield:
			self.shield.shield_points = self.shield.max_shield_points

	# Tick function to charge shields each game tick
	def tickChargeShields(self):
		if not self.hasShield():
			return
		
		self.shield.shield_points += self.shield.shield_regen

		if self.shield.shield_points > self.shield.max_shield_points:
			self.shield.shield_points = self.shield.max_shield_points

	# The target's evasion determines whether an attack hits
	def rollHit(self, target):
		attackerRoll = d20()
		defenderRoll = d20() + target.evasion
		return attackerRoll > defenderRoll

	# Apply damage to the starship, first to shields then to hull
	def takeDamage(self, damage):
		shield = None
		shield = self.shield

		remaining_damage = damage

		# Apply damage to shields first, if available
		if shield and shield.shield_points > 0:
			shield.shield_points -= remaining_damage
			if shield.shield_points < 0:
				remaining_damage = -shield.shield_points
				shield.shield_points = 0
			else:
				remaining_damage = 0

		# Apply any remaining damage to the hull
		if remaining_damage > 0:
			self.hull -= remaining_damage

		if self.hull <= 0:
			self.is_destroyed = True

	def isDestroyed(self):
		self.is_destroyed = self.hull <= 0
		return self.is_destroyed

	def __repr__(self):
		return f"<Starship name={self.name} faction={self.faction} hull={self.hull} shield={self.shield.shield_points if self.shield else 'None'} destroyed={self.is_destroyed}>"

# X-Wing starship subclass
class XWing(Starship):
	def __init__(self, name):
		super().__init__(name, "Rebel", 75, 5, 1, [XWingLaserCannon() for _ in range(4)], XWingShield())

# TIE Fighter starship subclass
class TIEFighter(Starship):
	def __init__(self, name):
		super().__init__(name, "Empire", 50, 7, 7, [TIEFighterLaserCannon() for _ in range(2)])

# Simulates a single combat round where only the attacking starships attack the defending starships
# NOTHING IS BALANCED FOR THIS, SHOULD MAKE A NEW PROEJCT BALANCED AROUND ATTACKING, DEFENDING
def simulateSingleCombatRoundOneSided(attacking_starships: List[Starship], defending_starships: List[Starship]):
	# Each attacking starship attacks a random defending starship
	for attacker in attacking_starships:
		if attacker.isDestroyed():
			continue
		alive_defenders = [s for s in defending_starships if not s.isDestroyed()]
		if not alive_defenders:
			break
		target = random.choice(alive_defenders)
		for weapon in attacker.weapons:
			if attacker.rollHit(target):
				target.takeDamage(weapon.roll_damage())

# Helper function to create multiple starships of a given class
def createXNumberOfStarships(starship_class, count, faction_prefix):
	return [starship_class(f"{faction_prefix} {i+1}") for i in range(count)]

# Works the same way as singleFullEngagement, but uses units and alternating combat rounds
def singleFullEngagementUnitCombat(unit1: Unit, unit2: Unit, verbose=False):
	rounds = 0
	if verbose:
		print("Starting unit combat...")
		print(f"Unit 1: {len([s for s in unit1.starships if not s.isDestroyed()])} ships remaining")
		print(f"Unit 2: {len([s for s in unit2.starships if not s.isDestroyed()])} ships remaining")

	# Continue combat rounds until one unit is completely destroyed or no ships remain
	while any(not s.isDestroyed() for s in unit1.starships) and any(not s.isDestroyed() for s in unit2.starships):
		if verbose:
			print(f"Starting round {rounds + 1}...")
			print(f"Unit 1: {len([s for s in unit1.starships if not s.isDestroyed()])} ships remaining")
			print(f"Unit 2: {len([s for s in unit2.starships if not s.isDestroyed()])} ships remaining")

		# Unit 1 attacks unit 2
		simulateSingleCombatRoundOneSided(unit1.starships, unit2.starships)

		# Unit 2 attacks unit 1
		simulateSingleCombatRoundOneSided(unit2.starships, unit1.starships)

		# Gather destroyed starships for this round
		destroyed_starships = [s for s in unit1.starships + unit2.starships if s.isDestroyed()]

		if verbose:
			print()
			print("Destroyed starships this round:")
			if destroyed_starships:
				for ship in destroyed_starships:
					print(f"{ship.name} ({ship.faction}) destroyed this round")
			else:
				print("No starships were destroyed this round.")
		if verbose:
			print(f"Unit 1: {len([s for s in unit1.starships if not s.isDestroyed()])} ships remaining")
			print(f"Unit 2: {len([s for s in unit2.starships if not s.isDestroyed()])} ships remaining")
			print()
		rounds += 1

	rebels_left = len([s for s in unit1.starships if not s.isDestroyed()])
	empire_left = len([s for s in unit2.starships if not s.isDestroyed()])

	if verbose:
		print(f"Total rounds: {rounds}")
		print(f"Unit 1: {len([s for s in unit1.starships if not s.isDestroyed()])} ships remaining")
		print(f"Unit 2: {len([s for s in unit2.starships if not s.isDestroyed()])} ships remaining")
		print()
		if verbose:
			print(f"Rebels left: {rebels_left}")
			print(f"Empire left: {empire_left}")
		print()
		if rebels_left > 0 and empire_left == 0:
			print("Rebels win!")
		elif empire_left > 0 and rebels_left == 0:
			print("Empire wins!")
		else:
			print("No clear winner.")

	# Return the results of the engagement as a dictionary
	return {
		"rounds": rounds,
		"rebels_left": rebels_left,
		"empire_left": empire_left
	}


# Monte Carlo simulation: runs the same unit battle many times and reports aggregate results
def monteCarloSimulation(unit1: Unit, unit2: Unit, runs: int):
	rebel_wins = 0
	empire_wins = 0
	draws = 0
	total_rounds = 0
	total_rebel_survivors = 0
	total_empire_survivors = 0

	if runs <= 0:
		print("No simulation runs requested.")
		return

	for _ in range(runs):
		# Each engagement needs fresh ships so damage does not carry between runs.
		rebel_unit = copy.deepcopy(unit1)
		empire_unit = copy.deepcopy(unit2)
		result = singleFullEngagementUnitCombat(rebel_unit, empire_unit)
		rebels_left = result["rebels_left"]
		empire_left = result["empire_left"]

		if rebels_left > 0:
			rebel_wins += 1
		elif empire_left > 0:
			empire_wins += 1
		else:
			draws += 1

		total_rounds += result["rounds"]
		total_rebel_survivors += rebels_left
		total_empire_survivors += empire_left

	print(f"Monte Carlo results over {runs} simulations:")
	print("-----------------------------------")
	print(f"Rebel wins:  {rebel_wins} ({rebel_wins / runs:.1%})")
	print(f"Empire wins: {empire_wins} ({empire_wins / runs:.1%})")
	print(f"Draws:       {draws} ({draws / runs:.1%})")
	print(f"Average rounds per battle: {total_rounds / runs:.2f}")
	print(f"Average Rebel survivors:   {total_rebel_survivors / runs:.2f}")
	print(f"Average Empire survivors:  {total_empire_survivors / runs:.2f}")

# Main function to run the combat simulation
def main():
	# Example usage of the combat simulation

	# Initialize the list of starships for the battle

	# Outside of the scope of this one, nothing is balanced for this

	
	rebel_squadron_red = Unit("Red", "Rebels")
	rebel_squadron_red.addStarships(createXNumberOfStarships(XWing, 12, "Red"))
	'''rebel_squadron_blue = Unit("Blue", "Rebels")
	rebel_squadron_blue.addStarships(createXNumberOfStarships(XWing, 12, "Blue"))
	rebel_squadron_green = Unit("Green", "Rebels")
	rebel_squadron_green.addStarships(createXNumberOfStarships(XWing, 12, "Green"))'''

	imperial_squadron_black = Unit("Black", "Empire")
	imperial_squadron_black.addStarships(createXNumberOfStarships(TIEFighter, 12, "Black"))
	'''imperial_squadron_grey = Unit("Grey", "Empire")
	imperial_squadron_grey.addStarships(createXNumberOfStarships(TIEFighter, 12, "Grey"))
	imperial_squadron_white = Unit("White", "Empire")
	imperial_squadron_white.addStarships(createXNumberOfStarships(TIEFighter, 12, "White"))'''

	# Run the Monte Carlo simulation for these units
	monteCarloSimulation(rebel_squadron_red, imperial_squadron_black, 1000)

	# Run a single full engagement with verbose output
	#singleFullEngagementUnitCombat(rebel_squadron_red, imperial_squadron_black, verbose=True)


if __name__ == "__main__":
	main()