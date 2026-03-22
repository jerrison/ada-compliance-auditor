# Azure Blob


The Azure Blob node is a source node in the RocketRide. It allows users to connect to their Azure Blob Storage and ingest files into a pipeline. The node requires Azure credentials and folder paths to include or exclude during the data import process.


### Required Configuration


- Azure Account Credentials

Account name - The unique namespace in your Azure storage account. This is found in the Azure Portal.
Key - The account access key used to authenticate with Azure Blob Storage. This is found in the Azure Portal.
Endpoint suffix - The suffix of the endpoint domain.

Common example - core.windows.net


### Data Path Configuration


- Include Path

Accepted Format

path/to/your/blobs/*


Add one or more folders using the “Include path” input and the “Add Another Folder” button.
- Exclude Path

Accepted Format (same as Include Path)

path/to/your/blobs/*


You can add multiple exclusions by clicking “Add Another Folder.”
