========================================
Créer l'exécutable avec py2exe:

- Ouvrir le terminale
- Créer un fichier 'setup.py' tel quel:
"""
# setup.py
from distutils.core import setup
import py2exe

setup(windows=['wxLivre.py'])
"""
- Lancer la commande: python setup.py py2exe

Cela créera 2 dossiers 'build' et 'dist'. Le fichier .exe se trouve dans le dossier 'dist'
========================================

========================================
Créer l'exécutable avec cx_Freeze

python setupcxF.py bdist_msi

cxfreeze wxLivre.py --target-dir distcxF --icon Biblio.ico

========================================

