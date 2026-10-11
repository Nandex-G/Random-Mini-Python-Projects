
import pygame
import random
import math
import sys

# ============================================================
# NULL//WORD
# Pygame Horror Word Game
# ============================================================

pygame.init()

# ------------------------------------------------------------
# SETTINGS
# ------------------------------------------------------------

WIDTH = 1280
HEIGHT = 720
FPS = 60

TITLE = "NULL//WORD"

BG = (5, 7, 10)
PANEL = (10, 14, 20)
PANEL_LIGHT = (16, 22, 30)

WHITE = (225, 235, 245)
GREY = (100, 115, 130)
DARK_GREY = (45, 55, 65)

CYAN = (45, 220, 255)
GREEN = (70, 255, 140)
RED = (255, 45, 75)
YELLOW = (255, 210, 70)
PURPLE = (160, 80, 255)

MAX_ATTEMPTS = 7


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


# ------------------------------------------------------------
# SCREEN
# ------------------------------------------------------------

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

clock = pygame.time.Clock()


# ------------------------------------------------------------
# FONTS
# ------------------------------------------------------------

FONT_BIG = pygame.font.SysFont("consolas", 52, bold=True)
FONT_TITLE = pygame.font.SysFont("consolas", 72, bold=True)
FONT_MED = pygame.font.SysFont("consolas", 24, bold=True)
FONT_SMALL = pygame.font.SysFont("consolas", 16)
FONT_TINY = pygame.font.SysFont("consolas", 13)


# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------

def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))


def lerp(a, b, amount):
    return a + (b - a) * amount


def draw_text(surface, text, font, color, x, y, center=False):
    image = font.render(text, True, color)

    if center:
        rect = image.get_rect(center=(x, y))
    else:
        rect = image.get_rect(topleft=(x, y))

    surface.blit(image, rect)
    return rect


def draw_center_text(surface, text, font, color, y):
    return draw_text(
        surface,
        text,
        font,
        color,
        WIDTH // 2,
        y,
        center=True
    )


# ------------------------------------------------------------
# PARTICLE
# ------------------------------------------------------------

class Particle:

    def __init__(self, x, y, color=None):
        self.x = x
        self.y = y

        self.vx = random.uniform(-2.0, 2.0)
        self.vy = random.uniform(-2.0, 2.0)

        self.life = random.randint(20, 80)
        self.max_life = self.life

        self.size = random.randint(1, 3)

        self.color = color or random.choice([
            CYAN,
            RED,
            PURPLE,
            GREY,
            WHITE
        ])

    def update(self):

        self.x += self.vx
        self.y += self.vy

        self.vx *= 0.98
        self.vy *= 0.98

        self.life -= 1

    def draw(self, surface):

        if self.life <= 0:
            return

        alpha = int(
            255 * (self.life / self.max_life)
        )

        temp = pygame.Surface(
            (self.size * 4, self.size * 4),
            pygame.SRCALPHA
        )

        color = (
            self.color[0],
            self.color[1],
            self.color[2],
            alpha
        )

        pygame.draw.circle(
            temp,
            color,
            (self.size * 2, self.size * 2),
            self.size
        )

        surface.blit(
            temp,
            (
                int(self.x - self.size * 2),
                int(self.y - self.size * 2)
            )
        )


# ------------------------------------------------------------
# PARTICLE SYSTEM
# ------------------------------------------------------------

class ParticleSystem:

    def __init__(self):
        self.particles = []

    def burst(self, x, y, amount=30, color=None):

        for _ in range(amount):
            self.particles.append(
                Particle(x, y, color)
            )

    def ambient(self):

        if random.random() < 0.12:

            self.particles.append(
                Particle(
                    random.randint(0, WIDTH),
                    random.randint(0, HEIGHT),
                    random.choice([
                        (30, 80, 90),
                        (50, 50, 70),
                        (80, 40, 50)
                    ])
                )
            )

    def update(self):

        for particle in self.particles:
            particle.update()

        self.particles = [
            p for p in self.particles
            if p.life > 0
        ]

    def draw(self, surface):

        for particle in self.particles:
            particle.draw(surface)


# ------------------------------------------------------------
# GLITCH SYSTEM
# ------------------------------------------------------------

