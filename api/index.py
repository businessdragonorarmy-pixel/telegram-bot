def handler(request, context):
    return {
        "statusCode": 200,
        "headers": {"content-type": "text/plain"},
        "body": "Hello from Vercel!",
    }
