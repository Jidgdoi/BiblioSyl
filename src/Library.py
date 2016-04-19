#-*- coding: utf-8 -*-
#! /usr/bin/env python
# C. Fournier, 2014

import os, string
import fileinput
import shutil
from Book import Book
from MyUtils import DEFAULTCOVER

# ===============================
#    ===   Class Library   ===
# ===============================

class Library():
	"""
	Object representing the list of books in a library.
	His function is to manage books: addition, deletion, modification.
	"""
	def __init__(self, pathLibrary='', pathCover='', extLivre=".lsc"):
		# --- Définition des paths des différents dossiers ---
		self.OS = os.sep # '/' si linux, '//' si windows
		self.extLivre = extLivre
		self.pathLibrary = pathLibrary
		self.pathCover = pathCover or pathLibrary.replace(extLivre, "_book_cover%s"%self.OS)
		
		# Dictionary of books: 'ID:Book()'
		self.dLibrary = {}
		# Dictionnaire des listes d'éditeurs, de genre et de lieu
		self.dEGL = {"editeur":[], "genre":[], "lieu":[]}
		
		# --- Fill dictionaries
		if os.path.isfile(self.pathLibrary):
			self.readLibrary(self.pathLibrary)
		if self.dLibrary:
			self.updateEGL()

	def __repr__(self):
		text = ""
		for (key,l) in self.dLibrary.items():
			text += l.__repr__()
		return text

	# ----------------------------------
	# --- All 'set' functions
	# ----------------------------------
	def setPathLibrary(self, path):
		"""
		Set pathLibrary and update pathCover.
		"""
		self.pathLibrary = path
		self.pathCover = self.pathLibrary.replace(self.extLivre, "_book_cover%s"%self.OS)

	# ----------------------------------
	# --- All 'get' functions
	# ----------------------------------
	def getLCover(self):
		"""
		Return the list of book cover, sorted by ascending ID.
		"""
		return [self.dLibrary[b].getAttr("couverture") for b in sorted(self.dLibrary.keys())]

	def getLAttr(self, attr):
		"""
		Return the list of book 'attr', sorted by ascending ID.
		"""
		if attr in Book().__dict__():
			return [self.dLibrary[b].getAttr(attr) for b in sorted(self.dLibrary.keys())]
		return []

	# ----------------------------------
	# --- Read and write functions
	# ----------------------------------
	def readLibrary(self, fileName):
		"""
		Read a '.lsc' file and fill the dictionary self.dLibrary 'ID:Book'.
		"""
		with open(fileName, 'r') as f:
			for l in f:
				currBook = Book().readBook(l)
				if self.dLibrary.has_key(currBook.ID):
					print "This ID already exist in your library."
				self.dLibrary[currBook.ID] = currBook
		# --- Decoding books for windows 32 encoding caracters.
		self.win32Decoding()
		return

	def writeBook(self, book, delete=False):
		"""
		Write the book in the current uploaded library file.lsc.
		"""
		replace = True
		# --- Find book position in library
		lID = sorted(self.dLibrary.keys())
		# The book doesn't exist
		if not book.ID in lID:
			lID = sorted(lID + [book.ID])
			replace = False
		bookPosition = lID.index(book.ID) + 1
		
		# --- Open and add the book
		for line in fileinput.input(self.pathLibrary, inplace=1):
			if bookPosition == fileinput.lineno():
				# Delete book True: we print nothing
				if not delete: print book.bookFormat()
				# Replace book True: we print nothing
				if not replace : print line[:-1]
			else:
				print line[:-1]
		fileinput.close()

	def writeLibrary(self):
		"""
		Write the library data in the current uploaded library file.lsc.
		"""
		try:
			f = open(self.pathLibrary, 'w')
			[f.write(self.dLibrary[ID].bookFormat().encode('utf-8')) for ID in sorted(self.dLibrary.keys())]
			f.close()
		except UnicodeEncodeError:
			print "/!\ Erreur d'encodage, on ne sauvegarde pas le fichier."
		return

	# ----------------------------------
	# --- Manipulating list and files functions
	# ----------------------------------

	def addBook(self, book, forcer=False):
		"""
		Add the new book to the library.
		L'attribut 'forcer' signifie que l'on force l'ajout du livre, bien que celui-ci semble déjà exister.
		"""
		ID = book.getAttr('ID')
		# --- On force l'ajout du livre: création d'une ID similaire
		if forcer:
			alphabet = string.ascii_letters
			ite = 0
			ID += alphabet[ite]
			while ID in self.dLibrary.keys():
				ite += 1
				if ite == len(alphabet):
					ite = 0
					ID += alphabet[ite]
				else:
					ID = ID[:-1] + alphabet[ite]
		# On vérifie si l'ID n'existe pas déjà
		else:
			# --- Check si le livre existe déjà
			if self.dLibrary.has_key(ID):
				return True, ID
		
		# --- On l'ajoute au dico biblio.
		self.dLibrary[ID] = book
		self.win32Decoding(ID)
		return False, ID

	def removeBook(self, ID):
		"""
		Remove Book object from the dictionary dLibrary.
		"""
		self.dLibrary.pop(ID)
		return 0

	def modifyBook(self, ID, modif):
		"""
		Update the modified book in the dictionary.
		"""
		# --- MAJ book in dictionary.
		for i in modif.keys():
			self.dLibrary[ID].setAttr(i,modif[i])
		# --- Update book's ID.
		self.dLibrary[ID].updateID()