class Glitch:

    def __init__(self):

        self.timer = 0
        self.strength = 0

    def trigger(self, strength=10):

        self.timer = random.randint(5, 15)
        self.strength = strength

    def update(self):

        if self.timer > 0:
            self.timer -= 1

    def draw(self, surface):

        if self.timer <= 0:
            return

        for _ in range(
            random.randint(2, 6)
        ):

            y = random.randint(
                0,
                HEIGHT - 10
            )

            h = random.randint(
                2,
                10
            )

            offset = random.randint(
                -self.strength,
                self.strength
            )

            strip = surface.subsurface(
                pygame.Rect(
                    0,
                    y,
                    WIDTH,
                    min(h, HEIGHT - y)
                )
            ).copy()

            surface.blit(
                strip,
                (offset, y)
            )

        # RGB split

        if random.random() < 0.5:

            copy = surface.copy()

            red_overlay = pygame.Surface(
                surface.get_size(),
                pygame.SRCALPHA
            )

            red_overlay.fill(
                (255, 0, 50, 25)
            )

            surface.blit(
                red_overlay,
                (
                    random.randint(-3, 3),
                    0
                )
            )

            surface.blit(
                copy,
                (
                    random.randint(-2, 2),
                    random.randint(-1, 1)
                ),
                special_flags=pygame.BLEND_RGB_ADD
            )


# ------------------------------------------------------------
# SCREEN SHAKE
# ------------------------------------------------------------

class Shake:

    def __init__(self):
        self.timer = 0
        self.strength = 0

    def trigger(self, strength=8, duration=20):

        self.strength = strength
        self.timer = duration

    def update(self):

        if self.timer > 0:
            self.timer -= 1

    def offset(self):

        if self.timer <= 0:
            return 0, 0

        return (
            random.randint(
                -self.strength,
                self.strength
            ),
            random.randint(
                -self.strength,
                self.strength
            )
        )


# ------------------------------------------------------------
# CRT EFFECT
# ------------------------------------------------------------

def draw_crt(surface):

    overlay = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    # Scanlines

    for y in range(0, HEIGHT, 4):

        pygame.draw.line(
            overlay,
            (0, 0, 0, 45),
            (0, y),
            (WIDTH, y)
        )

    # Slight vignette

    vignette = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    for i in range(12):

        alpha = int(
            3 + i * 2
        )

        pygame.draw.rect(
            vignette,
            (0, 0, 0, alpha),
            (
                i * 10,
                i * 7,
                WIDTH - i * 20,
                HEIGHT - i * 14
            ),
            8
        )

    surface.blit(
        overlay,
        (0, 0)
    )


# ------------------------------------------------------------
# NOISE
# ------------------------------------------------------------

def draw_noise(surface, amount=100):

    for _ in range(amount):

        x = random.randrange(WIDTH)
        y = random.randrange(HEIGHT)

        color = random.choice([
            (30, 40, 45),
            (50, 50, 55),
            (20, 30, 35),
            (80, 80, 80)
        ])

        pygame.draw.rect(
            surface,
            color,
            (x, y, 1, 1)
        )


# ------------------------------------------------------------
# BUTTON
# ------------------------------------------------------------

class Button:

    def __init__(
        self,
        rect,
        text,
        color=CYAN
    ):

        self.rect = pygame.Rect(rect)
        self.text = text
        self.color = color

        self.hover = False
        self.clicked = False

    def update(self):

        mouse = pygame.mouse.get_pos()

        self.hover = self.rect.collidepoint(
            mouse
        )

    def draw(self, surface):

        color = self.color

        if self.hover:
            bg = color
        else:
            bg = PANEL_LIGHT

        pygame.draw.rect(
            surface,
            bg,
            self.rect,
            border_radius=4
        )

        pygame.draw.rect(
            surface,
            color,
            self.rect,
            1,
            border_radius=4
        )

        text_color = (
            BG if self.hover else color
        )

        draw_text(
            surface,
            self.text,
            FONT_SMALL,
            text_color,
            self.rect.centerx,
            self.rect.centery,
            center=True
        )

    def is_clicked(self, event):

        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


# ------------------------------------------------------------
# KEY
# ------------------------------------------------------------

