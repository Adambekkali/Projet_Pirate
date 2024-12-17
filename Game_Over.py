import pygame
import sys





screen_width = 800
screen_height = 600





class GameOver:
    
    def __init__(self, image_path, music_path):
        global screen
    
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Game Over with Retry Option")
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (400, 200))
        self.start_y = -self.image.get_height()
        self.target_y = (screen_height - self.image.get_height()) // 2
        self.music_path = music_path

    def play_music(self):
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


            screen.fill((0, 0, 0))  # Fond noir


            screen.blit(self.image, ((screen_width - self.image.get_width()) // 2, y))


            pygame.display.update()


            y += 6


            clock.tick(60)

    def game_loop(self):

        
        retry_screen = RetryScreen(
            "GameOver/menu1.png"
        )
        print("ici2")
        while True:

            pygame.time.delay(2000)
            self.animate()
            print("ici3")

            pygame.time.delay(3000)


            action = retry_screen.display()


            if action == "retry":
                """Jeu.boucle_principale()"""
                continue


# Classe RetryScreen
class RetryScreen:
    def __init__(self, background_image_path):
        self.background = pygame.image.load(background_image_path)
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))  # Ajuster la taille
        self.button_width = 200
        self.button_height = 60
        self.button_color = (139, 69, 19)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont("Blackadder ITC", 30)
        self.button_rect = pygame.Rect(
            (screen_width - self.button_width) // 2,
            (screen_height - self.button_height) // 2 + 200,
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







