# Knights vs Orcs Combat Simulator
# Author: Bobby Smith
# Date: 2026-1-30

# A Simulation of combat between Knights and Orcs using dice rolls for attacks and damage.
# It uses a basic set of Dungeons & Dragons style mechanics.

# It simulates many battles and provides statistics on win rates and average damage dealt.

# Objectives:
# 1. Implement unit classes for Knights and Orcs with attributes like health, strength, endurance, weapons, and armor.
# 2. Create functions to simulate attacks, defenses, and damage calculations using dice rolls.
# 3. Run multiple simulations of combat encounters and gather statistics on outcomes.
# 4. Output the results of the simulations, including win rates and average damage dealt.
# 5. Ensure the code is modular and well-documented for clarity.
# 6. Experiment with different unit attributes and combat mechanics to observe their effects on battle outcomes.
# 7. Optimize the rules to try to balance the combat between Knights and Orcs.

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
class sword(Weapon):
	def __init__(self):
		super().__init__(name="Sword", damage_die=6, number_of_die=1, damage_bonus=2)
class axe(Weapon):
	def __init__(self):
		super().__init__(name="Axe", damage_die=6, number_of_die=2, damage_bonus=0)
class mace(Weapon):
	def __init__(self):
		super().__init__(name="Mace", damage_die=4, number_of_die=2, damage_bonus=1)
class dagger(Weapon):
	def __init__(self):
		super().__init__(name="Dagger", damage_die=4, number_of_die=1, damage_bonus=0)
class club(Weapon):
	def __init__(self):
		super().__init__(name="Club", damage_die=8, number_of_die=1, damage_bonus=0)


# Armor class
class Armor:
	def __init__(self, name, defense_bonus):
		self.name = name
		self.defense_bonus = defense_bonus

# Specific armor classes
class leather_armor(Armor):
	def __init__(self):
		super().__init__(name="Leather Armor", defense_bonus=1)
class chainmail_armor(Armor):
	def __init__(self):
		super().__init__(name="Chainmail Armor", defense_bonus=2)
class plate_armor(Armor):
	def __init__(self):
		super().__init__(name="Plate Armor", defense_bonus=4)
class orc_armor(Armor):
	def __init__(self):
		super().__init__(name="Orc Armor", defense_bonus=2)

# Unit class
class Unit:
	def __init__(self, name, health, strength, endurance, weapon=None, armor=None):
		self.name = name
		self.health = health
		self.strength = strength
		self.endurance = endurance
		self.weapon = weapon
		self.armor = armor
				
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
	

	def rollDamage(self):
		if self.weapon:
			return self.weapon.roll_damage()
		return d4() + self.strength  # Default damage if no weapon
	

	
# Knight class
class Knight(Unit):
	def __init__(self):
		random_weapon = random.choice([sword(), mace()])
		random_armor = random.choice([chainmail_armor(), plate_armor()])
		super().__init__(name="Knight", health=100, strength=2, endurance=1, weapon=random_weapon, armor=random_armor)

# Orc class
class Orc(Unit):
	def __init__(self):
		random_weapon = random.choice([axe(), club(), dagger()])
		random_armor = orc_armor()
		super().__init__(name="Orc", health=119, strength=3, endurance=2, weapon=random_weapon, armor=random_armor)


# Attack calculator function, returns damage dealt
def attackCalculator(attacker: Unit, defender: Unit) -> int:
	# Check if either unit is dead or not valid
	if attacker.isAlive() == False or defender.isAlive() == False:
		return
	if attacker is None or defender is None:
		return
	
	# Roll attack and defense
	attack_roll = attacker.rollAttack()
	defense_roll = defender.rollDefense()

	# Check if attack hits
	if attack_roll <= defense_roll:
		return  # Attack missed
	
	# Calculate damage
	damage = attacker.rollDamage()
	
	# Apply damage to defender
	defender.health -= damage
	if defender.health < 0:
		defender.health = 0

	return damage

# Simulate one combat encounter
def simulate1Combat(unitA: Unit, unitB: Unit, winners: dict, damage_dealt: dict, print_debug: bool=False):
	# Create deep copies of units to avoid modifying originals
	units = [copy.deepcopy(unitA), copy.deepcopy(unitB)]

	turn_number = 1

	# Initialize damage_dealt keys if they don't exist
	if unitA.name not in damage_dealt:
		damage_dealt[unitA.name] = 0
	if unitB.name not in damage_dealt:
		damage_dealt[unitB.name] = 0

	# Battle loop
	while len(units) > 1:
		# Print Turn
		if print_debug:
			print(f"\n--- Turn {turn_number} ---")
		turn_number += 1

		# Print health status
		if print_debug:
			for unit in units:
				print(f"{unit.__class__.__name__} Health: {unit.health}")

		# Each unit attacks in turn
		for unit in units:
			# Calcualte attack for A 
			damage = attackCalculator(units[0], units[1])
			if damage:
				damage_dealt[units[0].name] += damage
			
			# Calcualte attack for B
			damage = attackCalculator(units[1], units[0])
			if damage:
				damage_dealt[units[1].name] += damage
		
		# Announce deaths
		if print_debug:
			for unit in units:
				if not unit.isAlive():
					print(f"{unit.__class__.__name__} has died.")

		# Cleanup dead units
		units = [unit for unit in units if unit.isAlive()]

	# Add winner to tally
	winners[units[0].name] = winners.get(units[0].name, 0) + 1

	# Return number of turns taken
	return turn_number - 1


# main function
def main():

	# Simulation parameters
	print_debug = False
	simulation_rounds = 10000

	# Statistics
	winners = {}
	average_turns = 0
	damage_dealt = {}

	# Simulate many combat encounters
	for i in range(simulation_rounds):
		# Create units
		knight = Knight()
		orc = Orc()

		# Simulate combat
		turns = simulate1Combat(knight, orc, winners, damage_dealt, print_debug)

		# Accumulate turns
		average_turns += turns

	# Calculate average turns
	average_turns /= simulation_rounds

	# Print results
	print("\n--- Battle Results ---")
	for winner, count in winners.items():
		print(f"{winner} won {count} times.")
	print(f"\nAverage turns per battle: {average_turns:.2f}")
	print("\n--- Damage Dealt ---")
	for unit_name, total_damage in damage_dealt.items():
		average_damage = total_damage / simulation_rounds
		print(f"{unit_name} dealt an average of {average_damage:.2f} damage per battle.")

	


if __name__ == "__main__":
	main()