class LetterButton:

    def __init__(self, letter, rect):

        self.letter = letter
        self.rect = pygame.Rect(rect)

        self.state = "normal"

    def draw(self, surface):

        if self.state == "correct":
            color = GREEN

        elif self.state == "wrong":
            color = RED

        else:
            color = DARK_GREY

        if self.state == "normal":

            if self.rect.collidepoint(
                pygame.mouse.get_pos()
            ):
                bg = PANEL_LIGHT
            else:
                bg = PANEL

        else:
            bg = tuple(
                int(x * 0.25)
                for x in color
            )

        pygame.draw.rect(
            surface,
            bg,
            self.rect,
            border_radius=3
        )

        pygame.draw.rect(
            surface,
            color,
            self.rect,
            1,
            border_radius=3
        )

        draw_text(
            surface,
            self.letter.upper(),
            FONT_SMALL,
            color,
            self.rect.centerx,
            self.rect.centery,
            center=True
        )

    def clicked(self, event):

        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


# ------------------------------------------------------------
# GAME
# ------------------------------------------------------------

class Game:

    def __init__(self):

        self.running = True

        self.scene = "menu"

        self.player_name = "UNKNOWN"

        self.word = ""
        self.guessed = set()
        self.wrong = set()

        self.attempts = MAX_ATTEMPTS

        self.particles = ParticleSystem()
        self.glitch = Glitch()
        self.shake = Shake()

        self.dialog = []
        self.dialog_index = 0
        self.dialog_text = ""
        self.dialog_progress = 0

        self.dialog_speed = 2
        self.dialog_timer = 0

        self.intro_timer = 0

        self.horror_timer = 0
        self.horror_stage = 0

        self.final_timer = 0

        self.name_input = ""
        self.cursor_timer = 0

        self.logs = []

        self.flash_timer = 0
        self.flash_color = RED

        self.keys = []

        self.create_keyboard()

        self.restart_button = Button(
            (
                WIDTH // 2 - 120,
                HEIGHT - 85,
                240,
                42
            ),
            "NEW SESSION",
            CYAN
        )

        self.menu_button = Button(
            (
                WIDTH // 2 - 120,
                HEIGHT - 85,
                240,
                42
            ),
            "START SESSION",
            CYAN
        )

    # --------------------------------------------------------
    # KEYBOARD
    # --------------------------------------------------------

    def create_keyboard(self):

        self.keys.clear()

        letters = "abcdefghijklmnopqrstuvwxyz"

        start_x = 720
        start_y = 390

        key_w = 55
        key_h = 42

        gap = 7

        for index, letter in enumerate(letters):

            row = index // 7
            col = index % 7

            x = start_x + col * (
                key_w + gap
            )

            y = start_y + row * (
                key_h + gap
            )

            self.keys.append(
                LetterButton(
                    letter,
                    (
                        x,
                        y,
                        key_w,
                        key_h
                    )
                )
            )

    # --------------------------------------------------------
    # START GAME
    # --------------------------------------------------------

    def start_game(self):

        self.word = random.choice(
            WORDS
        ).lower()

        self.guessed.clear()
        self.wrong.clear()

        self.attempts = MAX_ATTEMPTS

        self.logs.clear()

        self.scene = "game"

        self.glitch.timer = 0
        self.shake.timer = 0

        for key in self.keys:
            key.state = "normal"

        self.log(
            "> CONNECTION ESTABLISHED"
        )

        self.log(
            "> HIDDEN WORD LOADED"
        )

        self.log(
            "> SUBJECT: " + self.player_name.upper()
        )

        self.log(
            "> SYSTEM STATUS: NORMAL"
        )

    # --------------------------------------------------------
    # LOG
    # --------------------------------------------------------

    def log(self, text):

        self.logs.append(text)

        if len(self.logs) > 8:
            self.logs.pop(0)

    # --------------------------------------------------------
    # GUESS
    # --------------------------------------------------------

    def guess(self, letter):

        if self.scene != "game":
            return

        if letter in self.guessed:
            return

        if letter in self.wrong:
            return

        if letter in self.word:

            self.guessed.add(letter)

            for key in self.keys:

                if key.letter == letter:
                    key.state = "correct"

            self.log(
                f"> INPUT '{letter.upper()}' ACCEPTED"
            )

            self.particles.burst(
                random.randint(250, 650),
                random.randint(200, 350),
                15,
                GREEN
            )

        else:

            self.wrong.add(letter)

            self.attempts -= 1

            for key in self.keys:

                if key.letter == letter:
                    key.state = "wrong"

            self.log(
                f"> INPUT '{letter.upper()}' REJECTED"
            )

            self.glitch.trigger(
                random.randint(5, 12)
            )

            self.shake.trigger(
                5,
                12
            )

            self.flash_timer = 5

            self.flash_color = RED

            self.particles.burst(
                WIDTH // 2,
                300,
                12,
                RED
            )

        # WIN

        if all(
            char in self.guessed
            for char in self.word
        ):

            self.start_win()

        # LOSE

        elif self.attempts <= 0:

            self.start_lose()

    # --------------------------------------------------------
    # WIN
    # --------------------------------------------------------

    def start_win(self):

        self.scene = "win"

        self.dialog = [
            "Ohhhhhh...",
            "Interesting.",
            "You actually solved it.",
            f"{self.player_name}, you're the first one to get this far.",
            "The door is open.",
            "You are free to go.",
            "BUT...",
            "Remember this.",
            "Every answer creates another question.",
            "And next time...",
            "I might choose a word you don't know.",
            "SESSION TERMINATED."
        ]

        self.dialog_index = 0
        self.dialog_text = ""
        self.dialog_progress = 0

        self.particles.burst(
            WIDTH // 2,
            HEIGHT // 2,
            80,
            GREEN
        )

    # --------------------------------------------------------
    # LOSE
    # --------------------------------------------------------

    def start_lose(self):

        self.scene = "horror"

        self.horror_timer = 0
        self.horror_stage = 0

        self.glitch.trigger(20)

        self.shake.trigger(
            12,
            30
        )

        self.flash_timer = 10
        self.flash_color = RED

        self.particles.burst(
            WIDTH // 2,
            HEIGHT // 2,
            100,
            RED
        )

    # --------------------------------------------------------
    # DIALOG
    # --------------------------------------------------------

    def update_dialog(self):

        if self.dialog_index >= len(
            self.dialog
        ):
            return

        current = self.dialog[
            self.dialog_index
        ]

        if self.dialog_progress < len(current):

            self.dialog_progress += (
                self.dialog_speed
            )

        else:

            self.dialog_timer += 1

            if self.dialog_timer > 70:

                self.dialog_index += 1

                self.dialog_progress = 0

                self.dialog_timer = 0

    # --------------------------------------------------------
    # DRAW HEADER
    # --------------------------------------------------------

    def draw_header(self, surface):

        draw_text(
            surface,
            "NULL//WORD",
            FONT_MED,
            CYAN,
            35,
            25
        )

        draw_text(
            surface,
            "SECURITY LEVEL: UNKNOWN",
            FONT_TINY,
            RED,
            WIDTH - 250,
            30
        )

        pygame.draw.line(
            surface,
            (30, 70, 80),
            (35, 65),
            (WIDTH - 35, 65)
        )

    # --------------------------------------------------------
    # DRAW PANEL
    # --------------------------------------------------------

    def panel(
        self,
        surface,
        rect,
        border=CYAN
    ):

        rect = pygame.Rect(rect)

        pygame.draw.rect(
            surface,
            PANEL,
            rect,
            border_radius=4
        )

        pygame.draw.rect(
            surface,
            border,
            rect,
            1,
            border_radius=4
        )

    # --------------------------------------------------------
    # DRAW GAME
    # --------------------------------------------------------

    def draw_game(self, surface):

        self.draw_header(surface)

        # LEFT PANEL

        self.panel(
            surface,
            (35, 100, 620, 520)
        )

        draw_text(
            surface,
            "UNKNOWN WORD",
            FONT_SMALL,
            GREY,
            60,
            125
        )

        display = ""

        for char in self.word:

            if char in self.guessed:
                display += char.upper()
            else:
                display += "_"

            display += " "

        draw_center_text(
            surface,
            display,
            FONT_BIG,
            WHITE,
            225
        )

        # STATUS

        status_color = (
            GREEN
            if self.attempts >= 4
            else YELLOW
            if self.attempts >= 2
            else RED
        )

        draw_center_text(
            surface,
            f"ATTEMPTS  {self.attempts:02d} / {MAX_ATTEMPTS}",
            FONT_MED,
            status_color,
            290
        )

        # PROGRESS BAR

        bar = pygame.Rect(
            90,
            325,
            510,
            10
        )

        pygame.draw.rect(
            surface,
            (25, 30, 35),
            bar
        )

        ratio = (
            self.attempts /
            MAX_ATTEMPTS
        )

        pygame.draw.rect(
            surface,
            status_color,
            (
                bar.x,
                bar.y,
                int(
                    bar.width * ratio
                ),
                bar.height
            )
        )

        # FAILED INPUTS

        draw_text(
            surface,
            "FAILED INPUTS",
            FONT_TINY,
            GREY,
            60,
            365
        )

        wrong = "  ".join(
            x.upper()
            for x in sorted(
                self.wrong
            )
        )

        draw_text(
            surface,
            wrong if wrong else "—",
            FONT_MED,
            RED,
            60,
            390
        )

        # LOG

        pygame.draw.rect(
            surface,
            (5, 8, 12),
            (60, 435, 570, 155)
        )

        for i, line in enumerate(
            self.logs
        ):

            draw_text(
                surface,
                line,
                FONT_TINY,
                (
                    90,
                    120,
                    135
                ),
                75,
                448 + i * 17
            )

        # RIGHT PANEL

        self.panel(
            surface,
            (680, 100, 565, 520)
        )

        draw_text(
            surface,
            "INPUT TERMINAL",
            FONT_SMALL,
            GREY,
            710,
            125
        )

        # Terminal line

        pygame.draw.rect(
            surface,
            (4, 7, 10),
            (710, 170, 505, 60)
        )

        pygame.draw.rect(
            surface,
            CYAN,
            (710, 170, 505, 60),
            1
        )

        draw_text(
            surface,
            "> ENTER LETTER",
            FONT_SMALL,
            CYAN,
            730,
            188
        )

        # Keyboard

        for key in self.keys:
            key.draw(surface)

        # Hint

        draw_text(
            surface,
            "TYPE A LETTER OR CLICK A KEY",
            FONT_TINY,
            GREY,
            710,
            575
        )

    # --------------------------------------------------------
    # MENU
    # --------------------------------------------------------

    def draw_menu(self, surface):

        # animated background

        center_x = WIDTH // 2
        center_y = HEIGHT // 2

        pulse = (
            math.sin(
                pygame.time.get_ticks()
                * 0.002
            ) + 1
        ) / 2

        # rings

        for radius in range(
            80,
            500,
            70
        ):

            alpha = int(
                15 * (1 - radius / 550)
            )

            temp = pygame.Surface(
                (WIDTH, HEIGHT),
                pygame.SRCALPHA
            )

            pygame.draw.circle(
                temp,
                (
                    30,
                    200,
                    240,
                    alpha
                ),
                (
                    center_x,
                    center_y
                ),
                radius
            )

            surface.blit(
                temp,
                (0, 0)
            )

        draw_center_text(
            surface,
            "NULL//WORD",
            FONT_TITLE,
            CYAN,
            220
        )

        draw_center_text(
            surface,
            "A WORD GUESSING GAME",
            FONT_SMALL,
            GREY,
            285
        )

        # subtitle

        draw_center_text(
            surface,
            "SOMETHING IS WATCHING.",
            FONT_MED,
            RED,
            345
        )

        self.menu_button.update()
        self.menu_button.draw(surface)

        draw_center_text(
            surface,
            "ENTER TO BEGIN",
            FONT_TINY,
            GREY,
            610
        )

    # --------------------------------------------------------
    # NAME SCREEN
    # --------------------------------------------------------

    def draw_name(self, surface):

        draw_center_text(
            surface,
            "IDENTIFICATION REQUIRED",
            FONT_MED,
            CYAN,
            190
        )

        draw_center_text(
            surface,
            "What is your name?",
            FONT_SMALL,
            GREY,
            250
        )

        rect = pygame.Rect(
            WIDTH // 2 - 250,
            300,
            500,
            65
        )

        pygame.draw.rect(
            surface,
            PANEL,
            rect
        )

        pygame.draw.rect(
            surface,
            CYAN,
            rect,
            1
        )

        cursor = ""

        if (
            pygame.time.get_ticks()
            // 500
        ) % 2 == 0:
            cursor = "_"

        draw_text(
            surface,
            self.name_input + cursor,
            FONT_MED,
            WHITE,
            rect.x + 20,
            rect.y + 18
        )

        draw_center_text(
            surface,
            "PRESS ENTER TO CONNECT",
            FONT_TINY,
            GREY,
            410
        )

    # --------------------------------------------------------
    # WIN SCREEN
    # --------------------------------------------------------

    def draw_win(self, surface):

        # green particles

        draw_center_text(
            surface,
            "ACCESS GRANTED",
            FONT_BIG,
            GREEN,
            130
        )

        draw_center_text(
            surface,
            "ANOMALY DETECTED",
            FONT_SMALL,
            GREY,
            200
        )

        # Dialog box

        box = pygame.Rect(
            220,
            260,
            840,
            250
        )

        self.panel(
            surface,
            box,
            GREEN
        )

        if self.dialog_index < len(
            self.dialog
        ):

            text = self.dialog[
                self.dialog_index
            ]

            visible = text[
                :int(self.dialog_progress)
            ]

            draw_center_text(
                surface,
                visible,
                FONT_MED,
                GREEN,
                380
            )

        else:

            draw_center_text(
                surface,
                "SESSION TERMINATED.",
                FONT_MED,
                GREEN,
                380
            )

            self.restart_button.update()
            self.restart_button.draw(surface)

    # --------------------------------------------------------
    # HORROR
    # --------------------------------------------------------

    def draw_horror(self, surface):

        self.horror_timer += 1

        # Completely dark

        surface.fill(
            (2, 2, 4)
        )

        stage = self.horror_timer // 35

        messages = [
            "ACCESS DENIED",
            "SYSTEM FAILURE",
            "NO SIGNAL",
            "UNKNOWN PROCESS",
            "WHO ARE YOU?",
            "WHO IS PLAYING?",
            "CONNECTION LOST"
        ]

        if stage >= len(messages):
            stage = len(messages) - 1

        text = messages[
            stage
        ]

        # Flickering text

        if random.random() < 0.8:

            color = (
                RED
                if random.random() < 0.6
                else WHITE
            )

            x = WIDTH // 2 + random.randint(
                -5,
                5
            )

            y = HEIGHT // 2 + random.randint(
                -5,
                5
            )

            # RGB split

            draw_center_text(
                surface,
                text,
                FONT_BIG,
                CYAN,
                y + random.randint(-2, 2)
            )

            draw_center_text(
                surface,
                text,
                FONT_BIG,
                RED,
                y + random.randint(-2, 2)
            )

            draw_center_text(
                surface,
                text,
                FONT_BIG,
                color,
                y
            )

        # glitch bars

        for _ in range(
            random.randint(2, 8)
        ):

            y = random.randint(
                0,
                HEIGHT
            )

            pygame.draw.rect(
                surface,
                random.choice([
                    RED,
                    CYAN,
                    WHITE
                ]),
                (
                    random.randint(
                        0,
                        WIDTH // 2
                    ),
                    y,
                    random.randint(
                        50,
                        WIDTH
                    ),
                    random.randint(
                        1,
                        5
                    )
                )
            )

        # After a while show final message

        if self.horror_timer > 280:

            surface.fill(
                (2, 2, 4)
            )

            text_lines = [
                "CONNECTION LOST.",
                "",
                "...",
                "",
                "YOU WERE NEVER",
                "PLAYING ALONE."
            ]

            for i, line in enumerate(
                text_lines
            ):

                draw_center_text(
                    surface,
                    line,
                    FONT_MED,
                    RED,
                    250 + i * 45
                )

        if self.horror_timer > 520:

            self.scene = "final"

    # --------------------------------------------------------
    # FINAL
    # --------------------------------------------------------

    def draw_final(self, surface):

        surface.fill(
            (3, 4, 6)
        )

        draw_center_text(
            surface,
            "SESSION TERMINATED",
            FONT_MED,
            (60, 70, 80),
            250
        )

        draw_center_text(
            surface,
            "NULL//WORD",
            FONT_BIG,
            (35, 42, 48),
            330
        )

        draw_center_text(
            surface,
            "v1.0",
            FONT_TINY,
            (40, 45, 50),
            390
        )

        self.restart_button.update()
        self.restart_button.draw(surface)

    # --------------------------------------------------------
    # INPUT
    # --------------------------------------------------------

    def handle_event(self, event):

        if event.type == pygame.QUIT:

            self.running = False
            return

        # ----------------------------------------
        # MENU
        # ----------------------------------------

        if self.scene == "menu":

            if self.menu_button.is_clicked(
                event
            ):

                self.scene = "name"

            if (
                event.type ==
                pygame.KEYDOWN
                and event.key ==
                pygame.K_RETURN
            ):

                self.scene = "name"

        # ----------------------------------------
        # NAME
        # ----------------------------------------

        elif self.scene == "name":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:

                    self.player_name = (
                        self.name_input.strip()
                        or "UNKNOWN"
                    )

                    self.start_game()

                elif event.key == pygame.K_BACKSPACE:

                    self.name_input = (
                        self.name_input[:-1]
                    )

                elif (
                    event.unicode.isprintable()
                    and len(self.name_input) < 18
                ):

                    self.name_input += (
                        event.unicode
                    )

        # ----------------------------------------
        # GAME
        # ----------------------------------------

        elif self.scene == "game":

            if event.type == pygame.KEYDOWN:

                if event.unicode.isalpha():

                    letter = (
                        event.unicode
                        .lower()
                    )

                    self.guess(letter)

            for key in self.keys:

                if key.clicked(event):

                    self.guess(
                        key.letter
                    )

        # ----------------------------------------
        # WIN
        # ----------------------------------------

        elif self.scene == "win":

            if self.dialog_index >= len(
                self.dialog
            ):

                if self.restart_button.is_clicked(
                    event
                ):

                    self.start_game()

        # ----------------------------------------
        # FINAL
        # ----------------------------------------

        elif self.scene == "final":

            if self.restart_button.is_clicked(
                event
            ):

                self.start_game()

            if (
                event.type ==
                pygame.KEYDOWN
                and event.key ==
                pygame.K_RETURN
            ):

                self.start_game()

    # --------------------------------------------------------
    # UPDATE
    # --------------------------------------------------------

    def update(self):

        self.particles.ambient()
        self.particles.update()

        self.glitch.update()
        self.shake.update()

        if self.flash_timer > 0:
            self.flash_timer -= 1

        if self.scene == "win":

            self.update_dialog()

    # --------------------------------------------------------
    # DRAW
    # --------------------------------------------------------

    def draw(self):

        # Background

        screen.fill(BG)

        # subtle moving background noise

        for _ in range(20):

            x = random.randint(
                0,
                WIDTH
            )

            y = random.randint(
                0,
                HEIGHT
            )

            pygame.draw.circle(
                screen,
                (10, 15, 20),
                (x, y),
                1
            )

        # Scene

        if self.scene == "menu":

            self.draw_menu(screen)

        elif self.scene == "name":

            self.draw_name(screen)

        elif self.scene == "game":

            self.draw_game(screen)

        elif self.scene == "win":

            self.draw_win(screen)

        elif self.scene == "horror":

            self.draw_horror(screen)

        elif self.scene == "final":

            self.draw_final(screen)

        # Particles

        self.particles.draw(screen)

        # CRT

        draw_crt(screen)

        # Glitch

        self.glitch.draw(screen)

        # Flash

        if self.flash_timer > 0:

            overlay = pygame.Surface(
                (WIDTH, HEIGHT),
                pygame.SRCALPHA
            )

            alpha = min(
                100,
                self.flash_timer * 15
            )

            overlay.fill(
                (
                    self.flash_color[0],
                    self.flash_color[1],
                    self.flash_color[2],
                    alpha
                )
            )

            screen.blit(
                overlay,
                (0, 0)
            )

        # Shake

        # We render to the main screen first.
        # For a stronger shake effect, the whole
        # game can later be moved to a buffer.

        pygame.display.flip()

    # --------------------------------------------------------
    # LOOP
    # --------------------------------------------------------

    def run(self):

        while self.running:

            for event in pygame.event.get():

                self.handle_event(
                    event
                )

            self.update()
            self.draw()

            clock.tick(FPS)

        pygame.quit()
        sys.exit()


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    game = Game()
    game.run()
