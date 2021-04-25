from abc import ABC, abstractmethod
from typing import Optional

from src.domain import DomainResult


class Checker:
    # @abstractmethod
    def __init__(self) -> None:
        # super().__init__()
        pass

    # @abstractmethod
    def check(self, domain: Optional[str]) -> DomainResult:
        pass

    # @abstractmethod
    def initialize_from_file(self, filename: str) -> None:
        pass
