#-*- coding: utf-8 -*-
#! /usr/bin/env python
# C. Fournier, 2014

import os
import wx
import webbrowser as wb

from Book import Book
from MyUtils import *

# =============================================================================
#
#	Fenêtre d'ajout de livre
#
# =============================================================================

class BookFormular(wx.Dialog):
	"""
	Window of modification and creation of books.
	"""
	def __init__(self, parent, id, title="Boîte de dialogue", size=(770, 650), state=False, defValue=Book().__dict__):
		wx.Dialog.__init__(self, parent, id, title, size=size, style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
		
		self.principalFrame = parent
		self.SetBackgroundColour("#FFFFFF")
		self.size = size			# Dimension de la fenêtre
		if self.principalFrame.win32:
			self.size = (self.size[0], self.size[1]+60)
			self.SetSize(self.size)
		self.isModif = state		# Prend la valeur de l'ID du livre à modifier, sinon False
		self.defValue = defValue	# Valeur par défaut pour chaque widget de capture
		self.modifActuelle = ""		# Prend la valeur de la dernière valeur entrée dans les widgets TextCtrl
		self.InitUI()

		# --- Définition des évènements
		self.Bind(wx.EVT_TEXT, self.OnTextChange)
		self.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		
		self.SetMinSize(self.size)

	def InitUI(self):
		"""
		Initialisation des éléments de la fenêtre
		"""
		w = 120				# Largeur de base pour un texte
		h = 25				# Hauteur de base pour un texte
		self.lhbox = []		# Liste des box horizontales
		
		# Font pour tous les textes
		myFont = createMyFont({'pointSize':13, 'family':wx.ROMAN, 'style':wx.SLANT, 'weight':wx.BOLD})
		
		# Les valeurs listes Edition, Genre et Lieu
		self.dEGL = self.principalFrame.list.maBiblio.dEGL
		
		# IMAGE EN-TETE
		self.lhbox.append(wx.BoxSizer(wx.HORIZONTAL))
		entete = wx.Image(self.principalFrame.pathIcone + "arabesque1.jpg", wx.BITMAP_TYPE_ANY)
		# dim = entete.GetSize()
		# dim = dim[0]/float(dim[1])
		entete = entete.Scale(self.size[0]*0.8, 100, wx.IMAGE_QUALITY_HIGH)
		entete = entete.ConvertToBitmap()
		img = wx.StaticBitmap(self, -1, entete, (entete.GetWidth(), entete.GetHeight()))
		self.lhbox[-1].Add(img, flag=wx.ALL)
		self.lhbox.append(wx.BoxSizer(wx.HORIZONTAL))
		# self.lhbox[-1].Add((70,70), flag=wx.ALL)
		
		# AUTEUR
		self.lhbox.append(wx.BoxSizer(wx.HORIZONTAL))
		ST = wx.StaticText(self, label="Prénom de l'auteur :     ".decode('utf-8'))
		ST.SetFont(myFont)
		self.lhbox[-1].Add(ST, flag=wx.ALL)
		self.pAuteur = wx.TextCtrl(self, size=(w,h), value=self.defValue['auteurPrenom'], style=wx.TE_PROCESS_ENTER)
		self.lhbox[-1].Add(self.pAuteur, proportion=1, flag=wx.ALL)						# Prénom auteur
		self.lhbox[-1].Add((70,-1))
		ST = wx.StaticText(self, label="Nom de l'auteur :     ")
		ST.SetFont(myFont)
		self.lhbox[-1].Add(ST, flag=wx.ALL)
		self.nAuteur = wx.TextCtrl(self, size=(w,h), value=self.defValue['auteurNom'], style=wx.TE_PROCESS_ENTER)
		self.lhbox[-1].Add(self.nAuteur, proportion=1, flag=wx.ALL)						# Nom auteur
		
		# TITRE
		self.lhbox.append(wx.BoxSizer(wx.HORIZONTAL))
		ST = wx.StaticText(self, label="Titre :     ")
		ST.SetFont(myFont)
		self.lhbox[-1].Add(ST, flag=wx.LEFT)
		self.titre = wx.TextCtrl(self, size=(w*3,h), value=self.defValue['titre'], style=wx.TE_PROCESS_ENTER)
		self.lhbox[-1].Add(self.titre, flag=wx.ALIGN_RIGHT)

		# EDITEUR 
		self.lhbox.append(wx.BoxSizer(wx.HORIZONTAL))
		ST = wx.StaticText(self, label="Editeur :     ")
		ST.SetFont(myFont)
		self.lhbox[-1].Add(ST, flag=wx.LEFT)
		self.editeur = wx.ComboBox(self, value=self.defValue['editeur'], choices=self.dEGL['editeur'], style=wx.TE_PROCESS_ENTER)
		self.lhbox[-1].Add(self.editeur, flag=wx.LEFT)

		# ANNEE DE PARUTION
		self.lhbox.append(wx.BoxSizer(wx.HORIZONTAL))
		ST = wx.StaticText(self, label="Année de parution :     ".decode('utf-8'))
		ST.SetFont(myFont)
		self.lhbox[-1].Add(ST, flag=wx.LEFT)
		value = str(self.defValue['parution'])
		if value == '-1':
			value = ''
		self.parution = wx.TextCtrl(self, value=value, size=(w,h), style=wx.TE_PROCESS_ENTER)
		self.lhbox[-1].Add(self.parution, flag=wx.LEFT)

		# GENRE
		self.lhbox.append(wx.BoxSizer(wx.HORIZONTAL))
		ST = wx.StaticText(self, label="Genre :     ")
		ST.SetFont(myFont)
		self.lhbox[-1].Add(ST, flag=wx.LEFT)
		self.genre = wx.ComboBox(self, value=self.defValue['genre'], choices=self.dEGL['genre'], style=wx.TE_PROCESS_ENTER)
		self.lhbox[-1].Add(self.genre, flag=wx.LEFT)

		# NOMBRE DE PAGES
		self.lhbox.append(wx.BoxSizer(wx.HORIZONTAL))
		ST = wx.StaticText(self, label="Nombre de pages :     ")
		ST.SetFont(myFont)
		self.lhbox[-1].Add(ST, flag=wx.LEFT)
		value = str(self.defValue['nbPage'])
		if value == '-1':
			value = ''
		self.pages = wx.TextCtrl(self, value=value, size=(w,h), style=wx.TE_PROCESS_ENTER)
		self.lhbox[-1].Add(self.pages, flag=wx.LEFT)
		
		# LIEU
		self.lhbox.append(wx.BoxSizer(wx.HORIZONTAL))
		ST = wx.StaticText(self, label="Lieu :     ")
		ST.SetFont(myFont)
		self.lhbox[-1].Add(ST, flag=wx.LEFT)
		self.lieu = wx.ComboBox(self, value=self.defValue['lieu'], choices=self.dEGL['lieu'], style=wx.TE_PROCESS_ENTER)
		self.lhbox[-1].Add(self.lieu, flag=wx.LEFT)
		# FindString(string, casesensitive=True)

		# NOTE
		self.lhbox.append(wx.BoxSizer(wx.HORIZONTAL))
		ST = wx.StaticText(self, label="Note (de 1 à 5) :     \n(0=pas de note)".decode('utf-8'))
		ST.SetFont(myFont)
		self.lhbox[-1].Add(ST, flag=wx.LEFT)
		value = self.defValue['note']
		if value == -1:
			value = 0
		self.note = wx.Slider(self, value=value, minValue=0, maxValue=5, size=(250,-1), style=wx.SL_AUTOTICKS|wx.SL_LABELS)
		self.lhbox[-1].Add(self.note, flag=wx.LEFT)

		# COMMENTAIRE
		self.lhbox.append(wx.BoxSizer(wx.HORIZONTAL))
		ST = wx.StaticText(self, label="Commentaire :     ")
		ST.SetFont(myFont)
		self.lhbox[-1].Add(ST, flag=wx.LEFT)
		value = self.defValue['commentaire']
		if value == 'Aucune commentaire.':
			value = ''
		self.commentaire = wx.TextCtrl(self, value=value, size=(w*3,h*3), style=wx.TE_MULTILINE)
		self.lhbox[-1].Add(self.commentaire, flag=wx.LEFT|wx.SHAPED)

		self.lhbox.append(wx.BoxSizer(wx.HORIZONTAL))
		# COUVERTURE
		self.lhbox.append(wx.BoxSizer(wx.HORIZONTAL))
		ST = wx.StaticText(self, label="Couverture du livre :     ")
		ST.SetFont(myFont)
		self.lhbox[-1].Add(ST, flag=wx.LEFT)
		value = self.defValue['couverture']
		if value:
			value = self.principalFrame.pathCouv + value
		self.couverture = wx.FilePickerCtrl(self, path=value,
											message="Sélection de la couverture du livre".decode('utf-8'),
											wildcard="Tous les fichiers|*.*|JPG files (*.jpg)|*.jpg|JPEG files (*.jpeg)|*.jpeg|PNG files (*.png)|*.png|GIF files (*.gif)|*.gif",
											size=(450,25),
											style=wx.FLP_DEFAULT_STYLE)#wx.FLP_OPEN |wx.FLP_FILE_MUST_EXIST)
		self.lhbox[-1].Add(self.couverture, proportion=1, flag=wx.LEFT)
		# Bouton pour la recherche d'image google
		self.lhbox[-1].Add((25,-1), flag=wx.ALIGN_CENTER)
		img = wx.Image(self.principalFrame.pathIcone + 'googleSearch.png', wx.BITMAP_TYPE_ANY)
		img = img.Scale(30*3.7391, 30, wx.IMAGE_QUALITY_HIGH)
		img = img.ConvertToBitmap()
		btn = wx.BitmapButton(self, bitmap=img)
		btn.Bind(wx.EVT_BUTTON, self.OnGoogle)
		self.lhbox[-1].Add(btn, flag=wx.ALIGN_CENTER|wx.ALL)
		
		# ISBN
		self.lhbox.append(wx.BoxSizer(wx.HORIZONTAL))
		ST = wx.StaticText(self, label="ISBN :     ")
		ST.SetFont(myFont)
		self.lhbox[-1].Add(ST, flag=wx.LEFT)
		self.ISBN = wx.TextCtrl(self, size=(w,h), value=self.defValue['ISBN'], style=wx.TE_PROCESS_ENTER)
		self.lhbox[-1].Add(self.ISBN, flag=wx.ALIGN_RIGHT)

		#---------------------------------------------------
		# --- Les boutons 
		self.lhbox.append(wx.BoxSizer(wx.HORIZONTAL))

		if not self.isModif:
			btn = wx.Button(self, label='Ajouter', size=(70, -1))
			btn.myName = "OnAdd"
			btn.Bind(wx.EVT_BUTTON, self.OnAdd)
			self.lhbox[-1].Add(btn, flag=wx.ALIGN_CENTER)
			self.lhbox[-1].Add((15,-1), flag=wx.ALIGN_CENTER)

			btn = wx.Button(self, label='Ajouter et continuer', size=(150, -1))
			btn.myName = "OnAddAndContinue"
			btn.Bind(wx.EVT_BUTTON, self.OnAdd)
			self.lhbox[-1].Add(btn, flag=wx.ALIGN_CENTER)
			self.lhbox[-1].Add((15,-1), flag=wx.ALIGN_CENTER)
		else:
			btn = wx.Button(self, label='Ok', size=(70, -1))
			btn.myName = "OnModif"
			btn.Bind(wx.EVT_BUTTON, self.OnAdd)
			self.lhbox[-1].Add(btn, flag=wx.ALIGN_CENTER)
			self.lhbox[-1].Add((15,-1), flag=wx.ALIGN_CENTER)

		btn = wx.Button(self, label='Annuler', size=(70, -1))
		btn.Bind(wx.EVT_BUTTON, self.OnClose)
		self.lhbox[-1].Add(btn, flag=wx.ALIGN_CENTER)

		#---------------------------------------------------
		# --- Intégration des hbox dans une vbox, et resize
		# --- de la fenêtre sur la vbox

		self.vbox = wx.BoxSizer(wx.VERTICAL)
		self.vbox.Add(self.lhbox[0], proportion=1, flag=wx.ALIGN_CENTER, border=10)		# En-tete
		self.vbox.Add(self.lhbox[1], proportion=1, flag=wx.ALIGN_CENTER, border=10)		# En-tete
		# Boucle sur [1:-1] pour ne pas prendre l'en-tête et les boutons
		for i in range(2,len(self.lhbox)-1):
			self.vbox.Add(self.lhbox[i],proportion=1,flag=wx.ALL, border=10)
		self.vbox.Add(self.lhbox[-1], proportion=1, flag=wx.ALIGN_CENTER, border=10)	# Boutons
		self.SetSizer(self.vbox)

	#---------------------------------------------------
	# --- Action des boutons et autre event

	def OnAdd(self, evt):
		"""
		Lance le mécanisme d'ajout de livre (ou les modifications apportées).
		"""
		# --- Check for errors
		err = False
		label = "D'accord ..."
		values = self.RecupAllValue()
		if values == 0:
			err = "Veuillez au moins entrer le titre du livre pour l'ajouter à la biliothèque virtuelle.\n\n ".decode('utf-8')
		elif values == 1:
			err = "L'année de parution du livre doit être écrite en chiffre uniquement.\n\nExemples: '1958', '1990', ...".decode('utf-8')
		elif values == 2:
			err = "Le nombre de pages du livre doit être écrit en chiffre uniquement.\n\nExemples: '42', '687', ...".decode('utf-8')
		elif values == 3:
			err = "L'image spécifiée pour la couverture du livre n'existe pas.\n\nNe mettez rien pour associer ce livre à l'image par défaut.".decode('utf-8')
			label = "Ok"
		
		if err:
			dialog = wx.MessageDialog(self, message=err, caption="Livre non conforme".decode('utf-8'), style=wx.OK|wx.STAY_ON_TOP|wx.ICON_EXCLAMATION)
			if wxVersion == '2.9.0': dialog.SetOKLabel(label)
			dialog.ShowModal()
			return 0
		
		# --- Check button
		name = evt.GetEventObject().myName
		if name == "OnAdd":
			self.AjoutLivre(values)
			self.Close()
		elif name == "OnAddAndContinue":
			self.AjoutLivre(values)
			for egl in self.dEGL.keys():
				if values[egl] not in self.dEGL[egl]:
					x = "self.%s.Append(values[egl])" % egl
					exec(x)
					self.dEGL[egl].append(values[egl])
		elif name == "OnModif":
			self.ModifLivre(values)
			self.Close()

	def OnClose(self, evt):
		"""
		Annule l'opération en fermant la fenêtre.
		"""
		self.principalFrame.ajoutLivreFrame = False
		self.Destroy()

	def OnGoogle(self, evt):
		"""
		Ouvre une page internet pour retouver l'image de couverture du livre.
		"""
		info = [self.titre.GetValue(), self.editeur.GetValue(), self.pAuteur.GetValue(), self.nAuteur.GetValue(), self.ISBN.GetValue()]
		info = '+'.join(info)
		query = "https://www.google.fr/search?site=imghp&tbm=isch&source=hp&biw=1594&bih=930&q=%s"%(info)
		wb.open(url=query, new=0)

	def OnTextChange(self, evt):
		"""
		Modifie le texte saisie en fontion du champs associé.
		Capitalise la saisie pour tous les champs excepté Nom Auteur.
		Met tout en majuscule pour le champs Nom Auteur.
		"""
		id = evt.GetId()
		for n in ['pAuteur','nAuteur','titre','editeur','genre','lieu','commentaire']:
			exec("var=self.%s"%n)
			if var.GetId() == id:
				txt = var.GetValue()
				if txt :
					# Si le texte n'est pas vide
					if n == 'nAuteur' and not txt.isupper() and txt[0].isalpha():
						# Si c'est le nom d'auteur, ET pas entièrement en majuscule
						var.SetValue(txt.upper())			# upper met tout le string en majuscule
						var.SetInsertionPoint(len(txt))		# Définie la position du curseur dans le champs de saisie
					elif not txt[0].isupper() and txt[0].isalpha():
						# Si la première lettre n'est pas une majuscule
						var.SetValue(txt.capitalize())		# 'capitalize' met la première lettre d'une string en majuscule, le reste en minuscule
						var.SetInsertionPoint(len(txt))		# Définie la position du curseur dans le champs de saisie

	def OnEnter(self, evt):
		"""
		Passe au champs suivant en appuyant sur Entrer, comme une tabulation
		"""
		if evt.GetId() != self.commentaire.GetId():
			evt.EventObject.Navigate()

	#---------------------------------------------------
	# --- Fonctions

	def RecupAllValue(self):
		"""
		Récupère toutes les données saisies par l'utilisateur
		"""
		res = {}	# Contient les résutlats
		
		# --- RECUPERATION DES DONNEES
		# Prenom Auteur
		res['auteurPrenom'] = self.pAuteur.GetValue().encode('utf-8') or " "
		# Nom Auteur
		res['auteurNom'] = self.nAuteur.GetValue().encode('utf-8') or " "
		# Titre
		res['titre'] = self.titre.GetValue().encode('utf-8')
		if not res['titre']: return 0
		# Editeur
		res['editeur'] = self.editeur.GetValue().encode('utf-8') or " "
		# Année de parution
		tmp = self.parution.GetValue()
		if tmp:
			try:
				res['parution'] = int(tmp)
			except ValueError:
				return 1
		else :
			res['parution'] = -1
		# Genre
		res['genre'] = self.genre.GetValue().encode('utf-8') or " "
		# Nombre de page
		tmp = self.pages.GetValue()
		if tmp:
			try:
				res['nbPage'] = int(tmp)
			except ValueError:
				return 2
		else:
			res['nbPage'] = -1
		# Lieu
		res['lieu'] = self.lieu.GetValue().encode('utf-8') or " "
		# Note
		res['note'] = self.note.GetValue()
		# Commentaire
		res['commentaire'] = self.commentaire.GetValue().encode('utf-8') or "Aucun commentaire."
		# Couverture
		tmp = self.couverture.GetPath().encode('utf-8')
		if not tmp:
			tmp = self.principalFrame.pathCouv + 'image-not-available.jpg'
		elif not os.path.isfile(tmp):
			return 3
		imgName = tmp.split(self.principalFrame.list.maBiblio.OS)[-1]	# Nom de l'image
		# On vérifie si l'image sélectionnée se trouve dans le dossier des couvertures
		if tmp[:-len(imgName)] != self.principalFrame.pathCouv:		# Si ce n'est pas le cas, on copie l'image dans notre dossier 'pathCouv'
			cpto = ''.join([self.principalFrame.pathCouv + imgName]).replace(' ','\ ')		# Au cas où il y est des espaces
			tmp = tmp.replace(' ','\ ')
			command = "cp %s %s" %(tmp, cpto)
			os.system(command)
		res['couverture'] = imgName
		# ISBN
		res['ISBN'] = self.ISBN.GetValue() or " "
		
		return(res)

	def AjoutLivre(self, values):
		"""
		Crée le livre et l'ajoute à la liste, puis actualise cette liste ainsi que celle des couvertures Bitmap.
		"""
		# --- Création de l'objet Livre
		tmp = "newBook = Book("
		for k,v in values.items():
			tmp += "%s = '%s'," %(k, v)
		tmp = tmp[:-1] + ')'
		exec(tmp)
		
		# --- Ajout du livre à la bibliothèque
		exist, ID = self.principalFrame.list.maBiblio.addBook(newBook)
		
		if exist:
			# --- CAS LIVRE IDENTIQUE DEJA EXISTANT
			mess = 'Un livre semblant identique au votre existe déjà dans la bibliothèque:\n\n'.decode('utf-8') +\
					self.principalFrame.list.maBiblio.dLibrary[ID].__repr__() +\
					"\n\nÊtes-vous sûre de vouloir l'ajouter ?".decode('utf-8')
			supp = wx.MessageDialog(self, message=mess, caption="Forcer l'ajout d'un livre", style=wx.YES_NO|wx.STAY_ON_TOP|wx.ICON_EXCLAMATION)
			rep = supp.ShowModal()
			if rep == wx.ID_YES:
				self.principalFrame.list.maBiblio.addBook(newBook, forcer=True)
		
		# --- Acutalisation de 'lCouvBitmap' et 'list', puis focus sur le nouveau livre
		self.principalFrame.updateLCouvBitmap(newBook.couverture)
		self.principalFrame.list.listActu()
		# Focus sur le livre, avec actualisation Couv/Com
		try:
			self.principalFrame.list.Focus(self.principalFrame.list.itemIndexMap.index(ID))
		except ValueError:
			return
		self.principalFrame.list.selectedItem = self.principalFrame.list.itemIndexMap.index(ID)
		self.principalFrame.list.vboxActu()
	
	def ModifLivre(self, values):
		"""
		Applique les modifications à apporter au livre.
		"""
		dico = {}
		# --- On récupère uniquement les champs modifiés
		for k in values.keys():
			if values[k] != self.defValue[k]:
				dico[k] = values[k]
		
		# --- On récupère les anciennes valeurs des EGL et couverture
		EGL = [(k, self.defValue[k]) for k in ['editeur','genre','lieu'] if dico.has_key(k)]
		if dico.has_key("couverture"):
			oldCouv = self.defValue["couverture"]
		
		# --- Lancement des modifications
		self.principalFrame.list.maBiblio.modifyBook(self.isModif,dico)
		
		# --- Actualisation des différents objets
		if dico.has_key("couverture"):
			self.principalFrame.updateLCouvBitmap(dico["couverture"], oldCouv)
		self.principalFrame.list.listActu()
		self.principalFrame.list.maBiblio.updateEGL()
		self.principalFrame.list.vboxActu()

