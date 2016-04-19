#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python 3
 
"""
Icone sous Windows: il faut:
=> un xxx.ico pour integration dans le exe, avec "icon=xxx.ico"
=> un xxx.png pour integration avec PyQt4 + demander la recopie avec includefiles.
"""
 
import sys, os
import platform
from cx_Freeze import setup, Executable

# Détection de l'architecture windows (32bits/64bits)
if sys.platform == "win32":
	archi = platform.architecture()[0]
#############################################################################
# preparation des options
 
# chemins de recherche des modules
# ajouter d'autres chemins (absolus) si necessaire: sys.path + ["chemin1", "chemin2"]
OS = os.sep
pathRoot = os.getcwd()
pathRoot = pathRoot[:pathRoot.find('BiblioSyl')] + 'BiblioSyl' + OS	# Dossier racine du projet
pathCode = pathRoot + "src" + OS										# Dossier du code source
pathData = pathRoot + "data" + OS										# Dossier des données
pathCouv = pathData + "couvertures" + OS								# Dossier de sauvegarde des couvertures de livre
pathIcone = pathData + "icones" + OS									# Dossier de sauvegarde des icones
pathLivre = pathData + "livres" + OS									# Dossier de sauvegarde des livres
pathExe = pathRoot + "exe_and_setup" + OS								# Dossier de sauvegarde du build créé par cxFreeze
path = sys.path + [pathRoot, pathCode, pathData, pathCouv, pathIcone, pathLivre]

# options d'inclusion/exclusion des modules
includes = []  # nommer les modules non trouves par cx_freeze
excludes = ['tkinter']
packages = []  # nommer les packages utilises

targetDir = "buildExe"
if sys.platform == "win32":
	targetDir += "-" + archi

# copier les fichiers non-Python et/ou repertoires et leur contenu:
#includefiles = [(pathData, "../../"+targetDir+"\data")]			# Avec quelques données
#includefiles = [(pathExe+"data", "../../"+targetDir+"\data")]		# Sans données mais avec tout le dossier data de base
#includefiles = [(pathExe+"data\icones", "../../"+targetDir+"\data\icones")]	# Sans données mais le dossier icones
includefiles = []		# Sans données sans dossier data

if sys.platform == "win32":
	pass
	# includefiles += [...] : ajouter les recopies specifiques à Windows
elif sys.platform == "linux2":
	pass
	# includefiles += [...] : ajouter les recopies specifiques à Linux
else:
	pass
	# includefiles += [...] : cas du Mac OSX non traite ici
 
# pour que les bibliotheques binaires de /usr/lib soient recopiees aussi sous Linux
binpathincludes = []
if sys.platform == "linux2":
	binpathincludes += ["/usr/lib"]
 
# niveau d'optimisation pour la compilation en bytecodes
optimize = 0
 
# si True, n'affiche que les warning et les erreurs pendant le traitement cx_freeze
silent = True
 
# construction du dictionnaire des options
options = {"path": path,
		   "includes": includes,
		   "excludes": excludes,
		   "packages": packages,
		   "include_files": includefiles,
		   "bin_path_includes": binpathincludes,
		   "create_shared_zip": False,  # <= ne pas generer de fichier zip
		   "include_in_shared_zip": False,  # <= ne pas generer de fichier zip
		   "compressed": False,  # <= ne pas generer de fichier zip
		   "optimize": optimize,
		   "silent": silent
		   }
 
# pour inclure sous Windows les dll system de Windows necessaires
if sys.platform == "win32":
	options["include_msvcr"] = True
 
#############################################################################
# preparation des cibles
base = None
if sys.platform == "win32":
	base = "Win32GUI"  # pour application graphique sous Windows
	# base = "Console" # pour application en console sous Windows

icone = pathIcone+"Biblio.ico"
 
cible_1 = Executable(
	script=pathCode + "wxLivre.py",
	base=base,
	targetDir=targetDir,
	targetName="BiblioSyl.exe",
	compress=False,  # <= ne pas generer de fichier zip
	copyDependentFiles=True,
	appendScriptToExe=True,
	appendScriptToLibrary=False,  # <= ne pas generer de fichier zip
	icon=icone
	)

 
#############################################################################
# creation du setup
setup(
	name="BiblioSyl",
	version="1.00",
	description="Bibliotheque virtuelle personnalisee pour maman",
	author="Cyril Fournier",
	options={"build_exe": options, "install_exe":{"build_dir":pathExe}},
	executables=[cible_1]
	)
