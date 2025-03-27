import os
import sys
import subprocess
import shutil
import customtkinter as ctk
from gestion.favoris import add_recents, ajouter_favori, send_recent
import time

# Fonctions de dialogue personnalisées avec customtkinter

def center_window(win, width, height):
    win.update_idletasks()
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

def custom_show_error(title, message):
    dialog = ctk.CTkToplevel()
    dialog.title(title)
    # Définir la taille souhaitée pour la fenêtre de dialogue
    width, height = 300, 150
    center_window(dialog, width, height)
    label = ctk.CTkLabel(dialog, text=message, wraplength=280)
    label.pack(padx=20, pady=20)
    btn = ctk.CTkButton(dialog, text="OK", command=dialog.destroy)
    btn.pack(pady=10)
    dialog.grab_set()
    dialog.wait_window()

def custom_show_info(title, message):
    dialog = ctk.CTkToplevel()
    dialog.title(title)
    width, height = 300, 150
    center_window(dialog, width, height)
    label = ctk.CTkLabel(dialog, text=message, wraplength=280)
    label.pack(padx=20, pady=20)
    btn = ctk.CTkButton(dialog, text="OK", command=dialog.destroy)
    btn.pack(pady=10)
    dialog.grab_set()
    dialog.wait_window()

def custom_ask_yes_no(title, message):
    result = [False]
    def on_yes():
        result[0] = True
        dialog.destroy()
    def on_no():
        result[0] = False
        dialog.destroy()
    dialog = ctk.CTkToplevel()
    dialog.title(title)
    width, height = 300, 150
    center_window(dialog, width, height)
    label = ctk.CTkLabel(dialog, text=message, wraplength=280)
    label.pack(padx=20, pady=20)
    frame = ctk.CTkFrame(dialog)
    frame.pack(pady=10)
    btn_yes = ctk.CTkButton(frame, text="Oui", command=on_yes)
    btn_yes.pack(side="left", padx=10)
    btn_no = ctk.CTkButton(frame, text="Non", command=on_no)
    btn_no.pack(side="left", padx=10)
    dialog.grab_set()
    dialog.wait_window()
    return result[0]

def custom_ask_string(title, prompt):
    dialog = ctk.CTkInputDialog(text=prompt, title=title)
    return dialog.get_input()


# 🔹 Gestion des fichiers et dossiers

def creer_fichier(dir, update_barre_callback=None):
    nom_fichier = custom_ask_string("Créer un fichier", "Nom du fichier à créer :")
    if nom_fichier:
        chemin = os.path.join(dir, nom_fichier)
        attempt = 0
        while attempt < 2:
            try:
                with open(chemin, "w") as f:
                    pass
                if update_barre_callback:
                    update_barre_callback(chemin)
                return
            except OSError as ose:
                if ose.errno == 13:
                    if attempt == 0:
                        retry = custom_ask_yes_no("Autorisation requise", 
                                                  f"Accès refusé pour créer le fichier.\nVoulez-vous réessayer ?")
                        if not retry:
                            return
                        attempt += 1
                    else:
                        custom_show_error("Accès refusé", f"Accès toujours refusé pour créer le fichier")
                        return
                else:
                    custom_show_error("Erreur", f"Impossible de créer le fichier")
                    return
            except Exception as e:
                custom_show_error("Erreur", f"Impossible de créer le fichier")
                return

def creer_dossier(dir, update_barre_callback=None):
    nom_dossier = custom_ask_string("Créer un dossier", "Nom du dossier à créer :")
    if nom_dossier:
        chemin = os.path.join(dir, nom_dossier)
        attempt = 0
        while attempt < 2:
            try:
                os.makedirs(chemin, exist_ok=True)
                if update_barre_callback:
                    update_barre_callback(chemin)
                return
            except OSError as ose:
                if ose.errno == 13:
                    if attempt == 0:
                        retry = custom_ask_yes_no("Autorisation requise", 
                                                  f"Accès refusé pour créer le dossier.\nVoulez-vous réessayer ?")
                        if not retry:
                            return
                        attempt += 1
                    else:
                        custom_show_error("Accès refusé", f"Accès toujours refusé pour créer le dossier")
                        return
                else:
                    custom_show_error("Erreur", f"Impossible de créer le dossier")
                    return
            except Exception as e:
                custom_show_error("Erreur", f"Impossible de créer le dossier")
                return

