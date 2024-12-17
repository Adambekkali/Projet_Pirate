import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pygame
from Projet_Pirate import *

def lancer_jeu():
    root.withdraw()  # Masquer la fenêtre tkinter pendant que le jeu tourne
    pygame.mixer.music.stop()
    jeu = Jeu()
    jeu.boucle_principale()
    pygame.quit()
    root.deiconify()  # Réafficher la fenêtre tkinter après la fin du jeu

def charger_partie():
    messagebox.showinfo("Charger une partie", "Sélectionnez une partie à charger!")

def quitter():
    pygame.mixer.music.stop()  # Arrêter la musique avant de fermer
    if messagebox.askyesno("Quitter", "Êtes-vous sûr de vouloir quitter?"):
        root.destroy()

# Initialisation de la musique avec pygame
pygame.mixer.init()
musique_fichier = r"Dossier\Menu\musique.mp3"
try:
    pygame.mixer.music.load(musique_fichier)
    pygame.mixer.music.play(-1)
except pygame.error as e:
    print(f"Erreur lors du chargement de la musique : {e}")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Menu du jeu Pirate")
root.geometry("800x600")

# Ajout d'une image de fond
try:
    image_fichier = r"Dossier\Menu\Image\menu1.png"
    image = Image.open(image_fichier)
    image = image.resize((1550, 800))
    fond_image = ImageTk.PhotoImage(image)
    fond_label = tk.Label(root, image=fond_image)
    fond_label.image = fond_image
    fond_label.place(relwidth=1, relheight=1)
except Exception as e:
    print(f"Erreur lors du chargement de l'image : {e}")
    fond_label = tk.Label(root, text="Image introuvable", bg="white", fg="red", font=("Arial", 24))
    fond_label.place(relwidth=1, relheight=1)

# Création des boutons du menu
frame_menu = tk.Frame(root, bg="black", bd=5)
frame_menu.place(relx=0.5, rely=0.9, anchor="s")

bouton_lancer = tk.Button(frame_menu, text="Lancez le jeu", font=("Blackadder ITC", 18), command=lancer_jeu, bg="brown", fg="white")
bouton_lancer.pack(side=tk.LEFT, padx=10, pady=5)

bouton_charger = tk.Button(frame_menu, text="Chargez une partie", font=("Blackadder ITC", 18), command=charger_partie, bg="brown", fg="white")
bouton_charger.pack(side=tk.LEFT, padx=10, pady=5)

bouton_quitter = tk.Button(frame_menu, text="Quitter", font=("Blackadder ITC", 18), command=quitter, bg="brown", fg="white")
bouton_quitter.pack(side=tk.LEFT, padx=10, pady=5)

# Boucle principale de l'application
root.mainloop()

# Arrêt de la musique à la fermeture
pygame.mixer.music.stop()
q