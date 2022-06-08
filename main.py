# This will be the main file for the wordle game.


import pygame
import random
import time
import sys

# INIT
pygame.init()
pygame.display.set_caption('Wordle')


# Width and height
WIDTH, HEIGHT = 800, 800

# Colours
BG_COLOUR = (25,25,25)
GREY = (100,100,100)
DARK_GREY = (50, 50, 50)
ORANGE = (255,150,50) # Check these colours when u get a chance
GREEN = (90,222,120)
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (240,10,10)

# Square side length and distance between squares
SQUARE_LENGTH = WIDTH//8
PADDING = SQUARE_LENGTH//15
# FONT	
pygame.font.init()
FONT = pygame.font.SysFont(pygame.font.get_default_font(), 80) # for the letters in the game
screenFont = pygame.font.SysFont(pygame.font.get_default_font(), 50)  # for messages on the screen
scoreFont = pygame.font.SysFont(pygame.font.get_default_font(), 30)    # for the win/loss score counters

# Classes
class Board:

	def __init__(self, difficulty=5):
		self.solution = self.chooseWord()
		self.rows = difficulty
		self.cols = difficulty
		self.contains=[[0 for i in range(self.rows)] for j in range(self.cols)]
		self.gridColours = [[DARK_GREY]*self.cols]*self.rows

		self.current_row = 0
		self.current_col = 0
		self.invalidWordTimer = 0

		# When the game finishes, use these timer values to measure when to restart.
		self.finishTimer = 150
		self.currentTimer = 0

		# Assign True to these values when it happens.
		self.won = False
		self.lost = False

	def chooseWord(self): #DONE, works perfectly.
		word = str(random.choice(open("validWords.txt").read().split())).upper()
		print(word)
		return word

	def information(self, word): # Needs more nuanced information. example pupal may return Orange, grey, green, gray, gray, for a word with a single p in the centre.
		# Takes a word, compares it to the solution and returns info regarding the grey, orange and green letters.
		info = [GREY for i in range(self.cols)]
		guessed_letter_counts = {letter:0 for letter in set(word)}   #
		actual_letter_counts = {letter:self.solution.count(letter) for letter in set(self.solution)}
		for index, ch in enumerate(word):
			if self.solution[index]==ch:
				# increment the count for the letter, make that square green!
				guessed_letter_counts[ch] += 1
				info[index] = GREEN
		# So now all the greens are highlighted
		# Go through and highlight oranges iff
		# letter appears but not in thta position AND
		# Letter hasnt appeared enough times yet, (in guessed letter count)
		for index, ch in enumerate(word):
			if ch in self.solution and info[index]!=GREEN:
				# increment the count for the letter
				guessed_letter_counts[ch] += 1
				# if the letter has already appeared its number of times, make it grey!
				if guessed_letter_counts[ch]>actual_letter_counts[ch]: # appeared too many times?
					info[index] = GREY
				else: info[index] = ORANGE
		return info     # e.g. return [GREY, GREY, ORANGE, GREY, GREEN]

	def isWordValid(self, word): # Works perfectly
		with open("validWords.txt") as file:
			contents = file.read()
			return (word.lower() in contents)

	def submitWord(self): # works perfectly.
		word = self.contains[self.current_row]
		if 0 in word: return
		word = "".join(word)

		if self.isWordValid(word):
			#Update self.contains
			self.contains[self.current_row] = [str(i) for i in str(word)]
			# Update the grid colours
			self.gridColours[self.current_row] = self.information(word)
			# after word gets submitted
			self.current_row += 1
			self.current_col = 0
			# Test if we've put in the right word, or put too many words i.e. won or lost?
			if word==self.solution: self.won = True
			elif self.current_row>=self.rows: self.lost = True
		else:
			self.invalidWordTimer = 120


	def enterLetter(self, letter):  # DONE
		# if we arent on a full row then add the letter into self.contains and increment self.current_col, else do nothing.
		if self.current_col < self.cols: 
			self.contains[self.current_row][self.current_col] = str(letter).upper()
			self.current_col += 1

	def deleteLetter(self): #DONE
		# Find spot where last letter entered, delete it
		# IF we arent on an empty row, delete the last letter (turn it into a 0 in the storage)
		if self.current_col != 0:
			self.contains[self.current_row][self.current_col-1] = 0
			self.current_col -= 1 



	def drawBoard(self, win, losses, wins): # needs the grid overlayed on top.

		# draw background/empty board/grid first
		win.fill(BG_COLOUR)


		#iterate through self.contains
		# if letter, put letter in the next spot
		# Else just put a grey square
		# Every square must be a little bit away from every other square by PADDING amount
		for row in range(self.rows):
			for col in range(self.cols):
				# Add distance from top or left hand side of screen
				x = (WIDTH - self.cols*(SQUARE_LENGTH+PADDING))//2
				y = (HEIGHT - self.rows*(SQUARE_LENGTH+PADDING))//2 
				# Add distance due to the relevant square (col, row)
				x += col*SQUARE_LENGTH
				y += row*SQUARE_LENGTH
				# Add distance for padding
				x += col*PADDING
				y += row*PADDING
				if self.contains[row][col]!=0: 
					# draw the colour from self.gridColours[row][col
					pygame.draw.rect(win,self.gridColours[row][col],(x,y,SQUARE_LENGTH,SQUARE_LENGTH))
					# then draw the letter from self.contains[row][col]
					text = FONT.render(str(self.contains[row][col]), 1, WHITE)
					# centre text
					x += (SQUARE_LENGTH-text.get_width())//2
					y += (SQUARE_LENGTH-text.get_height())//2
					win.blit(text, (x,y))
				else: 
					pygame.draw.rect(win,self.gridColours[row][col],(x,y,SQUARE_LENGTH,SQUARE_LENGTH))

		# Draw the wins and losses counters/scores
		winText = scoreFont.render(f"Won: {wins}", 1, WHITE)
		lossesText = scoreFont.render(f"Lost: {losses}", 1, WHITE)
		win.blit(winText, (20,20))
		win.blit(lossesText, (20,20+winText.get_height()+5))


		# IF recent word was not valid, put this message up and decrement the invalidWordTimer.
		if self.invalidWordTimer>0:
			text_on_screen = screenFont.render("Invalid Word! Try Another!", 1, RED)
			win.blit(text_on_screen, ((WIDTH-text_on_screen.get_width())//2,50))
			self.invalidWordTimer -= 1

		# If we are at the end of a game (win or lose) we need to count frames so we know when to restart.
		if self.won:
			self.currentTimer += 1
			finishText = screenFont.render("Very nice, you got it!", 1, GREEN)
			win.blit(finishText, ((WIDTH-finishText.get_width())//2,50))
		if self.lost: 
			self.currentTimer += 1
			finishText = screenFont.render("Next time, king <3", 1, RED)
			win.blit(finishText, ((WIDTH-finishText.get_width())//2,50))
			# tell the user what the solution was so they dont die of frustration
			theActualSolution = screenFont.render(f"The solution was:  {self.solution}", 1, RED)
			win.blit(theActualSolution, ((WIDTH-theActualSolution.get_width())//2,HEIGHT - 100))

		pygame.display.update()

# Main Function Loop

def main(wins, losses):
	board = Board()
	clock = pygame.time.Clock()
	win = pygame.display.set_mode((WIDTH, HEIGHT))

	run = True

	while run:
		clock.tick(60)
		# Check events
		for event in pygame.event.get():
			if not (board.won or board.lost):
		        # If we click the red X, then quit the game
				if event.type==pygame.QUIT:
					pygame.quit() # Quit the game
					sys.exit()
				# Enter letter, press delete or press enter?
				elif event.type==pygame.KEYDOWN:
					if event.key == pygame.K_a:
						board.enterLetter("A")
					elif event.key == pygame.K_b:
						board.enterLetter("B")
					elif event.key == pygame.K_c:
						board.enterLetter("C")
					elif event.key == pygame.K_d:
						board.enterLetter("D")
					elif event.key == pygame.K_e:
						board.enterLetter("E")
					elif event.key == pygame.K_f:
						board.enterLetter("F")
					elif event.key == pygame.K_g:
						board.enterLetter("G")
					elif event.key == pygame.K_h:
						board.enterLetter("H")
					elif event.key == pygame.K_i:
						board.enterLetter("I")
					elif event.key == pygame.K_j:
						board.enterLetter("J")
					elif event.key == pygame.K_k:
						board.enterLetter("K")
					elif event.key == pygame.K_l:
						board.enterLetter("L")
					elif event.key == pygame.K_m:
						board.enterLetter("M")
					elif event.key == pygame.K_n:
						board.enterLetter("N")
					elif event.key == pygame.K_o:
						board.enterLetter("O")
					elif event.key == pygame.K_p:
						board.enterLetter("P")
					elif event.key == pygame.K_q:
						board.enterLetter("Q")
					elif event.key == pygame.K_r:
						board.enterLetter("R")
					elif event.key == pygame.K_s:
						board.enterLetter("S")
					elif event.key == pygame.K_t:
						board.enterLetter("T")
					elif event.key == pygame.K_u:
						board.enterLetter("U")
					elif event.key == pygame.K_v:
						board.enterLetter("V")
					elif event.key == pygame.K_w:
						board.enterLetter("W")
					elif event.key == pygame.K_x:
						board.enterLetter("X")
					elif event.key == pygame.K_y:
						board.enterLetter("Y")
					elif event.key == pygame.K_z:
						board.enterLetter("Z")
					# delete letter with backspace
					elif event.key == pygame.K_BACKSPACE: board.deleteLetter()
					# try to submit the word on this row with return
					elif event.key == pygame.K_RETURN: board.submitWord()


		board.drawBoard(win, losses, wins) # also increments finish timers, and decrements invalid word timer
		if board.currentTimer>board.finishTimer:
			if board.won == True: 
				wins += 1
			elif board.lost == True: 
				losses += 1
			# restart! call the main function again
			main(wins, losses)

	pygame.quit()


losses = 0
wins = 0
main(wins, losses)