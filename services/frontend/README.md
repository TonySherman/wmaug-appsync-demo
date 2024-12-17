# Sample Frontend

This is a very simplified nextjs app to demonstrate making some API calls to the AppSync api(s). It has only
been run locally and there is no infrastructure to deploy this.

This could probably be deployed to cloudfront as a static build if the individual item pages were modified to
not use a dynamic route. (`/<sku>` changed to `</product?sku=<sku>`)

## Getting Started
You will need to create a `.env` or `.env.local` file with the following env vars:

```
API_ENDPOINT=https://<your-api-id>.appsync-api.us-east-1.amazonaws.com/graphql
AWS_REGION=us-east-1
API_KEY=<your-api-key>
```

If you deployed via cdk, these should all be in the cloudformation outputs.

First, run the development server:

```bash
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

