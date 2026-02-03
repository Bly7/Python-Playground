# Knights vs Orcs Combat Simulator - Version 2
# Author: Bobby Smith
# Date: 2026-2-3

# A Simulation of combat between Knights and Orcs using dice rolls for attacks and damage.
# It uses a basic set of Dungeons & Dragons style mechanics.

# It simulates many battles and provides statistics on win rates and average damage dealt.

# This is an enhanced version of the original Knights vs Orcs simulator with additional features.

# Objectives:
# 1. Add a Dexterity attribute that allows for initiative rolls to determine attack order.
# 2. Initiative Rolls
# 3. Turn Order based on Initiative Rolls
# 4. Simulate Combat with more than two units (e.g., small skirmishes)
# 5. Team numbers and team-based combat
# 6. Target Selection
# 7. Simulation round update in console
# 8. Add more unit types (e.g., Goblins)

# Includes
import random
import copy



# D4 roll function
def d4():
	return random.randint(1, 4)

# D6 roll function
def d6():
	return random.randint(1, 6)

# D8 roll function
def d8():
	return random.randint(1, 8)

# D20 roll function
def d20():
	return random.randint(1, 20)

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
			if self.damage_die == 4:
				total_damage += d4()
			elif self.damage_die == 6:
				total_damage += d6()
			elif self.damage_die == 8:
				total_damage += d8()
			elif self.damage_die == 20:
				total_damage += d20()
		total_damage += self.damage_bonus
		return total_damage

# Specific weapon classes
class Sword(Weapon):
	def __init__(self):
		super().__init__(name="Sword", damage_die=6, number_of_die=1, damage_bonus=2)
class Axe(Weapon):
	def __init__(self):
		super().__init__(name="Axe", damage_die=6, number_of_die=2, damage_bonus=0)
class Mace(Weapon):
	def __init__(self):
		super().__init__(name="Mace", damage_die=4, number_of_die=2, damage_bonus=1)
class Dagger(Weapon):
	def __init__(self):
		super().__init__(name="Dagger", damage_die=4, number_of_die=1, damage_bonus=0)
class Club(Weapon):
	def __init__(self):
		super().__init__(name="Club", damage_die=8, number_of_die=1, damage_bonus=0)


# Armor class
class Armor:
	def __init__(self, name, defense_bonus):
		self.name = name
		self.defense_bonus = defense_bonus

# Specific armor classes
class LeatherArmor(Armor):
	def __init__(self):
		super().__init__(name="Leather Armor", defense_bonus=1)
class ChainmailArmor(Armor):
	def __init__(self):
		super().__init__(name="Chainmail Armor", defense_bonus=2)
class PlateArmor(Armor):
	def __init__(self):
		super().__init__(name="Plate Armor", defense_bonus=4)
class OrcArmor(Armor):
	def __init__(self):
		super().__init__(name="Orc Armor", defense_bonus=1)

# Unit class
class Unit:
	def __init__(self, name, health, strength, dexterity, endurance, weapon=None, armor=None, team_number=None):
		self.name = name
		self.health = health
		self.strength = strength
		self.endurance = endurance
		self.dexterity = dexterity
		self.weapon = weapon
		self.armor = armor
		self.team_number = team_number  # For future team-based combat
				
	def isAlive(self):
		return self.health > 0
	
	def defenseBonus(self):
		if self.armor:
			return self.armor.defense_bonus
		return 0
	
	
	def rollAttack(self):
		return d20() + self.strength

	def rollDefense(self):
		return d20() + self.endurance + self.defenseBonus()
	
	def rollInitiative(self):
		return d20() + self.dexterity

	def rollDamage(self):
		if self.weapon:
			return self.weapon.roll_damage()
		return d4() + self.strength  # Default damage if no weapon
	

	
# Knight class
class Knight(Unit):
	def __init__(self, team_number=1):
		random_weapon = random.choice([Sword(), Mace()])
		random_armor = random.choice([ChainmailArmor(), PlateArmor()])
		super().__init__(name="Knight", health=40, strength=2, dexterity=2, endurance=1, weapon=random_weapon, armor=random_armor, team_number=team_number)

# Orc class
class Orc(Unit):
	def __init__(self, team_number=2):
		random_weapon = random.choice([Axe(), Club(), Dagger()])
		random_armor = OrcArmor()
		super().__init__(name="Orc", health=15, strength=2, dexterity=1, endurance=2, weapon=random_weapon, armor=random_armor, team_number=team_number)

