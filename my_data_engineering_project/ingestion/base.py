from abc import ABC, abstractmethod

class BaseIngestor(ABC):
    @abstractmethod
    def load_file(self, path: str):
        """
        Ingest data from the specified path.

        Args:
            path (str): The path to the data source.

        Returns:
            Any: The ingested data.
        """
        pass