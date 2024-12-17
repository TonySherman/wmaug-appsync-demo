# Reviews Service

The reviews service maintains all review data related to products.

## Infrastructure

data store: Postgres Database that contains review information by various users and a star rating.

API: AppSync GraphQL API that allows retrieving all reviews for a given products SKU.

database management: A custom resource in CDK invokes a lambda that will create the inital database schema.
                     There is also an EC2 instance in the same VPC that allows you to use SSM port forwarding
                     to interact with the database locally. (This will be needed to run the seed script)
