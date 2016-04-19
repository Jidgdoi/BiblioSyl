#-*- coding: utf-8 -*-
#! /usr/bin/env python
# C. Fournier, 2014

import wx
import wx.lib.mixins.listctrl as listmix
import numpy as np

from Library import Library
from DisplayBook import DisplayBook
from MyUtils import *

# =============================================================================
#
#	Classe de type ListCtrl
#
# =============================================================================

class VirtualList(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin, listmix.ColumnSorterMixin):
	"""
	Widget contrôlant la liste des livres: c'est d'ici qu'on accède à l'objet Etagere, et donc aux objets Livre.
	"""
	def __init__(self, parent):
		wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT|wx.LC_VIRTUAL|wx.LC_HRULES|wx.LC_VRULES)
		
		self.principalFrame = parent
		
		self.defaultFont = self.GetFont()
		self.styledFont = createMyFont()
		self.SetFont(self.styledFont)
		
		self.selectedItem = 0
		self.selectedID = ''
		
		self.visuLivreFrame = False
		self.modifLivreFrame = False
		
		# --- Initialisation de la classe Etagere, avec chargement de la liste de livre
		self.maBiblio = Library(self.principalFrame.pathLibrary)
		
		# --- Ajout des icônes
		self.il = wx.ImageList(32, 16)
		# Icônes de triages et de notes données aux livres
		triage={'sm_up':'GO_UP_B.png', 'sm_dn':'GO_DOWN_B.png', 'note_a':'note_a.jpg', 'note_b':'note_b.jpg', 'note_c':'note_c.jpg', 'note_d':'note_d.jpg', 'note_f':'note_f.jpg'}
		for k,v in triage.items():
			img = wx.Image(self.principalFrame.pathIcone+v, wx.BITMAP_TYPE_ANY)
			img = img.Scale(32, 16, wx.IMAGE_QUALITY_HIGH)
			img = img.ConvertToBitmap()
			s="self.%s= self.il.Add(img)" %k
			exec(s)
#		a={"sm_up":"GO_UP","sm_dn":"GO_DOWN"}
#		for k,v in a.items():
#			s="self.%s= self.il.Add(wx.ArtProvider_GetBitmap(wx.ART_%s,wx.ART_TOOLBAR,(32,16)))" % (k,v)
#			exec(s)
		self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)

		# --- Ajout de couleurs de fond pour différencier les lignes
		self.listColor = []
		self.listColor.append(wx.ListItemAttr())
		self.listColor[-1].SetBackgroundColour("#B3FFFA")	# Bleu pâle
		self.listColor.append(wx.ListItemAttr())
		self.listColor[-1].SetBackgroundColour("#FAB3FF")	# Rose pâle
		self.listColor.append(wx.ListItemAttr())
		self.listColor[-1].SetBackgroundColour("#FFFAB3")	# Jaune pâle
		self.listColor.append(wx.ListItemAttr())
		self.listColor[-1].SetBackgroundColour("#FFFFFF")	# Blanc
		self.listColor.append(wx.ListItemAttr())
		self.listColor[-1].SetBackgroundColour("#DDDDDD")	# Gris claire

		self.currentColor = 0		# Iterateur de couleur

		# --- Initialisation des colonnes
		self.columnList={0:['Auteur',140],
				1:['Titre',320],
				2:['Editeur',130],
				3:['Parution',95],
				4:['Genre',140],
				5:['Pages',70],
				6:['Lieu',140],
				7:['Note',0]}
		for k,v in self.columnList.items():
			if k in [3,5]:
				s="self.InsertColumn(%i, '%s', wx.LIST_FORMAT_CENTER, width=%i)" % (k,v[0],v[1])
			else:
				s="self.InsertColumn(%i, '%s', width=%i)" % (k,v[0],v[1])
			exec(s)
		
		# --- Initialisation des premiers items (nombre d'items = nombre d'éléments dans le dictionnaire)
		self.itemDataMap = self.convertToDataMap()
		self.itemIndexMap = range(1,len(self.itemDataMap)+1)
		self.SetItemCount(len(self.itemDataMap))
