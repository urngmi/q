# 🎨 Import libraries we need for this quantum madness
from termcolor import colored, cprint  # Makes our terminal look pretty with colors 💅
import json  # For handling data that looks like JavaScript objects
from qiskit import *  # The main quantum computing library - this is where the magic happens ✨
from qiskit.tools.monitor import job_monitor  # Watches our quantum jobs like a hawk 👀

# 🔑 Your secret key to access IBM's actual quantum computers (keep this private bestie!)
TOKEN = "404713877cdee77e48a874066538a3cecab6e044ddbc06b7f25d4b2178a3b3c25151add0d8135bd8fed43867888555109239891a38555adeaef7f0342994b4fe"
IBMQ.save_account(TOKEN)  # Save this token so we can connect to real quantum computers later

def resetBoard():
  """
  🎮 Creates a fresh tic-tac-toe board - think of it as respawning after you die in a game
  
  Each position (1-9) has two things:
  - [0]: What symbol is there ('X', 'O', or ' ' for empty)
  - [1]: Whether it's quantum (1) or classical (0) - basically is it glitching or solid?
  
  Returns a dictionary where keys are positions '1' to '9'
  """
  return {'1': [' ', 0] , '2': [' ', 0], '3': [' ', 0],
          '4': [' ', 0], '5': [' ', 0], '6': [' ', 0],
          '7': [' ', 0], '8': [' ', 0], '9': [' ', 0]}

def printBoard(board):
  """
  🎨 Shows the tic-tac-toe board on screen with fancy colors
  
  The colors indicate what type of move each piece is:
  - No color = classical move (solid, not changing)
  - Red, green, blue, yellow = quantum moves (these are in superposition, kinda glitchy)
  
  Layout looks like:
   X | O | 
  -----------
   O | X | O
  -----------
     |   | X
  """
  print()
  colour = 0  # Keeps track of which color to use next for quantum pieces
  
  # Loop through all 9 positions (1-9)
  for i in range (1,10):
    if board[str(i)][1] == 0:  # If it's a classical move (solid)
      cprint(board[str(i)][0], end='')  # Print it normal (no color)
    else:  # If it's quantum (in superposition, needs to look different)
      # Cycle through different colors to show quantum weirdness
      if (colour == 0 or colour == 1):
        cprint(board[str(i)][0], 'red', end='')  # Print in red
        colour = colour + 1
      elif (colour == 2 or colour == 3):
        cprint(board[str(i)][0], 'green', end='')  # Print in green
        colour = colour + 1
      elif (colour == 4 or colour == 5):
        cprint(board[str(i)][0], 'blue', end='')  # Print in blue
        colour = colour + 1
      elif (colour == 6 or colour == 7):
        cprint(board[str(i)][0], 'yellow', end='')  # Print in yellow
        colour = colour + 1

    # Add the grid lines to make it look like tic-tac-toe
    if i % 3 == 0:  # End of each row
      print()  # New line
      if i != 9:   # Don't print line after the last row
        print('-+-+-')  # Horizontal line separator
    else:
      cprint('|', end='')  # Vertical line separator 

def make_classic_move(theBoard, turn, count, circuit):
  """
  🎯 Makes a regular tic-tac-toe move - just like the OG game your grandparents played
  
  This is the "boring" move where you just place your X or O in one spot and it stays there.
  No quantum weirdness, no superposition, just straight facts.
  
  Args:
    theBoard: The current game board
    turn: Whose turn it is ('X' or 'O')
    count: How many pieces are on the board
    circuit: The quantum circuit (we still need to track this even for classical moves)
  """
  
  valid_move = 0  # Flag to check if the move is legal
  valid_moves = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]  # Valid positions
  
  # Keep asking until they pick a valid spot
  while (not valid_move):
    print()
    print("Which location? (1-9) ", end='')
    location = input()

    if location in valid_moves:  # Check if they picked a number 1-9
        
      if theBoard[location][0] == ' ':  # Check if that spot is empty
        valid_move = 1  # We good, let's place the piece
        
        # Actually place the piece on the board
        theBoard[location][0] = turn  # Put X or O in that spot
        count += 1  # One more piece on the board
        theBoard[location][1] = 0  # Mark it as classical (not quantum)

        # 🔬 QUANTUM STUFF: Even for classical moves, we need to set the qubit
        # This sets the qubit for this position to |1⟩ (definitely ON)
        # The X gate flips a qubit from |0⟩ to |1⟩ - like flipping a switch
        circuit.x(int(location)-1)  # -1 because arrays start at 0 but our board starts at 1

        print(circuit.draw())  # Show what our quantum circuit looks like now
      else: 
        print()
        print("That place is already filled.")  # Bruh, someone already took that spot
    else:
      print("Please select a square from 1-9")  # Invalid input, try again

  return theBoard, turn, count, circuit

