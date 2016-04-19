#-*- coding: utf-8 -*-
#! /usr/bin/env python
# C. Fournier, 2014

import string

# ============================
#    ===   Class Book   ===
# ============================

class Book():
	"""
	Object representing all the attributes of a book.
	"""
	def __init__(self, auteurPrenom="NA", auteurNom="NA", titre="NA", editeur="NA", parution=-1, genre="NA", nbPage=-1, lieu="NA", note=-1, commentaire="NA", couverture="NA", ISBN="NA", read=["NA"]):
		# List of attributes
		self.auteurPrenom = auteurPrenom		# Prénom de l'auteur
		self.auteurNom = auteurNom				# Nom de l'auteur
		self.titre = titre						# Titre du livre
		self.editeur = editeur					# Edition POCKET, ...
		self.parution = int(parution)			# Date de parution
		self.genre = genre						# Roman policier, Science-fiction, ...
		self.nbPage = int(nbPage)				# Nombre de pages
		self.lieu = lieu						# Lieu de rangement du livre
		self.note = int(note)					# Note donnée au livre
		self.commentaire = commentaire			# Commentaire sur le livre
		self.couverture = couverture			# Photo de couverture
		self.ISBN = ISBN						# International Standard Book Number
		self.read = read						# Liste des personnes ayant lu ce livre
		
		self.ID = ""							# Identifiant du livre pour l'étagère
		self.updateID()

	def __repr__(self):
		space = (len(self.ID)+2) * ' '
		text = """%s
[%s] %s %s
%s %s
%s %s - %s (%s pages), %s
%s ISBN: %s
%s Read by: %s
%s
"""		%('-'*40,
		self.ID, self.auteurPrenom, self.auteurNom,
		space, self.titre,
		space, self.editeur, str(self.parution), str(self.nbPage), self.genre,
		space, self.ISBN,
		space, ', '.join(self.read),
		'-'*40)
		return text

	def __eq__(self, o):
		return self.ID == o.ID

	# ----------------------------------
	# --- All 'get' functions
	# ----------------------------------
	def getAttr(self, attr):
		"""
		Return the query attribute.
		Params are: 'auteurPrenom', 'nbPage', 'commentaire', 'couverture', 'lieu', 'parution', 'note', 'auteurNom', 'editeur', 'genre', 'titre', 'ID', 'ISBN', 'read'
		"""
		if attr in self.__dict__:
			return self.__dict__[attr]

	def getAuteur(self):
		"""
		Return the full name of the author: Prenom Nom
		"""
		return "%s %s" %(self.auteurPrenom, self.auteurNom)

	def getListingAttr(self):
		"""
		Return a dictionary of the attributes which can be listed (Editor, Genre, Place).
		"""
		return {"editeur":self.editeur, "genre":self.genre, "lieu":self.lieu}

	def getReadBy(self):
		"""
		Return a string of the readers, separated by ', '.
		"""
		return ', '.join(self.read)

	# ----------------------------------
	# --- All 'set' functions
	# ----------------------------------
	def setAttr(self, attr, value):
		"""
		Set the attribute with the given value.
		Params are: 'auteurPrenom', 'nbPage', 'commentaire', 'couverture', 'lieu', 'parution', 'note', 'auteurNom', 'editeur', 'genre', 'titre'
		"""
		if attr in ["parution", "nbPage", "note"]:
			try:
				self.__dict__[attr] = int(value)
			except ValueError:
				print "Error: your value '%s' is inapropriate for the attribute '%s'. You have to specify an integer." %(value, attr)
		elif attr in self.__dict__:
			self.__dict__[attr] = value
		else:
			print "Error: this attribute doesn't exist: %s." %attr

	# ----------------------------------
	# --- Other functions
	# ----------------------------------
	def updateID(self):
		"""
		Créé un identifiant 'ID' unique pour le livre
		ID: Initiales de l'auteur + somme des valeurs ASCII du titre et de l'éditeur
		"""
		ID = self.auteurPrenom[:1] or "Z"
		ID += self.auteurNom[:1] or "Z"
		ID += str(sum([ord(i) for i in self.titre+self.editeur]))
		self.ID = ID

	def readBook(self, line):
		"""
		Return an object Book filled with 'line' information.
		'line': one line of the '.lsc' file.
		"""
		# --- Split line
		elements = line.strip().split('\t')
		# --- Replace tabulations and carriage return.
		for i in range(len(elements)):
			elements[i] = elements[i].replace('\\n', '\n')
			elements[i] = elements[i].replace('\\t', '\t')
		# --- Fill book
		self.ID = 			elements[0]
		self.auteurPrenom = elements[1]
		self.auteurNom = 	elements[2]
		self.titre = 		elements[3]
		self.editeur = 		elements[4]
		self.parution = 	elements[5]
		self.genre = 		elements[6]
		self.nbPage = 		elements[7]
		self.lieu = 		elements[8]
		self.note = 		elements[9]
		self.commentaire = 	elements[10]
		self.couverture = 	elements[11]
		self.ISBN = 		elements[12]
		self.read = 		elements[13].split(',')
		return self

	def bookFormat(self):
		"""
		Return a string of the book writing format (.lsc).bash 
		"""
		# --- Replace tabulations and carriage return.
		commentary = self.commentaire.replace('\n','\\n').replace('\t','\\t')
		return "%s	%s	%s	%s	%s	%s	%s	%s	%s	%s	%s	%s	%s	%s\n".encode('utf-8') %(
				self.ID,
				self.auteurPrenom,
				self.auteurNom,
				self.titre,
				self.editeur,
				str(self.parution),
				self.genre,
				str(self.nbPage),
				self.lieu,
				str(self.note),
				commentary,
				self.couverture,
				self.ISBN,
				','.join(self.read))
