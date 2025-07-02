from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.model.message import SystemPromptMessage, UserPromptMessage
from dify_plugin.entities.tool import ToolInvokeMessage
from langchain_neo4j import Neo4jGraph

from tools.prompt import (
    ANSWER_SYSTEM_PROMPT_TEMPLATE,
    NL_CQL_SYSTEM_PROMPT_TEMPLATE,
    NL_CQL_USER_PROMPT_TEMPLATE,
)


class Neo4jChatTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        model = tool_parameters["model"]
        query = tool_parameters["query"]
        graph = self._init_graph(tool_parameters)
        query_cql = self.gen_cql(model, query, graph)
        result = self.cql_executor(query_cql, graph)
        answer = self.summary_answer(query, model, result)
        yield self.create_json_message(
            json=dict(answer=answer, query_cql=query_cql, query_result=result)
        )

    def _init_graph(self, tool_parameters: dict[str, Any]) -> Neo4jGraph:
        graph = Neo4jGraph(
            url=tool_parameters.get("neo4j_uri")
            or self.runtime.credentials["neo4j_uri"],
            username=tool_parameters.get("neo4j_user")
            or self.runtime.credentials["neo4j_user"],
            password=tool_parameters.get("neo4j_password")
            or self.runtime.credentials["neo4j_password"],
        )
        return graph

    def _get_schema(self, graph: Neo4jGraph) -> str:
        try:
            schema = graph.get_schema
        except Exception:
            raise Exception("Failed to get schema")
        return schema

    def gen_cql(self, model, query: str, graph: Neo4jGraph) -> str:
        schema = self._get_schema(graph)
        # print("schema:", schema)
        prompt_messages = [
            SystemPromptMessage(
                content=NL_CQL_SYSTEM_PROMPT_TEMPLATE.format(schema=schema)
            ),
            UserPromptMessage(content=NL_CQL_USER_PROMPT_TEMPLATE.format(input=query)),
        ]

        response = self.session.model.llm.invoke(
            model_config=model,
            prompt_messages=prompt_messages,
            stream=False,
        )
        return response.message.content

    def cql_executor(self, query_cql: str, graph: Neo4jGraph) -> str:
        try:
            return graph.query(query_cql)
        except Exception:
            raise Exception("Failed to execute query")

    def summary_answer(self, query: str, model, result: str) -> str:

        prompt_messages = [
            SystemPromptMessage(
                content=ANSWER_SYSTEM_PROMPT_TEMPLATE.format(
                    input=query, query_result=result
                )
            )
        ]
        response = self.session.model.llm.invoke(
            model_config=model,
            prompt_messages=prompt_messages,
            stream=False,
        )
        return response.message.content
