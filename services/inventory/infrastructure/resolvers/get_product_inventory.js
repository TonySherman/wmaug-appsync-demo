import * as ddb from '@aws-appsync/utils/dynamodb'

export function request(ctx) {
    return ddb.get({ key: { PK: ctx.args.sku } });}

export function response(ctx) {
    return ctx.result;
}
