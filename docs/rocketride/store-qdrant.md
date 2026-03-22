# Qdrant Vector Store


The Qdrant Vector Store node enables integration with a Qdrant vector database for storing and retrieving vector embeddings based on semantic similarity. It supports both Qdrant cloud servers and self-hosted deployments. 


## Key Features


- Semantic similarity search for efficient document retrieval
- Support for multiple deployment options (Cloud, Local, and Embedded)
- Customizable similarity metrics and retrieval thresholds
- Scalable for both development and production environments


 



## Configuration:


### Host Address


Cloud: your-instance-name.region.qdrant.io Local: localhost


### Port


Cloud Default: 443 Local Default: 6333 API Key: Required for Qdrant Cloud authentication Collection Name: Name of the vector database collection (e.g., "documents")


 



## Deployment Options


- Embedded: Uses an embedded Qdrant server within the application
- Local: Connects to a Qdrant server on your infrastructure

This guide walks you through configuring Ngrok on your local machine to expose Local Service as Mysql or Qdrant to RocketRide Cloud, which runs remotely.
- Cloud: Connects to a Qdrant cloud instance


 



## Inputs and outputs


### Input:


- Documents: Vector embeddings to be stored in the collection
- Questions: Query embeddings used to retrieve similar documents


### Output:


- Documents: Processed versions of the stored input documents
- Answers: The most relevant matches based on the input query
- Questions: Processed versions of the input queries


 



## Troubleshooting


- Connection refused: Verify your host and port settings
- Authentication failure: Check your API key validity
- Timeout errors: Verify network connectivity
- Slow queries: Consider trying a different similarity metric
- Memory errors: Adjust chunk and payload limits
- Poor search results: Ensure consistent embedding dimensions


 



## Common Use Cases:


### Semantic Document Search


- Find documents with similar meaning regardless of exact wording
- Implement knowledge bases and information retrieval systems
- Power RAG (Retrieval Augmented Generation) workflows


### Recommendation Systems


- Suggest similar products or content based on embeddings
- Create "more like this" functionality
- Personalize recommendations based on user preferences


### Anomaly Detection


- Identify outliers in vector space
- Detect unusual patterns or behavior
- Flag potential security issues or fraud


 



## Advanced Configuration:


| Setting | Description | Example |
| --- | --- | --- |
| Vector Size | Dimensionality of stored vectors | 768, 1024, 1536 |
| Distance Function | Metric used for similarity comparison | Cosine, Euclid, Dot |
| Indexing Algorithm | Method for efficient vector search | HNSW, IVF, Scalar |
| Payload Schema | Structure of metadata attached to vectors | JSON schema definition |


## Additional Resources:


Qdrant Tutorials and Guides Qdrant GitHub Repository
