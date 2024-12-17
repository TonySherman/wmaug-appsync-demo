import { ResourcesConfig } from "aws-amplify";

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

export default config;
