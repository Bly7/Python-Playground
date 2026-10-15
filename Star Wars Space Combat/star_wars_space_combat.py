# Star Wars Space Combat Simulator - Version 1
# Author: Bobby Smith
# Date: 2026-10-14

# A Simulation of combat between X-Wings and TIE Fighters using dice rolls for attacks and damage.
# It is based on my Knights vs Orcs combat simulator.

# It simulates many battles and provides statistics on win rates and average damage dealt.

# This is the first version of the Star Wars Space Combat simulator.

# Objectives:
# 1. Add a basic starship classes with combat mechanics with shields and hull points.
# 2. Implement weapon classes for X-Wings and TIE Fighters.
# 3. Implement shield classes for starships.
# 4. Implement damage application to shields and hull.
# 5. Implement shield regeneration over time.
# 6. Track starship destruction status.
# 7. Simulate round by round combat between starships until one side is destroyed.

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
			if self.damage_die == 2:
				total_damage += d2()
			elif self.damage_die == 4:
				total_damage += d4()
			elif self.damage_die == 6:
				total_damage += d6()
			elif self.damage_die == 8:
				total_damage += d8()
			elif self.damage_die == 20:
				total_damage += d20()
		total_damage += self.damage_bonus
		return total_damage

# X-Wing laser cannon weapon class
class XWingLaserCannon(Weapon):
	def __init__(self):
		super().__init__("Laser Cannon (X-Wing)", 4, 1)

# TIE Fighter laser cannon weapon class
# Slightly higher fire speed per cannon, and slightly higher explosive power per shot
class TIEFighterLaserCannon(Weapon):
	def __init__(self):
		super().__init__("Laser Cannon (TIE Fighter)", 6, 1, 1) 

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
		super().__init__("X-Wing Shield", "Standard X-Wing shield", 3, 1)


# Class representing a starship in Star Wars space combat
class Starship:
	def __init__(self, name, faction, hull_points, speed, weapons, shield = None):
		self.name = name
		self.is_destroyed = False
		self.faction = faction
		self.hull = hull_points
		self.speed = speed
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
		super().__init__(name, "Rebel", 6, 5, [XWingLaserCannon() for _ in range(4)], XWingShield())

# TIE Fighter starship subclass
class TIEFighter(Starship):
	def __init__(self, name):
		super().__init__(name, "Empire", 5, 7, [TIEFighterLaserCannon() for _ in range(2)])

# A single full combat round simulation function, where all starships attack simultaneously based on speed order
def simulateSingleCombatRound(starships: List[Starship]):
	# Sort all starships by speed (+-2 random variation) in descending order
	sorted_starships = starships.copy()
	sorted_starships.sort(key=lambda s: s.speed + random.randint(-2, 2), reverse=True)

	# Create a list of destroyed starships
	destroyed_starships = []

	# Each ship gets assigned a target from the opposing faction, there can be overlapping targets
	targets = {}
	for ship in starships:
		opposing_faction_ships = [s for s in starships if s.faction != ship.faction and not s.isDestroyed()]
		if opposing_faction_ships:
			targets[ship] = random.choice(opposing_faction_ships)

	# Go through starship list and have each ship attack their target
	# if the target is already destroyed it skips this combat, this simulates two ships attacking simultaneously
	for ship in starships:
		if ship in targets and not ship.isDestroyed():
			target = targets[ship]
			if not target.isDestroyed():
				for weapon in ship.weapons:
					target.takeDamage(weapon.roll_damage())
				if target.isDestroyed():
					destroyed_starships.append(target)

	return destroyed_starships

# Helper function to create multiple starships of a given class
def createXNumberOfStarships(starship_class, count, faction_prefix):
	return [starship_class(f"{faction_prefix} {i+1}") for i in range(count)]

