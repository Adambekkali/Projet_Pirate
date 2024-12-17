import os
from random import randint
import time
from Game_Over import GameOver
from dialogue import *
import sys
from Class.Perso_class import Perso
from Class.Ennemi_class import Ennemis
from Class.Obstacle_class import Obstacle
from Class.Port_class import Porte
import cv2

# Initialisation de Pygame
pygame.init()
class Jeu:
    def __init__(self):
        # Paramètres de la fenêtre
        self.largeur = 1550
        self.hauteur = 800
        self.screen = pygame.display.set_mode((self.largeur, self.hauteur))
        pygame.display.set_caption("Piscine Python")

        self.porte = None
        self.ennemi_detruits = 0
        self.porte_apparue = False

        # Chargement des ressources
        self.background_image = pygame.image.load(r"Dossier\Image\decorprison.png")
        self.background_image = pygame.transform.scale(
            self.background_image, (self.largeur, self.hauteur)
        )
        self.running = True
    # Initialisation des entités
        chemin_perso = r"Dossier\image\jack"
        self.personnage = Perso(
            nom="Sparrow",
            largeur=400,
            hauteur=350,
            chemin_sprites=chemin_perso,
            position=[self.largeur - 1300 , self.hauteur - 350 - 50],
            vitesse=15,
            vie=3
        )
        chemin_ennemi = r"Dossier\Image\Ennemi\stand.png"
        self.ennemi = Ennemis(
            nom="Garde",
            largeur=400,
            hauteur=350,
            sprite_path=chemin_ennemi,
            position_x=self.largeur + 300,
            position_y=self.hauteur - 350 - 50,
            vitesse=5,
        )

        # Liste d'ennemis
        self.ennemis = [self.ennemi]

        # Variables de défilement
        self.scroll_x = 0
        self.clock = pygame.time.Clock()
        self.running = True

        self.obstacle = Obstacle(
            "tonneau",
            [1000, self.hauteur - 450 +150]       
             )
        self.obstacles = [self.obstacle]  # Initialisez avec l'obstacle de départ

        self.ennemi_timer = time.time()  # Timer pour les ennemis
        self.ennemi_interval = randint(4, 8)  # Intervalle entre 4 et 8 secondes pour apparaître un nouvel ennemi


    def spawn_porte(self):
        """Fait apparaître une porte à côté du personnage."""
        if not self.porte_apparue:
            position_porte = [
                1900,  # Un peu à droite du personnage
                self.hauteur - 800  # Positionné en bas de l'écran
            ]
        self.porte = Porte(position_porte)
        self.porte_apparue = True

        
        # Initialisation des entités
        chemin_perso = r"Dossier\image\jack"
        self.personnage = Perso(
            nom="Sparrow",
            largeur=400,
            hauteur=350,
            chemin_sprites=chemin_perso,
            position=[self.largeur - 1300 , self.hauteur - 350 - 50],
            vitesse=15,
            vie=3
        )
        chemin_ennemi = r"Dossier\Image\Ennemi\stand.png"
        self.ennemi = Ennemis(
            nom="Garde",
            largeur=400,
            hauteur=350,
            sprite_path=chemin_ennemi,
            position_x=self.largeur + 300,
            position_y=self.hauteur - 350 - 50,
            vitesse=5,
        )

        # Liste d'ennemis
        self.ennemis = [self.ennemi]

        # Variables de défilement
        self.scroll_x = 0
        self.clock = pygame.time.Clock()
        self.running = True

        self.obstacle = Obstacle(
            "tonneau",
            [1000, self.hauteur - 450 +150]       
             )
        self.obstacles = [self.obstacle]  # Initialisez avec l'obstacle de départ

        self.ennemi_timer = time.time()  # Timer pour les ennemis
        self.ennemi_interval = randint(4, 8)  # Intervalle entre 4 et 8 secondes pour apparaître un nouvel ennemi




    def afficher_vie(self):
        """Affiche la vie du personnage en haut à gauche."""
        vie_text = f"Vie : {self.personnage.vie}"
        vie_surface = self.font.render(vie_text, True, (255, 0, 0))  # Texte en rouge
        self.screen.blit(vie_surface, (10, 10))  # Coordonnées pour l'afficher
    
    def boucle_principale(self):
        """Boucle principale du jeu."""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Gestion des touches
            keys = pygame.key.get_pressed()
            self.personnage.deplacer(keys)

            if self.personnage.en_attaque == False and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.personnage.attaquer()

            # Apparition des ennemis
            current_time = time.time()
            if current_time - self.ennemi_timer >= self.ennemi_interval:
                self.ennemi_timer = current_time  # Réinitialiser le timer
                self.ennemi_interval = randint(4, 8)  # Choisir un nouvel intervalle aléatoire
                # Créer un nouvel ennemi
                ennemi = Ennemis(
                    nom="Garde",
                    largeur=400,
                    hauteur=350,
                    sprite_path=r"Dossier\Image\Ennemi\stand.png",
                    position_x=self.personnage.position[0] + randint(1600, 2400),
                    position_y=self.hauteur - 350 - 50,
                    vitesse=5
                )
                self.ennemis.append(ennemi)

            if keys[pygame.K_d]:
                # Vérifiez si l'obstacle est proche d'être dépassé
                if self.personnage.position[0] + self.scroll_x >= self.obstacles[-1].pos[0] + self.scroll_x - 1000:
                    nouvel_obstacle = Obstacle(
                        "tonneau",
                        [self.obstacles[-1].pos[0] + randint(1600, 2400), self.hauteur - 450 + 150]
                    )
                    self.obstacles.append(nouvel_obstacle)
                if self.porte:
                    self.porte.position[0] -= 15

                for ennemi in self.ennemis:
                    ennemi.position_x -= 15
            for obstacle in self.obstacles:
                if keys[pygame.K_d]:
                    obstacle.pos[0] -= 15  # Déplacer l'obstacle avec le personnage
                elif keys[pygame.K_q]:
                    obstacle.pos[0] += 15

                elif keys[pygame.K_q]:
                    for ennemi in self.ennemis:
                        ennemi.position_x += 15  # Diminue progressivement la position_x de l'ennemi

            personnage_rect = self.personnage.rect
            for obstacle in self.obstacles:
                if obstacle.collision(personnage_rect):
                    self.obstacles.remove(obstacle)
                    self.personnage.degat()
            if self.personnage.en_attaque == False:
                for ennemi in self.ennemis:
                    if ennemi.collision(personnage_rect):
                        self.ennemis.remove(ennemi)
                        self.personnage.degat()
            else:
                for ennemi in self.ennemis:
                    if ennemi.collision(personnage_rect):
                        self.ennemis.remove(ennemi)
                        self.ennemi_detruits += 1  # Incrémente le compteur d'ennemis détruits

                        # Vérifier si 10 ennemis ont été détruits
                        if self.ennemi_detruits >= 1 and not self.porte_apparue:
                            self.spawn_porte()

            # gestion porte
            if self.porte and self.porte.collision(personnage_rect):
                main()
                self.running = False
                

            # Mise à jour du rectangle de collision de la porte
            if self.porte:
                self.porte.rect.topleft = self.porte.position

            # Détection de la collision entre le personnage et les ennemis

            # Déplacement de l'arrière-plan
            if keys[pygame.K_q]:
                self.scroll_x += self.personnage.vitesse
                if self.porte:
                    self.porte.position[0] += 15
            elif keys[pygame.K_d]:
                self.scroll_x -= self.personnage.vitesse
            self.scroll_x %= self.background_image.get_width()


            if self.porte_apparue and keys[pygame.K_p]:
                i= randint(1,5)
                video_path = f"Dossier/Image/edits/{i}.mp4"  # Remplacez par votre fichier
                play_video_in_pygame(video_path, self.screen)
        


                # Affichage
            self.afficher_ecran(keys)

                # Limiter la vitesse d'exécution
            self.clock.tick(60)

        

    def afficher_ecran(self, keys):
        """Affiche les éléments du jeu."""
        # Affichage de l'arrière-plan
        for x in range(
            -self.background_image.get_width(),
            self.largeur + self.background_image.get_width(),
            self.background_image.get_width(),
        ):
            self.screen.blit(self.background_image, (x + self.scroll_x, 0))

        # Affichage des entités
        self.personnage.afficher(self.screen, keys)
        for ennemi in self.ennemis:
            ennemi.afficher(self.screen)
        
        for obstacle in self.obstacles:
            obstacle.afficher(self.screen)

        if self.porte:
            self.porte.afficher(self.screen)
        
        self.afficher_vie


    


        # Mise à jour de l'affichage
        pygame.display.flip()


def play_video_in_pygame(video_path, screen):

    # Charger la vidéo avec OpenCV
    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        print("Erreur : Impossible de charger la vidéo.")
        return

    # Obtenir la taille de la vidéo
    video_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_rate = int(video.get(cv2.CAP_PROP_FPS))

    # Boucle pour lire et afficher chaque frame
    clock = pygame.time.Clock()
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break  # Fin de la vidéo

        # Convertir l'image OpenCV (BGR) en format compatible Pygame (RGB)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.transpose(frame)  # Optionnel, pour ajuster la rotation
        frame_surface = pygame.surfarray.make_surface(frame)

        # Redimensionner la frame pour s'adapter à la fenêtre Pygame
        frame_surface = pygame.transform.scale(frame_surface, (video_width, video_height))

        # Afficher la frame sur la fenêtre Pygame
        screen.blit(frame_surface, (0, 0))
        pygame.display.update()

        # Limiter à la vitesse de la vidéo
        clock.tick(frame_rate)

        # Vérifier les événements pour quitter
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                video.release()
                pygame.quit()
                sys.exit()

    video.release()


# Lancer le jeu
if __name__ == "__main__":
    jeu = Jeu()
    jeu.boucle_principale()
    pygame.quit()


