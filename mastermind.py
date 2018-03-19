import random
from termcolor import colored




class Color:

	def __init__(self,name,style):
		self.name = name
		self.style = style

	def __repr__(self):
		return self.style + 'X' + '\x1b[0m'


class Board:

	def __init__(self):
		self.availableColors = set([Color('Red','\x1b[0;31;3m'),
			Color('Green','\x1b[0;32;3m'),
			Color('Yellow','\x1b[0;33;3m'),
			Color('Magenta','\x1b[0;35;3m'),
			Color('Grey','\x1b[0;38;3m'),
			Color('Blue','\x1b[0;34;3m'),
			Color('White','\x1b[0;37;3m'),
			Color('Cyan','\x1b[0;36;3m')])
		self.counterGuess = 0
		self.combinationLen = 5
		self.combination = [None]*self.combinationLen

	def create(self):	
		for i in range(self.combinationLen):
			self.combination[i] = random.sample(self.availableColors, 1)[0]
		print "Combination created: " + str(self.combination)

	def results(self,pins):
		self.counterGuess += 1
		print "guess N_" + str(self.counterGuess), pins
		rightPositions = 0
		counterColors = {}
		for pos, pin in enumerate(pins):
			counterColors[pin] = self.combination.count(pin)
			if pin == self.combination[pos]:
				rightPositions += 1
		rightColors = sum(counterColors.values())
		return {'pos':rightPositions,'col':rightColors}

		
class Solver:

	def __init__(self):
		self.rightColors = {}

	def solve(self,board):
		self._findColors(board)
		self._findCombination(board)

	def _findColors(self,board):
		for color in board.availableColors:
			pins = [color for i in range(board.combinationLen)]
			foundColors = board.results(pins)['col']
			if foundColors > 0:	
				self.rightColors[color] = foundColors
				if sum(self.rightColors.values()) == board.combinationLen:
					break
		print "Colors found are: " + str(self.rightColors)

	def _findCombination(self,board):
		for color in board.availableColors:
			if color not in self.rightColors:
				unfoundColor = color
				break
		rightPositions = [unfoundColor]*board.combinationLen
		index = 0
		while index < board.combinationLen:
			for color in self.rightColors.keys():
				rightPositions[index] = color
				if board.results(rightPositions)['pos'] > index :
					index += 1
					if self.rightColors[color] == 1:
						del self.rightColors[color]
					else:
						self.rightColors[color] -= 1
		print "Solution is: " + str(rightPositions)




board = Board()
board.create()
solver = Solver()
solver.solve(board)
