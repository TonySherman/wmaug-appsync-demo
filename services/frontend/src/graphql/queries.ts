/* tslint:disable */
/* eslint-disable */
// this is an auto generated file. This will be overwritten

import * as APITypes from "../types/graphql";
type GeneratedQuery<InputType, OutputType> = string & {
  __generatedQueryInput: InputType;
  __generatedQueryOutput: OutputType;
};

export const Product = /* GraphQL */ `query Product($sku: String) {
  Product(sku: $sku) {
    sku
    name
    description
    __typename
  }
}
` as GeneratedQuery<APITypes.ProductQueryVariables, APITypes.ProductQuery>;
export const Products = /* GraphQL */ `query Products($limit: Int, $nextToken: String) {
  Products(limit: $limit, nextToken: $nextToken) {
    items {
      sku
      name
      description
      __typename
    }
    nextToken
    __typename
  }
}
` as GeneratedQuery<APITypes.ProductsQueryVariables, APITypes.ProductsQuery>;
export const getInventory = /* GraphQL */ `query GetInventory($sku: String) {
  getInventory(sku: $sku) {
    sku
    available_count
    __typename
  }
}
` as GeneratedQuery<
  APITypes.GetInventoryQueryVariables,
  APITypes.GetInventoryQuery
>;
