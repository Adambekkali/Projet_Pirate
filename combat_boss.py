import os
import pygame
import random
import sys
from Game_Over import *

# Initialisation de Pygame
pygame.init()
pygame.mixer.init()  # Initialisation du module de son

class Perso:
    def __init__(self, nom, largeur, hauteur, chemin_sprites, position, vitesse, points_vie=3):
        self.nom = nom
        self.largeur = largeur
        self.hauteur = hauteur
        self.chemin_sprites = chemin_sprites
        self.position = position
        self.vitesse = vitesse
        self.points_vie = points_vie
        self.orientation = "d"  # Orientation par défaut (droite)
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_delay = 3  # Vitesse de changement de frames (plus bas = plus rapide)
        self._charger_sprites()
        self.saut_en_cours = False
        self.vitesse_saut = 0
        self.gravite = 2
        self.position_initiale_y = position[1]
        self.en_attaque = False
        self.cooldown_attaque = 0  # Cooldown pour les frappes
        self.cooldown_max = 50    # Temps en frames entre deux attaques

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
            pygame.image.load(os.path.join(self.chemin_sprites, f"attack{i}.png")),
            (self.largeur, self.hauteur)) for i in range(1, 4)
        ]
        self.sprites_attaque_gauche = [pygame.transform.scale(
            pygame.image.load(os.path.join(self.chemin_sprites, f"r_attack{i}.png")),
            (self.largeur, self.hauteur)) for i in range(1, 4)
        ]

    def deplacer(self, keys, ennemi):
        if not self.saut_en_cours:  # Si le personnage n'est pas en train de sauter
            new_position_x = self.position[0]
            if keys[pygame.K_q]:  # Aller à gauche
                self.orientation = "g"
                new_position_x -= self.vitesse
            if keys[pygame.K_d]:  # Aller à droite
                self.orientation = "d"
                new_position_x += self.vitesse

            # Vérification des collisions horizontales avec la hitbox de l'ennemi
            if not pygame.Rect(new_position_x, self.position[1], self.largeur, self.hauteur).colliderect(
                    ennemi.get_hitbox()):
                self.position[0] = new_position_x

            # Empêcher le personnage de dépasser la verticale de la hitbox du boss
            if self.position[0] + self.largeur > ennemi.get_hitbox().left:
                self.position[0] = ennemi.get_hitbox().left - self.largeur

            self.position[0] = max(0, min(self.position[0], 1550 - self.largeur))

            if keys[pygame.K_SPACE]:  # Début du saut
                self.saut_en_cours = True
                self.vitesse_saut = -35  # Initialisation de la vitesse verticale
        else:  # Si un saut est en cours
            self.position[1] += self.vitesse_saut  # Déplacement vertical
            self.vitesse_saut += self.gravite  # Accélération due à la gravité

            # Courbe du saut (réduction de la vitesse horizontale pendant le saut)
            new_position_x = self.position[0]
            if self.orientation == "d":
                new_position_x += self.vitesse // 2  # Déplacement réduit à droite
            elif self.orientation == "g":
                new_position_x -= self.vitesse // 2  # Déplacement réduit à gauche

            # Vérification des collisions pendant le saut
            if not pygame.Rect(new_position_x, self.position[1], self.largeur, self.hauteur).colliderect(
                    ennemi.get_hitbox()):
                self.position[0] = max(0, min(new_position_x, 1550 - self.largeur))

            # Empêcher le personnage de dépasser la verticale de la hitbox du boss
            if self.position[0] + self.largeur > ennemi.get_hitbox().left:
                self.position[0] = ennemi.get_hitbox().left - self.largeur

            # Vérification si le personnage touche le sol
            if self.position[1] >= self.position_initiale_y:
                self.position[1] = self.position_initiale_y  # Réinitialisation au sol
                self.saut_en_cours = False

    def attaquer(self, ennemi):
        """Déclenche l'animation d'attaque et inflige des dégâts au boss."""
        if not self.en_attaque and self.cooldown_attaque == 0:
            self.en_attaque = True
            self.frame_index = 0
            self.cooldown_attaque = self.cooldown_max  # Définir le cooldown

            # Détermine la zone d'attaque basée sur l'orientation
            if self.orientation == "d":  # Si le personnage regarde à droite
                zone_attaque = pygame.Rect(
                    self.position[0] + self.largeur, self.position[1],
                    50, self.hauteur  # Zone de 50px à droite du personnage
                )
            else:  # Si le personnage regarde à gauche
                zone_attaque = pygame.Rect(
                    self.position[0] - 50, self.position[1],
                    50, self.hauteur  # Zone de 50px à gauche du personnage
                )

            # Vérifie si la zone d'attaque touche le boss
            if zone_attaque.colliderect(ennemi.get_hitbox()):
                ennemi.points_vie -= 1  # Réduit les points de vie du boss

                # Vérifie si le boss est vaincu
                if ennemi.points_vie <= 0:
                    pygame.mixer.music.stop()  # Arrête la musique
                    pygame.quit()  # Ferme la fenêtre actuelle
                    os.system('python victoire.py')  # Lance la fenêtre de victoire
                    sys.exit()  # Quitte le programme principal

    def mettre_a_jour(self):
        """Met à jour les états du personnage."""
        if self.cooldown_attaque > 0:
            self.cooldown_attaque -= 1  # Réduire le cooldown au fil du temps

    def get_rect(self):
        """Retourne le rectangle de collision du personnage."""
        return pygame.Rect(self.position[0], self.position[1], self.largeur, self.hauteur)

    def afficher(self, surface, keys):
        """Affiche le sprite correspondant à l'état du personnage."""
        if self.en_attaque:  # Animation d'attaque
            if self.frame_index >= len(self.sprites_attaque_droite):
                self.frame_index = 0
            self.animation_timer += 1

            if self.animation_timer >= self.animation_delay:
                self.animation_timer = 0
                self.frame_index += 1

                if self.frame_index >= len(self.sprites_attaque_droite):
                    self.frame_index = 0
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
        elif self.orientation == "d":
            surface.blit(self.sprite_stand_droite, self.position)
        else:
            surface.blit(self.sprite_stand_gauche, self.position)

    def lancer_game_over(self):
        """Lance le fichier GameOver.py."""
        pygame.quit()
        GameOver.animate(GameOver.self)
            
        sys.exit()

