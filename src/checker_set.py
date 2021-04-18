from typing import Optional
from dataclasses import dataclass
from itertools import chain

@dataclass
class DomainData:
    subdomain: str
    domain: str
    etld: str
    tld: str

@dataclass
class DomainResult:
    is_valid: bool
    data: Optional[DomainData]

exception_suffix_list = set()
wildcard_suffix_list = set()
normal_suffix_list = set()

def create_set():
    with open('list.dat', encoding='utf-8') as f:
        for line in f:
            suffix = line.strip()
            if suffix[0] == '!':
                exception_suffix_list.add(suffix[1:])
            elif suffix[0] == '*':
                wildcard_suffix_list.add(suffix[2:])
            else:
                normal_suffix_list.add(suffix)
    print(len(exception_suffix_list))
    print(len(wildcard_suffix_list))
    print(len(normal_suffix_list))

def check(domain: str) -> DomainResult:
    none_result = DomainResult(is_valid=False, data=None)

    if domain == None:
        return none_result

    words = list(reversed(domain.lower().split('.')))
    if any(map(lambda x: len(x) == 0,words)):
        return none_result

    subdomains = []
    while len(words) > 0:
        domain = '.'.join(reversed(words))
        for suffix in exception_suffix_list:
            if domain == suffix:
                return DomainResult(
                    is_valid=True,
                    data=DomainData(
                        subdomain='.'.join(subdomains),
                        domain='.'.join(reversed(words)),
                        etld='.'.join(reversed(words[:-1])),
                        tld=words[0],
                    ),
                )
                # words.pop()
                # return '.'.join(reversed(words))
        for suffix in wildcard_suffix_list:
            if domain == suffix:
                if len(subdomains) < 2:
                    return none_result
                domain_words = list(chain(subdomains[-2:], reversed(words)))
                return DomainResult(
                    is_valid=True,
                    data=DomainData(
                        subdomain='.'.join(subdomains[:-2]),
                        domain='.'.join(domain_words),
                        etld='.'.join(domain_words[1:]),
                        tld=words[0],
                    ),
                )
                # return f"{last_last_word}.{last_word}.{domain}"
        for suffix in normal_suffix_list:
            if domain == suffix:
                if len(subdomains) < 1:
                    return none_result
                domain_words = list(chain(subdomains[-1:], reversed(words)))
                return DomainResult(
                    is_valid=True,
                    data=DomainData(
                        subdomain='.'.join(subdomains[:-1]),
                        domain='.'.join(domain_words),
                        etld='.'.join(domain_words[1:]),
                        tld=words[0],
                    ),
                )
                # return f"{last_word}.{domain}"

        subdomains.append(words.pop())

    return none_result

def checkPublicSuffix(domain: str) -> Optional[str]:
    result = check(domain)
    if result.is_valid:
        return result.data.domain
    else:
        return None

if __name__ == '__main__':
    create_set()
