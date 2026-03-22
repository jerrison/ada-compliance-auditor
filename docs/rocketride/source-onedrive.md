# Microsoft OneDrive


The Microsoft OneDrive node connects to OneDrive or SharePoint Online accounts using enterprise-level credentials. This allows users to access files stored in Microsoft cloud environments. Configuration requires Azure-based application credentials and region information. 


### Configuration Steps


- Authentication Type - Select the authentication type. The current option shown is “Enterprise”, which uses Azure AD credentials.
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

Accepted Format

[tenant_name].sharepoint.com/sites/[site_name]/Shared Documents/[folder_name]/


Click “Add Another Folder” to include additional paths.
- Provide the Path to Exclude

Accepted Format (same as Include Path)
Click “Add Another Folder” to exclude more paths.
