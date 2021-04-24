from typing import Optional
from itertools import chain

from src.domain import DomainData, DomainResult
from src.checker import Checker

class ETLDChecker(Checker):
    def __init__(self) -> None:
        self.exception_suffix_list = set()
        self.wildcard_suffix_list = set()
        self.normal_suffix_list = set()

    def check(self, domain: Optional[str]) -> DomainResult:
        none_result = DomainResult(is_valid=False, data=None)

        if domain == None:
            return none_result

        words = list(reversed(domain.lower().split('.')))
        if any(map(lambda x: len(x) == 0,words)):
            return none_result

        subdomains = []
        while len(words) > 0:
            domain = '.'.join(reversed(words))
            for suffix in self.exception_suffix_list:
                if domain == suffix:
                    return DomainResult(
                        is_valid=True,
                        data=DomainData(
                            subdomain='.'.join(subdomains),
                            root_domain='.'.join(reversed(words)),
                            etld='.'.join(reversed(words[:-1])),
                            tld=words[0],
                        ),
                    )

            for suffix in self.wildcard_suffix_list:
                if domain == suffix:
                    if len(subdomains) < 2:
                        return none_result
                    domain_words = list(chain(subdomains[-2:], reversed(words)))
                    return DomainResult(
                        is_valid=True,
                        data=DomainData(
                            subdomain='.'.join(subdomains[:-2]),
                            root_domain='.'.join(domain_words),
                            etld='.'.join(domain_words[1:]),
                            tld=words[0],
                        ),
                    )

            for suffix in self.normal_suffix_list:
                if domain == suffix:
                    if len(subdomains) < 1:
                        return none_result
                    domain_words = list(chain(subdomains[-1:], reversed(words)))
                    return DomainResult(
                        is_valid=True,
                        data=DomainData(
                            subdomain='.'.join(subdomains[:-1]),
                            root_domain='.'.join(domain_words),
                            etld='.'.join(domain_words[1:]),
                            tld=words[0],
                        ),
                    )

            subdomains.append(words.pop())

        return none_result

    def initialize_from_file(self, filename: str) -> None:
        with open(filename, encoding='utf-8') as f:
            for line in f:
                suffix = line.strip()
                if suffix[0] == '!':
                    self.exception_suffix_list.add(suffix[1:])
                elif suffix[0] == '*':
                    self.wildcard_suffix_list.add(suffix[2:])
                else:
                    self.normal_suffix_list.add(suffix)
