from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from langchain_community.graphs import Neo4jGraph


class Neo4jChatProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            """
            IMPLEMENT YOUR VALIDATION HERE
            """
            self._connect(credentials)
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))

    def _connect(self, credentials: dict[str, Any]) -> None:
        """
        IMPLEMENT YOUR CONNECTION HERE
        """
        self.graph = Neo4jGraph(
            url=credentials["neo4j_uri"],
            username=credentials["neo4j_user"],
            password=credentials["neo4j_password"],
        )
        return self.graph.get_schema
