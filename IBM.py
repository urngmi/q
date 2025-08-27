# 🎨 Import libraries we need for this quantum madness
from termcolor import colored, cprint  # Makes our terminal look pretty with colors 💅
import json  # For handling data that looks like JavaScript objects
from qiskit import *  # The main quantum computing library - this is where the magic happens ✨
import time  # For simple job monitoring since qiskit.tools.monitor is deprecated

# 🔧 Try to import IBM provider with fallback handling
try:
    from qiskit_ibm_provider import IBMProvider
    IBM_PROVIDER_AVAILABLE = True
    print("✅ IBM Provider loaded successfully!")
except ImportError as e:
    print(f"⚠️ IBM Provider not available: {e}")
    print("🔄 Game will use local simulation only")
    IBM_PROVIDER_AVAILABLE = False

# 🔧 Simple job monitor function (since the old one is deprecated)
def job_monitor(job):
    """
    🕐 Simple job monitoring function - watches our quantum job progress
    
    This replaces the deprecated qiskit.tools.monitor.job_monitor function.
    It just waits for the job to complete and shows some progress dots.
    """
    print("⏳ Waiting for quantum job to complete", end="")
    while job.status().name not in ['DONE', 'CANCELLED', 'ERROR']:
        print(".", end="", flush=True)
        time.sleep(1)
    
    status = job.status().name
    if status == 'DONE':
        print("\n✅ Quantum job completed successfully!")
    elif status == 'CANCELLED':
        print("\n❌ Quantum job was cancelled!")
    else:
        print(f"\n⚠️ Quantum job finished with status: {status}")

# 🔑 Your secret key to access IBM's actual quantum computers (keep this private bestie!)
TOKEN = "404713877cdee77e48a874066538a3cecab6e044ddbc06b7f25d4b2178a3b3c25151add0d8135bd8fed43867888555109239891a38555adeaef7f0342994b4fe"

# 💾 Save the IBM account token for later use (only if provider is available)
if IBM_PROVIDER_AVAILABLE:
    try:
        IBMProvider.save_account(token=TOKEN, overwrite=True)
        print("🔑 IBM account token saved successfully!")
    except Exception as e:
        print(f"⚠️ Note: {e}")
        print("🔄 IBM connection may not work, will use simulator")
        IBM_PROVIDER_AVAILABLE = False