#		self.itemsColor = [-1]*len(self.itempDataMap)		# Couleur pour chaque item
		
		# --- Initialisation des modules mixins
		listmix.ListCtrlAutoWidthMixin.__init__(self)
		listmix.ColumnSorterMixin.__init__(self, len(self.columnList))
		
		# --- On définit le trie par défaut sur 'Genre' (colonne 4) A->Z ordre alphabétique (1)
		self.currentSorter = 4		# Numéro courant de la colonne triante
		self.SortListItems(self.currentSorter, 1)
		
		# --- Initialisation du menu popup
		self.initPopupMenu()
		
		# --- Définition des events
		self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)
		self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected)
		self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnItemRightClick)
		self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick)

	#---------------------------------------------------
	# --- Initialisation

	def initPopupMenu(self):
		"""
		Initialise le menu popup qui s'ouvrira suite à l'événement clique droit sur un item de la liste
		"""
		self.popupmenu = wx.Menu()
		for text in ["Modifier","Supprimer"]:
			item = self.popupmenu.Append(-1, text)
			self.Bind(wx.EVT_MENU, self.OnPopupItemSelected, item)

	#---------------------------------------------------
	# --- Events

	def OnItemSelected(self, evt):
		"""
		Evenement lors de la sélection d'un livre
		"""
		self.selectedItem = evt.m_itemIndex	# Correspond au numéro de la ligne
		printLogText('OnItemSelected: "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s"' %
						   (self.selectedItem,
							self.GetItemText(self.selectedItem),
							self.getColumnText(self.selectedItem, 1),
							self.getColumnText(self.selectedItem, 2),
							self.getColumnText(self.selectedItem, 3),
							self.getColumnText(self.selectedItem, 4),
							self.getColumnText(self.selectedItem, 5),
							self.getColumnText(self.selectedItem, 6),
							self.getColumnText(self.selectedItem, 7)))
		
		self.vboxActu()
		print("OnItemSelected", self.selectedItem)

	def OnItemActivated(self, evt):
		""" 
		Evenement double clique sur item: ouvre la fenêtre de visualisation d'un livre
		"""
		self.selectedItem = evt.m_itemIndex
		printLogText("OnItemActivated: %s -- TopItem: %s" %
						(self.GetItemText(self.selectedItem), self.GetTopItem()))
		if self.visuLivreFrame :
			self.visuLivreFrame.SetFocus()
			self.visuLivreFrame.actuPage(self.selectedItem)
		else:
			self.visuLivreFrame = DisplayBook(self, wx.ID_PREVIEW, self.selectedItem)
			self.visuLivreFrame.Show(True)
			self.visuLivreFrame.CentreOnParent()
		print "itemIndexMap", self.itemIndexMap[self.selectedItem]
		print "itemDataMap", self.itemDataMap[self.itemIndexMap[self.selectedItem]]

	def OnItemDeselected(self, evt):
		""" **USELESS**
		Evenement de déselection d'un item
		"""
		printLogText("OnItemDeselected: %s" % evt.m_itemIndex)

	def OnItemRightClick(self, evt):
		"""
		Evenement du clique droit sur un item
		"""
		self.selectedID = self.itemIndexMap[evt.m_itemIndex]
		printLogText("OnItemRightClick: %s" % (self.selectedID))
		printLogText("Path: %s" % (self.principalFrame.pathRoot))
		click = evt.GetPosition()
		frame = self.principalFrame.GetPosition()
		liste = self.GetPosition()
		pos = (click[0] + frame[0] + liste[0], click[1] + frame[1] + liste[1]+52)
		pos = self.ScreenToClient(pos)
		self.PopupMenu(self.popupmenu, pos)

	def OnColClick(self, evt):
		"""
		Evenement du clique sur colonne
		"""
		print "OnCOlClick"
		evt.Skip()
		x,y = evt.GetPosition()		# On prend la position du clique
		print "col",evt.GetPosition()
		print "eventType",evt.GetEventType()
		self.majColumnWidth()		# On actualise la largeur des colonnes
		self.currentSorter = self.getColumnNumber(x)	# On met à jour le numéro de colonne triante
		printLogText("OnColClick: %s" % self.currentSorter)
