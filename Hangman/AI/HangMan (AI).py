import random
import tkinter as tk


WORDS = [
    "apple", "window", "ocean", "rocket", "forest",
    "pencil", "mirror", "cloud", "dragon", "coffee",
    "planet", "guitar", "bridge", "shadow", "garden",
    "thunder", "river", "castle", "camera", "diamond",
    "keyboard", "mountain", "sunset", "puzzle", "butterfly",
    "island", "robot", "blanket", "volcano", "rainbow",
    "helmet", "desert", "candle", "spaceship", "library",
    "telescope", "bottle", "snowflake", "pyramid", "compass",
    "elephant", "lantern", "village", "whistle", "magnet",
    "calendar", "sandwich", "airport", "jungle", "umbrella",
    "throne", "notebook", "waterfall", "penguin", "submarine",
    "pocket", "train", "adventure", "galaxy", "hammer",
    "feather", "engine", "museum", "basket", "signal",
    "anchor", "ticket", "piano", "battery", "cactus"
]


# =========================
# COLORS
# =========================

BG = "#080b10"
PANEL = "#0d1219"
PANEL_2 = "#111821"

TEXT = "#d9e4ef"
MUTED = "#657384"

CYAN = "#39d9ff"
GREEN = "#55f28c"
RED = "#ff4f6d"
YELLOW = "#ffd166"


# =========================
# GAME
# =========================