else:
    print("💡 No worries! The game will work perfectly with local simulation")

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
  if IBM_PROVIDER_AVAILABLE:
    try:
      # Load the IBM provider with the newer syntax
      provider = IBMProvider()
      
      # Get available backends (quantum computers)
      backends = provider.backends()
      
      # Try to get a working backend (newer Qiskit versions may have different backend names)
      # Let's use a more general approach to find an available backend
      available_backends = [backend.name for backend in backends if backend.simulator == False]
      
      if available_backends:
        # Use the first available real quantum computer
        backend_name = available_backends[0]
        qcomp = provider.get_backend(backend_name)
        print(f"🔬 Using quantum computer: {backend_name}")
      else:
        print("⚠️ No real quantum computers available, falling back to simulator")
        # Fall back to simulator if no real hardware available
        from qiskit_aer import AerSimulator
        qcomp = AerSimulator()
        
    except Exception as e:
      print(f"⚠️ IBM connection issue: {e}")
      print("🔄 Falling back to local simulator")
      # Use local simulator as backup
      from qiskit_aer import AerSimulator
      qcomp = AerSimulator()
  else:
    print("🔄 Using local simulator (IBM provider not available)")
    # Use local simulator since IBM provider isn't available
    from qiskit_aer import AerSimulator
    qcomp = AerSimulator()

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

  # 🚀 Send our circuit to the quantum computer and wait for results
  # shots=1 means we only run this once (one measurement)
  
  # For real IBM quantum computers, we need to transpile first
  if hasattr(qcomp, 'run'):
    # Using newer Qiskit syntax
    job = qcomp.run(circuit, shots=1)
  else:
    # Fallback for older syntax
    from qiskit import transpile
    transpiled_circuit = transpile(circuit, qcomp)
    job = qcomp.run(transpiled_circuit, shots=1)

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
  """
  🏆 Check if someone actually won this chaotic quantum game
  
  We check all the classic tic-tac-toe winning patterns:
  - Three in a row horizontally, vertically, or diagonally
  
  BUT WAIT - there's a catch! We only count it as a win if all three pieces
  are "classical" (not quantum). If any piece is still in quantum superposition,
  it doesn't count as a real win yet.
  
  It's like saying "you only win if your pieces are actually there, not just
  maybe there in some parallel universe"
  
  Args:
    theBoard: Current game state
    turn: Current player ('X' or 'O')
    
  Returns:
    True if someone won, False if game continues
  """
  
  # Check top row (positions 7, 8, 9)
  if theBoard['7'][0] == theBoard['8'][0] == theBoard['9'][0] != ' ': # Same symbol across top
      if theBoard['7'][1] == theBoard['8'][1] == theBoard['9'][1] == 0: # All pieces are classical (solid)
          printBoard(theBoard)
          print("\nGame Over.\n")                
          print(" **** ", end='')
          print(theBoard['8'][0], end='')  # Print the winning symbol
          print(" won ****")
          print() 
          return True

  # Check middle row (positions 4, 5, 6)
  elif theBoard['4'][0] == theBoard['5'][0] == theBoard['6'][0] != ' ':
      if theBoard['4'][1] == theBoard['5'][1] == theBoard['6'][1] == 0:
          printBoard(theBoard)
          print("\nGame Over.\n")                
          print(" **** ", end='')
          print(theBoard['5'][0], end='')
          print(" won ****")
          print()
          return True

  # Check bottom row (positions 1, 2, 3)
  elif theBoard['1'][0] == theBoard['2'][0] == theBoard['3'][0] != ' ':
      if theBoard['1'][1] == theBoard['2'][1] == theBoard['3'][1] == 0:
          printBoard(theBoard)
          print("\nGame Over.\n")                
          print(" **** ", end='')
          print(theBoard['2'][0], end='')
          print(" won ****")
          print()
          return True

  # Check left column (positions 1, 4, 7)
  elif theBoard['1'][0] == theBoard['4'][0] == theBoard['7'][0] != ' ':
      if theBoard['1'][1] == theBoard['4'][1] == theBoard['7'][1] == 0:
          printBoard(theBoard)
          print("\nGame Over.\n")                
          print(" **** ", end='')
          print(theBoard['4'][0], end='')
          print(" won ****")
          print()
          return True

  # Check middle column (positions 2, 5, 8)
  elif theBoard['2'][0] == theBoard['5'][0] == theBoard['8'][0] != ' ':
      if theBoard['2'][1] == theBoard['5'][1] == theBoard['8'][1] == 0:
          printBoard(theBoard)
          print("\nGame Over.\n")                
          print(" **** ", end='')
          print(theBoard['5'][0], end='')
          print(" won ****")
          print()
          return True

  # Check right column (positions 3, 6, 9)
  elif theBoard['3'][0] == theBoard['6'][0] == theBoard['9'][0] != ' ':
      if theBoard['3'][1] == theBoard['6'][1] == theBoard['9'][1] == 0:
          printBoard(theBoard)
          print("\nGame Over.\n")                
          print(" **** ", end='')
          print(theBoard['6'][0], end='')
          print(" won ****")
          print()
          return True

  # Check diagonal top-left to bottom-right (positions 7, 5, 3)
  elif theBoard['7'][0] == theBoard['5'][0] == theBoard['3'][0] != ' ':
      if theBoard['7'][1] == theBoard['5'][1] == theBoard['3'][1] == 0:
          printBoard(theBoard)
          print("\nGame Over.\n")                
          print(" **** ", end='')
          print(theBoard['5'][0], end='')
          print(" won ****")
          print()
          return True

  # Check diagonal top-right to bottom-left (positions 1, 5, 9)
  elif theBoard['1'][0] == theBoard['5'][0] == theBoard['9'][0] != ' ':
      if theBoard['1'][1] == theBoard['5'][1] == theBoard['9'][1] == 0:
          printBoard(theBoard)
          print("\nGame Over.\n")                
          print(" **** ", end='')
          print(theBoard['5'][0], end='')
          print(" won ****")
          print()
          return True
          
  # If we get here, nobody won yet
  return False

