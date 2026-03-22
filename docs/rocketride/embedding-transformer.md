# Sentence Transformer


The Sentence Transformer node converts input text into vector representations using a sentence transformer model. These embeddings can be used in downstream tasks such as semantic search or question answering.


### Inputs


- Text - Text content to convert to embeddings
- Documents - Document objects containing text to embed
- Questions - Short form text and queries


### Outputs


- Vectors - Generated vector embeddings
- Documents - Original documents with embeddings attached
- Questions - Vector embeddings of the Questions Input


### Configuration


Model Settings


- Model - Transformer model to use

Default - "sentence-transformers/all-MiniLM-L6-v2"
Note - Various models available from Hugging Face

Use all-MiniLM models for efficient general-purpose embeddings
Use MPNet models for higher quality embeddings
Use multilingual models for cross-language applications
Use domain-specific models for specialized content
- Dimensions - Vector dimensions

Default - 384
Note - Model-dependent
- Batch Size - Number of texts to embed at once

Default - 32
Note - Affects memory usage and speed
- Normalize - Normalize vector lengths

Default - true
Note - Improves similarity calculations


#### Pooling Settings


- Pooling Strategy - Token pooling method

Default - "mean"
Options - mean, max, cls
- Attention Mask - Use attention mask for pooling

Default - true
Note - Ignores padding tokens
- Token Weighting - Apply token importance weighting

Default - false
Note - Emphasizes important tokens


#### Advanced Settings


- Cache - Cache embeddings for reuse

Default - true
Note - Improves performance for repeated texts
- Device - Processing device

Default - "auto"
Options - auto, cpu, cuda
- Precision - Computation precision

Default - "float32"
Options - float32, float16, bfloat16
- Max Length - Maximum sequence length

Default - 512
Note - Limits for very long texts


### Samples


#### Basic Text Embedding


This example shows how to configure the Transformer Embedding component for basic text embedding: { "model": "sentence-transformers/all-MiniLM-L6-v2", "dimensions": 384, "batchSize": 32, "normalize": true, "poolingStrategy": "mean", "attentionMask": true, "cache": true }


#### High-Performance Multilingual Embedding


For high-performance multilingual embedding with GPU acceleration: { "model": "sentence-transformers/paraphrase-multilingual-mpnet-base-v2", "dimensions": 768, "batchSize": 16, "normalize": true, "poolingStrategy": "mean", "attentionMask": true, "tokenWeighting": true, "cache": true, "device": "cuda", "precision": "float16", "maxLength": 384 }


### Best Practices


#### Text Preparation


- Preprocess text to remove noise and irrelevant content
- Consider chunking long texts for more granular embeddings
- Ensure consistent text formatting for comparable embeddings


#### Performance Optimization


- Adjust batch size based on available memory
- Use GPU acceleration when available
- Enable caching for repeated processing of the same texts
- Use lower precision (float16) for faster processing with minimal quality loss


### Troubleshooting


#### Processing Problems


- Out of memory errors - Reduce batch size or sequence length
- Slow processing - Enable GPU acceleration or use a smaller model
- Poor embedding quality - Try different models or text preprocessing


#### Compatibility Issues


- Model loading errors - Verify model availability and compatibility
- Device errors - Check CUDA installation for GPU acceleration
- Tokenization errors - Check for unsupported characters or formats


Technical Reference


For detailed technical information, refer to:


- Sentence Transformers Documentation
- Hugging Face Transformers
- Transformer Embedding Source Code ../../../nodes/embedding_transformer/transformer.py
