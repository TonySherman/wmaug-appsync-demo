import { Amplify, ResourcesConfig } from "aws-amplify";
import { generateClient } from "aws-amplify/api";

if (!process.env.API_ENDPOINT) {
  throw new Error('API_ENDPOINT environment variable is not set');
}

const config: ResourcesConfig =  {
    API: {
        GraphQL: {
          endpoint: process.env.API_ENDPOINT,
          region: process.env.AWS_REGION || 'us-east-1',
          defaultAuthMode: 'apiKey',
          apiKey: process.env.API_KEY
        }
    }
};

Amplify.configure(config);

const appsyncClient = generateClient();

export default appsyncClient;


