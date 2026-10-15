from enum import Enum, auto

class Weapon:
	def __init__(self, name, range, fire_points):
		self.name = name
		self.range = range
		self.fire_points = fire_points
	
	def getFirePointsAtDistance(self, distance):
		if distance <= self.range:
			return self.fire_points
		return 0  # Out of range

class Pistol(Weapon):
	def __init__(self, name="Pistol", range=8, fire_points=1):
		super().__init__(name, range, fire_points)
class Revolver(Weapon):
	def __init__(self, name="Revolver", range=8, fire_points=1):
		super().__init__(name, range, fire_points)
class InfantryRifle(Weapon):
	def __init__(self, name="Infantry Rifle", range=24, fire_points=1):
		super().__init__(name, range, fire_points)
class SniperRifle(Weapon):
	def __init__(self, name="Sniper Rifle", range=32, fire_points=2):
		super().__init__(name, range, fire_points)
class SubmachineGun(Weapon):
	def __init__(self, name="Submachine Gun", range=16, fire_points=3):
		super().__init__(name, range, fire_points)
class LightMachineGun(Weapon):
	def __init__(self, name="Light Machine Gun", range=32, fire_points=3):
		super().__init__(name, range, fire_points)
class CombatShotgun(Weapon):
	def __init__(self, name="Combat Shotgun", range=8, fire_points=3):
		super().__init__(name, range, fire_points)
class GrenadeLauncher(Weapon):
	def __init__(self, name="Grenade Launcher", range=16, fire_points=3):
		super().__init__(name, range, fire_points)
class AssaultRifle(Weapon):
	def __init__(self, name="Assault Rifle", range=24, fire_points=1):
		super().__init__(name, range, fire_points)
	
	def getFirePointsAtDistance(self, distance):
		if distance > self.range:
			return 0  # Out of range
		elif distance < self.range / 2:
			return self.fire_points * 2  # Close range bonus
		else:
			return self.fire_points  # Standard range

class Armor:
	def __init__(self, name, save):
		self.name = name
		self.save = save

class LightArmor(Armor):
	def __init__(self, name="Light Armor", save=6):
		super().__init__(name, save)
class MediumArmor(Armor):
	def __init__(self, name="Medium Armor", save=5):
		super().__init__(name, save)
class HeavyArmor(Armor):
	def __init__(self, name="Heavy Armor", save=4):
		super().__init__(name, save)
class PowerArmor(Armor):
	def __init__(self, name="Power Armor", save=3):
		super().__init__(name, save)
class BattlesuitArmor(Armor):
	def __init__(self, name="Battle Suit", save=2):
		super().__init__(name, save)

class Soldier:
	def __init__(self, name, weapon, armor):
		self.name = name
		self.weapon = weapon
		self.armor = armor

class WW2Officer(Soldier):
	def __init__(self, name="Officer", weapon=Pistol(), armor=None):
		super().__init__(name, weapon, armor)
class WW2Rifleman(Soldier):
	def __init__(self, name="Rifleman", weapon=InfantryRifle(), armor=None):
		super().__init__(name, weapon, armor)
class WW2SubmachineGunner(Soldier):
	def __init__(self, name="Submachine Gunner", weapon=SubmachineGun(), armor=None):
		super().__init__(name, weapon, armor)
class WW2Sniper(Soldier):
	def __init__(self, name="Sniper", weapon=SniperRifle(), armor=None):
		super().__init__(name, weapon, armor)
class WW2MachineGunner(Soldier):
	def __init__(self, name="Machine Gunner", weapon=LightMachineGun(), armor=None):
		super().__init__(name, weapon, armor)



class ExperienceLevel:
	def __init__(self, name, activation, expertise, suppress):
		self.name = name
		self.activation = activation
		self.expertise = expertise
		self.suppress = suppress

class Green(ExperienceLevel):
	def __init__(self, name="Green", activation=5, expertise=6, suppress=1):
		super().__init__(name, activation, expertise, suppress)
class Seasoned(ExperienceLevel):
	def __init__(self, name="Seasoned", activation=4, expertise=5, suppress=2):
		super().__init__(name, activation, expertise, suppress)
class Veteran(ExperienceLevel):
	def __init__(self, name="Veteran", activation=3, expertise=4, suppress=3):
		super().__init__(name, activation, expertise, suppress)
class Elite(ExperienceLevel):
	def __init__(self, name="Elite", activation=2, expertise=4, suppress=4):
		super().__init__(name, activation, expertise, suppress)

class Unit:
	def __init__(self, name, soldiers, experience=Green()):
		self.name = name
		self.soldiers = soldiers
		self.experience = experience

class USRifleSquad(Unit):
	def __init__(self, name="US Rifle Squad", soldiers=None, experience=Green()):
		# add rifleman and an mg to the squad
		if soldiers is None:
			soldiers = [WW2Rifleman() for _ in range(11)]
			soldiers.append(WW2MachineGunner())  # Add a machine gunner to the squad

		super().__init__(name, soldiers, experience)
class GermanRifleSquad(Unit):
	def __init__(self, name="German Rifle Squad", soldiers=None, experience=Green()):
		# add rifleman and an mg to the squad
		if soldiers is None:
			soldiers = [WW2Rifleman() for _ in range(6)]
			soldiers.append(WW2MachineGunner())  # Add a machine gunner to the squad
			soldiers.append(WW2SubmachineGunner())  # Add a submachine gunner to the squad
			soldiers.append(WW2SubmachineGunner())  # Add a submachine gunner to the squad

		super().__init__(name, soldiers, experience)


def simulate_combat(attacker, defender, distance):
	attacker_fire_points = sum(soldier.weapon.getFirePointsAtDistance(distance) for soldier in attacker.soldiers)
	defender_save = min(soldier.armor.save for soldier in defender.soldiers if soldier.armor) if any(soldier.armor for soldier in defender.soldiers) else 6

	print(f"{attacker.name} has {attacker_fire_points} fire points at distance {distance}.")
	print(f"{defender.name} has a save of {defender_save}.")

# main function
def main():
	# Create some units
	us_squad = USRifleSquad()
	german_squad = GermanRifleSquad()

	# Print out the squads
	print(f"{us_squad.name} has {len(us_squad.soldiers)} soldiers.")
	print(f"{german_squad.name} has {len(german_squad.soldiers)} soldiers.")

if __name__ == "__main__":
	main()