class Ennemis:
    def __init__(self, nom, largeur, hauteur, chemin_sprites, position_x, position_y):
        self.nom = nom
        self.largeur = largeur
        self.hauteur = hauteur
        self.chemin_sprites = chemin_sprites
        self.sprites_saut = self._charger_sprites_saut()
        self.sprite_sol = pygame.transform.scale(
            pygame.image.load(os.path.join(self.chemin_sprites, "boss.png")),
            (self.largeur, self.hauteur),
        )
        self.position_x = position_x
        self.position_y = position_y
        self.position_initiale_y = position_y

        self.saut_en_cours = False
        self.vitesse_saut = 0
        self.gravite = 2
        self.saut_timer = random.randint(60, 180)  # Intervalle aléatoire pour sauter
        self.frame_index = 0
        self.points_vie = 1  # Points de vie initiaux du boss
        self.vivant = True

        # Chargement des tirs
        self.balles = []  # Liste des balles
        self.tir_timer = random.randint(60, 180)  # Intervalle aléatoire pour tirer
        self.base_tir_interval = 180  # Base de l'intervalle pour tirer

        # Charger le son de saut
        self.son_saut = pygame.mixer.Sound(os.path.join(self.chemin_sprites, "son_saut.mp3"))

    def _charger_sprites_saut(self):
        """Charge les sprites du boss pour le saut."""
        return [
            pygame.transform.scale(
                pygame.image.load(os.path.join(self.chemin_sprites, f"saut_{i}.png")),
                (self.largeur, self.hauteur),
            )
            for i in range(1, 7)
        ]

    def sauter(self):
        """Gère le saut du boss."""
        if not self.saut_en_cours:
            self.saut_en_cours = True
            self.vitesse_saut = -30  # Début du saut
            self.frame_index = 0
            self.son_saut.play()  # Jouer le son de saut
        else:
            self.position_y += self.vitesse_saut
            self.vitesse_saut += self.gravite

            if self.position_y >= self.position_initiale_y:
                self.position_y = self.position_initiale_y
                self.saut_en_cours = False
                self.saut_timer = random.randint(60, 180)  # Réinitialise le timer après avoir atterri

    def prendre_degats(self):
        """Réduit les points de vie du boss."""
        self.points_vie -= 1
        if self.points_vie <= 0:
            self.vivant = False  # Le boss est mort

    def tirer(self, joueur):
        """Tire une balle en direction du joueur uniquement si le boss est au sol."""
        if not self.saut_en_cours:  # Le boss ne tire que s'il est au sol
            direction = 1 if joueur.position[0] > self.position_x else -1
            x_balle = self.position_x if direction == -1 else self.position_x + self.largeur
            nouvelle_balle = Balle(
                x=x_balle,
                y=self.position_y + self.hauteur // 2 + 10,  # Ajustement pour que la balle parte légèrement en dessous
                direction=direction,
                largeur=20,  # Taille de la balle
                hauteur=20,
                image_path=os.path.join(self.chemin_sprites, "balle.png")  # Chemin de l'image de la balle
            )
            self.balles.append(nouvelle_balle)

    def prendre_degats(self):
        """Réduit les points de vie du boss et augmente la fréquence des tirs."""
        self.points_vie -= 1
        self.base_tir_interval = max(10, self.base_tir_interval // 2)  # Multiplie la fréquence par 2
        self.tir_timer = random.randint(1, self.base_tir_interval)

    def mettre_a_jour(self, joueur):
        """Met à jour l'état du boss et ses tirs."""
        if self.saut_timer > 0:
            self.saut_timer -= 1
        else:
            self.sauter()

        # Gestion des tirs
        if self.tir_timer > 0:
            self.tir_timer -= 1
        else:
            self.tirer(joueur)
            self.tir_timer = random.randint(1, self.base_tir_interval)  # Utilise l'intervalle ajusté

        # Mettre à jour les balles
        for balle in self.balles[:]:
            balle.deplacer()
            if balle.x < 0 or balle.x > 1550:  # Supprimer les balles hors écran
                self.balles.remove(balle)

    def get_hitbox(self):
        """Retourne la hitbox de l'ennemi."""
        return pygame.Rect(
            self.position_x + (self.largeur // 4),
            self.position_y,
            self.largeur // 2,
            self.hauteur
        )

    def afficher(self, surface):
        """Affiche le boss et ses balles."""
        if self.saut_en_cours:
            surface.blit(self.sprites_saut[self.frame_index // 2], (self.position_x, self.position_y))
            self.frame_index = (self.frame_index + 1) % (len(self.sprites_saut) * 2)
        else:
            surface.blit(self.sprite_sol, (self.position_x, self.position_y))

        # Affichage des balles
        for balle in self.balles:
            balle.afficher(surface)

# Classe Balle
class Balle:
    def __init__(self, x, y, direction, vitesse=10, largeur=10, hauteur=10, image_path=None):
        self.x = x
        self.y = y
        self.direction = direction  # -1 pour gauche, 1 pour droite
        self.vitesse = vitesse
        self.largeur = largeur
        self.hauteur = hauteur
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        if image_path:
            self.image = pygame.transform.scale(
                pygame.image.load(image_path), (self.largeur, self.hauteur)
            )
        else:
            self.image = None

    def deplacer(self):
        """Déplace la balle selon sa direction."""
        self.x += self.vitesse * self.direction
        self.rect.x = self.x

    def afficher(self, surface):
        """Affiche la balle."""
        if self.image:
            surface.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(surface, (255, 0, 0), self.rect)

class Jeu:
    def __init__(self):
        # Initialisation de la musique de fond
        try:
            pygame.mixer.music.load("Dossier\Boss.mp3")  # Charger la bande son
            pygame.mixer.music.set_volume(0.5)  # Réglez le volume (0.0 à 1.0)
            pygame.mixer.music.play(-1)  # Jouer en boucle (-1 pour répétition infinie)
        except pygame.error as e:
            print(f"Erreur de chargement de la musique : {e}")

        # Paramètres de la fenêtre
        self.largeur = 1550
        self.hauteur = 800
        self.screen = pygame.display.set_mode((self.largeur, self.hauteur))
        pygame.display.set_caption("Piscine Python")

        # Chargement des ressources
        self.background_image = pygame.image.load(r"Dossier\Image\fond_boss.png")
        self.background_image = pygame.transform.scale(
            self.background_image, (self.largeur, self.hauteur)
        )

        # Initialisation des entités
        chemin_perso = r"Dossier\image\jack"
        self.personnage = Perso(
            nom="Sparrow",
            largeur=320,
            hauteur=280,
            chemin_sprites=chemin_perso,
            position=[self.largeur // 4, self.hauteur - 280 - 50],
            vitesse=15,
        )
        chemin_ennemi = r"Dossier\Image\Boss"
        self.ennemi = Ennemis(
            nom="Boss",
            largeur=400,
            hauteur=360,
            chemin_sprites=chemin_ennemi,
            position_x=3 * self.largeur // 5,
            position_y=self.hauteur - 360 - 50,
        )

        self.clock = pygame.time.Clock()
        self.running = True

    def boucle_principale(self):
        """Boucle principale du jeu."""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Gestion des touches
            keys = pygame.key.get_pressed()
            self.personnage.deplacer(keys, self.ennemi)
            self.personnage.mettre_a_jour()

            # Déclenchement de l'attaque si clic gauche de la souris
            if pygame.mouse.get_pressed()[0]:  # Si clic gauche
                self.personnage.attaquer(self.ennemi)

            # Mise à jour des entités
            self.ennemi.mettre_a_jour(self.personnage)

            # Vérification des collisions des balles avec le personnage
            for balle in self.ennemi.balles[:]:
                if balle.rect.colliderect(self.personnage.get_rect()):
                    self.personnage.points_vie -= 1  # Réduction des points de vie
                    self.ennemi.balles.remove(balle)
                    if self.personnage.points_vie <= 0:
                        self.personnage.lancer_game_over()

            # Affichage
            self.afficher_ecran(keys)

            # Limiter la vitesse d'exécution
            self.clock.tick(60)

    def afficher_ecran(self, keys):
        """Affiche les éléments du jeu."""
        self.screen.blit(self.background_image, (0, 0))
        self.personnage.afficher(self.screen, keys)
        self.ennemi.afficher(self.screen)
        pygame.display.flip()

# Lancer le jeu
if __name__ == "__main__":
    jeu = Jeu()
    jeu.boucle_principale()
    pygame.quit()