class HangManGUI:

    MAX_ATTEMPTS = 7

    def __init__(self, root):

        self.root = root

        self.root.title("NULL//WORD — Hangman")
        self.root.geometry("1050x700")
        self.root.minsize(900, 620)

        self.root.configure(bg=BG)

        # Game data
        self.name = ""
        self.word = ""

        self.guessed = set()
        self.wrong = set()

        self.left_attempts = self.MAX_ATTEMPTS

        self.game_over = False

        self.typing_job = None
        self.dialog_job = None

        self.build_ui()

        self.show_intro()


    # =========================
    # UI
    # =========================

    def build_ui(self):

        # ---------------------
        # HEADER
        # ---------------------

        self.header = tk.Frame(
            self.root,
            bg=BG
        )

        self.header.pack(
            fill="x",
            padx=35,
            pady=(24, 10)
        )


        tk.Label(
            self.header,
            text="NULL//WORD",
            font=("Consolas", 25, "bold"),
            fg=CYAN,
            bg=BG
        ).pack(side="left")


        tk.Label(
            self.header,
            text="SECURITY LEVEL: UNKNOWN",
            font=("Consolas", 10, "bold"),
            fg=RED,
            bg=BG
        ).pack(
            side="right",
            pady=8
        )


        # Header line

        tk.Frame(
            self.root,
            bg=CYAN,
            height=1
        ).pack(
            fill="x",
            padx=35
        )


        # ---------------------
        # MAIN
        # ---------------------

        self.main = tk.Frame(
            self.root,
            bg=BG
        )

        self.main.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=22
        )


        # =====================
        # LEFT PANEL
        # =====================

        self.left_panel = tk.Frame(
            self.main,
            bg=PANEL,
            highlightbackground="#182532",
            highlightthickness=1
        )

        self.left_panel.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )


        tk.Label(
            self.left_panel,
            text="UNKNOWN WORD",
            font=("Consolas", 11, "bold"),
            fg=MUTED,
            bg=PANEL
        ).pack(
            anchor="w",
            padx=25,
            pady=(22, 5)
        )


        self.word_label = tk.Label(
            self.left_panel,
            text="_ _ _ _ _",
            font=("Consolas", 31, "bold"),
            fg=TEXT,
            bg=PANEL
        )

        self.word_label.pack(
            pady=(18, 30)
        )


        self.status_label = tk.Label(
            self.left_panel,
            text="WAITING FOR SUBJECT...",
            font=("Consolas", 11, "bold"),
            fg=YELLOW,
            bg=PANEL
        )

        self.status_label.pack()


        self.attempt_label = tk.Label(
            self.left_panel,
            text="ATTEMPTS  07 / 07",
            font=("Consolas", 12, "bold"),
            fg=GREEN,
            bg=PANEL
        )

        self.attempt_label.pack(
            pady=(20, 5)
        )


        # Progress bar

        self.progress = tk.Canvas(
            self.left_panel,
            height=12,
            bg="#18212b",
            highlightthickness=0
        )

        self.progress.pack(
            fill="x",
            padx=25,
            pady=(0, 25)
        )

        self.progress.bind(
            "<Configure>",
            lambda event: self.draw_progress()
        )


        # Wrong guesses

        tk.Label(
            self.left_panel,
            text="FAILED INPUTS",
            font=("Consolas", 10, "bold"),
            fg=MUTED,
            bg=PANEL
        ).pack()


        self.wrong_label = tk.Label(
            self.left_panel,
            text="—",
            font=("Consolas", 14, "bold"),
            fg=RED,
            bg=PANEL
        )

        self.wrong_label.pack(
            pady=8
        )


        # Terminal log

        self.log = tk.Text(
            self.left_panel,
            height=8,
            bg="#070a0e",
            fg="#7f94a8",
            font=("Consolas", 9),
            relief="flat",
            bd=0,
            padx=12,
            pady=10,
            insertbackground=CYAN
        )

        self.log.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(10, 25)
        )

        self.log.config(
            state="disabled"
        )


        # =====================
        # RIGHT PANEL
        # =====================

        self.right_panel = tk.Frame(
            self.main,
            bg=PANEL,
            highlightbackground="#182532",
            highlightthickness=1
        )

        self.right_panel.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(10, 0)
        )


        tk.Label(
            self.right_panel,
            text="INPUT TERMINAL",
            font=("Consolas", 11, "bold"),
            fg=MUTED,
            bg=PANEL
        ).pack(
            anchor="w",
            padx=25,
            pady=(22, 12)
        )


        # Input

        self.entry = tk.Entry(
            self.right_panel,
            font=("Consolas", 20, "bold"),
            fg=CYAN,
            bg="#070a0e",
            insertbackground=CYAN,
            relief="flat",
            justify="center"
        )

        self.entry.pack(
            fill="x",
            padx=25,
            ipady=12
        )

        self.entry.bind(
            "<Return>",
            self.submit_guess
        )

        self.entry.bind(
            "<KeyRelease>",
            self.filter_entry
        )


        # Keyboard

        self.key_frame = tk.Frame(
            self.right_panel,
            bg=PANEL
        )

        self.key_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )


        self.keys = {}

        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


        for i, letter in enumerate(alphabet):

            row, col = divmod(i, 6)

            btn = tk.Button(
                self.key_frame,
                text=letter,
                font=("Consolas", 12, "bold"),
                fg=TEXT,
                bg=PANEL_2,
                activeforeground=BG,
                activebackground=CYAN,
                relief="flat",
                bd=0,

                command=lambda l=letter.lower():
                self.guess(l)
            )

            btn.grid(
                row=row,
                column=col,
                sticky="nsew",
                padx=3,
                pady=3
            )

            self.keys[letter.lower()] = btn


        for r in range(5):
            self.key_frame.rowconfigure(
                r,
                weight=1
            )


        for c in range(6):
            self.key_frame.columnconfigure(
                c,
                weight=1
            )


        # Restart

        self.reset_btn = tk.Button(
            self.right_panel,
            text="RESTART SESSION",
            font=("Consolas", 10, "bold"),
            fg=CYAN,
            bg="#16232d",
            activeforeground=BG,
            activebackground=CYAN,
            relief="flat",
            command=self.new_game
        )

        self.reset_btn.pack(
            fill="x",
            padx=25,
            pady=(0, 25),
            ipady=9
        )


        # Keyboard focus

        self.root.bind(
            "<KeyPress>",
            self.global_key
        )


    # =========================
    # INTRO
    # =========================

    def show_intro(self):

        self.disable_input()

        self.type_dialog(
            "SYSTEM: connection established...\n"
            "SYSTEM: identity required.\n\n"
            "What is your name?",
            self.ask_name
        )


    # =========================
    # NAME
    # =========================

    def ask_name(self):

        self.name_window = tk.Toplevel(
            self.root
        )

        self.name_window.title(
            "IDENTITY"
        )

        self.name_window.geometry(
            "400x210"
        )

        self.name_window.configure(
            bg=BG
        )

        self.name_window.resizable(
            False,
            False
        )

        self.name_window.transient(
            self.root
        )

        self.name_window.grab_set()


        tk.Label(
            self.name_window,
            text="IDENTIFY YOURSELF",
            font=("Consolas", 14, "bold"),
            fg=CYAN,
            bg=BG
        ).pack(
            pady=(30, 15)
        )


        entry = tk.Entry(
            self.name_window,
            font=("Consolas", 14),
            fg=TEXT,
            bg=PANEL_2,
            insertbackground=CYAN,
            relief="flat",
            justify="center"
        )

        entry.pack(
            fill="x",
            padx=40,
            ipady=8
        )

        entry.focus()


        def confirm():

            self.name = (
                entry.get().strip()
                or "UNKNOWN"
            )

            self.name_window.destroy()

            self.new_game()


        tk.Button(
            self.name_window,
            text="CONNECT",
            command=confirm,
            font=("Consolas", 10, "bold"),
            fg=BG,
            bg=CYAN,
            activebackground=GREEN,
            relief="flat"
        ).pack(
            pady=20,
            ipadx=35,
            ipady=7
        )


        entry.bind(
            "<Return>",
            lambda event: confirm()
        )


    # =========================
    # NEW GAME
    # =========================

    def new_game(self):

        self.word = random.choice(
            WORDS
        ).lower()

        self.guessed.clear()
        self.wrong.clear()

        self.left_attempts = self.MAX_ATTEMPTS

        self.game_over = False


        self.enable_input()

        self.update_ui()


        self.write_log(
            f"> SESSION STARTED // SUBJECT: {self.name}"
        )

        self.write_log(
            "> A hidden word has been loaded."
        )


        self.status_label.config(
            text="THE SYSTEM IS WATCHING.",
            fg=YELLOW
        )


        self.reset_btn.config(
            text="RESTART SESSION"
        )


        self.entry.focus_set()


    # =========================
    # INPUT
    # =========================

    def filter_entry(self, event=None):

        value = self.entry.get().lower()

        filtered = "".join(
            c for c in value
            if c.isalpha()
        )

        self.entry.delete(
            0,
            "end"
        )

        self.entry.insert(
            0,
            filtered[:1]
        )


    def global_key(self, event):

        if self.game_over:
            return

        if event.char and event.char.isalpha():

            self.entry.focus_set()


    def submit_guess(self, event=None):

        if self.game_over:
            return

        letter = (
            self.entry
            .get()
            .strip()
            .lower()
        )

        self.entry.delete(
            0,
            "end"
        )

        if letter:
            self.guess(letter)


    # =========================
    # GUESS
    # =========================

    def guess(self, letter):

        if self.game_over:
            return

        if (
            letter in self.guessed
            or letter in self.wrong
        ):
            return


        # Correct

        if letter in self.word:

            self.guessed.add(
                letter
            )

            self.write_log(
                f"> INPUT '{letter.upper()}' ACCEPTED."
            )

            self.flash_status(
                "SIGNAL ACCEPTED.",
                GREEN
            )

            self.keys[letter].config(
                bg=GREEN,
                fg=BG
            )


        # Wrong

        else:

            self.wrong.add(
                letter
            )

            self.left_attempts -= 1

            self.write_log(
                f"> INPUT '{letter.upper()}' REJECTED."
            )

            self.flash_status(
                "WRONG INPUT.",
                RED
            )

            self.keys[letter].config(
                bg=RED,
                fg=BG
            )


        self.update_ui()


        # Win

        if all(
            char in self.guessed
            for char in self.word
        ):

            self.root.after(
                500,
                self.win
            )


        # Lose

        elif self.left_attempts <= 0:

            self.root.after(
                600,
                self.lose
            )


    # =========================
    # UPDATE UI
    # =========================

    def update_ui(self):

        display = " ".join(
            char.upper()
            if char in self.guessed
            else "_"

            for char in self.word
        )


        self.word_label.config(
            text=display
        )


        self.wrong_label.config(
            text="  ".join(
                sorted(
                    x.upper()
                    for x in self.wrong
                )
            )
            or "—"
        )


        self.attempt_label.config(
            text=(
                f"ATTEMPTS  "
                f"{self.left_attempts:02d}"
                f" / "
                f"{self.MAX_ATTEMPTS}"
            ),

            fg=(
                GREEN
                if self.left_attempts >= 4

                else YELLOW
                if self.left_attempts >= 2

                else RED
            )
        )


        self.draw_progress()


    # =========================
    # PROGRESS BAR
    # =========================

    def draw_progress(self):

        self.progress.delete(
            "all"
        )

        width = max(
            self.progress.winfo_width(),
            1
        )


        ratio = (
            self.left_attempts
            / self.MAX_ATTEMPTS
        )


        self.progress.create_rectangle(
            0,
            0,
            width * ratio,
            12,

            fill=(
                GREEN
                if ratio > .5

                else YELLOW
                if ratio > .2

                else RED
            ),

            outline=""
        )


    # =========================
    # STATUS
    # =========================

    def flash_status(
        self,
        text,
        color
    ):

        self.status_label.config(
            text=text,
            fg=color
        )


        self.root.after(
            1000,

            lambda:
            self.status_label.config(
                text="THE SYSTEM IS WATCHING.",
                fg=YELLOW
            )

            if not self.game_over
            else None
        )


    # =========================
    # LOG
    # =========================

    def write_log(self, text):

        self.log.config(
            state="normal"
        )

        self.log.insert(
            "end",
            text + "\n"
        )

        self.log.see(
            "end"
        )

        self.log.config(
            state="disabled"
        )


    # =========================
    # TYPEWRITER
    # =========================

    def type_dialog(
        self,
        text,
        callback=None
    ):

        if self.typing_job:

            self.root.after_cancel(
                self.typing_job
            )


        self.log.config(
            state="normal"
        )

        self.log.delete(
            "1.0",
            "end"
        )

        self.log.config(
            state="disabled"
        )


        index = 0


        def tick():

            nonlocal index


            if index < len(text):

                self.log.config(
                    state="normal"
                )

                self.log.insert(
                    "end",
                    text[index]
                )

                self.log.see(
                    "end"
                )

                self.log.config(
                    state="disabled"
                )


                index += 1


                self.typing_job = self.root.after(
                    28,
                    tick
                )


            elif callback:

                self.root.after(
                    500,
                    callback
                )


        tick()


    # =========================
    # ENABLE / DISABLE
    # =========================

    def disable_input(self):

        self.entry.config(
            state="disabled"
        )

        for btn in self.keys.values():

            btn.config(
                state="disabled"
            )


    def enable_input(self):

        self.entry.config(
            state="normal"
        )

        for btn in self.keys.values():

            btn.config(
                state="normal"
            )


    # =========================
    # WIN
    # =========================

    def win(self):

        self.game_over = True

        self.disable_input()


        self.status_label.config(
            text="ACCESS GRANTED.",
            fg=GREEN
        )


        self.write_log(
            "> !!! ANOMALY DETECTED: PLAYER SURVIVED !!!"
        )

        self.write_log(
            "> Opening exit channel..."
        )


        self.dialog_sequence(
            [

                ("Ohhhhhh...", 700),

                ("Interesting.", 900),

                ("You actually solved it.", 1000),

                (
                    f"{self.name}, "
                    "you're the first one to get this far.",
                    1200
                ),

                ("The door is open.", 900),

                ("You are free to go.", 1200),

                ("BUT...", 900),

                ("Remember this.", 900),

                (
                    "Every answer creates another question.",
                    1100
                ),

                ("And next time...", 1000),

                (
                    "I might choose a word you don't know.",
                    1200
                ),

                ("SESSION TERMINATED.", 0)

            ],

            GREEN
        )


    # =========================
    # LOSE
    # =========================

    def lose(self):

        self.game_over = True

        self.disable_input()


        self.status_label.config(
            text="ACCESS DENIED.",
            fg=RED
        )


        self.write_log(
            "> ALL ATTEMPTS EXHAUSTED."
        )

        self.write_log(
            "> CONTAINMENT PROTOCOL INITIALIZED."
        )


        self.dialog_sequence(
            [

                ("It's over...", 700),

                ("It's really over.", 900),

                ("You ran out of guesses.", 1000),

                ("ACCESS DENIED.", 1200),

                (
                    "Containment protocol initializing...",
                    1100
                ),

                (
                    "Locking the terminal...",
                    1000
                ),

                ("3...", 600),

                ("2...", 600),

                ("1...", 800),

                ("...", 900),

                ("Connection lost.", 1000),

                ("Maybe in another session...", 0)

            ],

            RED
        )


    # =========================
    # DIALOG SEQUENCE
    # =========================

    def dialog_sequence(
        self,
        lines,
        color
    ):

        self.dialog_lines = lines

        self.dialog_index = 0

        self.dialog_color = color

        self.show_next_dialog()


    def show_next_dialog(self):

        if (
            self.dialog_index
            >= len(self.dialog_lines)
        ):

            self.reset_btn.config(
                text="START NEW SESSION"
            )

            return


        text, delay = (
            self.dialog_lines[
                self.dialog_index
            ]
        )


        self.dialog_index += 1


        self.type_dialog_to_log(
            text,
            self.dialog_color
        )


        if delay:

            self.dialog_job = self.root.after(
                delay,
                self.show_next_dialog
            )

        else:

            self.reset_btn.config(
                text="START NEW SESSION"
            )


    # =========================
    # COLORED DIALOG
    # =========================

    def type_dialog_to_log(
        self,
        text,
        color
    ):

        self.log.config(
            state="normal"
        )

        self.log.insert(
            "end",
            "\n"
        )

        self.log.config(
            state="disabled"
        )


        index = 0


        def tick():

            nonlocal index


            if index < len(text):

                self.log.config(
                    state="normal"
                )

                self.log.insert(
                    "end",
                    text[index]
                )

                self.log.tag_config(
                    "dialog",
                    foreground=color
                )

                self.log.tag_add(
                    "dialog",
                    "end-1c",
                    "end"
                )

                self.log.see(
                    "end"
                )

                self.log.config(
                    state="disabled"
                )


                index += 1


                self.root.after(
                    35,
                    tick
                )


        tick()


# =========================
# START
# =========================

if __name__ == "__main__":

    root = tk.Tk()

    app = HangManGUI(
        root
    )

    root.mainloop()