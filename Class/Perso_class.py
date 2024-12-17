import os
import pygame

from Game_Over import GameOver


class Perso:
    def __init__(self, nom, largeur, hauteur, chemin_sprites, position, vitesse,vie):
        self.nom = nom
        self.largeur = largeur
        self.hauteur = hauteur
        self.chemin_sprites = chemin_sprites
        self.position = position
        self.vitesse = vitesse
        self.orientation = "d"  # Orientation par défaut (droite)
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_delay = 5  # Vitesse de changement de frames
        self._charger_sprites()
        self.saut_en_cours=False
        self.vitesse_saut=0
        self.gravite=2
        self.position_initiale_y = position[1]
        self.en_attaque=False
        self.vie=vie
        self.rect_normal = pygame.Rect(position[0]+50, position[1], largeur-150, hauteur-120)  # Normal collision rectangle
        self.rect = self.rect_normal  # Default to normal rectangle
        self.rect_attaque = pygame.Rect(  # Separate rectangle for attack
            position[0] + (largeur if self.orientation == "d" else -largeur//2), 
            position[1], 
            largeur, 
            hauteur
        )

    def _charger_sprites(self):
        """Charge les sprites du personnage."""
        self.sprites_droite = [
            pygame.transform.scale(
                pygame.image.load(os.path.join(self.chemin_sprites, f"walk{i}.png")),
                (self.largeur, self.hauteur),
            )
            for i in range(1, 4)
        ]
        self.sprites_gauche = [
            pygame.transform.scale(
                pygame.image.load(os.path.join(self.chemin_sprites, f"r_walk{i}.png")),
                (self.largeur, self.hauteur),
            )
            for i in range(1, 4)
        ]
        self.sprite_saut_droite = pygame.transform.scale(
            pygame.image.load(os.path.join(self.chemin_sprites, "jump.png")),
            (self.largeur, self.hauteur),
        )
        self.sprite_stand_droite = pygame.transform.scale(
            pygame.image.load(os.path.join(self.chemin_sprites, "stand.png")),
            (self.largeur, self.hauteur),
        )
        self.sprite_stand_gauche = pygame.transform.scale(
            pygame.image.load(os.path.join(self.chemin_sprites, "r_stand.png")),
            (self.largeur, self.hauteur),
        )

        self.sprites_attaque_droite = [pygame.transform.scale(
            pygame.image.load(os.path.join(self.chemin_sprites,f"attack{i}.png")),
            (self.largeur,self.hauteur))for i in range (1,4)
        
        ]
        self.sprites_attaque_gauche = [pygame.transform.scale(
            pygame.image.load(os.path.join(self.chemin_sprites,f"r_attack{i}.png")),
            (self.largeur,self.hauteur))for i in range (1,4)
        
        ]

    def deplacer(self, keys):
        if not self.saut_en_cours:  # Si le personnage n'est pas en train de sauter
            if keys[pygame.K_q]:  # Aller à gauche
                self.orientation = "g"
            if keys[pygame.K_d]:  # Aller à droite
                self.orientation = "d"
            if keys[pygame.K_SPACE]:  # Début du saut
                self.saut_en_cours = True
                self.vitesse_saut = -40 # Initialisation de la vitesse verticale
        else:  # Si un saut est en cours
            self.position[1] += self.vitesse_saut  # Déplacement vertical
            self.vitesse_saut += self.gravite  # Accélération due à la gravité
        # Vérification si le personnage touche le sol
            if self.position[1] >= self.position_initiale_y:
                self.position[1] = self.position_initiale_y  # Réinitialisation au sol
                self.saut_en_cours = False
        

    def attaquer(self):
        """Déclenche l'animation d'attaque et change la hitbox."""
        self.en_attaque = True
        self.frame_index = 0
        # Change hitbox during attack
        if self.orientation == "d":
            self.rect_attaque.topleft = (self.position[0], self.position[1])
        else:
            self.rect_attaque.topleft = (self.position[0], self.position[1])
        self.rect = self.rect_attaque  # Use attack rectangle for collisiont 

    def degat(self):
        self.vie-=1
        if self.vie <=0:
        
            game_over = GameOver("GameOver/gameover1.jpg","GameOver/fail.mp3")
            game_over.game_loop()
            
    def afficher(self, surface, keys):
        """Affiche le sprite correspondant à l'état du personnage."""
        self.rect.topleft = self.position
        if not self.en_attaque:
            self.rect = self.rect_normal

        self.rect.topleft = self.position
        if self.en_attaque:  # Animation d'attaque
            if self.frame_index >= len(self.sprites_attaque_droite):
                self.frame_index = 0
            self.animation_timer += 1

            if self.animation_timer >= self.animation_delay:
                self.animation_timer = 0
                self.frame_index += 1

                if self.frame_index >= len(self.sprites_attaque_droite):
                    self.frame_index=0
                    self.en_attaque = False  # Fin de l'attaque

            if self.orientation == "d":
                surface.blit(self.sprites_attaque_droite[self.frame_index], self.position)
            else:
                surface.blit(self.sprites_attaque_gauche[self.frame_index], self.position)

        elif keys[pygame.K_q]:  # Animation marche gauche
            self.animation_timer += 1
            if self.animation_timer >= self.animation_delay:
                self.animation_timer = 0
                self.frame_index = (self.frame_index + 1) % len(self.sprites_gauche)
            surface.blit(self.sprites_gauche[self.frame_index], self.position)
        elif keys[pygame.K_d]:  # Animation marche droite
            self.animation_timer += 1
            if self.animation_timer >= self.animation_delay:
                self.animation_timer = 0
                self.frame_index = (self.frame_index + 1) % len(self.sprites_droite)
            surface.blit(self.sprites_droite[self.frame_index], self.position)
        elif keys[pygame.K_SPACE]:  # Animation saut droite
            surface.blit(self.sprite_saut_droite, self.position)
        elif self.orientation == "d":  # Stationnaire droite
            surface.blit(self.sprite_stand_droite, self.position)
        else:  # Stationnaire gauche
            surface.blit(self.sprite_stand_gauche, self.position)
    def get_rect(self):
        """Retourne le rectangle de collision du personnage."""
        return self.rect