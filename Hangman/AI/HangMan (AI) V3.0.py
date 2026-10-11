import random
import tkinter as tk


# =========================================================
# WORD DATABASE
# =========================================================

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


# =========================================================
# COLORS
# =========================================================

BG = "#080b10"
PANEL = "#0d1219"
PANEL_2 = "#111821"

TEXT = "#d9e4ef"
MUTED = "#657384"

CYAN = "#39d9ff"
GREEN = "#55f28c"
RED = "#ff3b5c"
YELLOW = "#ffd166"


# =========================================================
# GAME
# =========================================================

class HangManGUI:

    MAX_ATTEMPTS = 7

    def __init__(self, root):

        self.root = root

        self.root.title("NULL//WORD")
        self.root.geometry("1050x700")
        self.root.minsize(900, 620)

        self.root.configure(bg=BG)

        # -------------------------
        # GAME STATE
        # -------------------------

        self.name = ""
        self.word = ""

        self.guessed = set()
        self.wrong = set()

        self.left_attempts = self.MAX_ATTEMPTS

        self.game_over = False

        # -------------------------
        # ANIMATION STATE
        # -------------------------

        self.shake_running = False
        self.glitch_mode = False

        self.scanline_offset = 0
        self.crt_running = True

        self.overlay = None

        self.build_ui()

        self.start_crt_effect()

        self.show_intro()


    # =====================================================
    # MAIN UI
    # =====================================================

    def build_ui(self):

        # =================================================
        # CENTRAL CANVAS
        # =================================================

        self.canvas = tk.Canvas(
            self.root,
            bg=BG,
            highlightthickness=0
        )

        self.canvas.place(
            x=0,
            y=0,
            relwidth=1,
            relheight=1
        )


        # =================================================
        # ACTUAL UI
        # =================================================

        self.ui = tk.Frame(
            self.root,
            bg=BG
        )

        self.ui.place(
            x=0,
            y=0,
            relwidth=1,
            relheight=1
        )


        # =================================================
        # HEADER
        # =================================================

        self.header = tk.Frame(
            self.ui,
            bg=BG
        )

        self.header.pack(
            fill="x",
            padx=35,
            pady=(24, 10)
        )


        # -------------------------
        # Glitch title
        # -------------------------

        self.title_label = tk.Label(
            self.header,
            text="NULL//WORD",
            font=("Consolas", 25, "bold"),
            fg=CYAN,
            bg=BG
        )

        self.title_label.pack(
            side="left"
        )


        self.security_label = tk.Label(
            self.header,
            text="SECURITY LEVEL: UNKNOWN",
            font=("Consolas", 10, "bold"),
            fg=RED,
            bg=BG
        )

        self.security_label.pack(
            side="right",
            pady=8
        )


        # Header line

        self.header_line = tk.Frame(
            self.ui,
            bg=CYAN,
            height=1
        )

        self.header_line.pack(
            fill="x",
            padx=35
        )


        # =================================================
        # MAIN
        # =================================================

        self.main = tk.Frame(
            self.ui,
            bg=BG
        )

        self.main.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=22
        )


        # =================================================
        # LEFT PANEL
        # =================================================

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


        # =================================================
        # PROGRESS
        # =================================================

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


        # =================================================
        # WRONG GUESSES
        # =================================================

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


        # =================================================
        # TERMINAL
        # =================================================

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


        # =================================================
        # RIGHT PANEL
        # =================================================

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


        # =================================================
        # INPUT
        # =================================================

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


        # =================================================
        # KEYBOARD
        # =================================================

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

            button = tk.Button(
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

            button.grid(
                row=row,
                column=col,
                sticky="nsew",
                padx=3,
                pady=3
            )

            self.keys[
                letter.lower()
            ] = button


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


        # =================================================
        # RESTART
        # =================================================

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


        self.root.bind(
            "<KeyPress>",
            self.global_key
        )


    # =====================================================
    # CRT EFFECT
    # =====================================================

    def start_crt_effect(self):

        if not self.crt_running:
            return


        self.canvas.delete(
            "crt"
        )


        width = self.root.winfo_width()
        height = self.root.winfo_height()


        if width <= 1 or height <= 1:

            self.root.after(
                50,
                self.start_crt_effect
            )

            return


        # ---------------------------------------------
        # Scanlines
        # ---------------------------------------------

        for y in range(
            self.scanline_offset,
            height,
            6
        ):

            self.canvas.create_line(
                0,
                y,
                width,
                y,
                fill="#10151a",
                tags="crt"
            )


        self.scanline_offset += 1


        if self.scanline_offset >= 6:

            self.scanline_offset = 0


        # ---------------------------------------------
        # CRT vignette-like borders
        # ---------------------------------------------

        self.canvas.create_rectangle(
            0,
            0,
            width,
            8,
            fill="#030405",
            outline="",
            tags="crt"
        )

        self.canvas.create_rectangle(
            0,
            height - 8,
            width,
            height,
            fill="#030405",
            outline="",
            tags="crt"
        )


        # ---------------------------------------------
        # Tiny flicker
        # ---------------------------------------------

        if random.random() < 0.035:

            self.canvas.create_rectangle(
                0,
                random.randint(
                    0,
                    height
                ),
                width,
                random.randint(
                    0,
                    height
                ),
                fill="#142027",
                outline="",
                tags="crt"
            )


        self.root.after(
            70,
            self.start_crt_effect
        )


    # =====================================================
    # GLITCH TEXT
    # =====================================================

    def glitch_title(self):

        if self.game_over:
            return


        normal = "NULL//WORD"


        glitch_versions = [
            "NULL//WORD",
            "NUL█//WORD",
            "NULL//W0RD",
            "NUŁŁ//WORD",
            "NULL//W██D",
            "N̷U̷L̷L̷/̷/̷W̷O̷R̷D̷"
        ]


        if random.random() < 0.08:

            self.title_label.config(
                text=random.choice(
                    glitch_versions
                )
            )

        else:

            self.title_label.config(
                text=normal
            )


        self.root.after(
            random.randint(
                250,
                700
            ),
            self.glitch_title
        )


    # =====================================================
    # INTRO
    # =====================================================

    def show_intro(self):

        self.disable_input()

        self.glitch_title()

        self.type_dialog(
            "SYSTEM: connection established...\n"
            "SYSTEM: identity required.\n\n"
            "What is your name?",
            self.ask_name
        )


    # =====================================================
    # NAME
    # =====================================================

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


    # =====================================================
    # NEW GAME
    # =====================================================

    def new_game(self):

        self.remove_horror_overlay()


        self.word = random.choice(
            WORDS
        ).lower()


        self.guessed.clear()
        self.wrong.clear()


        self.left_attempts = (
            self.MAX_ATTEMPTS
        )


        self.game_over = False


        # Restore UI

        self.ui.place(
            x=0,
            y=0,
            relwidth=1,
            relheight=1
        )


        self.enable_input()

        self.update_ui()


        self.write_log(
            f"> SESSION STARTED // SUBJECT: {self.name}"
        )

        self.write_log(
            "> HIDDEN WORD LOADED."
        )

        self.write_log(
            "> SYSTEM STATUS: NORMAL"
        )


        self.status_label.config(
            text="THE SYSTEM IS WATCHING.",
            fg=YELLOW
        )


        self.reset_btn.config(
            text="RESTART SESSION"
        )


        self.entry.focus_set()


    # =====================================================
    # INPUT
    # =====================================================

    def filter_entry(self, event=None):

        value = self.entry.get().lower()

        filtered = "".join(
            char
            for char in value
            if char.isalpha()
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

            self.guess(
                letter
            )


    # =====================================================
    # GUESS
    # =====================================================

    def guess(self, letter):

        if self.game_over:
            return


        if (
            letter in self.guessed
            or letter in self.wrong
        ):
            return


        # ---------------------------------------------
        # CORRECT
        # ---------------------------------------------

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


            self.keys[
                letter
            ].config(
                bg=GREEN,
                fg=BG
            )


        # ---------------------------------------------
        # WRONG
        # ---------------------------------------------

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


            self.keys[
                letter
            ].config(
                bg=RED,
                fg=BG
            )


            # Tiny glitch on wrong answer

            self.root.after(
                50,
                lambda:
                self.glitch_effect(
                    2
                )
            )


        self.update_ui()


        # ---------------------------------------------
        # WIN
        # ---------------------------------------------

        if all(
            char in self.guessed
            for char in self.word
        ):

            self.root.after(
                500,
                self.win
            )


        # ---------------------------------------------
        # LOSE
        # ---------------------------------------------

        elif self.left_attempts <= 0:

            self.root.after(
                600,
                self.lose
            )


    # =====================================================
    # UPDATE UI
    # =====================================================

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
                f"ATTEMPTS "
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


    # =====================================================
    # PROGRESS
    # =====================================================

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


    # =====================================================
    # STATUS
    # =====================================================

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


    # =====================================================
    # LOG
    # =====================================================

    def write_log(
        self,
        text
    ):

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


    # =====================================================
    # TYPEWRITER
    # =====================================================

    def type_dialog(
        self,
        text,
        callback=None
    ):

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


                self.root.after(
                    28,
                    tick
                )


            elif callback:

                self.root.after(
                    500,
                    callback
                )


        tick()


    # =====================================================
    # ENABLE / DISABLE
    # =====================================================

    def disable_input(self):

        self.entry.config(
            state="disabled"
        )


        for button in self.keys.values():

            button.config(
                state="disabled"
            )


    def enable_input(self):

        self.entry.config(
            state="normal"
        )


        for button in self.keys.values():

            button.config(
                state="normal"
            )


    # =====================================================
    # WIN
    # =====================================================

    def win(self):

        self.game_over = True

        self.disable_input()


        self.status_label.config(
            text="ACCESS GRANTED.",
            fg=GREEN
        )


        self.write_log(
            "> ANOMALY DETECTED."
        )

        self.write_log(
            "> PLAYER SURVIVED."
        )

        self.write_log(
            "> EXIT CHANNEL OPEN."
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


    # =====================================================
    # LOSE
    # =====================================================

    def lose(self):

        self.game_over = True

        self.disable_input()


        self.status_label.config(
            text="CONNECTION FAILURE.",
            fg=RED
        )


        self.write_log(
            "> ALL ATTEMPTS EXHAUSTED."
        )

        self.write_log(
            "> SYSTEM CONTROL LOST."
        )

        self.write_log(
            "> UNKNOWN PROCESS DETECTED."
        )


        self.root.after(
            300,
            self.start_horror
        )


    # =====================================================
    # DIALOG SEQUENCE
    # =====================================================

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

            self.root.after(
                delay,
                self.show_next_dialog
            )

        else:

            self.reset_btn.config(
                text="START NEW SESSION"
            )


    # =====================================================
    # COLORED DIALOG
    # =====================================================

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


    # =====================================================
    # GLITCH
    # =====================================================

    def glitch_effect(
        self,
        count=8
    ):

        if count <= 0:

            self.restore_normal_ui()

            return


        glitch_colors = [
            RED,
            "#00ffff",
            "#ffffff",
            BG,
            "#ff1744"
        ]


        color = random.choice(
            glitch_colors
        )


        self.ui.configure(
            bg=color
        )


        self.root.after(
            random.randint(
                25,
                70
            ),

            lambda:
            self.glitch_effect(
                count - 1
            )
        )


    def restore_normal_ui(self):

        self.ui.configure(
            bg=BG
        )


    # =====================================================
    # SCREEN SHAKE
    # =====================================================

    def screen_shake(
        self,
        intensity=8,
        duration=500
    ):

        if self.shake_running:
            return


        self.shake_running = True


        original_x = (
            self.root.winfo_x()
        )

        original_y = (
            self.root.winfo_y()
        )


        def shake(elapsed):

            if elapsed >= duration:

                self.root.geometry(
                    f"+{original_x}+{original_y}"
                )

                self.shake_running = False

                return


            x = (
                original_x
                + random.randint(
                    -intensity,
                    intensity
                )
            )


            y = (
                original_y
                + random.randint(
                    -intensity,
                    intensity
                )
            )


            self.root.geometry(
                f"+{x}+{y}"
            )


            self.root.after(
                30,

                lambda:
                shake(
                    elapsed + 30
                )
            )


        shake(0)


    # =====================================================
    # RED FLASH
    # =====================================================

    def red_flash(
        self,
        duration=120
    ):

        flash = tk.Frame(
            self.root,
            bg=RED
        )


        flash.place(
            x=0,
            y=0,
            relwidth=1,
            relheight=1
        )


        self.root.after(
            duration,
            flash.destroy
        )


    # =====================================================
    # HORROR SEQUENCE
    # =====================================================

    def start_horror(self):

        # -------------------------
        # 1. RED FLASH
        # -------------------------

        self.red_flash(
            100
        )


        # -------------------------
        # 2. SCREEN SHAKE
        # -------------------------

        self.screen_shake(
            intensity=8,
            duration=550
        )


        # -------------------------
        # 3. GLITCH
        # -------------------------

        self.root.after(
            100,
            lambda:
            self.glitch_effect(
                12
            )
        )


        # -------------------------
        # 4. GLITCH TITLE
        # -------------------------

        self.root.after(
            1000,
            self.show_horror_title
        )


    # =====================================================
    # HORROR TITLE
    # =====================================================

    def show_horror_title(self):

        self.ui.place_forget()


        self.horror_canvas = tk.Canvas(
            self.root,
            bg="black",
            highlightthickness=0
        )


        self.horror_canvas.place(
            x=0,
            y=0,
            relwidth=1,
            relheight=1
        )


        self.horror_title_step(
            0
        )


    def horror_title_step(
        self,
        step
    ):

        if step >= 14:

            self.root.after(
                300,
                self.start_final_message
            )

            return


        self.horror_canvas.delete(
            "all"
        )


        titles = [

            "ACCESS DENIED",

            "ACCESS D3NIED",

            "ACCESS//DENIED",

            "A̷C̷C̷E̷S̷S̷",

            "ERROR",

            "SYSTEM FAILURE",

            "SYSTEM FAILURE",

            "NO SIGNAL",

            "NO SIGNAL",

            "WHO ARE YOU?",

            "WHO ARE YOU?",

            "UNKNOWN PROCESS",

            "UNKNOWN PROCESS",

            "ACCESS DENIED"

        ]


        text = titles[
            step
        ]


        color = (
            RED
            if step % 2 == 0
            else "#ffffff"
        )


        width = self.root.winfo_width()
        height = self.root.winfo_height()


        # ---------------------------------------------
        # RGB split / glitch layers
        # ---------------------------------------------

        if random.random() < .8:

            self.horror_canvas.create_text(
                width / 2 + random.randint(
                    -8,
                    8
                ),
                height / 2,
                text=text,
                font=(
                    "Consolas",
                    34,
                    "bold"
                ),
                fill="#00ffff"
            )


            self.horror_canvas.create_text(
                width / 2 + random.randint(
                    -8,
                    8
                ),
                height / 2,
                text=text,
                font=(
                    "Consolas",
                    34,
                    "bold"
                ),
                fill="#ff003c"
            )


        self.horror_canvas.create_text(
            width / 2,
            height / 2,
            text=text,
            font=(
                "Consolas",
                34,
                "bold"
            ),
            fill=color
        )


        # Random horizontal glitch bars

        for _ in range(
            random.randint(1, 5)
        ):

            y = random.randint(
                0,
                max(
                    height,
                    1
                )
            )


            self.horror_canvas.create_rectangle(
                random.randint(
                    0,
                    max(
                        width // 2,
                        1
                    )
                ),
                y,
                random.randint(
                    max(
                        width // 2,
                        1
                    ),
                    max(
                        width,
                        1
                    )
                ),
                y + random.randint(
                    1,
                    5
                ),
                fill=random.choice(
                    [
                        RED,
                        CYAN,
                        "#ffffff"
                    ]
                ),
                outline=""
            )


        self.screen_shake(
            intensity=(
                3
                if step < 8
                else 7
            ),
            duration=100
        )


        self.root.after(
            random.randint(
                100,
                190
            ),

            lambda:
            self.horror_title_step(
                step + 1
            )
        )


    # =====================================================
    # FINAL MESSAGE
    # =====================================================

    def start_final_message(self):

        self.horror_canvas.delete(
            "all"
        )


        self.type_horror_message()


    def type_horror_message(self):

        text = (
            "CONNECTION LOST.\n\n"
            "...\n\n"
            "YOU WERE NEVER\n"
            "PLAYING ALONE."
        )


        self.horror_canvas.delete(
            "all"
        )


        width = self.root.winfo_width()
        height = self.root.winfo_height()


        label = self.horror_canvas.create_text(
            width / 2,
            height / 2,
            text="",
            font=(
                "Consolas",
                17,
                "bold"
            ),
            fill=RED,
            justify="center"
        )


        index = 0


        def tick():

            nonlocal index


            if index < len(text):

                self.horror_canvas.itemconfig(
                    label,
                    text=text[
                        :index + 1
                    ]
                )


                # Occasional micro glitch

                if random.random() < .12:

                    self.screen_shake(
                        intensity=3,
                        duration=80
                    )


                index += 1


                self.root.after(
                    55,
                    tick
                )


            else:

                self.root.after(
                    3000,
                    self.final_screen
                )


        tick()


    # =====================================================
    # FINAL SCREEN
    # =====================================================

    def final_screen(self):

        self.horror_canvas.delete(
            "all"
        )


        width = self.root.winfo_width()
        height = self.root.winfo_height()


        self.horror_canvas.create_text(
            width / 2,
            height * .40,
            text=(
                "SESSION TERMINATED"
            ),
            font=(
                "Consolas",
                17,
                "bold"
            ),
            fill="#404850"
        )


        self.horror_canvas.create_text(
            width / 2,
            height * .49,
            text="NULL//WORD",
            font=(
                "Consolas",
                24,
                "bold"
            ),
            fill="#252b31"
        )


        self.horror_canvas.create_text(
            width / 2,
            height * .55,
            text="v1.0",
            font=(
                "Consolas",
                10
            ),
            fill="#252b31"
        )


        button = tk.Button(
            self.root,
            text="START NEW SESSION",
            font=(
                "Consolas",
                10,
                "bold"
            ),
            fg=BG,
            bg=CYAN,
            activebackground=GREEN,
            relief="flat",
            command=self.new_game
        )


        button.place(
            relx=.5,
            rely=.66,
            anchor="center",
            width=240,
            height=42
        )


    # =====================================================
    # REMOVE HORROR
    # =====================================================

    def remove_horror_overlay(self):

        if hasattr(
            self,
            "horror_canvas"
        ):

            try:

                self.horror_canvas.destroy()

            except tk.TclError:

                pass


        self.ui.place(
            x=0,
            y=0,
            relwidth=1,
            relheight=1
        )


    # =====================================================
    # START
    # =====================================================


if __name__ == "__main__":

    root = tk.Tk()

    game = HangManGUI(
        root
    )

    root.mainloop()