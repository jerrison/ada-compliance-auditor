# Microsoft Outlook


The Microsoft Outlook node connects to Outlook mailboxes using Azure enterprise credentials. It allows ingestion of data such as emails and folders by authenticating through Microsoft’s secure APIs. 


### Configuration Steps


 


- Authentication Type - Select the method of authentication.

“Enterprise” uses Azure Active Directory credentials.
- Tenant ID - Enter the Azure Active Directory Tenant ID.
- This value is unique to your organization and can be found in the Azure AD portal.
- Region - Select the appropriate Microsoft data center region for your account.

This defines where the SharePoint or OneDrive instance is hosted.
- Client ID - Enter the Client ID generated during your Azure application registration.

Note - Must match what was configured in Azure.
- Client Secret - Enter the corresponding Client Secret for the Azure application.

Note - Must match what was configured in Azure.


### Path Configuration


- Provide the Path to Your Data

Accepted Formats

[email_address]/[folder_name]/*


Click “Add Another Folder” to include additional paths.
- Provide the Path to Exclude

Accepted Format (same as Include Path)
Click “Add Another Folder” to exclude more paths.
