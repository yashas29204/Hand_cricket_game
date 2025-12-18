import tkinter as tk
import random as r

class HandCricket(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hand Cricket")
        # Game state
        self.phase = "toss-call"
        self.user_choice_odd_even = None
        self.user_bats_first = None
        self.user_score = 0
        self.comp_score = 0
        self.batting = None
        self.innings = 1

        # Hand images
        self.img = {i: tk.PhotoImage(file=f"hand{i}.png").subsample(2,2) for i in range(1,7)}

        # Layout
        main = tk.Frame(self, padx=10, pady=10)
        main.pack()
        self.left = tk.Frame(main)
        self.left.grid(row=0, column=0, padx=10)
        tk.Label(self.left, text="You", font=("Arial",16)).pack()
        self.user_buttons = [tk.Button(self.left, image=self.img[i], command=lambda x=i: self.click(x)) for i in range(1,7)]
        for b in self.user_buttons: b.pack(pady=5)

        self.center = tk.Frame(main, padx=20)
        self.center.grid(row=0, column=1)
        tk.Frame(self.center, width=2, height=450, bg="black").pack(side="left")
        tk.Frame(self.center, width=2, height=450, bg="black").pack(side="right")
        self.info = tk.Label(self.center, text="Choose Odd or Even", font=("Arial",16), width=30, wraplength=300, justify="center")
        self.info.pack(padx=20)

        self.toss_buttons = [tk.Button(self.center, text=t, width=12, command=lambda t=t:self.click(t)) for t in ["Odd", "Even"]]
        for b in self.toss_buttons: b.pack(pady=5)

        self.right = tk.Frame(main)
        self.right.grid(row=0, column=2, padx=10)
        tk.Label(self.right, text="Computer", font=("Arial",16)).pack()
        self.comp_label = tk.Label(self.right, text="–", font=("Arial",50))
        self.comp_label.pack(pady=20)

        # Animation config
        self.shake_steps = 10
        self.shake_interval = 100

    # display computer hand
    def show_comp(self, num):
        self.comp_label.config(image=self.img[num])
        self.comp_label.image = self.img[num]

    # Animate computer hand shake
    def animate(self, num, callback=None):
        self.shake_count = 0
        self.final = num
        self.callback = callback
        self._shake()

    def _shake(self):
        n = (self.shake_count % 6) + 1
        self.show_comp(n)
        self.shake_count += 1
        if self.shake_count < self.shake_steps:
            self.after(self.shake_interval, self._shake)
        else:
            self.show_comp(self.final)
            if self.callback:
                self.callback()

    # Handle all clicks
    def click(self, val):
        if self.phase == "toss-call":
            self.user_choice_odd_even = val
            self.phase = "toss-pick"
            self.info.config(text=f"You chose {val}.\nClick a hand to pick number for toss.")
        elif self.phase == "toss-pick":
            user_num = val
            comp_num = r.randint(1,6)
            self.animate(comp_num, lambda: self.handle_toss_result(user_num, comp_num))
        elif self.phase in ["batting", "bowling"]:
            comp_num = r.randint(1,6)
            self.animate(comp_num, lambda: self.handle_play(val, comp_num))

    # Handle toss result and Bat/Bowl selection
    def handle_toss_result(self, user_num, comp_num):
        total = user_num + comp_num
        parity = "Even" if total % 2 == 0 else "Odd"
        msg = f"TOSS:\nYou: {user_num} | Computer: {comp_num}\nTotal={total} ({parity})"
        for b in self.toss_buttons: b.pack_forget()

        if parity == self.user_choice_odd_even:
            self.info.config(text=msg+"\nYou won the toss!\nChoose Bat or Bowl.")
            self.batbowl_buttons = [tk.Button(self.center, text=t, width=12, command=lambda choice=c: self.start_match(choice)) for t,c in [("Bat",True), ("Bowl",False)]]
            for b in self.batbowl_buttons: b.pack(pady=5)
        else:
            self.user_bats_first = r.choice([True, False])
            self.info.config(text=msg+f"\nComputer won the toss!\nComputer chooses to {'bat' if not self.user_bats_first else 'bowl'}.")
            self.after(2000, lambda: self.start_match(self.user_bats_first))

    # Start the match after toss
    def start_match(self, user_bats_first):
        if hasattr(self, 'batbowl_buttons'):
            for b in self.batbowl_buttons: b.pack_forget()
        self.user_bats_first = user_bats_first
        self.batting = self.user_bats_first
        self.phase = "batting" if self.batting else "bowling"
        self.info.config(text=f"{'You are batting' if self.batting else 'You are bowling'} first!\nClick your hand to play.")

    # Handle each play (batting or bowling)
    def handle_play(self, user_num, comp_num):
        out = False
        if self.phase == "batting":
            if user_num == comp_num:
                out = True
            else:
                self.user_score += user_num
        else:
            if user_num == comp_num:
                out = True
            else:
                self.comp_score += comp_num

        msg = f"You: {user_num} | Computer: {comp_num}\n"
        if out:
            msg += f"OUT!\n{'Your' if self.phase=='batting' else 'Computer'} Score = {self.user_score if self.phase=='batting' else self.comp_score}"
        else:
            msg += f"Runs = {self.user_score if self.phase=='batting' else self.comp_score}"
        self.info.config(text=msg)

        if out:
            if self.innings == 1:
                self.innings = 2
                self.batting = not self.batting
                self.phase = "batting" if self.batting else "bowling"
                tgt = self.comp_score + 1 if self.batting else self.user_score + 1
                text = f"Second Innings:\nTarget={tgt}\nStart {'batting' if self.batting else 'bowling'}."
                self.after(2000, lambda: self.info.config(text=text))
            else:
                self.after(2000, self.end_game)

    # End game and show result
    def end_game(self):
        for b in self.user_buttons:
            b.config(state="disabled")
        if self.user_score > self.comp_score:
            result = "You Won!"
        elif self.user_score < self.comp_score:
            result = "You Lost!"
        else:
            result = "Match Tied!"
        self.info.config(text=f"GAME OVER!\nYou: {self.user_score}\nComputer: {self.comp_score}\n{result}")

HandCricket().mainloop()
