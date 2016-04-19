# -*- coding:utf-8 -*-

# Cyril Fournier
# 09/08/2015

import os
import unittest
from Book import Book

class Test_Livre( unittest.TestCase ):

	def setUp(self):
		self.book = Book("Laurent","Gounelle","L'homme qui voulait être heureux","POCKET",2013,"Roman",168,"Chambre de Cyril",5,"Commentaire de ce livre, blabliblou\ttchou\ttchou.\nRetour a la ligne baby.","L'homme qui voulait etre heureux.jpg")
		print self.book.__module__

	# ---------------------------
	# --- Test Livre
	# ---------------------------
	def test_livre_getAuteur(self):
		exp = "Laurent Gounelle"
		obs = self.book.getAuteur()
		self.assertEqual(exp, obs)

	def test_livre_getAttr_titre(self):
		exp = "L'homme qui voulait être heureux"
		obs = self.book.getAttr('titre')
		self.assertEqual(exp, obs)

	def test_livre_setAttr_page(self):
		exp = 42
		self.book.setAttr('nbPage',42)
		obs = self.book.nbPage
		self.assertEqual(exp, obs)

	def test_livre_updateID(self):
		exp = "LG" + str(sum([ord(i) for i in self.book.titre + self.book.editeur]))
		self.book.updateID()
		obs = self.book.getAttr('ID')
		self.assertEqual(exp, obs)

	def test_readBook(self):
		exp = self.book
		obs = Book().readBook("LG3808	Laurent	Gounelle	L'homme qui voulait être heureux	POCKET	2013	Roman	168	Chambre de Cyril	5	Commentaire de ce livre, blabliblou\\ttchou\\ttchou.\\nRetour a la ligne baby.	L'homme qui voulait etre heureux.jpg	NA	NA\n")
		self.assertEqual(exp, obs)

	def test_bookFormat(self):
		exp = "LG3808	Laurent	Gounelle	L'homme qui voulait être heureux	POCKET	2013	Roman	168	Chambre de Cyril	5	Commentaire de ce livre, blabliblou\\ttchou\\ttchou.\\nRetour a la ligne baby.	L'homme qui voulait etre heureux.jpg	NA	NA\n"
		obs = self.book.bookFormat()
		self.assertEqual(exp, obs)


if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(Test_Livre)
	unittest.TextTestRunner(verbosity=2).run(suite)