#		self.itemsColor = [ -1 for i in range(len(self.itemsColor))]

	def OnPopupItemSelected(self, evt):
		"""
		Evenement de choix d'une action du menu popup
		"""
		item = self.popupmenu.FindItemById(evt.GetId())
		choix = item.GetText()
		if choix=="Modifier":
			values = self.maBiblio.dLibrary[self.selectedID].__dict__
			if self.modifLivreFrame:
				self.modifLivreFrame.SetFocus()
			else:
				self.modifLivreFrame = BookFormular(self.principalFrame, -1, title="Modification d'un livre", state=self.selectedID, defValue=values)
				self.modifLivreFrame.Show(True)
				self.modifLivreFrame.CentreOnParent()
		elif choix=="Supprimer":
			mess = 'Êtes-vous sûre de vouloir supprimer ce livre ?\n\n'.decode('utf-8') + self.maBiblio.dLibrary[self.selectedID].__repr__()
			supp = wx.MessageDialog(self, message=mess, caption='Supprimer un livre', style=wx.YES_NO|wx.STAY_ON_TOP|wx.ICON_EXCLAMATION)
			rep = supp.ShowModal()		# Attend une réponse de l'utilisateur
			if rep == wx.ID_YES:
				EGL = [('editeur', self.maBiblio.dLibrary[self.selectedID].editeur),
						('genre', self.maBiblio.dLibrary[self.selectedID].genre),
						('lieu', self.maBiblio.dLibrary[self.selectedID].lieu)]
				self.maBiblio.removeBook(self.selectedID)
				self.listActu()
				self.maBiblio.updateEGL()

	#---------------------------------------------------
	# --- Fonctions sur les colonnes

	def getColumnText(self, index, col):
		"""
		Retourne le texte contenu dans la colonne de la ligne sélectionnée (ligne=item)
		"""
		item = self.GetItem(index, col)
		return item.GetText()

	def getColumnNumber(self,x):
		"""
		Retourne le numéro de la colonne à la position verticale 'x' (pixel)
		"""
		col = 0		# Numéro de la colonne courante
		curseur = self.columnList[col][1]	# Position du curseur en pixel au niveau vertical
		# Tant que le clique est supérieur au curseur, ou que la dernière colonne n'est pas atteinte, on continue
		while x > curseur and col < len(self.columnList)-1:
			col += 1
			curseur += self.columnList[col][1]
		print("Col:",col,"width:",self.GetColumnWidth(col))
		return col

	def majColumnWidth(self):
		"""
		Actualise la largeur des colonnes dans la variable 'columnList', au cas où celles-ci auraient été modifiée
		"""
		for i in self.columnList.keys():
			w = self.GetColumnWidth(i)
			if self.columnList[i][1] != w:
				self.columnList[i][1] = w


	#---------------------------------------------------
	# Fonctions nécessaire pour les callback des thèmes
	# LC_REPORT et LC_VIRTUAL

	def OnGetItemText(self, item, col):
		index=self.itemIndexMap[item]
		s = self.itemDataMap[index][col]
		return s

	def OnGetItemColumnImage(self, item, col):
		"""
		Ajoute une petite icone pour les notes
		"""
		# Si ce n'est pas la colonne de note, on zappe
		if col!=7:
			return -1
		
		index=self.itemIndexMap[item]
		note=self.itemDataMap[index][col]
		
		if note==5:
			return self.note_a
		elif note==4:
			return self.note_b
		elif note==3:
			return self.note_c
		elif note==2:
			return self.note_d
		elif note==1:
			return self.note_f
		else:
			return -1
		
		# res = -1
		# exec("res = self.note_%s"%note)
		# return res

	def OnGetItemAttr(self, item):
		"""
		Modifie la couleur de chaque item suivant l'item précédent et la colonne triante
		"""
#		# ----------------------------------
#		# --- Test 1: 2 couleurs alternées
		if item%2 == 0:
			self.currentColor = 3
		else:
			self.currentColor = 4
		return self.listColor[self.currentColor]

#		# ----------------------------------
#		# --- Test 2: 3 couleurs, alternées par groupe
#		indexA = self.itemIndexMap[item]
#		if item > 0:
#			indexB = self.itemIndexMap[item-1]
#		else:
#			indexB = self.itemIndexMap[item]
#		
#		colA = self.itemDataMap[indexA][self.currentSorter]
#		colB = self.itemDataMap[indexB][self.currentSorter]
#		
#		if colA != colB:
#			self.currentColor = (self.currentColor + 1)%3
#		return self.listColor[self.currentColor]
		
