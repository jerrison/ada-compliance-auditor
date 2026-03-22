# Import/Export Pipelines


The pipeline import/export functionality allows you to save your pipeline configurations as JSON files and share them across different environments or restore them later. This enables you to backup your workflows, transfer configurations between systems, and reuse successful pipeline designs. The system preserves all component configurations, connections, and settings while allowing for environment-specific adjustments during import.



# Exporting a Pipeline


### 1. Access Export Function


- In the pipeline builder interface, look for the export option
- This is typically found in the pipeline menu or settings
- Select "Export Pipeline" or similar option


### 2. Download Configuration


- The system will generate a JSON file containing your pipeline
- The file will be automatically downloaded to your computer
- The filename typically includes the pipeline name and timestamp


### 3. Save the File


- Store the JSON file in a safe location
- You can rename it for easier identification
- Keep backups of important pipeline configurations


 



# Importing a Pipeline


### 1. Access Import Function


- In the pipeline builder interface, look for the import option
- This is typically found in the pipeline menu or settings
- Select "Import Pipeline" or similar option


### 2. Select the File


- Choose the JSON file you want to import
- The system will validate the file format
- Confirm the import action


### 3. Review and Configure


- The imported pipeline will appear in your builder
- Review all components and connections
- Reconfigure any environment-specific settings (see section below)


 



# Reconfiguration


When importing a pipeline, several components may require reconfiguration due to environment differences:


### API Keys and Credentials


| COMPONENT | WHAT TO CHECK | WHY IT NEEDS RECONFIGURATION |
| --- | --- | --- |
| LLM nodes (OpenAI, Anthropic, etc.) | API keys and authentication | API keys are environment-specific and not exported for security |
| Database nodes (MySQL, PostgreSQL) | Connection strings and credentials | Database access varies between environments |
| Cloud Services (AWS, Azure, GCP) | Access keys and service accounts | Cloud credentials are environment-specific |
| External APIs | API keys and endpoints | External service access may differ |


### Network and Host Settings


| COMPONENT | WHAT TO CHECK | WHY IT NEEDS RECONFIGURATION |
| --- | --- | --- |
| Webhook nodes | Host addresses and ports | Network configuration varies between environments |
| Chat/Dropper Interfaces | Server URLs and ports | Local vs. remote deployment affects URLs |
| Database Connections | Host names and ports | Database locations differ between environments |
| Vector Stores (Qdrant, Chroma) | Host addresses and ports | Local vs. cloud deployment affects connections |


### File Paths and Storage


| COMPONENT | WHAT TO CHECK | WHY IT NEEDS RECONFIGURATION |
| --- | --- | --- |
| File System nodes | File paths and directories | File system structure varies between environments |
| Local Storage nodes | Storage paths | Local file system paths are environment-specific |
| Output nodes | Destination paths | Output locations may differ between systems |


### Model and Service Configurations


| COMPONENT | WHAT TO CHECK | WHY IT NEEDS RECONFIGURATION |
| --- | --- | --- |
| Embedding Models | Model names and paths | Available models may differ between environments |
| LLM Models | Model selections and parameters | Model availability varies between deployments |
| Preprocessor Settings | Model configurations | Local vs. cloud model availability |


 



# Step-by-Step Reconfiguration Process


### 1. Review Imported Pipeline


- Check that all components imported correctly
- Verify connections between components
- Note any missing or error-indicated components


### 2. Configure Authentication


- LLM nodes: Update API keys for your environment
- Database nodes: Set correct connection strings
- Cloud Services: Configure appropriate credentials
- External APIs: Update API keys and endpoints


### 3. Update Network Settings


- Webhook URLs: Change to your environment's URLs
- Server Addresses: Update host names and ports
- Database Hosts: Set correct database locations
- Vector Store Connections: Configure for your deployment


### 4. Adjust File Paths


- Input Sources: Update file paths for your system
- Output Destinations: Set appropriate output locations
- Model Paths: Configure for your model installations


### 5. Test the Pipeline


- Run a small test to verify all connections work
- Check that all components can access their required resources
- Verify that outputs are generated correctly


 



# Common Reconfiguration Scenarios


#### Local to Cloud Migration


- Update all local file paths to cloud storage paths
- Change localhost URLs to cloud service URLs
- Configure cloud-specific authentication
- Update database connections to cloud databases


#### Development to Production


- Replace development API keys with production keys
- Update URLs from development to production domains
- Configure production database connections
- Set appropriate security and access controls


#### Cross-Environment Sharing


- Update environment-specific credentials
- Adjust network configurations for target environment
- Modify file paths for new file system structure
- Configure appropriate resource limits


 



# Best Practices


### Before Exporting


- Clean Configuration: Remove any temporary or test configurations
- Document Dependencies: Note any external services or resources required
- Test Pipeline: Ensure the pipeline works correctly before exporting
- Version Control: Consider using version control for pipeline configurations


### During Import


- Review Carefully: Check all components and connections
- Test Incrementally: Test each component individually if possible
- Document Changes: Keep notes of what was reconfigured
- Backup Original: Keep a copy of the original imported file


### After Import


- Validate Configuration: Ensure all settings are correct for your environment
- Test End-to-End: Run a complete pipeline test
- Monitor Performance: Watch for any performance issues
- Update Documentation: Update any relevant documentation


 



# Troubleshooting Import Issues


### Common Problems


- Missing Components: Some components may not be available in the target environment
- Version Mismatches: Different versions of nodes may cause compatibility issues
- Configuration Errors: Invalid configurations may prevent proper import
- Resource Unavailable: Required resources may not exist in the target environment


### Solutions


- Check Component Availability: Verify all nodes are installed in the target environment
- Update Versions: Ensure node versions are compatible
- Validate Configuration: Check that all settings are valid
- Create Missing Resources: Set up any required databases, storage, or services


 



# In summary:


Pipeline import/export functionality enables you to share and reuse pipeline configurations across different environments. While the basic structure and connections are preserved, you'll need to reconfigure environment-specific settings like API keys, network addresses, file paths, and credentials to ensure the pipeline works correctly in the new environment.
