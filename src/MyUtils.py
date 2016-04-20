#-*- coding: utf-8 -*-
#! /usr/bin/env python
# C. Fournier, 2014

import wx
import operator

#########################################################################

# GLOBAL VARIABLES

#########################################################################

DEFAULTCOVER = "image-not-available.jpg"
DEFAULTWINDOWSIZE = (1574, 850)
DEFAULTWINDOWPOSITION = wx.DEFAULT_FRAME_STYLE
DEFAULTLIBRARYPATH = "data/Example_library.lsc"

#########################################################################

# GLOBAL FUNCTIONS

#########################################################################

def wxVersion():
	return wx.version().split()[0]

def printLogText(text):
	"""
	Print text in the log (bottom of the window).
	"""
	wx.GetApp().GetTopWindow().SetStatusText(text)

def is_number(x):
	"""
	Check si la variable est un nombre
	"""
	try:
		int(x)
		return True
	except ValueError:
		return False

def tryNumber(x, revealNature=False):
	"""
	Return True if x is a number (int or float), else return False.
	'revealNature': if True, return the variable in his correct form instead of a boolean.
	(e.g: "42" -> 42
	      "0.74" -> 0.74
	      "foo" -> "foo")
	"""
	isNumber = True
	if not operator.isNumberType(x):
		# type(x) != int or float
		try:
			x = int(x)
		except ValueError:
			try:
				x = float(x)
			except ValueError:
				isNumber = False
	if revealNature:
		return x
	return isNumber

def dictAdd(d, key, value):
	"""
	Add the item 'key:value' to the dictionary 'd' if the key doesn't exist, otherwise it updates the key by appending the new value to the previous one.
	e.g.: d = {'a':5}
	    dictAdd(d, 'a', 7) --> d = {'a':[5,7]}
	    dictAdd(d, 'b', 42) --> d = {'a':5, 'b':42}
	"""
	if d.has_key(key):
		if type(d[key]) != list: d[key] = [d[key], value]
		else:                    d[key].append(value)
	else:
		d[key] = value

def setMiddle(win, item):
	"""
	Calcul la position x pour centrer un élément
	"""
	return int((win/2.0)-(item/2.0))

def createMyFont(values={}):
	"""
	Retourne un objet wx.Font
	"""
	if wx.Platform == '__WXMSW__':
		# Style d'écriture de base pour Windows
		font = {'pointSize': 11,
				'family': wx.DEFAULT,
				'style': wx.NORMAL,
				'weight': wx.NORMAL,
				'underline': False,
				'faceName': '',
				'encoding': wx.FONTENCODING_SYSTEM}
	else:
		# Style d'écriture de base pour les autres systèmes
		font = {'pointSize': 11,
				'family': wx.ROMAN,
				'style': wx.NORMAL,
				'weight': wx.NORMAL,
				'underline': False,
				'faceName': '',
				'encoding': wx.FONTENCODING_SYSTEM}
	
	if values:
		# On modifie les valeurs par défaut avec celles données en paramètres
		for k in values.keys():
			font[k] = values[k]
	
	return wx.Font(pointSize = font['pointSize'],
					family = font['family'],
					style = font['style'],
					weight = font['weight'],
					underline = font['underline'],
					faceName = font['faceName'],
					encoding =  font['encoding'])

def readKeyValueFile(fileName, sep='\t', reverse=False):
	"""
	Read a file with a line structure of type "Key Value(s)", with "#" for commentary.
	Multiple values must be separated by comma.
	'sep': separator. Default is tabulation.
	'reverse': in case of the structure of the file is "Value\tKey".
	"""
	dResult = {}
	with open(fileName,'rb') as f:
		for l in f:
			if l[0] != "#":
				if reverse: values, key = l.strip().split("\t")
				else:       key, values = l.strip().split("\t")
				v = [ tryNumber(i, revealNature=True) for i in values.split(',') ]
				if len(v) == 1: v = v[0]
				dictAdd(dResult, key, v)
	return dResult

def writeKeyValueFile(fileName, data, sep='\t', reverse=False):
	"""
	Read a file with a line structure of type "Key Value(s)", with "#" for commentary.
	Multiple values must be separated by comma.
	'data': dictionary.
	'sep': separator. Default is tabulation.
	'reverse': in case of the structure of the file is "Value\tKey".
	"""
	f = open(fileName, 'w')
	for key,v in data.items():
		key = str(key)
		if isinstance(v,(list,tuple)): values = ','.join(map(str,v))
		else: values = str(v)
		if reverse: f.write("%s\t%s\n" %(values, key))
		else: f.write("%s\t%s\n" %(key, values))
	f.close()
