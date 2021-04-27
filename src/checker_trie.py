from typing import Dict, List, Optional

from src.checker import Checker
from src.domain import DomainData, DomainResult


class TrieNode:
    def __init__(self) -> None:
        self.nodes: Dict[str, TrieNode] = dict()
        self.is_end = False

    def has(self, word: str) -> bool:
        return word in self.nodes

    def get(self, word: str) -> "TrieNode":
        return self.nodes[word]

    def add(self, word: str) -> "TrieNode":
        if word not in self.nodes:
            self.nodes[word] = TrieNode()
        return self.nodes[word]


class Trie:
    def __init__(self) -> None:
        self.root = TrieNode()

    def search(self, words: List[str]) -> int:
        node = self.root
        suffix_len = 0
        cnt = 0
        for word in reversed(words):
            if not node.has(word):
                break
            node = node.get(word)
            cnt += 1
            if node.is_end:
                suffix_len = cnt

        return suffix_len

    def add(self, words: List[str]) -> None:
        if any(map(lambda x: len(x) == 0, words)):
            return

        node = self.root
        while len(words) > 0:
            word = words.pop()
            node = node.add(word)
        node.is_end = True


class ETLDChecker(Checker):  # type: ignore
    def __init__(self) -> None:
        self.exception_suffix_list = Trie()
        self.wildcard_suffix_list = Trie()
        self.normal_suffix_list = Trie()

    def check(self, domain: Optional[str]) -> DomainResult:
        none_result = DomainResult(is_valid=False, data=None)

        if domain is None:
            return none_result

        words = domain.lower().split(".")
        if any(map(lambda x: len(x) == 0, words)):
            return none_result

        suffix_len = self.exception_suffix_list.search(words) - 1
        if suffix_len > 0:
            return DomainResult(
                is_valid=True,
                data=DomainData(
                    subdomain=".".join(words[: -suffix_len - 1]),
                    root_domain=".".join(words[-suffix_len - 1 :]),
                    etld=".".join(words[-suffix_len:]),
                    tld=words[-1],
                ),
            )

        suffix_len = self.wildcard_suffix_list.search(words) + 1
        if suffix_len == len(words):
            return none_result
        if suffix_len > 1 and suffix_len < len(words):
            return DomainResult(
                is_valid=True,
                data=DomainData(
                    subdomain=".".join(words[: -suffix_len - 1]),
                    root_domain=".".join(words[-suffix_len - 1 :]),
                    etld=".".join(words[-suffix_len:]),
                    tld=words[-1],
                ),
            )

        suffix_len = self.normal_suffix_list.search(words)
        if suffix_len == len(words):
            return none_result
        if suffix_len > 0 and suffix_len < len(words):
            return DomainResult(
                is_valid=True,
                data=DomainData(
                    subdomain=".".join(words[: -suffix_len - 1]),
                    root_domain=".".join(words[-suffix_len - 1 :]),
                    etld=".".join(words[-suffix_len:]),
                    tld=words[-1],
                ),
            )

        return none_result

    def initialize_from_file(self, filename: str) -> None:
        with open(filename, encoding="utf-8") as f:
            for line in f:
                suffix = line.strip()
                if suffix[0] == "!":
                    self.exception_suffix_list.add(suffix[1:].split("."))
                elif suffix[0] == "*":
                    self.wildcard_suffix_list.add(suffix[2:].split("."))
                else:
                    self.normal_suffix_list.add(suffix.split("."))
