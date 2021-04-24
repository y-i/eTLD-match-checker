from typing import Optional
from dataclasses import dataclass

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
