import sys
import pickle
from pathlib import Path

sys.path.append(str(Path('__file__').resolve().parent))

from src.checker_trie import ETLDChecker

checker = ETLDChecker()
checker.initialize_from_file('.github/ci/list.dat')
with open('files/list.pickle', 'wb') as f:
    pickle.dump(checker, f)
