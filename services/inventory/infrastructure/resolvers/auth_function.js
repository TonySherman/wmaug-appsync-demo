import { util } from "@aws-appsync/utils";

export function request(ctx) {
    return {
        operation: "Invoke",
        payload: {
            secret:  ctx.args.admin_key,
        },
    };
}

export function response(ctx) {
    const { result, error } = ctx;
    if (error) {
        util.error(error.message, error.type, result);
    }

    if (!ctx.result.authorized) {
        util.unauthorized();
    }

    return {};
}

