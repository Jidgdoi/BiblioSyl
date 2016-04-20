#-*- coding: utf-8 -*-
#! /usr/bin/env python
# C. Fournier, 2014

import os
import wx
from wx.lib.dialogs import ScrolledMessageDialog
from subprocess import check_output

from SessionLog import SessionLog
from BookFormular import BookFormular
from VirtualList import VirtualList
from MyUtils import *

# =============================================================================
#
#	Partie principale de la fenêtre
#
# =============================================================================

class PrincipalFrame(wx.Frame):
	"""
	Fenêtre gérant l'interface utilisateur avec le menu, la liste des livres, la recherche, etc.
	"""
	def __init__(self, parent, ID, title, size, pathSrc="./", style = wx.DEFAULT_FRAME_STYLE):
		self.sessionLog = SessionLog(pathSrc)
		wx.Frame.__init__(self, parent, ID, title, size=self.sessionLog.getSize(), style=style)

		# --- Détection du système d'exploitation
		self.win32 = (wx.Platform == '__WXMSW__')
		self.OS = os.sep
		# --- Définition des paths des différents dossiers ---
		self.pathSrc = pathSrc
		self.pathIcone = self.pathSrc + "icones" + self.OS
		self.pathLibrary = "/home/cfournier/Documents/Perso/BiblioSyl/data/Example_library.lsc"
		self.pathCouv = "/home/cfournier/Documents/Perso/BiblioSyl/data/Example_library_book_cover/"
		
		# --- Vérification de la présence des dossiers ---
#		for myDir in [self.pathData, self.pathCouv, self.pathLivre]:
#			if not os.path.isdir(myDir):
#				os.makedirs(myDir)
		
		# --- Changement de couleur de l'arrière plan
		self.myBackgroundColour = wx.Colour(255,255,255,255)
		self.SetBackgroundColour(self.myBackgroundColour)
		
		# --- Si True, fenêtre d'ajout de livre ouverte
		self.ajoutLivreFrame = False
		
		# --- Création de la barre de log
		self.CreateStatusBar(1)
		
		# --- Dimension de la fenêtre et de ses différents éléments
		self.menuSize = 0				# Hauteur en pixel du menu
		if self.win32: self.menuSize = 61
		self.searchBanner = 70		# Hauteur en pixel de la bannière du champs de recherche
		self.w = size[0]			# Largeur totale de la fenêtre
		self.h = size[1] - 20 - self.searchBanner - self.menuSize		# Hauteur de la fenêtre sans le log ni la bannière de recherche ni le menu
		self.vboxWidth = 280		# Largeur de la vbox avec couverture et commentaire
		self.couvRatio = 1.45		# Ratio Largeur/Hauteur de la couverture
		self.bordGWidth = 85	# Largeur de l'arabesque bordure gauche
		
		self.SetMinSize((size[0]/2.0, size[1]))

		# --- Création de la liste
		self.list = VirtualList(self)

		# --- Initialisation de la barre de menu
		self.initMenuBar()

		# --- Initialisation des box
		self.vboxAll = wx.BoxSizer(wx.VERTICAL)			# Contient tous les BoxSizer
		self.hbox = wx.BoxSizer(wx.HORIZONTAL)			# Bordure | list | vbox
		self.vbox = wx.BoxSizer(wx.VERTICAL)			# Couverture | Commentaire

		# --- Initialisation du champs de recherche et de statistiques
		fontStBox = createMyFont({'pointSize':12, 'weight':wx.BOLD, 'faceName':'Comic Sans MS'})
		fontStText = createMyFont()
		
		# 1er champs: TextCtrl
		self.vboxAll.Add((-1,self.searchBanner), flag=wx.LEFT)
		x,y = 5,0
		StBox = wx.StaticBox(self, label="Recherche par mots-clés".decode('utf-8'), pos=(x,y), size=(275, self.searchBanner-5))
		StBox.SetFont(fontStBox)
		x+=5
		self.keyWords = wx.TextCtrl(self, value="", pos=(x,25), size=(265,25), style=wx.TE_PROCESS_ENTER)
		x+=275
		# 2ème champs: Mots-clés actuels
		StBox = wx.StaticBox(self, label="Mots-clés actuels".decode('utf-8'), pos=(x,y), size=(280, self.searchBanner-5))
		StBox.SetFont(fontStBox)
		x+=5
		self.currKeyWords = wx.StaticText(self, label="", pos=(x,20), size=(270, self.searchBanner-30), style=wx.ST_NO_AUTORESIZE|wx.TE_MULTILINE)
		self.currKeyWords.SetFont(fontStText)
		x+=280
		# 3ème champs: Statistiques
		self.StBoxStat = wx.StaticBox(self, label="Quelques chiffres", pos=(x,y), size=(700, self.searchBanner-5))
		self.StBoxStat.SetFont(fontStBox)
		x+=5
		self.statistiques = wx.StaticText(self, label="", pos=(x,20), size=(690, self.searchBanner-30), style=wx.TE_MULTILINE)