def make_quantum_move(theBoard, count, circuit, turn):
  """
  🌀 This is where things get WILD - quantum superposition move!
  
  Instead of placing your piece in ONE spot like a normal person, you place it in
  TWO spots at the same time! It's like Schrödinger's cat but for tic-tac-toe.
  Your piece exists in both spots until someone "collapses" the board (measures it).
  
  Think of it like your piece is having an identity crisis and can't decide where to be,
  so it just... exists in both places. Quantum mechanics is honestly unhinged.
  
  Args:
    theBoard: Current game state
    count: Number of pieces on board 
    circuit: The quantum circuit where the magic happens
    turn: Whose turn ('X' or 'O')
  """

  valid_move = False
  valid_moves = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

  while (not valid_move):
      
    print()
    print("Which location? (1-9) ")  # First spot for your quantum piece
    location1 = input()
    print("Which location? (1-9) ")  # Second spot for your quantum piece
    location2 = input()

    # Make sure both spots are empty and different (can't be in same spot twice bestie)
    if theBoard[location1][0] == ' ' and theBoard[location2][0] == ' ' and location1 != location2:
        
        # Place your symbol in BOTH spots (this is the quantum weirdness)
        theBoard[location1][0] = turn
        theBoard[location2][0] = turn
        
        count += 2  # We placed 2 pieces (sort of?)
        
        # Mark both as quantum (they'll flash/be colored to show they're in superposition)
        theBoard[location1][1] = 1  # quantum (glitchy vibes)
        theBoard[location2][1] = 1  # quantum (glitchy vibes)

        # 🔬 QUANTUM CIRCUIT MAGIC - This is where the real science happens:
        
        # Step 1: Put the first qubit in superposition with Hadamard gate
        # This makes it 50% |0⟩ and 50% |1⟩ - like a coin that's spinning in the air
        circuit.h(int(location1)-1)

        # Step 2: Flip the second qubit with X gate (sets it to |1⟩)
        circuit.x(int(location2)-1)

        # Step 3: Entangle them with CNOT gate - this is the mind-bending part!
        # Now these qubits are cosmically connected. If one changes, the other does too.
        # Einstein called this "spooky action at a distance" and honestly, same energy
        circuit.cx(int(location1)-1,int(location2)-1)

        print(circuit.draw())  # Show the quantum circuit - it's like art but sciencey
        valid_move = True
    else:
        print()
        print("You have selected an invalid position/s")  # Try again bestie
    

  return theBoard, count, circuit, turn