def ouvrir_element(nom, dir, affichage=None, update_barre_callback=None):
    """
    Ouvre un fichier ou un dossier.
    
    Si c'est un dossier, l'affichage est mis à jour et le chemin est ajouté à l'historique.
    Si c'est un fichier, il est ouvert avec l'application par défaut du système.
    En cas d'erreur d'accès (PermissionError), l'utilisateur peut réessayer.
    """
    chemin = os.path.join(dir, nom)
    if not os.path.exists(chemin):
        custom_show_error("Erreur", f"L'élément '{chemin}' n'existe pas.")
        return

    attempt = 0
    while attempt < 2:
        try:
            if os.path.isdir(chemin):
                # Si c'est un dossier, on met à jour l'affichage et l'historique
                if affichage:
                    affichage.chemin = chemin
                    affichage.afficher_contenu()
                    add_recents(chemin)
                if update_barre_callback:
                    update_barre_callback(chemin)
            else:
                # Si c'est un fichier, ouvrir avec l'application par défaut
                if sys.platform.startswith("win"):
                    os.startfile(chemin)
                elif sys.platform.startswith("darwin"):
                    subprocess.Popen(["open", chemin])
                else:
                    subprocess.Popen(["xdg-open", chemin])
            return
        except OSError as ose:
            if ose.errno == 13:
                if attempt == 0:
                    retry = custom_ask_yes_no("Autorisation requise", 
                                               f"Accès refusé pour ouvrir l'élément.\nVoulez-vous réessayer ?")
                    if not retry:
                        return
                    attempt += 1
                else:
                    custom_show_error("Accès refusé", "Accès toujours refusé pour ouvrir l'élément.")
                    return
            else:
                custom_show_error("Erreur", "Erreur lors de l'ouverture.")
                return
        except Exception as e:
            custom_show_error("Erreur", "Erreur lors de l'ouverture.")
            return


def renommer_element(nom, dir):
    chemin = os.path.join(dir, nom)
    if not os.path.exists(chemin):
        custom_show_error("Erreur", f"L'élément '{chemin}' n'existe pas.")
        return
    nouveau_nom = custom_ask_string("Renommer", f"Nouveau nom pour '{nom}' :")
    if nouveau_nom:
        nouveau_chemin = os.path.join(dir, nouveau_nom)
        attempt = 0
        while attempt < 2:
            try:
                os.rename(chemin, nouveau_chemin)
                return
            except OSError as ose:
                if ose.errno == 13:
                    if attempt == 0:
                        retry = custom_ask_yes_no("Autorisation requise", 
                                                  f"Accès refusé lors du renommage.\nVoulez-vous réessayer ?")
                        if not retry:
                            return
                        attempt += 1
                    else:
                        custom_show_error("Accès refusé", f"Accès toujours refusé lors du renommage")
                        return
                else:
                    custom_show_error("Erreur", f"Erreur lors du renommage")
                    return
            except Exception as e:
                custom_show_error("Erreur", f"Erreur lors du renommage")
                return