# Simulates a full engagement between two fleets of starships until one side is completely destroyed or no ships remain.
def singleFullEngagement(starships: List[Starship], verbose=False):
	fleet = copy.deepcopy(starships)
	rounds = 0

	# Continue combat rounds until one side is completely destroyed or no ships remain
	while any(not s.isDestroyed() for s in fleet if s.faction == "Rebel") and any(not s.isDestroyed() for s in fleet if s.faction == "Empire"):
		rounds += 1

		# Print the start of a new combat round if verbose is enabled
		if verbose:
			print("Starting a new combat round...")
			print(f"Round {rounds}")
			print("Starship status before the round:")
			for ship in fleet:
				if not ship.isDestroyed():
					shield_points = ship.shield.shield_points if ship.shield else "N/A"
					print(f"{ship.name} ({ship.faction}) - Hull: {ship.hull}, Shield: {shield_points}")

		# Simulate a single combat round and get the list of destroyed starships
		destroyed = simulateSingleCombatRound(fleet)

		# Print the status of the fleet after the combat round if verbose is enabled
		if verbose:
			print()
			print("Destroyed starships this round:")
			if destroyed:
				for ship in destroyed:
					print(f"{ship.name} ({ship.faction}) destroyed this round")
			else:
				print("No starships were destroyed this round.")
			units_remaining = sum(not ship.isDestroyed() for ship in fleet)
			print()
			print(f"Units remaining: {units_remaining}")

		# Apply end-of-round effects to all surviving starships
		for ship in fleet:
			if not ship.isDestroyed():
				ship.tick()

	# Count the number of surviving starships for each faction after the engagement ends
	rebels_left = len([s for s in fleet if s.faction == "Rebel" and not s.isDestroyed()])
	empire_left = len([s for s in fleet if s.faction == "Empire" and not s.isDestroyed()])

	# Determine the winner based on the number of surviving starships
	if verbose:
		print()
		print(f"Number of rounds: {rounds}")
		print()
		print("Final status of all starships:")
		print("-----------------------------------")
		for ship in fleet:
			if ship.isDestroyed():
				status = "Destroyed"
			else:
				shield_points = ship.shield.shield_points if ship.shield else "N/A"
				status = f"Hull: {ship.hull}, Shield: {shield_points}"
			print(f"{ship.name} ({ship.faction}) - {status}")

		print()
		print(f"{rebels_left} Rebels remaining")
		print(f"{empire_left} Empire remaining")
		if rebels_left:
			print("Rebels win!")
		elif empire_left:
			print("Empire wins!")
		else:
			print("All starships destroyed. It's a draw!")

	# Return the results of the engagement as a dictionary
	return {
		"rounds": rounds,
		"rebels_left": rebels_left,
		"empire_left": empire_left
	}

# Monte Carlo simulation: runs the same battle as main() many times (silently) and reports aggregate results
# The given starships are used as a template; each run uses a fresh deep copy so damage never carries over
def monteCarloSimulation(starships: List[Starship], runs: int):
	rebel_wins = 0
	empire_wins = 0
	draws = 0
	total_rounds = 0
	total_rebel_survivors = 0
	total_empire_survivors = 0

	for _ in range(runs):
		fleet = copy.deepcopy(starships)
		rounds = 0

		# Run a single full engagement for this fleet
		result = singleFullEngagement(fleet)

		rounds = result["rounds"]
		rebels_left = result["rebels_left"]
		empire_left = result["empire_left"]

		if rebels_left > 0:
			rebel_wins += 1
		elif empire_left > 0:
			empire_wins += 1
		else:
			draws += 1

		total_rounds += rounds
		total_rebel_survivors += rebels_left
		total_empire_survivors += empire_left

	if runs <= 0:
		print("No simulation runs requested.")
		return

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
	starships = []
	starships.extend(createXNumberOfStarships(XWing, 12, "Red"))
	starships.extend(createXNumberOfStarships(TIEFighter, 12, "TIE"))

	# Run a single full engagement with verbose output
	singleFullEngagement(copy.deepcopy(starships), verbose=True)

	# Run the Monte Carlo simulation for the given starships
	monteCarloSimulation(starships, 1000)



if __name__ == "__main__":
	main()