import pygame
import random
import math

PLATFORM_COLOR = (100, 80, 50)
LAVA_COLOR = (220, 60, 20)


class Platform:
    def __init__(self, x, y, width, height=16, platform_type="normal"):
        self.rect = pygame.Rect(x, y, width, height)
        self.platform_type = platform_type

        # Crumbling platform
        self.crumbling = False
        self.crumble_timer = 0

        # Spring animation
        self.spring_timer = 0

    def start_crumbling(self):
        if self.platform_type == "crumbling" and not self.crumbling:
            self.crumbling = True
            self.crumble_timer = 60

    def activate_spring(self):
        if self.platform_type == "spring":
            self.spring_timer = 10

    def update(self):
        if self.crumbling:
            self.crumble_timer -= 1

        if self.spring_timer > 0:
            self.spring_timer -= 1

    def is_active(self):
        return not self.crumbling or self.crumble_timer > 0

    def draw(self, screen, cam_y):

        if not self.is_active():
            return

        dr = self.rect.move(
            0,
            -int(cam_y)
        )

        # Crumbling platform
        if self.crumbling:

            dr.x += random.randint(-2, 2)

            if self.crumble_timer % 10 < 5:
                color = (255, 140, 40)
            else:
                color = (180, 70, 30)

        # Spring platform
        elif self.platform_type == "spring":

            color = (60, 200, 90)

            # Spring compression animation
            if self.spring_timer > 0:
                dr.y += 5

        # Normal platform
        else:
            color = PLATFORM_COLOR

        pygame.draw.rect(
            screen,
            color,
            dr,
            border_radius=4
        )

        # Draw spring symbol
        if self.platform_type == "spring":

            center_x = dr.centerx
            bottom_y = dr.bottom

            points = [
                (center_x - 10, bottom_y - 3),
                (center_x - 5, bottom_y - 9),
                (center_x, bottom_y - 3),
                (center_x + 5, bottom_y - 9),
                (center_x + 10, bottom_y - 3)
            ]

            pygame.draw.lines(
                screen,
                (230, 255, 230),
                False,
                points,
                3
            )


def generate_platforms(width, base_y, count=30):

    plats = []

    # Starting ground
    plats.append(
        Platform(
            0,
            base_y,
            width,
            20,
            "normal"
        )
    )

    y = base_y - 110

    for i in range(count):

        w = random.randint(80, 200)
        x = random.randint(0, width - w)

        # Choose platform type
        if i > 1:

            chance = random.random()

            if chance < 0.20:
                platform_type = "crumbling"

            elif chance < 0.35:
                platform_type = "spring"

            else:
                platform_type = "normal"

        else:
            platform_type = "normal"

        plats.append(
            Platform(
                x,
                y,
                w,
                16,
                platform_type
            )
        )

        y -= random.randint(
            80,
            130
        )

    return plats


def draw_lava(
    screen,
    lava_y,
    cam_y,
    width,
    height,
    frame
):

    ly = int(
        lava_y - cam_y
    )

    if ly < height:

        # Lava wave
        pts = [(0, ly)]

        for x in range(
            0,
            width + 20,
            20
        ):

            pts.append(
                (
                    x,
                    ly + int(
                        math.sin(
                            x * 0.08
                            + frame * 0.1
                        ) * 8
                    )
                )
            )

        pts.append(
            (width, height)
        )

        pts.append(
            (0, height)
        )

        pygame.draw.polygon(
            screen,
            LAVA_COLOR,
            pts
        )

        # Glow
        s = pygame.Surface(
            (width, 30),
            pygame.SRCALPHA
        )

        for i in range(15):

            pygame.draw.line(
                s,
                (
                    255,
                    100,
                    0,
                    max(0, 60 - i * 4)
                ),
                (0, i),
                (width, i),
                1
            )

        screen.blit(
            s,
            (0, ly - 15)
        )
