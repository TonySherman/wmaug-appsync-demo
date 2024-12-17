# WMAUG December 2024 AWS AppSync Demo

## Project Structure

This is a demo monorepo that represents a minimal e-commerce platform that is broken into
several different microservices:

 - [Products](services/products/README.md)
 - [Inventory](services/inventory/README.md)
 - [Reviews](services/reviews/README.md)
 - [Merged API](services/merged_api/README.md)
 - [Frontend](services/frontend/README.md)

The goal is to show how these services can be accessed via a single AppSync GraphQL API.

## Setup Environment
Python Environment and Dependencies are managed with [uv](https://docs.astral.sh/uv/)

You also need to have AWS CDK installed to deploy `npm install -g aws-cdk`

1. Set up `uv` environment for Python

    - `uv venv`
    - `source .venv/bin/activate`
    - `uv sync` 


## Deploying

Since this repo is representative of various Microservices, each service is designed to be worked on
and deployed independently. The only prerequisite to deploying any individual service is to deploy
the merged_api stack first. 

Each service can be deployed right from the root of the repo by specifying the service:
`cdk deploy -a 'python -m services.merged_api.app' --profile <aws cli profile name>`


## Seed Databases 

This example depends on data being associated with a single SKU across the various service. There is 
a script that you can run to generate some dummy data to query. The script does connect to the RDS database 
via localhost, so you will need to use SSM port forwarding to allow for the local connection.


```bash
aws ssm start-session \
--document-name AWS-StartPortForwardingSessionToRemoteHost \
--parameters '{"host":["<cluster-endpoint-url>"], "portNumber":["5432"], "localPortNumber":["5432"]}' \
--target <ec2 instance id> \
--profile <aws cli profile name>
```

`AWS_PROFILE=<profile name> python -m 'scripts.seed_data'`