# 🎮 MAIN GAME FUNCTION - Where all the magic happens!
def game():
  """
  The main game loop - this is where players take turns and quantum chaos unfolds!
  
  Think of this as the "game engine" that keeps everything running smoothly.
  It handles player turns, move validation, win checking, and all that good stuff.
  """

  turn = 'X'  # X always goes first (classic tic-tac-toe rules)
  count = 0   # How many pieces are on the board
  win = False # Has someone won yet?
  x_collapse = 1  # X player can collapse once per game (special power!)
  y_collapse = 1  # O player can collapse once per game (special power!)

  # 🔬 Create our quantum circuit with 9 qubits (one for each board position)
  # and 9 classical bits (to store measurement results)
  # This is like setting up a 9-qubit quantum computer in software
  from qiskit import QuantumCircuit
  circuit = QuantumCircuit(9, 9)

  # 🔄 Main game loop - keep playing until someone wins
  while (not win):

    # ============================= ROUND START ============================= 
    global theBoard  # Use the global board variable
    printBoard(theBoard)  # Show current board state

    print()
    print("It's your turn " + turn + ". Do you want to make a (1) classical move, (2) quantum move, (3) collapse?, or (4) quit?")

    move = input()  # Get player's choice

    # ============================= CLASSIC MOVE ===========================
    if int(move) == 1:
        # Make a boring normal move (like your grandparents' tic-tac-toe)
        theBoard, turn, count, circuit = make_classic_move(theBoard, turn, count, circuit)
        madeMove = True

    # ============================= QUANTUM MOVE ===========================
    elif int(move) == 2 and count > 8:
      # Can't do quantum move if board is too full (need 2 empty spots)
      print()
      print("There aren't enough empty spaces for that!")

    elif int(move) == 2 and count < 8:
      # Make a quantum move (place piece in superposition across 2 spots)
      theBoard, count, circuit, turn = make_quantum_move(theBoard, count, circuit, turn)
      madeMove = True
    
    # ============================= COLLAPSE/MEASURE =======================
    elif int(move) == 3:
      # Use your special power to collapse all quantum pieces!
      # Each player can only do this once per game
      
      if (turn == 'X' and x_collapse== 1 ):
        # X player uses their collapse power
        circuit, string, theBoard, count = measure(circuit, theBoard, count)
        x_collapse = 0  # X can't collapse again
      elif (turn == 'O' and y_collapse == 1):
        # O player uses their collapse power  
        circuit, string, theBoard, count = measure(circuit, theBoard, count)
        y_collapse = 0  # O can't collapse again
      else:
        print("You have already used your collapse this game!")  # No more collapses for you!

    # ============================= QUIT ===================================
    elif int(move) == 4:
        break  # Rage quit 😤
    
    # ============================= CHECK FOR WIN ==========================
    # Only check for wins after there are at least 5 pieces on board
    # (mathematically impossible to win with fewer pieces)
    if count >= 5:
      win = check_win(theBoard, turn)
      if (win):
        break  # Someone won! End the game

    # ============================= BOARD FULL CHECK ====================
    # If board is completely full, force a collapse and check for winner
    if count == 9:
      circuit, string, theBoard, count = measure(circuit, theBoard, count)
      win = check_win(theBoard, turn)
      if count == 9:  # If still full after collapse, it's a tie
        print("\nGame Over.\n")                
        print("It's a Tie !")
        print()
        win = True

    # ============================= SWITCH PLAYERS ======================
    # Alternate between X and O after each valid move
    if (madeMove):  
      madeMove = False
      if turn =='X':
          turn = 'O'  # X's turn is over, now it's O's turn
      else:
          turn = 'X'  # O's turn is over, now it's X's turn
    
  # ============================= GAME OVER ============================
  # Ask if they want to play again (because this game is addictive)
  restart = input("Play Again?(y/n) ")
  if restart == "y" or restart == "Y":
      theBoard = resetBoard()  # Fresh board
      game()  # Start a new game (recursive call)

def start_menu():
    """
    🎯 The main menu - like the lobby of your favorite game
    
    This is what players see when they first start the game.
    Simple menu with options to start playing, learn how to play, or quit.
    """
    
    start_menu = """
    Start Menu:

    1. Start Game
    2. How to Play
    3. Quit
    """ 
    
    # 🎨 ASCII art title because we're fancy like that
    print("""
    ###########################
    ### Quantum Tic-Tac-Toe ###
    ###########################
    """)
    print(start_menu)
    
    choice = 0
    # Keep asking until they pick option 1 (Start Game)
    while (choice != '1'):
      print("What would you like to do? ", end='')
      choice = input()

      if (choice == '2'):
        # Show the tutorial/instructions
        How_To = """ 
        In Quantum Tic-Tac-Toe, each square starts empty and your goal is to create a line of three of your naughts/crosses. 
        Playing a classical move will result in setting a square permanently as your piece.
        Playing a quantum move will create a superposition between two squares of your choosing. You may only complete a quantum move in two empty squares.
        The board will collapse when the board is full. At collapse, each superposition is viewed and only 1 piece of the superposition will remain. 
        *Powerup* Each player can decide to collapse the board prematurely, they may do this once per round each.
        """
        print(How_To)

      if (choice == '3'):
        print("Goodbye")  # Peace out ✌️
        break
      
    return choice

# 🚀 GAME INITIALIZATION - This is where everything starts!

# Reset the board at start (create a fresh, empty board)
theBoard = resetBoard()

# 🎮 Start the game if player chooses option 1
if (start_menu() == '1'):  
  madeMove = False  # Track if a move was made this turn
  game()  # LET THE QUANTUM CHAOS BEGIN! 🌀