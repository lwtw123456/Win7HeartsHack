import tkinter as tk
from tkinter import messagebox

class CardSelector:
    def __init__(self, parent=None):
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("扑克牌选择器")
        
        if parent:
            self.window.transient(parent)
            self.window.grab_set()
        
        self.selected = set()
        self.buttons = {}
        self.card_to_number = {}
        self.result = None
        
        self.suits = ['♣', '♦', '♠', '♥']
        self.suits_cn = ['梅花', '方片', '黑桃', '红桃']
        self.suit_colors = ['black', 'red', 'black', 'red']
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        
        self.counter_label = tk.Label(self.window, text="已选：0/13", font=('Arial', 14, 'bold'))
        self.counter_label.grid(row=0, column=0, columnspan=13, pady=10)
        
        for i, (suit, color, name) in enumerate(zip(self.suits, self.suit_colors, self.suits_cn)):
            for j, rank in enumerate(self.ranks):
                card = f"{suit}{name}{rank}"
                number = i * 13 + j
                
                self.card_to_number[card] = number
                
                btn = tk.Button(
                    self.window, 
                    text=card, 
                    width=6, 
                    height=2,
                    font=('Arial', 10),
                    fg=color,
                    command=lambda c=card, n=number: self.toggle_card(c, n)
                )
                btn.grid(row=i+1, column=j, padx=2, pady=2)
                self.buttons[card] = btn
        
        button_frame = tk.Frame(self.window)
        button_frame.grid(row=5, column=0, columnspan=13, pady=10)
        
        confirm_btn = tk.Button(button_frame, text="确认选择", font=('Arial', 12), 
                               bg='#4CAF50', fg='white', command=self.confirm)
        confirm_btn.pack(side='left', padx=5)
        
        clear_btn = tk.Button(button_frame, text="清空选择", font=('Arial', 12), 
                             bg='#FF6B6B', fg='white', command=self.clear_selection)
        clear_btn.pack(side='left', padx=5)

        self._center_window()
    
    def _center_window(self):
        self.window.update_idletasks()  
        w = self.window.winfo_width() 
        h = self.window.winfo_height() 
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.window.geometry(f"{w}x{h}+{x}+{y}")

    def toggle_card(self, card, number):
        if number in self.selected:
            self.selected.remove(number)
            self.buttons[card].config(bg='SystemButtonFace', relief='raised')
        else:
            if len(self.selected) >= 13:
                messagebox.showwarning("提示", "最多只能选择13张牌！")
                return
            self.selected.add(number)
            self.buttons[card].config(bg='#FFD700', relief='sunken')
        
        self.counter_label.config(text=f"已选：{len(self.selected)}/13")
    
    def clear_selection(self):
        for card in self.buttons:
            self.buttons[card].config(bg='SystemButtonFace', relief='raised')
        self.selected.clear()
        self.counter_label.config(text="已选：0/13")
    
    def confirm(self):
        if len(self.selected) != 13:
            messagebox.showwarning("提示", f"请选择13张牌（当前已选{len(self.selected)}张）")
            return
        
        self.result = sorted(self.selected)
        self.window.destroy()
    
    def show(self):
        self.window.wait_window()
        return self.result