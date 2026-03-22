# Text Summarization: LLM


## What does it do?


The Text Summarization - LLM node automatically analyzes and condenses large volumes of unstructured text into concise summaries, key points, and named entities using advanced large language models (LLMs). This node allows you to control the summarization granularity and focus areas by specifying chunk sizes, summary lengths, key point limits, and entity extraction counts.


With this node, you can:


- Generate short, readable summaries of long documents
- Extract key points for quick reference
- Identify and list important entities (such as people, places, and organizations) mentioned in the text
- Streamline downstream workflows by providing structured, summarized content for indexing, search, or display
- Automate data ingestion and processing from virtually any text source



## Inputs and Outputs


### Inputs


- Text – Raw or structured text input to be summarized


### Outputs


- Documents – The full structured summary output, often in JSON or object format
- Text – A plain-text version of the generated summary



## Configuration Fields


| Field | Description | Example | Notes |
| --- | --- | --- | --- |
| Number of chunks to summarize after the document is split | Defines how many parts the document should be split into before summarization | 5 | Controls document segmentation |
| Number of words in each summary | Controls the length of the summary generated for each chunk | 100 | Set to 0 to disable summarization |
| Number of words in each key point | Sets the word limit for each extracted key point | 25 | Set to 0 to disable key point generation |
| Number of entities to extract from the document | Limits the number of named entities (people, locations, organizations) to extract | 10 | Set to 0 to disable entity extraction |



## How do I use it?


To use the Text Summarization - LLM node in your workflow:


1. Add the node to Your Pipeline

Drag the Text Summarization - LLM node into your workspace
Place it where you want to process and summarize text in your pipeline
2. Connect Input

Connect a source node to the Text input
This could be a parser, file reader, chat input, or any other text source
3. Configure Parameters

In the attributes editor, customize the summarization process
Fill in each configuration field depending on your desired summarization strategy
4. Connect Output

The node outputs summarized text, key points, and entities
Send these to downstream nodes for further processing, display, or storage
5. Save Configuration

Click SAVE to apply the configuration



## Configuration Example


| Field | Value |
| --- | --- |
| Chunks | 3 |
| Summary Words | 150 |
| Key Point Words | 20 |
| Entities to Extract | 5 |


Result: This configuration will break the input into 3 chunks, generate 150-word summaries, highlight up to 5 entities, and produce 20-word key points per chunk.



## Example Use Cases


- Summarize lengthy reports or articles for quick review
- Extract key points from meeting transcripts or research papers
- Identify important entities in legal documents or news stories
- Prepare content for search indexing or chatbot responses
- Process document uploads from web forms or external applications



## Summary Table of Parameters


| Parameter | Description | Effect/Usage |
| --- | --- | --- |
| Number of Chunks | Number of chunks to summarize after splitting the document | Controls how many summaries are generated |
| Number of Summary Words | Number of words in each summary (0 = disable summaries) | Controls summary length |
| Number of Key Point Words | Number of words in each key point (0 = disable key points) | Controls key point length |
| Number of Entities | Number of entities to extract (0 = disable entity extraction) | Controls how many entities are listed |



## Important Notes


- Set any numeric field to 0 to skip that type of output
- This node is commonly followed by storage, visualization, or export nodes depending on the pipeline goal
- The node uses advanced LLMs to ensure high-quality summarization and entity extraction



In summary:


The Text Summarization - LLM node brings the power of AI-driven summarization to your workflows, helping you distill and organize information from any text source with just a few clicks. It makes it easy to extract the most important information from documents, articles, or any lengthy text, enabling you to understand, search, and display key insights efficiently.
