# 🎮 Connect 6 - Python Game with AI

**Connect 6** is a strategic two-player board game built in Python using **Pygame** and **Tkinter** for a graphical interface and **NumPy** for board state management. This game implements **artificial intelligence** using the **Minimax algorithm with alpha-beta pruning** to provide a challenging experience for the player.

It supports dynamic board sizing, intelligent AI decision-making, and a polished graphical layout.

---

## 📖 Description

Connect 6 is an advanced version of traditional games like Gomoku or Connect 4. Players take turns placing **two pieces per turn** (except the first move, which places only one). The objective is simple:

> ✅ The first player to connect **six** of their pieces **in a row** — **horizontally**, **vertically**, or **diagonally** — wins the game.

This project is divided into modular files:
- `connect6.py`: The main game loop and interface
- `classes.py`: Contains structured classes for game logic

---

## 🧠 How Winning Is Determined

The game constantly checks for the following winning patterns for **each move**:

1. **Horizontal Win**:
   - Six consecutive pieces in the same row:  
     
2. **Vertical Win**:
   - Six consecutive pieces in the same column

3. **Positive Diagonal Win** (bottom-left to top-right):


4. **Negative Diagonal Win** (top-left to bottom-right):
   

Once any of these patterns are satisfied, the game displays a winning message and ends.

---

## 🌟 Features

✅ Customizable board size (minimum 6x6)  
✅ Pygame graphical interface  
✅ AI opponent with adjustable difficulty  
✅ Human vs AI mode  
✅ Turn-based logic with 2 pieces per turn  
✅ AI powered by Minimax + Alpha-Beta pruning  
✅ Heuristic evaluation for smarter AI decisions  
✅ Highlights winning move  
✅ Modular object-oriented structure (`Board`, `AI`, `Game`)

---

## 📌 Benefits

- 🧩 **Modular Code**: Easier to maintain and extend with `classes.py` providing separation of logic
- 🧠 **AI Smartness**: Simulates intelligent strategy through heuristics and lookahead depth
- 📈 **Scalable**: Supports larger boards with just a single input
- 👨‍🏫 **Educational**: Great for learning game development, AI, algorithms, and Pygame
- 🖼️ **Interactive**: GUI-based and beginner-friendly

---

## 🛠️ How to Run

### Requirements

- Python 3.x
- python IDE
- Pygame
- NumPy


## 🔔 Make sure both connect6.py and class.py are in the same folder.

## 🧱 Project Structure

connect6_project/

├── connect6.py         # Main game loop and logic
├── class.py            # Game classes: Board, AI, Game
├── README.md           # This documentation
📸 Screenshots

---

## 👨‍💻 Author
- Developed by: Ahmed Amr 

---

## 💬 Feedback
- Found a bug? Have a suggestion?
- Feel free to open an issue or a pull request.
---

# Enjoy the game! 🎉
