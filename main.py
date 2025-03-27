import customtkinter as ctk
from gui.fenetre_principale import FenetrePrincipale

def main():
    root = ctk.CTk()
    app = FenetrePrincipale(root)
    root.minsize(600,350)
    root.mainloop()

if __name__ == "__main__":
    main()
 