## neo4j-chat

**Author:** slp
**Version:** 0.0.1
**Type:** tool

### Description

This plugin allows you to interact with a Neo4j graph database using natural language. It translates your questions into Cypher queries, executes them, and returns the results in a human-readable format.

### Features

- **Natural Language to Cypher:** Converts natural language questions into Cypher queries.
- **Query Execution:** Executes the generated Cypher query against your Neo4j database.
- **Summarized Results:**  Provides a concise summary of the query results.

### Setup

1.  **Installation:** Install the plugin in your Dify environment.
2.  **Configuration:** Configure the plugin with your Neo4j database credentials:
    *   `NEO4J_URI`: The URI of your Neo4j database.
    *   `NEO4J_USER`: The username for your Neo4j database.
    *   `NEO4J_PASSWORD`: The password for your Neo4j database.

### How to Use

Once the plugin is configured, you can use it in your Dify applications. Simply provide a natural language query, and the plugin will return the answer from your Neo4j database.