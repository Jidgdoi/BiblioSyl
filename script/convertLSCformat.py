#-*- coding: utf-8 -*-
#! /usr/bin/env python
# C. Fournier, 2014

#########################################################################

# Convert list of .lsc into 1 new library file .lsc

#########################################################################

import os, sys, string
from src.Book import Book
from src.Library import Library


def uploadBook(pathFile):
	"""
	Return an object Livre.
	'pathFile': path to file.lsc
	"""
	attributes = []
	with open(pathFile,'r') as f:
		for line in f:
			attributes.append(line.strip())
	attributes[9] = attributes[9].replace('\N', '\n')	# On remplace les '\N' par de vrais retour chariot
	# TEMPORARY 
	if len(attributes) != 13:
		attributes.extend(["", []])
	# Get the several readers from the attr "read", separated by comma
	if attributes[12]:
		attributes[12] = attributes[12].split(',')
	# Create book
	newBook = Book(attributes[0],		# auteurPrenom
					attributes[1],		# auteurNom
					attributes[2],		# titre
					attributes[3],		# editeur
					attributes[4],		# parution
					attributes[5],		# genre
					attributes[6],		# nbPage
					attributes[7],		# lieu
					attributes[8],		# note
					attributes[9],		# commentaire
					attributes[10])		# couverture
	return newBook

# ------------
# --- Main ---
# ------------

if len(sys.argv) != 3:
	print "python2.7 convertLSCformat.py <dirPath_lsc/> <newLib.lsc>"
	sys.exit(0)

dirPathLsc = sys.argv[1]
newLibLsc = sys.argv[2]

lLivre = os.listdir(dirPathLsc)
lLivre = [ x for x in lLivre if x[-4:] == '.lsc']

lib = Library(newLibLsc, '/')
# --- On ouvre chaque fichier
for i in lLivre:
	newBook = uploadBook(dirPathLsc + i)
	lib.dLibrary[newBook.ID] = newBook


lib.writeLibrary()






