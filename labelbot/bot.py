# TODO remove this function.
def placeholder():
    """This is just a placeholder function for initial project setup."""
    return 42


def lambda_handler(event, context):
    # TODO implement
    # number = event['X-GitHub-Event']
    # data = json.loads(number)
    # env = os.environ['hej']

    return {"statusCode": 200, "body": json.dumps(placeholder())}
