import pygame
import sys
from Projet_Pirate import *


def scene_victoire():
    # Initialisation de Pygame
    pygame.init()
    pygame.mixer.init()  # Initialisation du module audio

    # Charger et jouer la musique de victoire
    try:
        pygame.mixer.music.load("Dossier/victoire.mp3")  # Charger la musique
        pygame.mixer.music.set_volume(0.5)  # Régler le volume (entre 0.0 et 1.0)
        pygame.mixer.music.play(-1)  # Jouer la musique en boucle (-1 pour infini)
    except pygame.error as e:
        print(f"Erreur lors du chargement de la musique : {e}")

    screen_width, screen_height = 1550, 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Victoire")

    # Charger l'image de fond
    fond_victoire = pygame.image.load("Dossier/Image/fond_victoire.png")
    fond_victoire = pygame.transform.scale(fond_victoire, (screen_width, screen_height))

    # Couleur pour le texte
    blanc = (255, 255, 255)
    noir = (0, 0, 0)
    gris_clair = (200, 200, 200)

    # Charger la police d'écriture
    try:
        font = pygame.font.Font("Pieces of Eight.ttf", 74)
        button_font = pygame.font.Font("Pieces of Eight.ttf", 40)
    except FileNotFoundError:
        print("Erreur : le fichier 'Pieces of Eight.ttf' est introuvable.")
        pygame.quit()
        sys.exit()

    # Texte de victoire
    texte_victoire = font.render("Vous avez gagné !", True, blanc)
    texte_rect = texte_victoire.get_rect(center=(screen_width // 2, screen_height // 4))

    # Charger les sprites du coffre
    chemin_coffre = "Dossier/Image/Coffre"
    coffre_sprites = [
        pygame.image.load(f"{chemin_coffre}/coffre{i}.png") for i in range(1, 5)
    ]
    coffre_sprites = [pygame.transform.scale(sprite, (200, 200)) for sprite in coffre_sprites]

    # Position du coffre (centré)
    coffre_x = (screen_width - 200) // 2  # 200 = largeur du coffre
    coffre_y = (screen_height - 200) // 2  # 200 = hauteur du coffre

    # Boutons
    button_width, button_height = 300, 70
    button_spacing = 20  # Espacement entre les boutons

    # Recommencer
    restart_button_rect = pygame.Rect(
        (screen_width - button_width) // 2,
        coffre_y + 220,
        button_width,
        button_height,
    )
    # Quitter
    quit_button_rect = pygame.Rect(
        (screen_width - button_width) // 2,
        coffre_y + 220 + button_height + button_spacing,
        button_width,
        button_height,
    )

    frame_index = 0
    timer = 0
    animation_delay = 10

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clic gauche
                mouse_pos = pygame.mouse.get_pos()
                if restart_button_rect.collidepoint(mouse_pos):
                    Jeu().boucle_principale()
                    running = False  # Sortir de la scène actuelle pour relancer le jeu
                elif quit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
                    

        # Animation du coffre
        timer += 1
        if timer >= animation_delay:
            timer = 0
            frame_index = (frame_index + 1) % len(coffre_sprites)

        # Affichage
        screen.blit(fond_victoire, (0, 0))  # Affiche l'image de fond
        screen.blit(texte_victoire, texte_rect.topleft)  # Affiche le texte centré
        screen.blit(coffre_sprites[frame_index], (coffre_x, coffre_y))  # Affiche le coffre centré

        # Boutons
        pygame.draw.rect(screen, gris_clair, restart_button_rect)
        pygame.draw.rect(screen, gris_clair, quit_button_rect)

        # Texte des boutons
        restart_text = button_font.render("Recommencer", True, noir)
        quit_text = button_font.render("Quitter", True, noir)

        restart_text_rect = restart_text.get_rect(center=restart_button_rect.center)
        quit_text_rect = quit_text.get_rect(center=quit_button_rect.center)

        screen.blit(restart_text, restart_text_rect)
        screen.blit(quit_text, quit_text_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.mixer.music.stop()  # Arrête la musique lorsque la scène se termine


if __name__ == "__main__":
    scene_victoire()
