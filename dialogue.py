import pygame
import sys
import random
from combat_boss import *


# Dimensions de la fenêtre
SCREEN_WIDTH = 1550
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bateau et Boss")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Classe Bateau
class Bateau:
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5
        self.health = 5  # Vie initiale du bateau

    def move(self, keys):
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Classe Tonneau
class Tonneau:
    def __init__(self, image_path, x, y, visible=True):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.visible = visible
        if not self.visible:
            self.image.set_alpha(100)  # Rendre peu visible

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Classe GameOver
class GameOver:
    def __init__(self, image_path, music_path):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (400, 200))
        self.start_y = -self.image.get_height()
        self.target_y = (SCREEN_HEIGHT - self.image.get_height()) // 2
        self.music_path = music_path

    def play_music(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.music_path)
        pygame.mixer.music.play()

    def animate(self):
        self.play_music()
        y = self.start_y
        clock = pygame.time.Clock()

        while y < self.target_y:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill(BLACK)
            screen.blit(self.image, ((SCREEN_WIDTH - self.image.get_width()) // 2, y))
            pygame.display.update()
            y += 6
            clock.tick(60)

        # Laisser l'image GAME OVER visible quelques secondes
        pygame.time.delay(3000)  # Pause de 3 secondes

# Classe RetryScreen
class RetryScreen:
    def __init__(self, background_image_path):
        self.background = pygame.image.load(background_image_path)
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.button_width = 200
        self.button_height = 60
        self.button_color = (139, 69, 19)
        self.text_color = WHITE

        # Initialiser explicitement pygame.font si nécessaire
        pygame.font.init()
        self.font = pygame.font.SysFont("Blackadder ITC", 30)  # Créer la police ici

        self.button_rect = pygame.Rect(
            (SCREEN_WIDTH - self.button_width) // 2,
            (SCREEN_HEIGHT - self.button_height) // 2 + 200,
            self.button_width,
            self.button_height
        )


    def display(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_rect.collidepoint(event.pos):
                        running = False
                        return "retry"

            screen.blit(self.background, (0, 0))
            pygame.draw.rect(screen, self.button_color, self.button_rect)
            text_surface = self.font.render("Réessayer", True, self.text_color)
            text_rect = text_surface.get_rect(center=self.button_rect.center)
            screen.blit(text_surface, text_rect)
            pygame.display.update()

# Classe Bulle
class Bulle:
    def __init__(self, texte, position, couleur_bulle=(255, 255, 255), couleur_texte=(0, 0, 0), chemin_police="Blackadder ITC", taille_police=42):
        self.texte = texte
        self.position = position
        self.couleur_bulle = couleur_bulle
        self.couleur_texte = couleur_texte
        self.police = pygame.font.SysFont(chemin_police, taille_police)

    def dessiner(self, surface):
        surface_texte = self.police.render(self.texte, True, self.couleur_texte)
        rect_texte = surface_texte.get_rect()
        marge = 20  # Augmenté pour des bulles plus grandes
        rect_bulle = pygame.Rect(self.position[0], self.position[1], rect_texte.width + 2 * marge, rect_texte.height + 2 * marge)
        bord_largeur = 3
        rect_bord = pygame.Rect(
            rect_bulle.x - bord_largeur,
            rect_bulle.y - bord_largeur,
            rect_bulle.width + 2 * bord_largeur,
            rect_bulle.height + 2 * bord_largeur,
        )
        pygame.draw.rect(surface, (0, 0, 0), rect_bord, border_radius=10)
        pygame.draw.rect(surface, self.couleur_bulle, rect_bulle, border_radius=10)
        surface.blit(surface_texte, (rect_bulle.x + marge, rect_bulle.y + marge))

# Affichage des dialogues
def afficher_dialogues():
    fond_dialogues = pygame.image.load(r"Dossier\Navigation\image.webp")
    fond_dialogues = pygame.transform.scale(fond_dialogues, (SCREEN_WIDTH, SCREEN_HEIGHT))
    dialogue_mechant = Bulle(
        texte="Tu es sorti de prison pour tenter de reprendre ton trésor mais au final, tu vas mourir. \n Cliquez sur entrée pour combattre",
        position=(SCREEN_WIDTH - 719, 50),  # Décalé un peu plus à gauche
        couleur_bulle=(255, 255, 255),
        couleur_texte=(0, 0, 0),
        taille_police=25  # Taille augmentée
    )
    dialogue_heros = Bulle(
        texte="On verra ça, petit joueur. \n Cliquez sur entrée pour combattre",
        position=(3, 50),
        couleur_bulle=(255, 255, 255),
        couleur_texte=(0, 0, 0),
        taille_police=25  # Taille augmentée
    )
    dialogues = [dialogue_mechant, dialogue_heros]
    index = 0
    while index < len(dialogues):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                index += 1
        if index >= len(dialogues):
            jeu = Jeu()
            jeu.boucle_principale()
            break
        screen.blit(fond_dialogues, (0, 0))
        dialogues[index].dessiner(screen)
        pygame.display.update()

# Boucle principale
def main():
    background_image = pygame.image.load(r"Dossier\Navigation\CarteNavig.png")
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    bateau = Bateau(r"Dossier\Navigation\MainBateau.webp", 50, SCREEN_HEIGHT // 2)
    game_over = GameOver(r"Dossier\Navigation\gameover1.jpg", r"GameOver\menu1.png")
    retry_screen = RetryScreen(r"Dossier\Navigation\menu1.png")

    pygame.mixer.music.load(r"Dossier\Navigation\NavigMusic.mp3")
    pygame.mixer.music.play(loops=-1)

    tonneaux = []
    for _ in range(20):
        tonneaux.append(Tonneau(r"Dossier\Navigation\tonneau.png", random.randint(100, SCREEN_WIDTH - 50), random.randint(0, SCREEN_HEIGHT - 50), visible=True))
    for _ in range(20):
        tonneaux.append(Tonneau(r"Dossier\Navigation\tonneau.png", random.randint(100, SCREEN_WIDTH - 50), random.randint(0, SCREEN_HEIGHT - 50), visible=False))
    random.shuffle(tonneaux)

    target_image = pygame.image.load(r"Dossier\Navigation\logo_boss.webp")
    target_image = pygame.transform.scale(target_image, (50, 50))
    target_rect = target_image.get_rect(midright=(SCREEN_WIDTH - 30, SCREEN_HEIGHT // 2))

    # Image décorative en bas à gauche
    decorative_image = pygame.image.load(r"Dossier\Navigation\ToucheX.png")
    decorative_image = pygame.transform.scale(decorative_image, (115, 115))
    decorative_position = (10, SCREEN_HEIGHT - 135)

    clock = pygame.time.Clock()
    tonneaux_touches = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        bateau.move(keys)
        for tonneau in tonneaux[:]:
            if bateau.rect.colliderect(tonneau.rect):
                bateau.health -= 1
                tonneaux_touches += 1
                tonneaux.remove(tonneau)
        if tonneaux_touches >= 5 or bateau.health <= 0:
            pygame.mixer.music.stop()
            game_over.animate()
            action = retry_screen.display()
            if action == "retry":
                main()
                return
        if bateau.rect.colliderect(target_rect):
            pygame.mixer.music.stop()
            afficher_dialogues()
            return
        screen.blit(background_image, (0, 0))
        bateau.draw(screen)
        for tonneau in tonneaux:
            tonneau.draw(screen)
        screen.blit(target_image, target_rect)
        screen.blit(decorative_image, decorative_position)  # Affichage de l'image décorative
        pygame.draw.rect(screen, RED, (10, 10, bateau.health * 40, 20))
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
    pygame.quit()