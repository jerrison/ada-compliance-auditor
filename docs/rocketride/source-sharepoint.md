# Microsoft SharePoint


The Microsoft SharePoint node enables access to SharePoint Online folders within an organization. It uses enterprise authentication via Azure and requires valid application credentials for access. 


### Configuration Steps


- Tenant ID - Enter the Azure Active Directory Tenant ID.

This value is unique to your organization and can be found in the Azure AD portal.
- Region - Select the appropriate Microsoft data center region for your account.

This defines where the SharePoint or OneDrive instance is hosted.
- Client ID - Enter the Client ID generated during your Azure application registration.

Note - Must match what was configured in Azure.
- Client Secret - Enter the corresponding Client Secret for the Azure application.

Note - Must match what was configured in Azure.


### Path Configuration


- Provide the Path to Your Data

Accepted Formats

[site_name]/folder/*
[site_name]/*


Click “Add Another Folder” to include additional paths.
- Provide the Path to Exclude

Accepted Format (same as Include Path)
Click “Add Another Folder” to exclude more paths.
