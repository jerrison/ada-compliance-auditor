# Milvus Vector Store


The Milvus Vector Store node connects to a Milvus vector database to store and retrieve embeddings. This node is used to query semantically similar documents or vectors based on the user's questions or inputs.


### Inputs


- Documents - Accepts vectorized documents (e.g., from embedding nodes) to be stored in Milvus
- Questions - Accepts vectorized queries for similarity search in the Milvus collection


### Outputs


- Documents - Emits associated metadata or document references retrieved by the query
- Answers - Returns the most relevant document matches based on vector similarity
- Questions - Returns the input question for chaining with other nodes like LLMs


### Configuration


#### GUI


- Type of Milvus Host - Choose your Milvus environment.

Example - Milvus cloud server
- Host - Define the endpoint of your Milvus instance.

Format - your-instance-name.region.zillizcloud.com
- Port - Set the port number used for Milvus API communication.

Example - 443
- API Key - Enter the access key provided by your Milvus service.
- Retrieval Score - Set the minimum similarity score for returning search results.

Options - Related, Highly Related, Most Relevant
- Collection - Name the target collection where your vectors are stored and retrieved.

Example - ROCKETRIDE


Milvus Vector Store supports several deployment modes:


### Example Usage


#### Basic RAG Pipeline


This example shows how to use Milvus Vector Store in a basic Retrieval Augmented Generation (RAG) pipeline:


1. Connect a Document Parser to extract text from documents
2. Connect a Preprocessor to clean and prepare the text
3. Connect an Embeddings node to convert text to vector embeddings
4. Connect the Embeddings output to the Milvus Vector Store Documents input
5. Connect a question input to the Milvus Vector Store Questions input
6. Connect the Milvus Answers output to an LLM for generating responses


### Best Practices


- Use separate collections for different data domains
- Choose the appropriate index type based on your dataset size and query requirements
- For large datasets, IVF_FLAT or HNSW indices provide better performance
- Adjust search parameters based on your precision vs. speed requirements
- Use Strong consistency for critical applications, Eventually for higher throughput


### Troubleshooting


#### Connection Problems


- Connection refused - Verify host and port settings
- Authentication failure - Check API token validity
- Timeout errors - Check network connectivity and Milvus server status


#### Query Performance


- Slow queries - Optimize index type and search parameters
- Memory errors - Check Milvus server resources
- Poor search results - Ensure vector dimensions match between embeddings and collection


### Technical Reference


For detailed technical information, refer to:


- Milvus Official Documentation
- RocketRide Milvus node Source Code /../../../rocketride-nodes/nodes/milvus/milvus.py
- Milvus Configuration Schema
- This guide walks you through configuring Ngrok on your local machine
