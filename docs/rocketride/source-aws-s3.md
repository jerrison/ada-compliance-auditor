# AWS S3


The AWS S3 node is a source node in the RocketRide. It allows users to securely connect to Amazon S3 buckets to import files and folders into their data pipelines.


This node requires AWS credentials and clearly defined include/exclude paths to specify which S3 objects to work with.


### Required Configuration


- AWS Credentials

Access key - A key that provides access to your AWS resources.

This is used to sign the requests you send to Amazon S3.


Secret key - The corresponding secret key to authorize access to AWS services.
Region - Select the AWS region where your S3 bucket is hosted.

Example - US East (N. Virginia)


### Data Path Configuration


- Include Paths - Specify which folders or buckets to include using the format

Accepted Formats

[bucket_name]/[folder_name]/*
[bucket_name]/*


Use the field labeled Include path* to define one or more include paths.
Click Add Another Folder to include multiple paths.
- Exclude Paths - Define folders or buckets to exclude using the same format

Accepted Formats (same as Include Paths)

[bucket_name]/[folder_name]/*
[bucket_name]/*


Click Add Another Folder to define additional exclusions.
