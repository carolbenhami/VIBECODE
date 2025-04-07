import tkinter as tk
from tkinter import messagebox, font
import random
import time

class SlotMachineGUI:
    def __init__(self, master):
        #Create popup window's characteristics
        self.master = master
        self.master.title("Casino Slot Machine") #Webpage title
        self.master.geometry("800x600") #Size
        self.master.resizable(False, False) #Ability to resize
        self.master.configure(bg="#1E1E2E") #Background Color
        
        # Game variables
        self.balance = 100 #Accounts for balance among the game
        self.bet_amount = 5 #Bet cost
        self.symbols = ["🤬", "🐃", "🙊", "🧘", "💣", "🪬", "❌"] #
        self.current_spin = [] 
        self.spinning = False #Currently in a spin
        self.spin_count = 0
        
        # Configure fonts
        self.title_font = font.Font(family="Courier New", size=24, weight="bold")
        self.display_font = font.Font(family="Courier New", size=36)
        self.button_font = font.Font(family="Courier New", size=14, weight="bold")
        self.info_font = font.Font(family="Courier New", size=12)
        
        # Create frames
        self.title_frame = tk.Frame(master, bg="#1E1E2E")
        self.title_frame.pack(pady=10)
        
        self.info_frame = tk.Frame(master, bg="#1E1E2E")
        self.info_frame.pack(pady=5)
        
        self.display_frame = tk.Frame(master, bg="#2E2E3E", bd=5, relief=tk.RAISED)
        self.display_frame.pack(pady=20)
        
        self.control_frame = tk.Frame(master, bg="#1E1E2E")
        self.control_frame.pack(pady=20)
        
        self.balance_frame = tk.Frame(master, bg="#1E1E2E")
        self.balance_frame.pack(pady=10)
        
        # Create widgets
        # Title
        self.title_label = tk.Label(
            self.title_frame,
            text="CASINO SLOT MACHINE",
            font=self.title_font,
            bg="#1E1E2E",
            fg="#FFD700"
        )
        self.title_label.pack()
        
        # Info labels
        self.info_label = tk.Label(
            self.info_frame,
            text="Every play costs $5\n\n3x Equal: $1 | 4x Equal: $2 | 5x Equal: $5 | 6x Equal: $50 | 7x Equal: $150",
            font=self.info_font,
            bg="#1E1E2E",
            fg="white"
        )
        self.info_label.pack()
        
        # Display slots
        self.slots_frame = tk.Frame(self.display_frame, bg="#2E2E3E")
        self.slots_frame.pack(padx=20, pady=20)
        
        self.slot_labels = []
        for i in range(7):
            frame = tk.Frame(
                self.slots_frame,
                width=80,
                height=80,
                bg="#3E3E4E",
                bd=2,
                relief=tk.SUNKEN
            )
            frame.pack_propagate(False)
            frame.grid(row=0, column=i, padx=5)
            
            label = tk.Label(
                frame,
                text="?",
                font=self.display_font,
                bg="#3E3E4E",
                fg="white"
            )
            label.pack(expand=True, fill=tk.BOTH)
            self.slot_labels.append(label)
        
        # Result label
        self.result_label = tk.Label(
            self.display_frame,
            text="Press SPIN to play!",
            font=self.info_font,
            bg="#2E2E3E",
            fg="white"
        )
        self.result_label.pack(pady=10)
        
        # Control buttons
        self.spin_button = tk.Button(
            self.control_frame,
            text="SPIN",
            font=self.button_font,
            bg="#4CAF50",
            fg="white",
            width=10,
            height=2,
            command=self.spin
        )
        self.spin_button.pack(side=tk.LEFT, padx=20)
        
        self.quit_button = tk.Button(
            self.control_frame,
            text="QUIT",
            font=self.button_font,
            bg="#F44336",
            fg="white",
            width=10,
            height=2,
            command=self.quit_game
        )
        self.quit_button.pack(side=tk.RIGHT, padx=20)
        
        # Balance display
        self.balance_label = tk.Label(
            self.balance_frame,
            text=f"Balance: ${self.balance}",
            font=self.button_font,
            bg="#1E1E2E",
            fg="#FFD700"
        )
        self.balance_label.pack()
        
        # Initialize UI
        self.reset_slots()
    
    def reset_slots(self):
        """Reset all slot symbols to '?'"""
        for label in self.slot_labels:
            label.config(text="?")
    
    def spin(self):
        """Handle the spin button click"""
        if self.spinning:
            return
        
        if self.balance < self.bet_amount:
            messagebox.showinfo("Game Over", f"Sorry, you don't have enough money to play!\nFinal balance: ${self.balance}")
            return
        
        # Deduct bet amount
        self.balance -= self.bet_amount
        self.balance_label.config(text=f"Balance: ${self.balance}")
        
        # Start spinning animation
        self.spinning = True
        self.spin_count = 0
        self.result_label.config(text="Spinning...")
        self.spin_animation()
    
    def spin_animation(self):
        """Animate the spinning slots"""
        if self.spin_count < 15:  # Number of animation frames
            # Update each slot with random symbols
            for label in self.slot_labels:
                label.config(text=random.choice(self.symbols))
            
            self.spin_count += 1
            self.master.after(100, self.spin_animation)
        else:
            self.finish_spin()
    
    def finish_spin(self):
        """Complete the spin and calculate results"""
        # Generate final results
        number_mapping = {
            "🤬": 1, "🐃": 2, "🙊": 3, "🧘": 4, "💣": 5, "🪬": 6, "❌": 7
        }
        
        self.current_spin = []
        for i in range(7):
            symbol = random.choice(self.symbols)
            self.slot_labels[i].config(text=symbol)
            self.current_spin.append(number_mapping[symbol])
        
        # Count occurrences
        counts = [0] * 8  # Index 0 is unused, 1-7 for the symbols
        for num in self.current_spin:
            counts[num] += 1
        
        # Find highest match
        max_count = max(counts)
        winning_symbol = counts.index(max_count)
        
        # Calculate winnings
        winnings = 0
        if max_count == 3:
            winnings = 1
        elif max_count == 4:
            winnings = 2
        elif max_count == 5:
            winnings = 5
        elif max_count == 6:
            winnings = 50
        elif max_count == 7:
            winnings = 150
        
        # Update balance
        self.balance += winnings
        self.balance_label.config(text=f"Balance: ${self.balance}")
        
        # Highlight matching symbols
        for i in range(7):
            if self.current_spin[i] == winning_symbol:
                self.slot_labels[i].config(bg="#FFD700" if winnings > 0 else "#3E3E4E")
            else:
                self.slot_labels[i].config(bg="#3E3E4E")
        
        # Update result text
        if winnings > 0:
            symbol_text = self.symbols[winning_symbol-1]
            self.result_label.config(
                text=f"Congratulations! {max_count}x {symbol_text} - You won ${winnings}!",
                fg="#FFD700"
            )
        else:
            self.result_label.config(
                text="No winning combination. Try again!",
                fg="white"
            )
        
        self.spinning = False
    
    def quit_game(self):
        """Handle the quit button click"""
        if messagebox.askyesno("Quit Game", f"Are you sure you want to quit?\nFinal balance: ${self.balance}"):
            self.master.destroy()


# Create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = SlotMachineGUI(root)
    root.mainloop()