def supprimer_element(nom, dir):
    chemin = os.path.join(dir, nom)
    if not os.path.exists(chemin):
        custom_show_error("Erreur", f"L'élément '{chemin}' n'existe pas.")
        return
    reponse = custom_ask_yes_no("Supprimer", f"Voulez-vous vraiment supprimer '{nom}' ?")
    if reponse:
        attempt = 0
        while attempt < 2:
            try:
                if os.path.isdir(chemin):
                    shutil.rmtree(chemin)
                else:
                    os.remove(chemin)
                return
            except OSError as ose:
                if ose.errno == 13:
                    if attempt == 0:
                        retry = custom_ask_yes_no("Autorisation requise", 
                                                  f"Accès refusé lors de la suppression.\nVoulez-vous réessayer ?")
                        if not retry:
                            return
                        attempt += 1
                    else:
                        custom_show_error("Accès refusé", f"Accès toujours refusé lors de la suppression")
                        return
                else:
                    custom_show_error("Erreur", f"Erreur lors de la suppression")
                    return
            except Exception as e:
                custom_show_error("Erreur", f"Erreur lors de la suppression")
                return

def ajouter_aux_favoris(nom, dir):
    """Ajoute un fichier ou un dossier aux favoris"""
    chemin = os.path.join(dir, nom)
    if not os.path.exists(chemin):
        custom_show_error("Erreur", f"L'élément '{chemin}' n'existe pas.")
        return
    try:
        ajouter_favori(chemin)
        custom_show_info("Favoris", f"'{nom}' a été ajouté aux favoris.")
    except Exception as e:
        custom_show_error("Erreur", f"Erreur lors de l'ajout aux favoris")

# Variable pour stocker l'élément à copier ou couper
chemin_copie = None
chemin_coupe = None

def copier_element(nom, dir):
    """Stocke l'élément à copier sans le supprimer."""
    global chemin_copie, chemin_coupe
    chemin_copie = os.path.join(dir, nom)
    chemin_coupe = None  # On s'assure qu'on ne coupe pas en même temps
    custom_show_info("Copie", f"'{nom}' est prêt à être copié.")

def couper_element(nom, dir):
    """Stocke l'élément à couper (déplacement)."""
    global chemin_coupe, chemin_copie
    chemin_coupe = os.path.join(dir, nom)
    chemin_copie = None  # On s'assure qu'on ne copie pas en même temps
    custom_show_info("Couper", f"'{nom}' est prêt à être déplacé.")

import threading

# Drapeaux globaux pour annuler l'opération
cancel_copy = threading.Event()

class ProgressBarWindow(ctk.CTkToplevel):
    def __init__(self, master, title="Progression", **kwargs):
        super().__init__(master, **kwargs)
        self.title(title)
        self.geometry("400x100")
        self.resizable(False, False)
        # Centrer la fenêtre si besoin (vous pouvez ajouter une fonction center_window)
        self.progress = ctk.CTkProgressBar(self, mode="determinate")
        self.progress.set(0)
        self.progress.pack(padx=20, pady=10, fill="x")
        self.cancel_btn = ctk.CTkButton(self, text="Annuler", command=self.annuler)
        self.cancel_btn.pack(pady=5)
        self.protocol("WM_DELETE_WINDOW", self.annuler)

    def annuler(self):
        cancel_copy.set()
        self.destroy()

def copy_file_with_progress(src, dest, progress_win, chunk_size=1024*1024):
    """
    Copie le fichier src vers dest par blocs, 
    met à jour la barre de progression et surveille l'annulation.
    """
    total_size = os.path.getsize(src)
    copied = 0
    try:
        with open(src, "rb") as fsrc, open(dest, "wb") as fdest:
            while True:
                if cancel_copy.is_set():
                    raise Exception("Copie annulée par l'utilisateur.")
                chunk = fsrc.read(chunk_size)
                if not chunk:
                    break
                fdest.write(chunk)
                copied += len(chunk)
                progress = copied / total_size
                progress_win.progress.set(progress)
                progress_win.update_idletasks()
        return True
    except Exception as e:
        return e

