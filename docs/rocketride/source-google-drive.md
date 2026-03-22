# Google Drive


The Google Drive node allows users to ingest files from Google Drive within a Google Workspace environment.


Configuration requires domain-level access and authentication via a service account. 


### Configuration Steps


- Authentication Type - Defines a corporate managed or personal GMail Account

Service - use a service account to access Corporate Gmail

Customer ID - Enter the Google Workspace Customer ID assigned by Google.

This ID identifies the domain you wish to access.


Administrator E-mail - Provide the email address of a Google Workspace administrator.

This email must belong to a user with admin rights in the domain.


Service Account Key File

Upload the JSON file for your Google Workspace service account.
This file contains the necessary credentials to authenticate API requests.




User - uses a "secret file" to access person Gmail

Google products will need a "Client Secret File".
Look at the following documentation for help creating the file: Google Account Setup


### Path Configuration


- Path to your data - This defines which user’s Gmail data and folder to ingest.

Accepted Format

[user_id]/[folder]/*


You can click “Add Another Folder” to define multiple include paths.
- Path to Exclude

Accepted Format (same as Path to your data)
Click “Add Another Folder” to exclude more paths.


### Example Video


- https://www.youtube.com/watch?v=KN8O8FM-pVU
- https://www.youtube.com/watch?v=bgx9ZEpBHJc
