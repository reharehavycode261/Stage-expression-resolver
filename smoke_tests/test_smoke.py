"""Tests de smoke - Validation basique de l'environnement"""
import unittest
import sys
import os


class SmokeTests(unittest.TestCase):
    """Tests de validation basique de l'environnement"""
    
    def test_python_version(self):
        """Vérifie que Python est opérationnel"""
        version = sys.version_info
        self.assertGreaterEqual(version.major, 3, "Python 3+ requis")
        print(f"✅ Python {version.major}.{version.minor} détecté")
    
    def test_working_directory_exists(self):
        """Vérifie que le répertoire de travail existe"""
        self.assertTrue(os.path.exists('.'), "Répertoire de travail doit exister")
        print(f"✅ Répertoire de travail: {os.getcwd()}")
    
    def test_basic_imports(self):
        """Vérifie que les imports basiques fonctionnent"""
        try:
            import json
            import re
            import datetime
            self.assertTrue(True)
            print("✅ Imports basiques fonctionnels")
        except ImportError as e:
            self.fail(f"Échec import basique: {e}")


if __name__ == '__main__':
    unittest.main()
