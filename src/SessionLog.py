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
			self.readSessionLog(self.sessionLogFile)
		else:
			self.__initSessionLogFile()

	def __initSessionLogFile(self):
		self.dParam["principalFrameSize"] = DEFAULTWINDOWSIZE
		self.dParam["principalFramePosition"] = DEFAULTWINDOWPOSITION
		self.dParam["libraryPath"] = DEFAULTLIBRARYPATH
		
		self.writeSessionLog(self.sessionLogFile, self.dParam)

	def updateSessionLog(self, dParameters):
		self.dParam.update(dParameters)

	# ----------------------------------
	# --- All write and read functions
	# ----------------------------------

	def readSessionLog(self, logFile):
		print "readSession: %s" %self.sessionLogFile
		dParameters = readKeyValueFile(logFile)
		self.dParam.update(dParameters)

	def writeSessionLog(self, logFile, dParameters):
		writeKeyValueFile(logFile, dParameters)

	# ----------------------------------
	# --- All 'get' functions
	# ----------------------------------

	def getSize(self):
		print self.dParam
		return self.dParam["principalFrameSize"]

	def getPosition(self):
		return self.dParam["principalFramePosition"]

	def getLibraryPath(self):
		return self.dParam["libraryPath"]