def measure(circuit, theBoard, count):
  """
  🎲 THE BIG MOMENT - Time to collapse the quantum superposition!
  
  This is like opening Schrödinger's box to see if the cat is alive or dead.
  All those quantum pieces that were chilling in multiple places at once?
  Now they have to pick ONE spot and stick with it.
  
  We're literally asking a REAL quantum computer to make these decisions.
  Not your laptop - an actual quantum computer at IBM that costs millions of dollars.
  We're basically rolling cosmic dice here.
  
  Args:
    circuit: Our quantum circuit with all the quantum weirdness
    theBoard: Current game board with quantum pieces
    count: Number of pieces on board
  """
  
  # Show the current board before the chaos
  printBoard(theBoard)
  print()
  print("Trigger collapse.")  # *dramatic music intensifies*
  print()

  # 🔗 Connect to IBM's actual quantum computer (not a simulation!)
  IBMQ.load_account()  # Use our saved account
  provider = IBMQ.get_provider(hub = 'ibm-q')  # Get access to IBM's quantum computers
  qcomp = provider.get_backend('ibmq_16_melbourne')  # Pick a specific quantum computer

  # 📏 Add measurement to all 9 qubits
  # This is like asking "what's the final state of each position?"
  # Each measurement forces the qubit to "choose" either 0 or 1
  circuit.measure(0,0)  # Measure qubit 0, store result in classical bit 0
  circuit.measure(1,1)  # Measure qubit 1, store result in classical bit 1
  circuit.measure(2,2)  # And so on for all 9 positions...
  circuit.measure(3,3)
  circuit.measure(4,4)
  circuit.measure(5,5)
  circuit.measure(6,6)
  circuit.measure(7,7)
  circuit.measure(8,8)

  print(circuit.draw())  # Show the final circuit with measurements

  # 🚀 Send our circuit to the REAL quantum computer and wait for results
  # shots=1 means we only run this once (one measurement)
  job = qiskit.execute(circuit, backend=qcomp, shots=1)

  job_monitor(job)  # Watch the job progress like watching a loading bar

  # 📊 Get the results from the quantum computer
  result = job.result()
  
  # Convert the quantum results into something we can understand
  out = json.dumps(result.get_counts())  # Get the measurement results
  string = out[2:11]  # Extract just the 9-bit string (removes extra JSON stuff)
  
  # 🎯 Update the board based on quantum measurement results
  # Each bit in the string tells us if that position should have a piece (1) or be empty (0)
  for i in range(9):
      if string[i] == '1':
          # This position survives the collapse - make it solid (classical)
          theBoard[str(9-i)][1] = 0  # Not quantum anymore
      else:
          # This position gets yeeted - remove the piece
          theBoard[str(9-i)][1] = 0  # Not quantum anymore  
          theBoard[str(9-i)][0] = ' '  # Remove the symbol

  # 🧮 Recount how many pieces are actually on the board now
  count = 0
  for i in range(9):
      theBoard[str(i+1)][1] = 0  # Make sure everything is classical now
      if theBoard[str(i+1)][0] != ' ':
          count += 1  # Count non-empty spots

  # 🔄 Reset all qubits back to |0⟩ state for future moves
  circuit.reset(0)
  circuit.reset(1)
  circuit.reset(2)
  circuit.reset(3)
  circuit.reset(4)
  circuit.reset(5)
  circuit.reset(6)
  circuit.reset(7)
  circuit.reset(8)

  # 🔧 Set up the circuit to match the new board state
  # For each position that has a piece, set its qubit to |1⟩
  for i in range(9):
      if string[8-i] == '1':  # If this position has a piece
          circuit.x(i)  # Set the corresponding qubit to |1⟩

  return circuit, string, theBoard, count

def check_win(theBoard, turn):
  if theBoard['7'][0] == theBoard['8'][0] == theBoard['9'][0] != ' ': # across the top
      if theBoard['7'][1] == theBoard['8'][1] == theBoard['9'][1] == 0: # only cemented markers
          printBoard(theBoard)
          print("\nGame Over.\n")                
          print(" **** ", end='')
          print(theBoard['8'][0], end='')
          print(" won ****")
          print() 
          return True

  elif theBoard['4'][0] == theBoard['5'][0] == theBoard['6'][0] != ' ': # across the middle
      if theBoard['4'][1] == theBoard['5'][1] == theBoard['6'][1] == 0: # only cemented markers
          printBoard(theBoard)
          print("\nGame Over.\n")                
          print(" **** ", end='')
          print(theBoard['5'][0], end='')
          print(" won ****")
          print()
          return True

  elif theBoard['1'][0] == theBoard['2'][0] == theBoard['3'][0] != ' ': # across the bottom
      if theBoard['1'][1] == theBoard['2'][1] == theBoard['3'][1] == 0: # only cemented markers
          printBoard(theBoard)
          print("\nGame Over.\n")                
          print(" **** ", end='')
          print(theBoard['2'][0], end='')
          print(" won ****")
          print()
          return True

  elif theBoard['1'][0] == theBoard['4'][0] == theBoard['7'][0] != ' ': # down the left side
      if theBoard['1'][1] == theBoard['4'][1] == theBoard['7'][1] == 0: # only cemented markers
          printBoard(theBoard)
          print("\nGame Over.\n")                
          print(" **** ", end='')
          print(theBoard['4'][0], end='')
          print(" won ****")
          print()
          return True

  elif theBoard['2'][0] == theBoard['5'][0] == theBoard['8'][0] != ' ': # down the middle
      if theBoard['2'][1] == theBoard['5'][1] == theBoard['8'][1] == 0: # only cemented markers
          printBoard(theBoard)
          print("\nGame Over.\n")                
          print(" **** ", end='')
          print(theBoard['5'][0], end='')
          print(" won ****")
          print()
          return True

  elif theBoard['3'][0] == theBoard['6'][0] == theBoard['9'][0] != ' ': # down the right side
      if theBoard['3'][1] == theBoard['6'][1] == theBoard['9'][1] == 0: # only cemented markers
          printBoard(theBoard)
          print("\nGame Over.\n")                
          print(" **** ", end='')
          print(theBoard['6'][0], end='')
          print(" won ****")
          print()
          return True

  elif theBoard['7'][0] == theBoard['5'][0] == theBoard['3'][0] != ' ': # diagonal
      if theBoard['7'][1] == theBoard['5'][1] == theBoard['3'][1] == 0: # only cemented markers
          printBoard(theBoard)
          print("\nGame Over.\n")                
          print(" **** ", end='')
          print(theBoard['5'][0], end='')
          print(" won ****")
          print()
          return True

  elif theBoard['1'][0] == theBoard['5'][0] == theBoard['9'][0] != ' ': # diagonal
      if theBoard['1'][1] == theBoard['5'][1] == theBoard['9'][1] == 0: # only cemented markers
          printBoard(theBoard)
          print("\nGame Over.\n")                
          print(" **** ", end='')
          print(theBoard['5'][0], end='')
          print(" won ****")
          print()
          return True