#		# ----------------------------------
#		# --- Test 3: 3 couleurs alternées, par groupe prenant en compte la couleur qui précède
#		# Première initialisation de itemsColor
#		if -1 in self.itemsColor:
#			if colA != colB:
#				self.currentColor = (self.currentColor + 1)%3
#		# itemsColor déjà initialisé
#		else:
#			if item > 0:
#				if self.itemsColor[item] == self.itemsColor[item-1]:
#					self.currentColor = self.itemsColor[item]
#					if colA!=colB:
#						self.currentColor = (self.currentColor + 1)%3
#				else:
#					if colA==colB:
#						self.currentColor = self.itemsColor[item-1]
#		self.itemsColor[item] = self.currentColor
#		print item, self.itemsColor
#		return self.listColor[self.currentColor]

	#---------------------------------------------------
	# Fonctions à définir obligatoirement pour le triage

	def SortItems(self,sorter=cmp):
		"""
		Trie les items
		"""
		#FIXME Bug lors d'un trie décroissant, si clique sur la liste: retrie automatiquement dans l'ordre croissant.
		print "SortItems", self.currentSorter
#		print help(sorter)
		items = list(self.itemDataMap.keys())
		items.sort(sorter)
		self.itemIndexMap = items
		
		# Actualise la liste triée
		self.Refresh()

	# Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
	def GetListCtrl(self):
		return self

	# Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
	def GetSortImages(self):
		return (self.sm_dn, self.sm_up)

	def getItem(self, index):
		"""
		Return the item corresponding to the ID at the index in the list.
		"""
		return self.maBiblio.dLibrary[self.itemIndexMap[index]]

	#---------------------------------------------------
	# Fonctions d'actualisation

	def vboxActu(self):
		"""
		Actualise la page de couverture et le commentaire correspondant
		au livre sélectionné
		"""
		index = self.itemIndexMap[self.selectedItem]
		comm = self.maBiblio.dLibrary[index].commentaire
		couv = self.maBiblio.dLibrary[index].couverture
		self.principalFrame.vboxActu(comm, couv)

	def convertToDataMap(self):
		"""
		Convert the list of books into a readble dictionary for ListCtrl.
		"""
		dataMap = {}
		for k,v in self.maBiblio.dLibrary.items():
			dataMap[k] = (v.auteurPrenom + ' ' + v.auteurNom,
							v.titre ,
							v.editeur ,
							v.parution ,
							v.genre ,
							v.nbPage ,
							v.lieu ,
							v.note ,
							v.commentaire,
							v.ISBN)
		return dataMap

	def listActu(self):
		"""
		Actualise la liste des livres à afficher
		"""
		if self.itemDataMap == None or (self.GetItemCount() == len(self.maBiblio.dLibrary)-1):
			# La liste est vide ou on vient de supprimer un item
			self.itemDataMap = self.convertToDataMap()
		self.itemIndexMap = range(1,len(self.itemDataMap)+1)
		self.SetItemCount(len(self.itemDataMap))
		self.SortListItems(self.currentSorter, 1)
		self.calcStatistiques()
		self.Refresh()

	def keyWordsActu(self, keyWords):
		"""
		Recherche tous les items contenant les mots-clés recherchés, et les stock dans 'itemDataMap'
		Recherche dans tous les champs sauf le champs 'commentaire' (et 'couverture' car non représenté dans 'itemDataMap')
		"""
		# S'il n'y a aucun mots-clés, on retourne None
		if not keyWords:
			self.itemDataMap = None
			return
		
		itemsSelected = {}	# Dico contenant les items recherchés
		found = False		# Booléen pour sortir des boucles
		for k,v in self.itemDataMap.items():
			for w in keyWords:
				# On cherche dans tous les champs sauf 'commentaire', le dernier de la liste
				for s in v[:-1]:
					# On vérifie le type de la valeur pour déterminer l'encodage
					if type(s) == str or type(s) == unicode:
						s_encoded = s.encode('utf-8')
					else:
						s_encoded = str(s)
					# Puis on cherche le mot-clé, sans prendre compte des Majuscules/minuscules (on met tout en minuscule)
					if s_encoded.lower().find(w.lower()) >= 0:
						found = True
						itemsSelected[k] = v
						break
				if found:
					found = False
					break
		self.itemDataMap = itemsSelected

	#---------------------------------------------------
	# Autres fonctions

	def calcStatistiques(self):
		"""
		Calcul de statistiques sur les livres
		"""
		page = 0		# Nombre moyen de pages par livre
		note = 0		# Note moyenne
		Genre = {}		# Nombre de livres par genre
		Lieu = {}		# Nombre de livres par lieu
		Auteur = []		# Nombre d'auteurs
		tot = self.GetItemCount()	# Nombre de livres total
		
		if tot == 0:
			# S'il n'y a aucun livre de sélectionné, on retourne ce message
			self.principalFrame.rawStatMess = "Bibliothèque vide.".decode('utf-8')
			return
		
		for k,v in self.itemDataMap.items():
			if v[5] > 0:
				page += v[5]
			if v[7] > 0:
				note += v[7]
			if v[4]:
				if not Genre.has_key(v[4]):
					Genre[v[4]] = 0
				Genre[v[4]] += 1
			if v[6]:
				if not Lieu.has_key(v[6]):
					Lieu[v[6]] = 0
				Lieu[v[6]] += 1
			if v[0] not in Auteur:
				Auteur.append(v[0])
		page /= float(tot)
		note /= float(tot)
		note = round(note,1)
		
		mAutre = 'Nombre de livres: '+str(tot)+'    Nombre de pages moyen: '+str(int(page))+'    Note moyenne: '+str(note)
		mGenre = '    '.join([ i + ': ' + str(Genre[i]) for i in Genre.keys()])
		mLieu = '    '.join([ i + ': ' + str(Lieu[i]) for i in Lieu.keys()])
		self.principalFrame.rawStatMess = [mAutre, mGenre, mLieu]
		return

	def calcStatistiques2(self):
		"""
		Compute statistics on selected books (and all books).
		"""
		dArray = {'':[], 'Selected':[], 'All':[]}
		spacement = "\n\n%s\n" %("-"*60)
		
		# --- Get dictionaries of All books and Selected books.
		dAll = self.principalFrame.list.maBiblio.dLibrary
		dSelected = {i:self.principalFrame.list.maBiblio.dLibrary[i] for i in self.itemDataMap.keys()}
		
		def getLAttr(lib, attr):
			return [lib[b].getAttr(attr) for b in sorted(lib.keys())]
		# --- Compute basic stats:
		# Number of books
		dArray[''].append('Nombre de livres')
		dArray['Selected'].append(len(dSelected))
		dArray['All'].append(len(dAll))
		# Mean note
		dArray[''].append('Note moyenne')
		dArray['Selected'].append(str(round(np.mean([getLAttr(dSelected, 'note')]),2)))
		dArray['All'].append(str(round(np.mean([getLAttr(dAll, 'note')]),2)))
		# Mean page number
		dArray[''].append('Nb page moyen')
		dArray['Selected'].append(str(round(np.mean([getLAttr(dSelected, 'nbPage')]),2)))
		dArray['All'].append(str(round(np.mean([getLAttr(dAll, 'nbPage')]),2)))
		# --- Format output
		message = "\t\t\t\tSélectionnés\t\tTous\n".decode('utf-8')
		message += '\n'.join( ["%s\t%s\t%s" %(dArray[''][i], dArray['Selected'][i], dArray['All'][i]) for i in range(len(dArray['']))] )
		message += spacement
		
		# Authors
		message += "Liste des auteurs\tNb livres\n\n"
		lAuthor = [i.getAuteur() for i in dSelected.values()]
		message += '\n'.join(["%s\t%s"%(i, lAuthor.count(i)) for i in sorted(set(lAuthor))])
		message += spacement
		
		# Genre
		message += "Liste des genre\tNb livres\n\n"
		lGenre = getLAttr(dSelected, 'genre')
		message += '\n'.join(["%s\t%s"%(i, lGenre.count(i)) for i in sorted(set(lGenre))])
		message += spacement
		
		return message
