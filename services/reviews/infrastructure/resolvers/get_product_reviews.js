import { util } from '@aws-appsync/utils';
import { select, createPgStatement, toJsonObject } from '@aws-appsync/utils/rds';
/**
 * Lists items in the table. Lists up to the provided `limit` and starts from the provided `nextToken` (optional).
 * @param {import('@aws-appsync/utils').Context} ctx the context
 * @returns {*} the request
 */
export function request(ctx) {
    const filter = {sku: {eq: ctx.args.sku}};
    const statement = select({
        table: 'public.product_reviews',
        columns: '*',
        where: filter,
    });
    return createPgStatement(statement);
}

/**
 * Returns the result or throws an error if the operation failed.
 * @param {import('@aws-appsync/utils').Context} ctx the context
 * @returns {*} the result
 */
export function response(ctx) {
    const {
        error,
        result,
    } = ctx;
    if (error) {
        return util.appendError(error.message, error.type, result);
    }
    const items = toJsonObject(result)[0];
    return items;
}
