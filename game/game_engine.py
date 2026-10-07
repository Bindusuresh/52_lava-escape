import pygame
import random

from game.player import Player
from game.world import (
    generate_platforms,
    draw_lava
)


WIDTH, HEIGHT = 500, 640
FPS = 60

BG = (20, 15, 30)
GROUND_Y = HEIGHT + 200


class GameEngine:

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(
            (WIDTH, HEIGHT)
        )

        pygame.display.set_caption(
            "Lava Escape"
        )

        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont(
            "monospace",
            24,
            bold=True
        )

        self.small_font = pygame.font.SysFont(
            "monospace",
            18,
            bold=True
        )

        self.big_font = pygame.font.SysFont(
            "monospace",
            42,
            bold=True
        )

        self.reset()

    def reset(self):

        self.platforms = generate_platforms(
            WIDTH,
            GROUND_Y
        )

        self.player = Player(
            WIDTH // 2 - 16,
            GROUND_Y - 50
        )

        self.cam_y = 0

        # Lava
        self.lava_y = GROUND_Y + 60
        self.lava_rise = 0.4

        # Lava surge system
        self.surge_active = False
        self.surge_timer = 0
        self.next_surge = random.randint(
            600,
            900
        )

        self.normal_lava_rise = 0.4
        self.surge_lava_rise = 2.0

        self.score = 0

        self.game_over = False
        self.won = False

        self.top_y = self.platforms[-1].rect.y

        self.frame = 0

    def handle_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False

            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_r
            ):
                self.reset()

        return True

    def update(self):

        if self.game_over or self.won:
            return

        keys = pygame.key.get_pressed()

        # -------------------------
        # PLAYER
        # -------------------------

        self.player.update(
            keys,
            self.platforms,
            WIDTH
        )

        # -------------------------
        # PLATFORMS
        # -------------------------

        for p in self.platforms:
            p.update()

        self.platforms = [
            p for p in self.platforms
            if p.is_active()
        ]

        # -------------------------
        # CAMERA
        # -------------------------

        target = (
            self.player.rect.centery
            - HEIGHT // 2
        )

        if target < self.cam_y:
            self.cam_y = target

        # -------------------------
        # LAVA SURGE SYSTEM
        # -------------------------

        self.next_surge -= 1

        # Start a new surge
        if self.next_surge <= 0 and not self.surge_active:

            self.surge_active = True

            # Surge lasts approximately 4 seconds
            self.surge_timer = 240

            # Schedule next surge
            self.next_surge = random.randint(
                600,
                900
            )

        # Active surge
        if self.surge_active:

            self.lava_rise = self.surge_lava_rise

            self.surge_timer -= 1

            if self.surge_timer <= 0:
                self.surge_active = False

        else:

            # Normal gradual acceleration
            self.lava_rise = min(
                1.2,
                self.lava_rise + 0.0003
            )

        # Move lava upward
        self.lava_y -= self.lava_rise

        # -------------------------
        # HEIGHT
        # -------------------------

        self.score = max(
            0,
            (GROUND_Y - self.player.rect.y) // 10
        )

        self.frame += 1

        # -------------------------
        # LAVA COLLISION
        # -------------------------

        if self.player.rect.bottom >= self.lava_y:
            self.game_over = True

        # -------------------------
        # VICTORY
        # -------------------------

        if self.player.rect.top <= self.top_y - 20:
            self.won = True

    def draw(self):

        self.screen.fill(BG)

        # -------------------------
        # PLATFORMS
        # -------------------------

        for p in self.platforms:

            p.draw(
                self.screen,
                self.cam_y
            )

        # -------------------------
        # PLAYER
        # -------------------------

        self.player.draw(
            self.screen,
            self.cam_y
        )

        # -------------------------
        # LAVA
        # -------------------------

        draw_lava(
            self.screen,
            self.lava_y,
            self.cam_y,
            WIDTH,
            HEIGHT,
            self.frame
        )

        # -------------------------
        # HEIGHT HUD
        # -------------------------

        sc = self.font.render(
            f"Height: {self.score}m",
            True,
            (220, 200, 180)
        )

        self.screen.blit(
            sc,
            (8, 10)
        )

        # -------------------------
        # DANGER METER
        # -------------------------

        self.draw_danger_meter()

        # -------------------------
        # SURGE WARNING
        # -------------------------

        if self.surge_active:

            warning = self.font.render(
                "!!! LAVA SURGE !!!",
                True,
                (255, 80, 40)
            )

            self.screen.blit(
                warning,
                (
                    WIDTH // 2
                    - warning.get_width() // 2,
                    45
                )
            )

        # -------------------------
        # GAME OVER
        # -------------------------

        if self.game_over:

            self._msg(
                "LAVA GOT YOU!",
                (220, 80, 40)
            )

        # -------------------------
        # VICTORY
        # -------------------------

        if self.won:

            self._msg(
                "ESCAPED!",
                (80, 220, 100)
            )

        pygame.display.flip()

    def draw_danger_meter(self):

        # Calculate danger from lava speed.
        # Normal maximum = 1.2
        # Surge speed = 2.0

        danger = min(
            1.0,
            self.lava_rise / 2.0
        )

        bar_width = 180
        bar_height = 18

        x = WIDTH - bar_width - 10
        y = 12

        # Label
        label = self.small_font.render(
            "LAVA DANGER",
            True,
            (230, 230, 230)
        )

        self.screen.blit(
            label,
            (x, y + 22)
        )

        # Background
        pygame.draw.rect(
            self.screen,
            (60, 60, 60),
            (
                x,
                y,
                bar_width,
                bar_height
            ),
            border_radius=4
        )

        # Danger level
        fill_width = int(
            bar_width * danger
        )

        if danger >= 0.75:

            color = (220, 50, 30)

        elif danger >= 0.45:

            color = (255, 170, 30)

        else:

            color = (70, 200, 80)

        pygame.draw.rect(
            self.screen,
            color,
            (
                x,
                y,
                fill_width,
                bar_height
            ),
            border_radius=4
        )

        # Border
        pygame.draw.rect(
            self.screen,
            (220, 220, 220),
            (
                x,
                y,
                bar_width,
                bar_height
            ),
            2,
            border_radius=4
        )

    def _msg(self, text, color):

        ov = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        ov.fill(
            (0, 0, 0, 150)
        )

        self.screen.blit(
            ov,
            (0, 0)
        )

        m = self.big_font.render(
            text,
            True,
            color
        )

        s = self.font.render(
            "Press R to Play Again",
            True,
            (200, 200, 200)
        )

        self.screen.blit(
            m,
            (
                WIDTH // 2
                - m.get_width() // 2,
                HEIGHT // 2 - 40
            )
        )

        self.screen.blit(
            s,
            (
                WIDTH // 2
                - s.get_width() // 2,
                HEIGHT // 2 + 20
            )
        )

    def run(self):

        running = True

        while running:

            running = self.handle_events()

            self.update()

            self.draw()

            self.clock.tick(FPS)

        pygame.quit()