# Goblin class
class Goblin(Unit):
	def __init__(self, team_number=2):
		random_weapon = Dagger()
		random_armor = LeatherArmor()
		super().__init__(name="Goblin", health=10, strength=1, dexterity=3, endurance=1, weapon=random_weapon, armor=random_armor, team_number=team_number)

def calculateTarget(attacker: Unit, units: list) -> Unit:
	# Filter out units that are on the same team and are dead
	possible_targets = [unit for unit in units if unit.team_number != attacker.team_number and unit.isAlive()]
	if not possible_targets:
		return None
	# Select a random target from possible targets
	return random.choice(possible_targets)

# Attack calculator function, returns damage dealt
def attackCalculator(attacker: Unit, defender: Unit) -> int:
	# Check if either unit is dead or not valid
	if attacker.isAlive() == False or defender.isAlive() == False:
		return 0
	if attacker is None or defender is None:
		return 0
	
	# Roll attack and defense
	attack_roll = attacker.rollAttack()
	defense_roll = defender.rollDefense()

	# Check if attack hits
	if attack_roll <= defense_roll:
		return 0  # Attack missed
	
	# Calculate damage
	damage = attacker.rollDamage()
	
	# Apply damage to defender
	defender.health -= damage
	if defender.health < 0:
		defender.health = 0

	return damage

# Simulate a single combat round, returns number of turns taken
def simulateCombatRound(units_in: list, winners: dict, damage_dealt: dict, print_debug: bool=False) -> int:
	# Create deep copies of units to avoid modifying originals
	units = [copy.deepcopy(unit) for unit in units_in]

	turn_number = 1

	# Initialize damage_dealt keys if they don't exist
	for unit in units:
		if unit.name not in damage_dealt:
			damage_dealt[unit.name] = 0

	# Battle loop, continue until only one team remains
	while len(set(unit.team_number for unit in units if unit.isAlive())) > 1:
		# Print Turn
		if print_debug:
			print(f"\n--- Turn {turn_number} ---")
		turn_number += 1

		# Print health status
		if print_debug:
			for unit in units:
				print(f"{unit.name} Health: {unit.health}")

		# Determine turn order based on initiative rolls
		initiative_order = []
		for unit in units:
			if unit.isAlive():
				initiative_roll = unit.rollInitiative()
				initiative_order.append((initiative_roll, unit))

		initiative_order.sort(key=lambda x: x[0], reverse=True)

		initiative_order = [unit for _, unit in initiative_order]

		# Each unit attacks in turn
		for attacker in initiative_order:
			# Skip if attacker is dead
			if not attacker.isAlive():
				continue

			# Select target	
			defender = calculateTarget(attacker, units)
			if defender is None:
				continue
			
			# Perform attack
			damage = attackCalculator(attacker, defender)
			if damage:
				damage_dealt[attacker.name] += damage

		# Announce deaths
		if print_debug:
			for unit in units:
				if not unit.isAlive():
					print(f"{unit.name} has died.")

		# Cleanup dead units
		units = [unit for unit in units if unit.isAlive()]

	# Add winner to tally
	winners[units[0].team_number] = winners.get(units[0].team_number, 0) + 1

	# Return number of turns taken
	return turn_number - 1

# main function
def main():

	# Simulation parameters
	print_debug = False
	simulation_rounds = 100000
	simulation_rounds_print_interval = 10000

	# Statistics
	winners = {}
	average_turns = 0
	damage_dealt = {}

	# Simulate many combat encounters
	for i in range(simulation_rounds):
		# Create units
		knight = Knight(team_number=1)
		orc = Orc(team_number=2)
		goblin1 = Goblin(team_number=2)
		goblin2 = Goblin(team_number=2)

		units = [knight, orc, goblin1, goblin2]

		# Simulate combat
		turns = simulateCombatRound(units, winners, damage_dealt, print_debug)

		# Accumulate turns
		average_turns += turns

		# Print progress
		if (i + 1) % simulation_rounds_print_interval == 0:
			print(f"Completed {i + 1} simulations...")

	# Calculate average turns
	average_turns /= simulation_rounds

	# Print results
	print("\n--- Battle Results ---")
	for winner, count in winners.items():
		print(f"Team {winner} won {count} times.")
	print(f"\nAverage turns per battle: {average_turns:.2f}")
	print("\n--- Damage Dealt ---")
	for unit_name, total_damage in damage_dealt.items():
		average_damage = total_damage / simulation_rounds
		print(f"{unit_name} dealt an average of {average_damage:.2f} damage per battle.")

	


if __name__ == "__main__":
	main()