import * as ddb from '@aws-appsync/utils/dynamodb';

export function request(ctx) {
	const { limit = 10, nextToken } = ctx.args;
	return ddb.scan({ limit, nextToken });
}

export function response(ctx) {
    return {
	items: ctx.result.items,
	nextToken: ctx.result.nextToken,
    };
}
