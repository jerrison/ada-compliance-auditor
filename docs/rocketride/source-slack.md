# Slack


The Slack node allows users to ingest their slack conversations and files shared within them, making messages and attachments available for processing in your RocketRide workflow.



## Key capabilities


- Ingest Conversations: Capture messages from public channels, private channels, and direct messages.
- File Ingestion: Collect files shared within Slack, including documents, images, and other attachments.
- Granular Channel Control: Include or exclude specific channels or conversations during setup.
- Pipeline Integration: Seamlessly feed Slack data into RocketRide pipelines for search, classification, and compliance workflows



## Configuration


- Authentication Type - Select whether to connect through a corporate-managed Slack bot or a personal Slack account.

Service - use a service account to access slack data through the RocketRide slack app bot
Personal - use a personal account to access slack data through a user token
- Steps to Connect:

Click "Connect to Slack"
When prompted by Slack, click “Allow” to grant RocketRide permission to access your workspace.
- Conversation Filtering (optional)

You can control which Slack conversations are ingested by including or excluding specific channels or DMs.
Include Conversations: Only the listed conversations will be ingested. By default, all conversations the user or bot has access to will be included
Exclude Conversations: The listed conversations will be skipped. By default, no conversations are excluded.
Finding IDs: To locate a channel or conversation ID, right-click on the channel or DM, select View details, and copy the ID at the bottom. For DMs, you must use the ID (since they do not have names). For channels, you can use either the channel name or the channel ID.



## Inputs and Outputs


### Input Channels


- none


### Output Channels


- Data: All Slack content (messages and files)



## Common Use Cases


- Compliance & eDiscovery: Ingest Slack conversations and files into RocketRide pipelines to meet regulatory or legal discovery requirements.
- Data Governance: Apply classification and retention policies to Slack messages and attachments to ensure proper handling of sensitive data.
- Analytics & Insights: Combine Slack data with other enterprise sources for sentiment analysis, productivity insights, or knowledge management.
- Selective Monitoring: Use conversation filtering to capture only specific channels or DMs that are relevant to ongoing projects or investigations.



## Frequently Asked Questions


### Service vs. Personal Token Access


- Service: Service accounts can only read messages from channels they have explicitly invited the RocketRide bot to. Service accounts cannot access direct messages (DMs)
- Personal: A user token allows access to all channels and DMs that the user is a member of. This includes direct messages and group conversations, but only those the user participates in.



## Additional Resources


- Slack API Documentation
