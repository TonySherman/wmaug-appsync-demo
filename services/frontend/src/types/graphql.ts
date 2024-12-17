/* tslint:disable */
/* eslint-disable */
//  This file was automatically generated and should not be edited.

export type ProductCount = {
  __typename: "ProductCount",
  sku: string,
  available_count?: number | null,
};

export type Product = {
  __typename: "Product",
  sku?: string | null,
  name?: string | null,
  description?: string | null,
};

export type ProductList = {
  __typename: "ProductList",
  items?:  Array<Product | null > | null,
  nextToken?: string | null,
};

export type UpdateInventoryMutationVariables = {
  sku: string,
  count: number,
  admin_key: string,
};

export type UpdateInventoryMutation = {
  updateInventory?:  {
    __typename: "ProductCount",
    sku: string,
    available_count?: number | null,
  } | null,
};

export type ProductQueryVariables = {
  sku?: string | null,
};

export type ProductQuery = {
  Product?:  {
    __typename: "Product",
    sku?: string | null,
    name?: string | null,
    description?: string | null,
  } | null,
};

export type ProductsQueryVariables = {
  limit?: number | null,
  nextToken?: string | null,
};

export type ProductsQuery = {
  Products?:  {
    __typename: "ProductList",
    items?:  Array< {
      __typename: "Product",
      sku?: string | null,
      name?: string | null,
      description?: string | null,
    } | null > | null,
    nextToken?: string | null,
  } | null,
};

export type GetInventoryQueryVariables = {
  sku?: string | null,
};

export type GetInventoryQuery = {
  getInventory?:  {
    __typename: "ProductCount",
    sku: string,
    available_count?: number | null,
  } | null,
};