#		self.statistiques = wx.TextCtrl(self, pos=(x,20), size = (690, self.searchBanner-30), style=wx.TE_MULTILINE|wx.TE_READONLY|wx.NO_BORDER)
		self.statistiques.SetFont(fontStText)
		self.statistiques.SetBackgroundColour(self.myBackgroundColour)

		# --- Initialisation bordure gauche
		self.hbox.Add((self.bordGWidth, -1), 0, flag=wx.EXPAND)
		img = wx.Image(self.pathIcone + "bordureDouble.png", wx.BITMAP_TYPE_ANY)
		img = img.Scale(self.bordGWidth, self.bordGWidth*10.7, wx.IMAGE_QUALITY_HIGH)
		self.bitmapBordG = img.ConvertToBitmap()
		img = self.bitmapBordG.GetSubBitmap(wx.Rect(0,0,self.bitmapBordG.GetWidth(), self.h))
		self.bordG = wx.StaticBitmap(self, -1, img, pos=(0, self.searchBanner), size=(img.GetWidth(), img.GetHeight()))

		# --- Ajout de la liste des livres à la hbox
		self.hbox.Add(self.list, proportion=1, flag=wx.EXPAND)

		# --- Initialisation de la liste de couverture des livres
		self.lCouvBitmap = self.initCouvertures(self.pathCouv)
		# Initialisation de la couverture du livre
		tmp = self.lCouvBitmap[DEFAULTCOVER]
		self.couv = wx.StaticBitmap(self, -1, tmp, size=(tmp.GetWidth(),tmp.GetHeight()))
		# self.vbox.Add(self.couv, flag=wx.SizerFlags().Align(wx.ALIGN_TOP))
		self.vbox.Add(self.couv, flag=wx.ALIGN_TOP)

		# --- Ajout des commentaires
		comSTtitle = wx.StaticText(self, label="Commentaire sur ce livre:", style=wx.DEFAULT)
		font = createMyFont({'pointSize':14, 'family':wx.ROMAN, 'style':wx.SLANT, 'weight':wx.BOLD, 'underline':True})
		comSTtitle.SetFont(font)
		comSTtitle.SetForegroundColour((255,0,0))
		
		self.comTC = wx.TextCtrl(self, value="Les commentaires associés à vos livres seront affichés ici.".decode('utf-8'), size=(self.vboxWidth,self.h), style=wx.TE_MULTILINE|wx.TE_READONLY)
		font = createMyFont({'pointSize':10, 'family':wx.SWISS, 'faceName':"Comic Sans MS"})
		self.comTC.SetFont(font)
		self.vbox.AddMany([(comSTtitle),(self.comTC, 1, wx.RIGHT)])

		# --- "Empillage" final des box
		self.hbox.Add(self.vbox, proportion=0, flag=wx.RIGHT)
		self.vboxAll.Add(self.hbox, proportion=1,flag=wx.EXPAND)
		self.SetSizer(self.vboxAll)

		# --- Définition des events
		# self.Bind(wx.EVT_SIZE, self.OnResize)
		self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftClick)
		self.Bind(wx.EVT_TEXT, self.OnKeyWords)
		self.Bind(wx.EVT_TEXT_ENTER, self.OnKeyWords)
		self.Bind(wx.EVT_TIMER, self.OnTimer)
		self.Bind(wx.EVT_CLOSE, self.OnQuit)

		# --- Initialisation du Timer
		self.timer = wx.Timer(self, 1)
		self.pointeur = 0			# Position du pointeur dans le message
		self.rawStatMess = ""		# Message brut des statistiques
		self.list.calcStatistiques()# Mise à jour du message
		self.timer.Start(200)		# X millisecondes d'intervalle

		# --- Affichage et centrage de la fenêtre
		self.Centre()
		self.Show(True)


	# ------------------------------------------------
	# --- Fontions d'initialisation et autres

	def vboxActu(self, comm, couv):
		"""
		Actualise la couverture et le commentaire associé au livre sélectionné
		"""
		# --- Actualisation du commentaire
		self.comTC.SetValue(comm)
		
		# --- Actualisation de la couverture
		imgSB = wx.StaticBitmap(self, -1, self.lCouvBitmap[couv], size=(self.lCouvBitmap[couv].GetWidth(), self.lCouvBitmap[couv].GetHeight()))
		self.vbox.Replace(self.couv, imgSB)
		self.couv = imgSB
		self.vbox.Layout()

	def initMenuBar(self):
		"""
		Initialise la barre de menu
		"""
		# --- Menu object
		menubar = wx.MenuBar()
		
		# --- File menu
		fileMenu = wx.Menu()
		
		# File's menu item
		ajouterItem = wx.MenuItem(fileMenu, wx.ID_ADD, '&Ajouter un livre\tCtrl+A')
		fileMenu.AppendItem(ajouterItem)
		self.Bind(wx.EVT_MENU, self.OnAdd, ajouterItem)
		
		openLib = wx.MenuItem(fileMenu, wx.ID_OPEN, '&Ouvrir bibliothèque...\tCtrl+N')
		fileMenu.AppendItem(openLib)
		self.Bind(wx.EVT_MENU, self.OnOpenLib, openLib)
		
		# -----------------------
		fileMenu.AppendSeparator()
		
		saveLib = wx.MenuItem(fileMenu, wx.ID_SAVE, '&Enregistrer\tCtrl+S')
		fileMenu.AppendItem(saveLib)
		self.Bind(wx.EVT_MENU, self.OnSaveLib, saveLib)
		
		saveAsLib = wx.MenuItem(fileMenu, wx.ID_SAVEAS, '&Enregistrer sous...\tCtrl+Shift+S')
		fileMenu.AppendItem(saveAsLib)
		self.Bind(wx.EVT_MENU, self.OnSaveAsLib, saveAsLib)
		
		# -----------------------
		fileMenu.AppendSeparator()
		
		quitItem = wx.MenuItem(fileMenu, wx.ID_EXIT, '&Quitter\tCtrl+Q')
		fileMenu.AppendItem(quitItem)
		self.Bind(wx.EVT_MENU, self.OnQuit, quitItem)
		
		# --- Edition menu
		editionMenu = wx.Menu()
		
		# Edition's menu item
		findItem = wx.MenuItem(editionMenu, wx.ID_FIND, '&Rechercher\tCtrl+F')
		editionMenu.AppendItem(findItem)
		self.Bind(wx.EVT_MENU, self.OnFind, findItem)
		
		# --- Tools menu
		toolMenu = wx.Menu()
		
		# Tool's menu item
		showStats = wx.MenuItem(toolMenu, wx.ID_ABOUT, 'Statistiques de la bibliothèque')
		toolMenu.AppendItem(showStats)
		self.Bind(wx.EVT_MENU, self.OnShowStats, showStats)

		menubar.Append(fileMenu, '&Fichier')
		menubar.Append(editionMenu, '&Edition')
		menubar.Append(toolMenu, '&Outils')
		self.SetMenuBar(menubar)

	def initCouvertures(self, path):
		"""
		Cré une liste d'images Bitmap de toutes les couv du dossier 'path'
		"""
		dNameBitmap = {}
		# --- Convert default cover to bitmap
		img = wx.Image(self.pathIcone + DEFAULTCOVER, wx.BITMAP_TYPE_ANY)
		img = img.Scale(self.vboxWidth, self.vboxWidth*self.couvRatio, wx.IMAGE_QUALITY_HIGH)
		img = img.ConvertToBitmap()
		dNameBitmap[DEFAULTCOVER] = img
		
		# --- List all cover pictures, then convert them to bitmap.
		if path:
			l = os.listdir(path)
			for name in l:
				img = wx.Image(path + name, wx.BITMAP_TYPE_ANY)
				img = img.Scale(self.vboxWidth, self.vboxWidth*self.couvRatio, wx.IMAGE_QUALITY_HIGH)
				img = img.ConvertToBitmap()
				dNameBitmap[name] = img
		return dNameBitmap

	def updateLCouvBitmap(self, couv, old=''):
		"""
		Met à jour la liste d'images Bitmap des couvertures de livre
		"""
		# --- Si précédente couverture existante et différente de la couverture par défaut
		if self.lCouvBitmap.has_key(old) and old != 'image-not-available.jpg':
			exist = False
			for liv in self.list.maBiblio.dLibrary.values():
				if liv.couverture == old:	# Un autre livre utilise la couverture 'old', on la garde
					exist = True
					break
			# Aucun autre livre n'utilise la couverture 'old', on la supprime de lCouvBitmap ainsi que du dossier 'couvertures'
			if not exist:
				self.lCouvBitmap.pop(old)
				os.remove(self.pathCouv + old)
		
		# --- Pour finir on importe la nouvelle couverture si elle n'existe pas déjà
		if not self.lCouvBitmap.has_key(couv):
			# Chargement et convertion de l'image en Bitmap
			img = wx.Image(self.pathCouv + couv, wx.BITMAP_TYPE_ANY)
			img = img.Scale(self.vboxWidth, self.vboxWidth*self.couvRatio, wx.IMAGE_QUALITY_HIGH)
			img = img.ConvertToBitmap()
			self.lCouvBitmap[couv] = img
		return 0

	def updateLibrary(self, newPath):
		"""
		Update path variables in Library, VirtualList and self.
		"""
		# --- Update paths and library
		self.pathLibrary = newPath
		self.list.maBiblio.updateLibrary(self.pathLibrary)
		self.pathCouv = self.list.maBiblio.pathCover
		# --- Update cover pictures
		[self.updateLCouvBitmap(cover) for cover in self.list.maBiblio.getLCover()]
		# --- Update the virtual list
		self.list.listActu()

	def maxMessLength(self, message, length=690):
		"""
		Recoupe le message pour qu'il tienne dans la fenêtre d'affichage
		"""
		tmp = message
		while self.statistiques.GetTextExtent(tmp)[0] > length:
			tmp = tmp[:-1]
		return len(tmp)

	def saveTo(self, pathFile):
		"""
		Save the library and the covers picture associated.
		"""
		# No extention: add one
		if os.path.splitext(pathFile)[1] != self.list.maBiblio.extLivre:
			pathFile += self.list.maBiblio.extLivre
		# Save to a new file: create book directory etc.
		if pathFile != self.pathLibrary:
			self.list.maBiblio.saveLibrary(pathFile)
		# Save to the current file
		else:
			self.list.maBiblio.saveLibrary()
		return True

	def quit(self):
		"""
		Save session information before closing the program properly.
		"""
		print "Save Window's position and size, save current library path."
		self.Destroy()

	# ------------------------------------------------
	# --- Evenements Menu

	def OnAdd(self, evt):
		"""
		Active la fenêtre d'ajout de livre.
		"""
		if self.ajoutLivreFrame:
			self.ajoutLivreFrame.SetFocus()
		else:
			self.ajoutLivreFrame = BookFormular(self, -1, title="Ajout d'un livre")
			self.ajoutLivreFrame.Show(True)
			self.ajoutLivreFrame.CentreOnParent()

	def OnOpenLib(self, evt):
		"""
		Select the new library and open it.
		"""
		dPath = os.path.dirname(self.pathLibrary)
		if not dPath and self.win32: dPath = "c:\\"
		fdlg = wx.FileDialog(self, message="Ouvrir bibliothèque...",
								defaultDir=dPath,
								wildcard="Library SC (*.lsc)|*.lsc",
								style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST)
		if fdlg.ShowModal() == wx.ID_OK:
			# A file has been selected
			pathFile = fdlg.GetPath()
			self.updateLibrary(pathFile)
		fdlg.Destroy()

	def OnSaveLib(self, evt):
		"""
		Save the library.
		"""
		print "Saved to : %s" %self.list.maBiblio.pathLibrary
		OK = True
		if not self.list.maBiblio.pathLibrary:
			OK = self.OnSaveAsLib(evt)
		if OK:
			self.list.maBiblio.saveLibrary()

	def OnSaveAsLib(self, evt):
		"""
		Save library as ...
		"""
		print "OnSaveAsLib: %s" %evt.GetId()
		saved = False
		# --- Open file dialog
		dPath = os.path.dirname(self.pathLibrary)
		if not dPath and self.win32: dPath = "c:\\"
		fdlg = wx.FileDialog(self, message="Enregistrer sous...",
								defaultDir=dPath,
								wildcard="Library SC (*.lsc)|*.lsc",
								style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)
		if fdlg.ShowModal() == wx.ID_OK:
			# A file has been selected
			saved = True
			pathFile = fdlg.GetPath()
			# Save
			self.saveTo(pathFile)
		fdlg.Destroy()
		return saved

	def OnQuit(self, evt):
		"""
		Quit the program and save library if the user wants to.
		"""
		OK = True
		# --- On demande si l'utilisateur veut faire une sauvegarde de ses données.
		box = wx.MessageDialog(self, message="Voulez-vous sauvegarder les données enregistrées pendant la session avant de quitter ?".decode('utf-8'), caption='Quitter BiblioSyl', style=wx.YES_NO|wx.CANCEL|wx.STAY_ON_TOP|wx.ICON_INFORMATION)
		choix = box.ShowModal()
		# --- Cancel
		if choix == wx.ID_CANCEL:
			box.Destroy()
			return
		# --- Accept
		elif choix == wx.ID_YES:
			if not self.list.maBiblio.pathLibrary:
				OK = self.OnSaveAsLib(evt)
		box.Destroy()
		# --- File correctly saved, we can quit
		if OK:
			self.quit()

	def OnFind(self, evt):
		"""
		Met le focus sur le TextCtrl de recherche par mots-clés
		"""
		self.keyWords.SetFocus()

	def OnShowStats(self, evt):
		"""
		Open a window with stats about the current library.
		"""
		message = self.list.calcStatistiques2()
