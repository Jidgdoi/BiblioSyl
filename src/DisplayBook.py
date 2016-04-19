#-*- coding: utf-8 -*-
#! /usr/bin/env python
# C. Fournier, 2014

import wx
import webbrowser as wb

from MyUtils import *

# =============================================================================
#
#	Fenêtre de visualisation de livre
#
# =============================================================================

class DisplayBook(wx.Frame):
	"""
	Fenêtre de visualisation des livres.
	"""
	def __init__(self, parent, ID, index, title="Visualisation d'un livre", size=(1250,650)):
		wx.Frame.__init__(self, parent, ID, title, size=size, style= wx.DEFAULT_FRAME_STYLE)
		
		self.virtualList = parent
		self.SetBackgroundColour("#FFFFFF")
		self.size = size			# Dimension de la fenêtre
		self.index = index			# Index of the ID of the item in the virtualList
		self.item = self.virtualList.getItem(self.index)	# Book object
		self.bitmapCouv = self.virtualList.principalFrame.lCouvBitmap[self.item.couverture]	# Bitmap de la couverture
		self.wTC = self.size[0]		# Longueur de base pour un texte
		
		# Contextual popup help bubble
		provider = wx.SimpleHelpProvider()
		wx.HelpProvider_Set(provider)
		
		self.initIcone()
		self.InitUI()
		
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		
		self.SetMinSize(self.size)

	def InitUI(self):
		"""
		Initialisation des éléments de la fenêtre
		"""
		couvSize = (self.bitmapCouv.GetWidth(), self.bitmapCouv.GetHeight())	# Dimension de la couverture
		self.wTC,h = self.size[0] - couvSize[0] -25, 25	# Dimension de base pour un texte
		style = wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH|wx.TE_RICH2|wx.BORDER_NONE	# Style par défaut pour chaque TextCtrl
		self.lTextCtrl = []		# Liste des TextCtrl

		# --- Remplissage de la liste des TextCtrl avec titre, auteur, ...
		self.params={'titre':["%s", self.item.titre, wx.TE_NO_VSCROLL|wx.TE_CENTER, {'pointSize':22,'weight':wx.BOLD,'faceName':'Comic Sans MS'}],
				'auteur':["de %s", self.item.getAuteur(), wx.TE_NO_VSCROLL|wx.TE_RIGHT, {'pointSize':15,'faceName':'Comic Sans MS'}],
				'EPGP':["Edition %s de %s, catégorie %s. %s pages.".decode('utf-8'), (self.item.editeur, self.item.parution, self.item.genre, self.item.nbPage), wx.TE_NO_VSCROLL|wx.TE_LEFT, {'pointSize':13,'faceName':'Comic Sans MS'}, wx.LIGHT_GREY],
				'commentaire':["%s", self.item.commentaire, wx.TE_LEFT, {'pointSize':13,'faceName':'Comic Sans MS'}],
				'ISBN':["ISBN: %s", self.item.ISBN, wx.TE_NO_VSCROLL|wx.TE_LEFT, {'pointSize':13,'faceName':'Comic Sans MS'}],
				'read':["Lu par: %s", self.item.getReadBy(), wx.TE_NO_VSCROLL|wx.TE_LEFT, {'pointSize':13,'faceName':'Comic Sans MS'}]}

		for k in ['titre','auteur','EPGP','commentaire']:
			self.lTextCtrl.append(wx.TextCtrl(self, value=(self.params[k][0]%self.params[k][1]), size=(self.wTC,h), style=style|int("%i" %self.params[k][2])))
			self.lTextCtrl[-1].SetFont(createMyFont(self.params[k][3]))
			if len(self.params[k]) > 4:
				# Si > 3 c'est qu'il y a une couleur de premier plan
				self.lTextCtrl[-1].SetForegroundColour(self.params[k][4])
			self.lTextCtrl[-1].SetMinSize(self.correctSize(self.lTextCtrl[-1],self.wTC))
		
		# --- Couverture
		self.couv = wx.StaticBitmap(self, -1, self.bitmapCouv, size=(couvSize))
		# --- Note
		self.note = wx.StaticBitmap(self, -1, self.lIcone[self.item.note])
		# --- ISBN
		self.ISBN = wx.TextCtrl(self, value=(self.params['ISBN'][0]%self.params['ISBN'][1]), size=(couvSize[0],25), style=style|int("%i" %self.params['ISBN'][2]))
		self.ISBN.SetFont(createMyFont(self.params['ISBN'][3]))
		# --- Read
		self.read = wx.TextCtrl(self, value=(self.params['read'][0]%self.params['read'][1] if self.params['read'][1] else "Non lu."), size=(couvSize[0],25), style=style|int("%i" %self.params['ISBN'][2]))
		
		# --- Les boutons
		lbtn = []		# Liste des boutons
		btn = wx.BitmapButton(self, id=wx.ID_BACKWARD, bitmap=self.lIcone['previous'])
		btn.Bind(wx.EVT_BUTTON, self.OnChange)
		btn.SetHelpText("Previous book.")
		lbtn.append(btn)
		btn = wx.BitmapButton(self, id=wx.ID_ABOUT, bitmap=self.lIcone['biographie'])
		btn.Bind(wx.EVT_BUTTON, self.OnWikipedia)
		btn.SetHelpText("Author biography.")
		lbtn.append(btn)
		btn = wx.BitmapButton(self, id=-1, bitmap=self.lIcone['biographieLucky'])
		btn.Bind(wx.EVT_BUTTON, self.OnWikipedia)
		btn.SetHelpText("Wikipedia author biography (if lucky).")
		lbtn.append(btn)
		btn = wx.BitmapButton(self, id=wx.ID_REPLACE, bitmap=self.lIcone['edit'])
		btn.myName = "OnModif"
		btn.Bind(wx.EVT_BUTTON, self.OnModif)
		btn.SetHelpText("Edit book.")
		lbtn.append(btn)
		btn = wx.BitmapButton(self, id=wx.ID_DELETE, bitmap=self.lIcone['delete'])
		btn.Bind(wx.EVT_BUTTON, self.OnSuppr)
		btn.SetHelpText("Delete book.")
		lbtn.append(btn)
		btn = wx.BitmapButton(self, id=wx.ID_FORWARD, bitmap=self.lIcone['next'])
		btn.Bind(wx.EVT_BUTTON, self.OnChange)
		btn.SetHelpText("Next book.")
		lbtn.append(btn)
		btn = wx.BitmapButton(self, id=wx.ID_CLOSE, bitmap=self.lIcone['exit'])
		btn.Bind(wx.EVT_BUTTON, self.OnClose)
		btn.SetHelpText("Quit.")
		lbtn.append(btn)
		btn = wx.ContextHelpButton(self, pos=(20,100))
		lbtn.append(btn)
		
		# --- GESTION DES BOXSIZER
		# lTextCtrl
		self.vboxTC = wx.BoxSizer(wx.VERTICAL)
		for i in self.lTextCtrl:
			self.vboxTC.Add(i, 0, wx.TOP|wx.RIGHT|wx.LEFT)
		# Couverture, note, ISBN et read
		self.vboxRight = wx.BoxSizer(wx.VERTICAL)
		self.vboxRight.Add(self.couv, 0, wx.RIGHT)
		self.vboxRight.Add(self.note, 0, wx.RIGHT)
		self.vboxRight.Add(self.ISBN, 0, wx.RIGHT)
		self.vboxRight.Add(self.read, 0, wx.RIGHT)
		# Ajout des 2 box précédentes dans la Majeure horizontale
		self.hboxLivre = wx.BoxSizer(wx.HORIZONTAL)
		self.hboxLivre.Add(self.vboxTC, 1, wx.EXPAND)
		self.hboxLivre.Add(self.vboxRight, 0, wx.RIGHT)
		# Boutons
		hboxBouton = wx.BoxSizer(wx.HORIZONTAL)
		for i in lbtn:
			hboxBouton.Add(i, flag=wx.ALIGN_CENTER)
			hboxBouton.Add((15,-1), flag=wx.ALIGN_CENTER)
		
		self.totVbox = wx.BoxSizer(wx.VERTICAL)
		self.totVbox.Add(self.hboxLivre,1, wx.EXPAND)
		self.totVbox.Add(hboxBouton, 0, wx.ALIGN_CENTER|wx.ALL)
		self.SetSizer(self.totVbox)

	def initIcone(self):
		"""
		Charge la liste d'images Bitmap pour les boutons et les notes
		"""
		self.lIcone = {}
		l = ['biographie','biographieLucky','previous','next','edit','delete','exit']
		for name in l:
			img = wx.Image(self.virtualList.principalFrame.pathIcone + name + 'Icon.png', wx.BITMAP_TYPE_ANY)
			img = img.Scale(50, 50, wx.IMAGE_QUALITY_HIGH)
			img = img.ConvertToBitmap()
			self.lIcone[name] = img
		
		for i in range(0,6):
			img = wx.Image(self.virtualList.principalFrame.pathIcone + "note_%s.png" %i, wx.BITMAP_TYPE_ANY)
			img = img.Scale(self.bitmapCouv.GetWidth(), self.bitmapCouv.GetWidth()/6, wx.IMAGE_QUALITY_HIGH)
			img = img.ConvertToBitmap()
			self.lIcone[i] = img
		l = [range(0,6)]

	def correctSize(self, TC, w):
		"""
		self.lTextCtrl[-1].GetTextExtent(self.lTextCtrl[-1].GetValue())
		"""
		s = TC.GetTextExtent(TC.GetValue())
		h = (s[0]/w +1)*s[1]
		return (w,h)

	def actuPage(self, index):
		""""
		Actualise les éléments de la page
		"""
