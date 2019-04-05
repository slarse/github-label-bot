import json
from jwcrypto import jwk
import python_jwt

# TODO remove this function.
def placeholder():
    """This is just a placeholder function for initial project setup."""
    return f"{jwk.__file__}\n{python_jwt.__file__}"


def lambda_handler(event, context):
    # TODO implement
    # number = event['X-GitHub-Event']
    # data = json.loads(number)
    # env = os.environ['hej']

    return {"statusCode": 200, "body": json.dumps(placeholder())}


if __name__ == "__main__":
    print(placeholder())
