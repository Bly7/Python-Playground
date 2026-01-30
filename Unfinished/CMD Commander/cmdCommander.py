from termcolor import colored
from perlin_noise import PerlinNoise
import os

class Vector:
	def __init__(self):
		self.x = 0.0
		self.y = 0.0
		self.z = 0.0
	
	def __init__(self, x, y, z = 0.0):
		self.x = float(x)
		self.y = float(y)
		self.z = float(z)

	def __str__(self):
		out = ""
		out += "(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")"
		return out

	def __mul__(self, other):
		if type(other) in [float, int, complex]:
			return Vector(self.x * other, self.y * other, self.z * other)
	
	def __rmul__(self, other):
		if type(other) in [float, int, complex]:
			return Vector(self.x * other, self.y * other, self.z * other)

class Tile:
	def __init__(self):
		self.position = Vector()
		self.symbol = " "
	
	def __init__(self, x, y, height = 0):
		self.position = Vector(x, y, height)
		self.symbol = " "
	
	def __str__(self):
		out = "["
		out += "P:" + str(self.position)
		out += "]"
		return out
	
	def strDebug(self):
		out = "["
		out += "P:" + str(self.position)
		out += "]"
		return out

	def strSymbol(self):
		out = "["
		out += str(self.symbol)
		out += "]"
		return out


worldScale = 100.0

class Map:
	def __init__(self, cols, rows):
		self.cols = cols
		self.rows = rows
		self.Tiles = []
		for x in range(cols):
			col = []
			for y in range(rows):
				col.append(Tile(x,y))
			self.Tiles.append(col)
		
		noise = PerlinNoise(octaves=5, seed=100)
		for y in range(rows):
			for x in range(cols):
				nval = abs(noise([1/(x+1),1/(y+1)]))*5
				if nval >= 0.75:
					self.GetTileAt(x,y).symbol = "T"
	
	def GetTileAt(self, x, y):
		if ((0 <= x <= self.cols) and (0 <= y <= self.rows)):
			return self.Tiles[y][x]

	def PrintDebug(self):
		out = ""
		for x in range(self.cols):          
			for y in range(self.rows):
				out += str(self.GetTileAt(x,y).strDebug())
			out += "\n"
		print(out)
	
	def Print(self):
		out = ""
		out += "   A  B  C  D  E  F  G  H  I  J \n"
		for y in range(self.rows):
			out += str(y) + " "
			for x in range(self.cols):
				out += str(self.GetTileAt(x,y).strSymbol())
			out += "\n"
		print(out)

class Unit:
	def __init__(self, position=Vector(0,0), men=10, name="U", team=0):
		self.position = position
		self.men = men
		self.name = name
		self.team = team
		self.order = Vector(0,0,0)
		self.moveSpeed = 1.0
	
	def __str__(self):
		out = ""
		out += self.name + " - "
		out += "Pos: " + chr(int(self.position.x/worldScale) + 65) + str(int(self.position.y/worldScale))
		out += ", Men: " + str(self.men)
		return out

	def PrintStatus(self):
		out = str(self)
		print(out)

def unitName(unit):
	return unit.name

def clearScreen():
	os.system('cls' if os.name=='nt' else 'clear')

gmap = Map(10,10)
#gmap.PrintDebug()


#print(colored('hello','red'))

units = [Unit(name="A"), Unit(position=(Vector(6,4) * worldScale),team=0,name="C"), Unit(position=Vector(3,3) * worldScale,name="B")]
units.sort(key=unitName)

playing = True

while (playing):
	print("----------------------------------")
	print("             Options")
	print("----------------------------------")
	print("(a) View Map\n(u) Show Unit Info\n(o) Give Unit Order\n(e) Exit Game")

	command = input()

	if (command == "a"):
		print("----------------------------------")
		print("                Map")
		print("----------------------------------")

		gmap.Print()

	if (command == "u"):	
		print("----------------------------------")
		print("              Units")
		print("----------------------------------")

		uIndex = 1
		for u in units:
			if u.team == 0:
				print(str(uIndex) + ". " + str(u))
				uIndex += 1
		print("")
	
	if (command == "o"):
		print("----------------------------------")
		print("            Give Order")
		print("----------------------------------")

		selectedUnit = None

		orderUnitIn = input("Unit: ").lower()
		orderLocationIn = input("Location: ").lower()

		for u in units:
			if u.name.lower() == orderUnitIn:
				selectedUnit = u
				break
		
		if selectedUnit == None:
			print("Cannot find unit with this name.")

		if len(orderLocationIn) == 2:
			xIn = int(ord(orderLocationIn[0])) - 97
			yIn = int(orderLocationIn[1])
			
			if (0 <= xIn <= 10) and (0 <= yIn <= 10) and selectedUnit:
				selectedUnit.order = Vector(xIn, yIn, 0)
			else:
				print("Invalid order location.")

		else:
			print("Invalid order location.")


	if (command == "e"):
		playing = False

	if playing:
		print("Press enter to continue...")
		command = input()
		#clearScreen()

