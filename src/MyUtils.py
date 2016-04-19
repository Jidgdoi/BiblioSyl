#-*- coding: utf-8 -*-
#! /usr/bin/env python
# C. Fournier, 2014

import wx

#########################################################################

# GLOBAL VARIABLES

#########################################################################

DEFAULTCOVER = "image-not-available.jpg"
DEFAULTWINDOWSIZE = (1574, 850)
DEFAULTWINDOWPOSITION = wx.DEFAULT_FRAME_STYLE
DEFAULTLIBRARYPATH = ""

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
				v = [ MTB.tryNumber(i, revealNature=True) for i in values.split(',') ]
				if len(v) == 1: v = v[0]
				MTB.dictAdd(dResult, key, v)
	return res

def writeKeyValueFile(fileName, data, sep='\t', reverse=False):
	"""
	Read a file with a line structure of type "Key Value(s)", with "#" for commentary.
	Multiple values must be separated by comma.
	'data': dictionary.
	'sep': separator. Default is tabulation.
	'reverse': in case of the structure of the file is "Value\tKey".
	"""
	dResult = {}
	f = open(fileName, 'w')
	for key,v in data.items():
		key = str(key)
		if isinstance(v,(list,tuple)): values = ','.join(map(str,v))
		else: values = str(v)
		if reverse: f.write("%s\t%s\n" %(values, key))
		else: f.write("%s\t%s\n" %(key, values))
	f.close()
