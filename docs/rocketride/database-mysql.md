# MySQL


## What does it do?


The MySQL Database node enables seamless interaction with MySQL databases for both data querying and insertion operations. It uses AI-powered natural language processing to convert questions into SQL queries, while providing robust safety features to prevent unauthorized database modifications. The node supports flexible output formats and efficient batch operations, making it ideal for database exploration, data analysis, and structured data storage.


## How do I use it?


To use the MySQL Database node in your workflow:


### Add the MySQL Database node


- Insert the node into your pipeline where you want to interact with MySQL databases
- Connect an LLM component to the "llm" invoke connection for query generation


### Connect Input


- Connect the input lanes (questions, answers, or table data) to your data sources
- Questions lane accepts natural language queries
- Answers lane accepts JSON data for insertion
- Table lane accepts structured table data


### Configure Parameters


- Set MySQL connection details (host, user, password, database, table)
- Adjust connection settings as needed (see tables below)


### Connect Output


- The node outputs transcribed text, formatted tables, or structured answers for further processing


## Configuration Parameters


Customize the database connection with the following parameters:


| Parameter | Description | Effect/Usage |
| --- | --- | --- |
| MySQL Host | Host name or IP address of the MySQL server | Controls which database server to connect to; use localhost for local databases |
| User | Username for MySQL authentication | Specifies the database user account for connection |
| Password | Password for MySQL authentication (securely stored) | Provides authentication credentials; encrypted in storage |
| Database Name | Name of the target database (2-32 characters) | Specifies which database to connect to and operate on |
| Table Name | Name of the target table for data operations | Defines the specific table for queries and data insertion |


## Input Types


The node accepts three types of inputs for different use cases:


### Questions Input


Purpose: Generate and execute SQL queries from natural language


Format: Plain text questions about your data


Example: "Show me all employees with salary greater than $50,000"


### Answers Input


Purpose: Insert structured data into MySQL tables


Format: JSON objects or arrays of objects


Example:


```
[  {"name": "John Doe", "email": "john@example.com", "department": "Engineering"},  {"name": "Jane Smith", "email": "jane@example.com", "department": "Marketing"}]
```


### Table Data Input


Purpose: Insert tabular data directly into MySQL


Format: Markdown tables or structured table data


Example: CSV-like data or markdown formatted tables


## Output Types


The node produces three types of outputs for different use cases:


### Text Output


- Format: Plain text representation of results
- Use Case: Simple data display or logging
- Example: "Query returned 15 records"


### Table Output


- Format: Markdown-formatted tables
- Use Case: Structured data display


Example:


```
| id | name | email | department ||----|------|-------|------------|| 1 | John Doe | john@example.com | Engineering || 2 | Jane Smith | jane@example.com | Marketing |
```


### Answers Output


- Format: Structured answer objects
- Use Case: Integration with other AI components
- Example: Answer objects containing formatted results


## Safety Features


The node includes comprehensive safety checks to prevent unauthorized database modifications:


### Blocked Operations


- DELETE statements
- INSERT statements (when in query mode)
- UPDATE statements
- DROP TABLE/DATABASE
- ALTER TABLE
- TRUNCATE TABLE
- CREATE TABLE/DATABASE
- GRANT/REVOKE permissions
- EXEC/EXECUTE commands
- LOAD DATA operations


### Allowed Operations


- SELECT queries (read-only)
- Safe data insertion (when configured for insertion)


## Example Use Cases


- Query customer data for analysis and reporting
- Insert processed data from other pipeline components
- Generate reports from database tables using natural language
- Create searchable archives of structured data
- Process and store results from AI analysis
- Extract specific information from large datasets
- Prepare data for machine learning workflows
- Generate real-time analytics from database queries


## Best Practices


Model Selection: Use smaller models for quick drafts, larger models for final transcripts


Audio Quality: Higher quality audio produces better transcription results


Chunking: Adjust minimum/maximum seconds based on your content type (shorter for conversational, longer for lectures)


VAD Tuning: Start with balanced VAD and adjust based on your audio environment


### For Data Querying


- Be specific with your questions
- Use natural language instead of SQL syntax
- The node automatically limits to 250 records unless specified otherwise
- Ensure your questions reference actual table and column names


### For Data Insertion


- Match your data columns to your table schema
- Use consistent data types for your table structure
- The node handles batch insertion efficiently
- Validate your data before insertion


### For Configuration


- Use strong passwords for database security
- Test connectivity before processing large datasets
- Use connection pooling for optimal performance
- Always backup data before bulk operations


## Troubleshooting


### Connection Errors


- Verify host, username, and password
- Check network connectivity
- Ensure MySQL server is running
- Verify database exists


### Query Errors


- Check if table names exist
- Verify column names in your questions
- Ensure you're not trying to modify data in query mode


### Insertion Errors


- Verify table schema matches your data
- Check data types compatibility
- Ensure required columns are provided


### Performance Issues


- Use connection pooling
- Batch large datasets
- Monitor database performance
- Consider indexing for large tables


## Dependencies


The MySQL node requires:


- pymysql==1.1.1 - MySQL Python driver
- cryptography==42.0.2 - Encryption support
- SQLAlchemy==2.0.38 - Database abstraction layer


## Integration Notes


- LLM Requirement: An LLM component must be connected for query generation
- Database Compatibility: Works with MySQL 5.7+ and MariaDB 10.2+
- Character Encoding: Supports UTF-8 encoding
- Timezone: Respects database timezone settings


## Security Considerations


- All passwords are encrypted in storage
- SQL injection protection through query validation
- Read-only mode prevents accidental data modification
- Connection credentials are never logged
- Automatic session management and cleanup


## Performance Tips


- Use connection pooling for high-volume operations
- Batch insert large datasets
- Index frequently queried columns
- Monitor query performance
- Use appropriate data types for your schema


In summary:


The MySQL Database node provides flexible, secure database interaction for querying and data insertion operations, with AI-powered natural language query generation, comprehensive safety features, and multiple output formats to fit a wide range of database management and analysis needs.
