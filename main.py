import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Import your custom standalone bot module
from bot import MinimaxBot

class IntelligentTicTacToe:
    def __init__(self, window):
        self.window = window
        self.window.title("Tic-Tac-Toe: Man vs Machine")
        self.window.geometry("500x550")
        self.window.configure(bg="#1e1e24")
        
        # Game Setup
        self.human = "X"
        self.bot_player = "O"
        self.current_player = self.human
        self.board = [""] * 9
        self.buttons = []
        self.is_bot_thinking = False
        
        # Initialize your imported bot instance
        self.bot_brain = MinimaxBot(bot_player=self.bot_player, human_player=self.human)
        
        self.load_assets()
        self.setup_ui()

    def load_assets(self):
        """Loads and auto-scales PNG templates; falls back to text safely."""
        assets_dir = os.path.join("src", "assets")
        x_path = os.path.join(assets_dir, "Avocado.png")
        o_path = os.path.join(assets_dir, "o.png")
        
        self.x_image = None
        self.o_image = None
        self.use_images = False
        
        if os.path.exists(x_path) and os.path.exists(o_path):
            try:
                x_raw = Image.open(x_path)
                o_raw = Image.open(o_path)
                self.x_image = ImageTk.PhotoImage(x_raw.resize((100, 100), Image.Resampling.LANCZOS))
                self.o_image = ImageTk.PhotoImage(o_raw.resize((100, 100), Image.Resampling.LANCZOS))
                self.use_images = True
            except Exception as e:
                print(f"Asset loading skipped: {e}. Using text fallback.")

    def setup_ui(self):
        """Creates a centered inner gameplay box and status bar."""
        self.status_label = tk.Label(
            self.window, text="YOUR TURN (X)", font=('Helvetica', 14, 'bold'), bg="#1e1e24", fg="#ffffff"
        )
        self.status_label.pack(pady=15)

        # Inner Container Box for the 3x3 Grid
        self.inner_box = tk.Frame(self.window, bg="#2a2a35", padx=15, pady=15, bd=3, relief="ridge")
        self.inner_box.pack(expand=True)
        
        for i in range(9):
            button = tk.Button(
                self.inner_box, text="", font=('Helvetica', 20, 'bold'),
                width=6, height=3, bg="#3e3e4f", fg="#ffffff", activebackground="#4e4e62",
                command=lambda idx=i: self.handle_human_move(idx)
            )
            button.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(button)

    def handle_human_move(self, idx):
        """Processes human interaction and hands control over to the bot module."""
        if self.board[idx] == "" and self.current_player == self.human and not self.is_bot_thinking:
            self.make_move(idx, self.human)
            
            if not self.check_game_over():
                self.current_player = self.bot_player
                self.status_label.config(text="BOT IS THINKING...")
                self.is_bot_thinking = True
                # Smooth 500ms delay so the bot feels natural
                self.window.after(500, self.handle_bot_move)

    def handle_bot_move(self):
        """Queries the external bot module for the best coordinate and plays it."""
        # Call the separated bot logic file directly
        best_move = self.bot_brain.get_best_move(self.board)
                    
        if best_move is not None:
            self.make_move(best_move, self.bot_player)
            
        self.is_bot_thinking = False
        if not self.check_game_over():
            self.current_player = self.human
            self.status_label.config(text="YOUR TURN (X)")

    def make_move(self, idx, player):
        """Updates internal board matrices and structural button graphics."""
        self.board[idx] = player
        if self.use_images:
            img = self.x_image if player == self.human else self.o_image
            self.buttons[idx].config(image=img, width=100, height=100)
        else:
            color = "#ff5964" if player == self.human else "#35a7ff"
            self.buttons[idx].config(text=player, fg=color)

    def check_game_over(self):
        """Determines if the active grid status meets game-over criteria."""
        # Route live board checking directly through the bot's matrix evaluator
        score = self.bot_brain.evaluate_board(self.board)
        if score == 10:
            messagebox.showinfo("Game Over", "The Bot wins! Absolute calculation perfection.")
            self.reset_game()
            return True
        elif score == -10:
            messagebox.showinfo("Game Over", "Unbelievable! You beat the bot!")
            self.reset_game()
            return True
        elif "" not in self.board:
            messagebox.showinfo("Game Over", "It's a draw! Perfect strategy on both sides.")
            self.reset_game()
            return True
        return False

    def reset_game(self):
        """Resets the UI grid and memory arrays for a fresh match."""
        self.board = [""] * 9
        self.current_player = self.human
        self.status_label.config(text="YOUR TURN (X)")
        for button in self.buttons:
            button.config(image="", text="", width=6, height=3)

if __name__ == "__main__":
    root = tk.Tk()
    app = IntelligentTicTacToe(root)
    root.mainloop()