#Implementation of Two Player Tic-Tac-Toe game in Python.
# start game function
# Now we'll write the main function which has all the gameplay functionality.


def game():

    turn = 'X'
    count = 0
    win = False
    x_collapse = 1
    y_collapse = 1

    # initialise quantum circuit with 9 qubits (all on OFF = 0)
    circuit = qiskit.QuantumCircuit(9, 9)

    while (not win):

        # ============================= ROUND START ============================ 
        global theBoard
        printBoard(theBoard)

        print()
        print("It's your turn " + turn + ". Do you want to make a (1) classical move, (2) quantum move, (3) collapse?, or (4) quit?")

        move = input()

        # ============================= CLASSIC MOVE ===========================

        if int(move) == 1:
            theBoard, turn, count, circuit = make_classic_move(theBoard, turn, count, circuit)
            madeMove = True

        # ============================= QUANTUM MOVE ===========================

        elif int(move) == 2 and count > 8:
          # cant do a quantum move if there's only 1 empty square left
          print()
          print("There aren't enough empty spaces for that!")

        elif int(move) == 2 and count < 8:
          theBoard, count, circuit, turn = make_quantum_move(theBoard, count, circuit, turn)
          madeMove = True
        
        # ============================= COLLAPSE/MEASURE =======================

        elif int(move) == 3:

          if (turn == 'X' and x_collapse== 1 ):
            circuit, string, theBoard, count = measure(circuit, theBoard, count)
            x_collapse = 0
          elif (turn == 'O' and y_collapse == 1):
            circuit, string, theBoard, count = measure(circuit, theBoard, count)
            y_collapse = 0
          else:
            print("You have already used your collapse this game!")

        # ============================= QUIT ===================================

        elif int(move) == 4:
            break
        
        # ============================= CHECK FOR WIN ==========================

        # Now we will check if player X or O has won,for every move  
        if count >= 5:
          win = check_win(theBoard, turn)
          if (win):
            break



        # If neither X nor O wins and the board is full, we'll declare the result as 'tie'.
        if count == 9:
          circuit, string, theBoard, count = measure(circuit, theBoard, count)
          win = check_win(theBoard, turn)
          if count == 9:
            print("\nGame Over.\n")                
            print("It's a Tie !")
            print()
            win = True
          


        # Now we have to change the player after every move.
        if  (madeMove):  
          madeMove = False
          if turn =='X':
              turn = 'O'
          else:
              turn = 'X'        
    

    # Now we will ask if player wants to restart the game or not.
    restart = input("Play Again?(y/n) ")
    if restart == "y" or restart == "Y":

        theBoard = resetBoard()
        game()

def start_menu():
    start_menu = """
    Start Menu:

    1. Start Game
    2. How to Play
    3. Quit
    """ 
    
    print("""
    ###########################
    ### Quantum Tic-Tac-Toe ###
    ###########################
    """)
    print(start_menu)
    choice = 0
    while (choice != '1'):
      print("What would you like to do? ", end='')
      choice = input()

      if (choice == '2'):
        How_To = """ 
        In Quantum Tic-Tac-Toe, each square starts empty and your goal is to create a line of three of your naughts/crosses. 
        Playing a classical move will result in setting a square permanently as your piece.
        Playing a quantum move will create a superposition between two squares of your choosing. You may only complete a quantum move in two empty squares.
        The board will collapse when the board is full. At collapse, each superposition is viewed and only 1 piece of the superposition will remain. 
        *Powerup* Each player can decide to collapse the board prematurely, they may do this once per round each.
        """
        print(How_To)

      if (choice == '3'):
        print("Goodbye")
        break
      
    return choice

#Reset the board at start
theBoard = resetBoard()

#Set no moves made yet
if (start_menu() == '1'):  
  madeMove = False
  game()