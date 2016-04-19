#-*- coding: utf-8 -*-
#! /usr/bin/env python
# C. Fournier, 2014

import os
from MyUtils import *

# ==================================
#    ===   Class SessionLog   ===
# ==================================

class SessionLog():
	"""
	Gestioning class of the session log.
	"""
	def __init__(self, srcPath):
		self.dParam = {}
		self.sessionLogFile = "%s%ssession.log" %(srcPath, os.sep)
		if os.path.isfile(self.sessionLogFile):
			self.readSessionLog()
		else:
			self.__initSessionLogFile()

	def __initSessionLogFile(self):
		self.dParam["principalFrameSize"] = DEFAULTWINDOWSIZE
		self.dParam["principalFramePosition"] = DEFAULTWINDOWPOSITION
		self.dParam["libraryPath"] = DEFAULTLIBRARYPATH
		
		self.writeSessionLog()

	def updateSessionLog(self, wSize="", wPostion="", libPath="", dico={}):
		if dico:
			self.dParam.update(dico)
		elif wSize and wPosition and libPath:
			self.dParam["principalFrameSize"] = wSize
			self.dParam["principalFramePosition"] = wPostion
			self.dParam["libraryPath"] = libPath

	# ----------------------------------
	# --- All write and read functions
	# ----------------------------------

	def readSessionLog(self):
		dParam = readKeyValueFile(self.sessionLogFile)
		self.updateSessionLog(dParam)

	def writeSessionLog(self):
		writeKeyValueFile(self.sessionLogFile, self.dParam)

	# ----------------------------------
	# --- All 'get' functions
	# ----------------------------------

	def getSize(self):
		return self.dParam["principalFrameSize"]

	def getPosition(self):
		return self.dParam["principalFramePosition"]

	def getLibraryPath(self):
		return self.dParam["libraryPath"]
