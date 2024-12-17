import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  env: {
    API_ENDPOINT: process.env.API_ENDPOINT,
    AWS_REGION: process.env.AWS_REGION,
    API_KEY: process.env.API_KEY
  }
};

export default nextConfig;
