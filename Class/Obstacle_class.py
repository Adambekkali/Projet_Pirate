import pygame


class Obstacle:
    def __init__(self, type, pos):
        self.type = type
        self.pos = pos
        self.sprite_width = 250
        self.sprite_height = 300

        self.sprite = pygame.transform.scale(
            pygame.image.load(f"Dossier/Image/obstacle/{type}.png"),
            (self.sprite_width, self.sprite_height),
        )

        # Taille du rectangle de collision
        rect_width = 75
        rect_height = 150

        # Calcul des offsets pour centrer
        rect_x = pos[0] + (self.sprite_width - rect_width) // 2
        rect_y = pos[1] + (self.sprite_height - rect_height) // 2

        # Rectangle centré
        self.rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
    def afficher(self, surface): 
        position_affichee = [self.pos[0], self.pos[1]]  
        surface.blit(self.sprite, position_affichee)

        self.rect.topleft = (
                    position_affichee[0] + (self.sprite_width - self.rect.width) // 2,
                    position_affichee[1] + (self.sprite_height - self.rect.height) // 2,
        )        
    
    def collision(self, autre_rect):
        """Vérifie si cet obstacle entre en collision avec un autre rectangle."""
        return self.rect.colliderect(autre_rect)
