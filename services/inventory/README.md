# Inventory Service

This service maintains the current inventory available for all products. It consists 
of a single dynamo table and an API with that table as a datasource. The API gets merged
into the single merged api.


## Infrastructure

Data Store: Simple DynamoDB table with count of available inventory by sku

API: AppSync GraphQL API with a Query to get the current count and a Mutation to update.
     The Mutation uses a pipeline resolver and adds an example of what an auth step might
     look like.
