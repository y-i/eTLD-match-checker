import pickle

from src.checker_trie import ETLDChecker

checker = ETLDChecker()
checker.initialize_from_file('.github/ci/list.dat')
with open("files/list.pickle", "wb") as f:
    pickle.dump(checker, f)
