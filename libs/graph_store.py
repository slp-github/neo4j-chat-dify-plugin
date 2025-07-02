from typing import Any, Dict, List, Protocol, runtime_checkable


@runtime_checkable
class GraphStore(Protocol):
    """Abstract class for graph operations."""

    @property
    def get_schema(self) -> str:
        """Return the schema of the Graph database"""
        ...

    @property
    def get_structured_schema(self) -> Dict[str, Any]:
        """Return the schema of the Graph database"""
        ...

    def query(self, query: str, params: dict = {}) -> List[Dict[str, Any]]:
        """Query the graph."""
        ...

    def refresh_schema(self) -> None:
        """Refresh the graph schema information."""
        ...
