import pygame

SPEED = 4


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.vel_y = 0
        self.on_ground = False
        self.color = (60, 160, 220)

    def update(self, keys, platforms, width):
        dx = 0

        # Left / right movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -SPEED

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = SPEED

        # Jump
        if (
            keys[pygame.K_SPACE]
            or keys[pygame.K_w]
            or keys[pygame.K_UP]
        ) and self.on_ground:
            self.vel_y = -13
            self.on_ground = False

        # Gravity
        self.vel_y = min(
            self.vel_y + 0.55,
            12
        )

        # Horizontal movement
        self.rect.x = max(
            0,
            min(
                width - self.rect.width,
                self.rect.x + dx
            )
        )

        # Vertical movement
        self.rect.y += int(self.vel_y)

        # Assume player is airborne
        self.on_ground = False

        # Platform collision
        for p in platforms:

            # Ignore destroyed platforms
            if not p.is_active():
                continue

            # Land only while falling
            if (
                self.rect.colliderect(p.rect)
                and self.vel_y > 0
                and self.rect.bottom <=
                    p.rect.top + self.vel_y + 2
            ):
                self.rect.bottom = p.rect.top
                self.vel_y = 0
                self.on_ground = True

                # Crumbling platform
                if p.platform_type == "crumbling":
                    p.start_crumbling()

                # Spring platform
                elif p.platform_type == "spring":
                    p.activate_spring()

                    # High-velocity jump
                    self.vel_y = -20
                    self.on_ground = False

    def draw(self, screen, cam_y):
        dr = self.rect.move(
            0,
            -int(cam_y)
        )

        pygame.draw.rect(
            screen,
            self.color,
            dr,
            border_radius=6
        )

        pygame.draw.circle(
            screen,
            (255, 220, 180),
            (dr.centerx, dr.top + 8),
            7
        )
