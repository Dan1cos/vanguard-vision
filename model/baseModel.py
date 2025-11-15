from abc import ABC, abstractmethod
from typing import Any


class BaseModel(ABC):
    @abstractmethod
    def predict(self, image: Any) -> Any:
        pass
