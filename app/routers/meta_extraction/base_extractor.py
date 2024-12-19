from .models import MetaExtractorConfig
from ..metadata.models import TableMetadataInput
from abc import ABC, abstractmethod


class MetaExtractor(ABC):
    def __init__(self, config: MetaExtractorConfig):
        self.config = config
        self._error_mes = "should be implemented in derived class"

    @abstractmethod
    def _get_connection_uri(self) -> str:
        pass
    
    @abstractmethod
    async def extract_meta(self) -> list[TableMetadataInput]:
        pass