#		if item:
#			self.item = item
#			self.id = self.virtualList.itemIndexMap[item]
		self.index = index
		self.item = self.virtualList.getItem(self.index)
		# --- Actualisation de la liste des TextCtrl
		i = 0	# indice courant de la lTextCtrl
		for k,v in [('titre', self.item.titre), ('auteur', self.item.getAuteur()), ('EPGP', (self.item.editeur, self.item.parution, self.item.genre, self.item.nbPage)), ('commentaire', self.item.commentaire)]:
			self.params[k][1] = v
			self.lTextCtrl[i].SetValue((self.params[k][0]%v))
			self.lTextCtrl[i].SetMinSize(self.correctSize(self.lTextCtrl[i],self.wTC))
			i += 1
		
		# --- Actualisation des images
		self.bitmapCouv = self.virtualList.principalFrame.lCouvBitmap[self.item.couverture]	# Bitmap de la couverture
		imgSB = wx.StaticBitmap(self, -1, self.bitmapCouv, size=(self.bitmapCouv.GetWidth(), self.bitmapCouv.GetHeight()))
		self.vboxRight.Replace(self.couv, imgSB)
		self.couv = imgSB
		
		imgSB = wx.StaticBitmap(self, -1, self.lIcone[self.item.note])
		self.vboxRight.Replace(self.note, imgSB)
		self.note = imgSB
		
		# --- Actualisation des textes à droite sous les images
		self.params['ISBN'][1] = self.item.ISBN
		self.ISBN.SetValue((self.params['ISBN'][0]%self.params['ISBN'][1]))
		self.params['read'][1] = self.item.getReadBy()
		self.read.SetValue((self.params['read'][0]%self.params['read'][1]))
		
		self.hboxLivre.Layout()
		self.Refresh()

	#---------------------------------------------------
	# --- Action des boutons et autre event

	def OnWikipedia(self, evt):
		"""
		Ouvre une page internet sur la biographie de l'auteur
		"_".join([i.capitalize() for i in x.split('_')])
		"""
		search = self.item.getAuteur()
		for i in " .'-":
			rplc = i+'_'
			search = search.replace(i,rplc)
		search = "_".join([i.capitalize() for i in search.split('_')])
		if evt.GetId() == wx.ID_ABOUT:
			search = 'wikipedia+' + search.replace('_','+')
			query = "https://www.google.fr/webhp?tab=ww&ei=trm6VKPQBJLWaqC_gHA&ved=0CAcQ1S4#q=%s"%(search)
		else:
			query = "http://fr.wikipedia.org/wiki/" + search
		wb.open(url=query, new=0)

	def OnModif(self, evt):
		"""
		Modifie le livre en cours
		"""
		values = self.item.__dict__
		fenetre = AjoutLivreFrame(self.virtualList.principalFrame, -1, title="Modification d'un livre", state=self.id, defValue=values)
		fenetre.Show(True)
		fenetre.Centre()

	def OnSuppr(self, evt):
		"""
		Supprime le livre en cours
		"""
		mess = 'Êtes-vous sûre de vouloir supprimer ce livre ?\n\n'.decode('utf-8') + self.item.__repr__()
		supp = wx.MessageDialog(self, message=mess, caption='Supprimer un livre', style=wx.YES_NO|wx.STAY_ON_TOP|wx.ICON_EXCLAMATION)
		rep = supp.ShowModal()		# Attend une réponse de l'utilisateur
		if rep == wx.ID_YES:
			EGL = [('editeur', self.item.editeur),
					('genre', self.item.genre),
					('lieu', self.item.lieu)]
			ID = self.item.ID
			self.virtualList.maBiblio.removeBook(ID)
			self.virtualList.listActu()
			self.virtualList.maBiblio.updateEGL(ID)
			# On passe au livre suivant
			if self.virtualList.GetItemCount() == 0:
				self.Close()
			elif self.index == self.virtualList.GetItemCount():
				self.actuPage(self.index-1)

	def OnChange(self, evt):
		"""
		Passe au livre suivant, ou au précédent
		"""
		if evt.GetId()==wx.ID_FORWARD:
			index = (self.index + 1)%self.virtualList.GetItemCount()
		else:
			index = (self.index - 1)%self.virtualList.GetItemCount()
		self.actuPage(index)

	def OnClose(self, evt):
		"""
		Ferme la fenêtre
		"""
		self.virtualList.visuLivreFrame = False
		self.Destroy()
