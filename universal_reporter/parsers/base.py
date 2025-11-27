from abc import ABC, abstractmethod
from typing import List
from ..models import Finding


class BaseParser(ABC):
    @abstractmethod
    def can_handle(self, file_path: str) -> bool:
        pass

    @abstractmethod
    def parse(self, file_path: str) -> List[Finding]:
        pass