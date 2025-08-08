# conftest.py  (at repo root, same level as src/ and tests/)
import os, sys
SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), "src"))
if SRC not in sys.path:
    sys.path.insert(0, SRC)
