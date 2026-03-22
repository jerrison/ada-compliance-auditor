# Weaviate Vector Store


The Weaviate Vector Store node enables integration with a Weaviate vector database, either hosted on the cloud or deployed locally. This node allows storage and retrieval of vectorized documents for downstream LLM tasks. 


## Inputs


- Documents - Vectorized document embeddings to store
- Questions - Incoming queries to search similar vectors


## Outputs


- Documents - Retrieved documents matching the query
- Answers - Search results (most relevant document chunks)
- Questions - The original question passed along


## Configuration


### GUI


- Type of Weaviate host

Weaviate cloud server
Your own Weaviate server
- Host

Cloud - your-instance-name.weaviate.cloud
Local - typically localhost
- Port

Default - 8080
Required when “Your own Weaviate server” is selected
- gRPC Port (only for local setup)

Default - 50051
- API Key - Enter your Weaviate API key (if applicable for authentication)
- Retrieval Score - Define the threshold for similarity

Options - Related, Very Related
This determines what results are returned from the vector store.
- Collection - The name of the collection or index to read/write vectors

Example - rocketride
Must be lowercase with optional hyphens
- Example

Host: localhost
Port: 8080
gRPC Port: 50051
Retrieval Score: Related
Collection: rocketride


Weaviate Vector Store supports several deployment modes:


## Local Mode


This guide walks you through configuring Ngrok on your local machine


## Cloud Mode


Connects to a Weaviate cloud instance.


{ "url": "https://your-cluster-id.weaviate.cloud", "api_key": "your-api-key", "class_name": "Document" }


Embedded Mode


Uses an embedded Weaviate instance within RocketRide.


```
{  "embedded": true,  "persistence_path": "./weaviate-data",  "class_name": "Document"}
```


## Advanced Settings


- Batch Size - Number of objects to batch insert

Default - 100
Notes - Higher values improve write performance
- Vector Index Type - Type of vector index

Default - "hnsw"
Options - hnsw, flat
- Vector Distance - Distance metric for similarity

Default - "cosine"
Options - cosine, dot, l2-squared
- Auto Schema - Automatically generate schema

Default - true
Notes - Set to false for custom schemas
- Tenant - Multi-tenancy identifier

Default - null
Notes - For multi-tenant deployments


## Example Usage


### Basic RAG Pipeline


This example shows how to use Weaviate Vector Store in a basic Retrieval Augmented Generation (RAG) pipeline:


1. Connect a Document Parser to extract text from documents
2. Connect a Preprocessor to clean and prepare the text
3. Connect an Embeddings node to convert text to vector embeddings
4. Connect the Embeddings output to the Weaviate Vector Store Documents input
5. Connect a question input to the Weaviate Vector Store Questions input
6. Connect the Weaviate Answers output to an LLM for generating responses


## Best Practices


- Use separate classes for different data domains
- Define custom schemas for better control over property indexing
- Use batch imports for large datasets to improve performance
- Adjust HNSW index parameters based on your precision vs. speed requirements
- Use GraphQL filtering capabilities for complex queries
- When using a local server, make sure the Weaviate instance is running and accessible at the specified host and port.
- Use matching embedding dimensions and model types between your embedding node and Weaviate collection schema.


 


## Troubleshooting


### Connection Problems


- Connection refused - Verify host and port settings
- Authentication failure - Check API key validity
- Timeout errors - Check network connectivity and Weaviate server status


### Query Performance


- Slow queries - Optimize index parameters (ef, maxConnections)
- Memory errors - Check Weaviate server resources
- Poor search results - Ensure vector dimensions match between embeddings and schema


### Technical Reference


For detailed technical information, refer to:


- Weaviate Official Documentation
