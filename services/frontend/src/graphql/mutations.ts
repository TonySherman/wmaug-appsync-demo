/* tslint:disable */
/* eslint-disable */
// this is an auto generated file. This will be overwritten

import * as APITypes from "../types/graphql";
type GeneratedMutation<InputType, OutputType> = string & {
  __generatedMutationInput: InputType;
  __generatedMutationOutput: OutputType;
};

export const updateInventory = /* GraphQL */ `mutation UpdateInventory($sku: String!, $count: Int!, $admin_key: String!) {
  updateInventory(sku: $sku, count: $count, admin_key: $admin_key) {
    sku
    available_count
    __typename
  }
}
` as GeneratedMutation<
  APITypes.UpdateInventoryMutationVariables,
  APITypes.UpdateInventoryMutation
>;
