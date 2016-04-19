# -*- coding:utf-8 -*-
#! /usr/bin/env python

# Cyril Fournier
# 09/08/2015

import os
import unittest
from Library import Library

class Test_Livre( unittest.TestCase ):

	def setUp(self):
		self.library = Library()

	# ---------------------------
	# --- Test Etagere
	# ---------------------------
	def test_etagere_addBook(self):
		etagere = Library()
		etagere.biblio = {}
		livre = Book("John","Grisham","The Racketeer","International Bestseller",2013,"Novel",382,"Chambre de Cyril",4,"Et voici un autre commentaire blablab abbla.","The Racketeer.jpg")
		etagere.addBook(livre)
		self.assertEqual(len(etagere.dLibrary), 1)

# etagere.ajouter(livre)
# print etagere
# livre = Livre("John","Grisham","The Racketeer","International Bestseller",2013,"Novel",382,"Chambre de Cyril",4,"Et voici un autre commentaire blablab abbla.","The Racketeer.jpg")
# etagere.ajouter(livre)
# livre = Livre("J.R.R.","Tolkien","Le Seigneur Des Anneaux I. La Communanuté de l'Anneau","Folio Junior",2000,"Science-fiction",688,"Chambre de Cyril",3,"Ca c'est le premier livre de la trilogie.","Le Seigneur Des Anneaux I.jpg")
# etagere.ajouter(livre)
# livre = Livre("J.R.R.","Tolkien","Le Seigneur Des Anneaux II. Les Deux Tours","Folio Junior",2000,"Science-fiction",566,"Chambre de Cyril",4,"Là c'est le deuxième, et il me semble qu'il y en a un troisième.","Le Seigneur Des Anneaux II.jpg")
# etagere.ajouter(livre)
# livre = Livre("J.R.R.","Tolkien","Le Seigneur Des Anneaux III. Le Retour du Roi","Folio Junior",2000,"Science-fiction",652,"Chambre de Cyril",5,"Enfin, un dernier commentaire.","Le Seigneur Des Anneaux III.jpg")
# etagere.ajouter(livre)
# print etagere

#etagere.retirer(etagere.biblio.keys()[0])
#print etagere

#etagere.modifier(etagere.biblio.keys()[0], {"auteurPrenom":"Fabien"})
#print etagere

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(Test_Livre)
	unittest.TextTestRunner(verbosity=2).run(suite)
