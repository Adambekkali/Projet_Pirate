import pygame


class Porte:
    def __init__(self, position):
        self.position = position
        self.sprite = pygame.transform.scale(
            pygame.image.load("Dossier/Image/porte0.png"),
            (250, 400),
        )
        self.rect = pygame.Rect(position[0], position[1], 250, 400)

    def afficher(self, surface):
        """Affiche la porte avec une position correcte."""
        self.rect.topleft = self.position  # Met à jour le rectangle de collision
        surface.blit(self.sprite, self.position)

    def collision(self, autre_rect):
        """Vérifie si la porte entre en collision avec un autre rectangle."""
        return self.rect.colliderect(autre_rect)
