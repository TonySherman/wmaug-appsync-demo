# Products Service

This service is responsible for maintaining all products and details pertaining to them 
such as sku, description, price, etc.

## Infrastructure

data store: DynamoDB table containing product names and description for skus

API: AppSync GraphQL API that allows retrieving all items via a scan or
     individual products by sku.
