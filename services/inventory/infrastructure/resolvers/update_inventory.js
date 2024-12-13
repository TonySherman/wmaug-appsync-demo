import { update, operations } from '@aws-appsync/utils/dynamodb';

export function request(ctx) {
	const updateObj = {
		available_count: operations.increment(ctx.args.count),
	};

	return update({ key: { PK: ctx.args.sku }, update: updateObj });
}

export function response(ctx) {
    return ctx.result;
}
