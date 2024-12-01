# WMAUG December 2024 AWS AppSync Demo

This project contains example code and infrastructure that represents an e-commerce solution. The main objective is to 
highlight AWS AppSync GraphQL APIs and how they can be used to access several different AWS datasources. All individual
APIs are then merged into a single API that can provide access to all datasources from a single graphQL endpoint.

## Project Structure

This is a demo monorepo that represents a minimal e-commerce platform that is broken into
several different microservices:

 - Products
 - Orders
 - Inventory
 - Reviews

The goal is to show how these services can be accessed via a single AppSync GraphQL API.

## Setup Environment
Python Environment and Dependencies are managed with [uv](https://docs.astral.sh/uv/)

You also need to have AWS CDK installed to deploy `npm install -g aws-cdk`

1. Set up `uv` environment for Python

    - `uv venv`
    - `source .venv/bin/activate`
    - `uv sync` 


## Deploying

In Microservice fashion, each service will need to be deployed independently. They are designed that each service
can be deployed and updated in any order with one exception, the merged_api needs to be deployed first since every
other service creates graphQL APIs that are merged into the merged API.

Each service has an `app.py` file that you can point cdk at to deploy:
`cdk deploy -a 'python -m services.merged_api.app --all`

### Seed Data

