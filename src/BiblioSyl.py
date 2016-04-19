#-*- coding: utf-8 -*-
#! /usr/bin/env python
# C. Fournier, 2014

#########################################################################

# Main script

#########################################################################

# ------------------------------------------
# --- Things to do, by order of priority ---
# ------------------------------------------
# ---------------------
# --- TODO Pro TODO ---
# - Supprimer la bande défilante des statistiques. La remplacer par autre chose. Créer un onglet du menu "Outils -> Statistiques de la bibliothèque".
# - Créer un fichier .log, qui contiendra les options de la dernière session: position fenêtre, taille, bibliothèque ouverte, ...

# --------------------------------------
# --- FIXME Correction of bugs FIXME ---
# - Lorsque le trie des lignes est par ordre décroissant et que l'on clique sur un livre, le trie se refait tout seul par ordre croissant sur la même colonne.

# -------------------------------
# --- TODO Functionality TODO ---
# - Ajouter une information pour les livres 'read', si lu par qqn. Ajouter une colonne dans ListCtrl ?
# - Créer une page d'aide, décrivant étape par étape comment ajouter un livre.
# - Ajouter dans le menu des onglets pour "Fichier récent".

# -------------------------------
# --- TODO Effectiveness TODO ---
# - Ajouter bulle d'aide sur les boutons !
# - Corriger clignotement de la bannière Stats défilante
# - Créer une classe GestionErreur qui s'occupera d'envoyer un message d'erreur à l'utilisateur/console, pour Livre non conforme, sauvegarde impossible, une couverture de livre inexistante, ...

# ----------------------------
# --- TODO Good shape TODO ---
# - Changer ListCtrl en UltimateListCtrl pour permettre la gestion de plusieurs ImageList (notes, trieur)
# - Actualiser dynamiquement la taille de l'arabesque bord gauche avec l'event EVT_SIZE (ou autre)
# - Changer la couleur des lignes suivant la colonne de trie actuelle. La couleur changera si le livre suivant a une valeur différente dans la colonne triée.


import os, sys
import wx
import getpass

from PrincipalFrame import PrincipalFrame

if __name__ == '__main__':
	print "PLATFORM",wx.Platform
	print sys.argv[0]
	print os.path.realpath(sys.argv[0])
	sys.exit(0)
	pathSrc = os.path.dirname(os.path.realpath(sys.argv[0])) + os.sep
	app = wx.PySimpleApp()
	user = getpass.getuser()
	PrincipalFrame(None, -1, title=("Bibliothèque personnalisée de %s"%(user)).decode('utf-8'), size=(1574, 850), pathSrc=pathSrc)
	app.MainLoop()
	print "\nProgram closed."