#		# --- MAJ book in library file.lsc.
#		self.writeBook(self.dLibrary[ID])
		# --- If the new ID is different from the precedent, we change the key of the dictionary.
		newID = self.dLibrary[ID].getAttr('ID')
		if newID != ID:
			self.dLibrary[newID] = self.dLibrary.pop(ID)
		
		# --- Decode the new book for win32.
		self.win32Decoding(newID)
		return 0

	def saveLibrary(self, newFile=""):
		"""
		Save the library.
		'newFile': if set, save to a new library, and so create a new cover directory.
		"""
		print "# Save library: %s" %(newFile or self.pathLibrary)
		# Create new directory and copy covers.
		if newFile:
			previousCoverDir = self.pathCover
			self.updatePaths(newFile)
			# Check if directory exist, if not, create it.
			if not os.path.isdir(self.pathCover): os.makedirs(self.pathCover)
			# Copy covers to the new directory.
			lCoverBook = self.getLCover()
			for c in lCoverBook:
				if c != DEFAULTCOVER:
					shutil.copy2("%s%s"%(previousCoverDir, c), self.pathCover)
		# Clean directory of obsolete covers.
		else:
			self.cleanCoverDir()
		
		# Finally write library.
		self.writeLibrary()

	def cleanCoverDir(self):
		"""
		Clean the book cover directory from unrelated pictures.
		"""
		print "# Clean book cover directory: %s"%self.pathCover.encode('utf-8')
		# --- Delete the book cover picture if isn't the default one, and if it's not used by another book.
		lCoverBook = self.getLCover()
		lCoverFile = os.listdir(self.pathCover)
		for picture in lCoverFile:
			if picture not in lCoverBook:
				os.remove("%s%s"%(self.pathCover, picture))
				print "\t- %s%s"%(self.pathCover.encode('utf-8'), picture)

	# ----------------------------------
	# --- Update functions
	# ----------------------------------
	def updatePaths(self, newPath):
		"""
		Update pathLibrary and pathCover.
		"""
		self.pathLibrary = newPath
		self.pathCover = self.pathLibrary.replace(self.extLivre, "_book_cover%s"%self.OS)

	def updateLibrary(self, newLibraryPath):
		"""
		Update all paths dependant of pathLibrary.
		'create': create directories if don't exist.
		"""
		self.updatePaths(newLibraryPath)
		
		# --- Check if directory exist, if not, create it
		if not os.path.isdir(self.pathCover): os.makedirs(self.pathCover)
		
		self.dLibrary.clear()
		self.readLibrary(self.pathLibrary)
		self.updateEGL()

	def updateEGL(self, book=None):
		"""
		Update the dictionary 'dEGL' with the new book, or with all the books.
		"""
		if not book:
			# Update for all books
			book = self.dLibrary
		# --- Update and suppress duplicated values
		for attribute in book.values()[0].getListingAttr():
			self.dEGL[attribute] = sorted(list(set([b.getAttr(attribute) for b in book.values() if b.getAttr(attribute) != 'NA'])))

	# ----------------------------------
	# --- Decoding functions
	# ----------------------------------
	def win32Decoding(self, givenID=''):
		"""
		Decodage caractère ASCII pour windows.
		"""
		if givenID:
			# Une ID spécifique à été donnée
			listID = [givenID]
		else:
			# Aucune ID donnée, on traite tous les livres
			listID = self.dLibrary.keys()
		
		for ID in listID:
			for k in self.dLibrary[ID].__dict__.keys():
				v = self.dLibrary[ID].getAttr(k)		# On récupère la valeur du paramètre 'k'
				if type(v) is str and k != 'couverture':
					self.dLibrary[ID].setAttr(k, v.decode('utf-8'))	# On la decode et la remplace
