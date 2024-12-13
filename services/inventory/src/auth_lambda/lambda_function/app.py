def lambda_handler(event, context):
    key = event.get("secret")

    # simplified example of auth
    if key == "secretkey":
        return {"authorized": True}


    return {"authorized": False}