#		statBox = ScrolledMessageDialog(self, msg=message.encode('utf-8'), caption='Statistiques de la bibliothèque', style=wx.STAY_ON_TOP)
		statBox = wx.MessageBox(message=message.encode('utf-8'), caption='Statistiques de la bibliothèque', style=wx.STAY_ON_TOP)
		close = statBox.ShowModal()
		statBox.Destroy()

	# ------------------------------------------------
	# --- Evenements Souris/Clavier/Timer/Frame

	def OnResize(self, evt):
		"""
		Evènement de mouvement de la fenêtre (déplacement/redimentionnement)
		"""
		print "evt.GetSize",evt.GetSize()
		# w,h = self.GetSize()
		# printLogText("Dimension de la fenêtre (w,h): (".decode('utf-8')+str(w)+", "+str(h)+")")
		# pos = self.StBoxStat.GetPosition()
		# size = self.StBoxStat.GetSize()
		# print pos, size
		# if pos[0] + size[0] > w:
			# if w-pos[0] -10> 200:
				# print "modif"
				# self.StBoxStat.SetSize((w-pos[0]-10, size[1]))
		# self.StBoxStat.Refresh()

	def OnLeftClick(self, evt):
		"""
		Evénement clique gauche
		"""
		x,y = evt.GetPosition()
		newLabel = "x: "+str(x)+" y: "+str(y)
		print(newLabel)
		printLogText(newLabel)

	def OnKeyWords(self, evt):
		"""
		Evenement touche Entrée/changement du champs du TextCtrl 'keyWords'
		"""
		words = self.keyWords.GetValue().encode('utf-8').split(";")
		try:
			words.remove('')
		except ValueError:
			None
		self.currKeyWords.SetLabel(', '.join(words))
		self.currKeyWords.Wrap(self.currKeyWords.GetSize()[0])
		self.list.keyWordsActu(words)
		self.list.listActu()

	def OnTimer(self, evt):
		"""
		Evenement du timer - se déclenche toutes les X millisecondes
		"""
		if type(self.rawStatMess) is list:
			# CAS: des livres sont sélectionnés
			fixe = self.rawStatMess[0]
			deroulant = '      '.join(self.rawStatMess[1:]) + '      '
			if len(deroulant) <= self.maxMessLength(deroulant):
				message = deroulant
			else:
				message = deroulant[self.pointeur:] + deroulant[:self.pointeur]
			label = fixe + '\n' + message[:self.maxMessLength(message)]
		else:
			# CAS: aucun livre sélectionné
			message = self.rawStatMess + '    '
			while len(message) <= self.maxMessLength(message):
				message += self.rawStatMess + '    '
			message = message[self.pointeur:] + message[:self.pointeur]
			label = message[:self.maxMessLength(message)]
		
		self.statistiques.SetLabel(label)
		
		# Incrémentation de la position du pointeur
		self.pointeur += 1
		self.pointeur %= len(message)

