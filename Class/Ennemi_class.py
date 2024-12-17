import pygame


class Ennemis:
    def __init__(self, nom, largeur, hauteur, sprite_path, position_x, position_y, vitesse):
        self.nom = nom
        self.largeur = largeur
        self.hauteur = hauteur
        self.sprite = pygame.transform.scale(
            pygame.image.load(sprite_path), (self.largeur, self.hauteur)
        )
        self.position_x = position_x
        self.position_y = position_y
        self.vitesse = vitesse

        # Rectangle centré
        self.rect = pygame.Rect(self.position_x, self.position_y, self.largeur, self.hauteur)
    def deplacer(self):
        """Déplace l'ennemi de droite à gauche."""
        pass

    def afficher(self, surface):
        """Affiche l'ennemi à l'écran."""
        surface.blit(self.sprite, (self.position_x, self.position_y))

        self.rect.topleft = (
                    self.position_x,
                    self.position_y
        )        

    def collision(self, perso_rect):
        """Vérifie la collision avec le personnage."""
        return self.rect.colliderect(perso_rect)  # Retourne True si collision