def coller_element():
    """Colle l'élément copié ou coupé dans la destination récente, avec suivi de progression."""
    destinations = send_recent()
    if not destinations:
        custom_show_error("Erreur", "Aucune destination disponible.")
        return

    destination = destinations[-1]  # Dernier élément récent
    # Si la destination est un fichier, prendre son dossier parent
    if os.path.isfile(destination):
        destination = os.path.dirname(destination)
    if not os.path.isdir(destination):
        custom_show_error("Erreur", f"Destination invalide : '{destination}'")
        return

    global chemin_copie, chemin_coupe

    # Fonction utilitaire pour générer un nom unique en cas de conflit
    def get_unique_name(src, dest_dir):
        base, ext = os.path.splitext(os.path.basename(src))
        compteur = 1
        nouveau_nom = f"{base}_{compteur}{ext}"
        nouveau_chemin = os.path.join(dest_dir, nouveau_nom)
        while os.path.exists(nouveau_chemin):
            compteur += 1
            nouveau_nom = f"{base}_{compteur}{ext}"
            nouveau_chemin = os.path.join(dest_dir, nouveau_nom)
        return nouveau_chemin

    # Mode copie avec progression
    if chemin_copie:
        try:
            cible = os.path.join(destination, os.path.basename(chemin_copie))
            if os.path.exists(cible):
                remplacer = custom_ask_yes_no(
                    "Conflit de nom",
                    f"Un élément nommé '{os.path.basename(chemin_copie)}' existe déjà dans '{destination}'.\nVoulez-vous le remplacer ?"
                )
                if not remplacer:
                    cible = get_unique_name(chemin_copie, destination)
            # Si c'est un dossier, utiliser copytree (sans barre de progression)
            if os.path.isdir(chemin_copie):
                shutil.copytree(chemin_copie, cible)
                custom_show_info("Collage réussi", f"'{os.path.basename(chemin_copie)}' a été copié dans '{destination}'.")
            else:
                # Pour un fichier, utiliser la copie avec progression
                progress_win = ProgressBarWindow(None, title="Copie en cours")
                def copy_task():
                    result = copy_file_with_progress(chemin_copie, cible, progress_win)
                    progress_win.destroy()
                    if result is True:
                        custom_show_info("Collage réussi", f"'{os.path.basename(chemin_copie)}' a été copié dans '{destination}'.")
                    else:
                        custom_show_error("Erreur", f"Erreur lors de la copie : {result}")
                threading.Thread(target=copy_task, daemon=True).start()
        except PermissionError as pe:
            custom_show_error("Accès refusé", f"Accès refusé pour copier l'élément : {pe}")
        except FileExistsError:
            custom_show_error("Erreur", f"Un élément portant le même nom existe déjà dans '{destination}'.")
        except Exception as e:
            custom_show_error("Erreur", f"Erreur lors de la copie : {e}")
        finally:
            chemin_copie = None

    # Mode déplacement
    elif chemin_coupe:
        try:
            cible = os.path.join(destination, os.path.basename(chemin_coupe))
            if os.path.exists(cible):
                remplacer = custom_ask_yes_no(
                    "Conflit de nom",
                    f"Un élément nommé '{os.path.basename(chemin_coupe)}' existe déjà dans '{destination}'.\nVoulez-vous le remplacer ?"
                )
                if not remplacer:
                    cible = get_unique_name(chemin_coupe, destination)
            shutil.move(chemin_coupe, cible)
            custom_show_info("Déplacement réussi", f"'{os.path.basename(chemin_coupe)}' a été déplacé vers '{destination}'.")
            chemin_coupe = cible  # Mise à jour du chemin si nécessaire
        except PermissionError as pe:
            custom_show_error("Accès refusé", f"Accès refusé pour déplacer l'élément : {pe}")
        except FileExistsError:
            custom_show_error("Erreur", f"Un élément portant le même nom existe déjà dans '{destination}'.")
        except Exception as e:
            custom_show_error("Erreur", f"Erreur lors du déplacement : {e}")
        finally:
            chemin_coupe = None
    else:
        custom_show_error("Erreur", "Aucun élément à coller.")
