# Deployment instructions for AWS Lambda

## Prerequisites
* You will need a Github account
* You will need an AWS account.


## Creating the lambda function

1. Create a function on AWS Lambda and author from scratch. Under `choose or create an execution role`, choose `create a execution role from a policy template` with
`Amazon S3 read only permissions` and name your role. Set your runtime to `Python 3.7` and
choose a name for your function.
press `Create function`
2. Choose `upload a .zip file` for your `Code entry type`
3. Set your handler to `labelbot.bot.lambda_handler`
4. Add an API Gateway as a trigger. Create a new API and set it to Open.
Press add, and then save. This will give you  a webhook url to add to your github app.

## Create the github app
1. Under `Settings>Developer settings>Github Apps`, press the `New Github App` button.
2. Give your app a name and enter a homepage url, for example your fork of labelbot.
3. Under `Webhook url` enter your API gateway url.
4. Under `Webhook secret (optional)`, enter a secret token, as described in Githubs [documentation](https://developer.github.com/webhooks/securing/#setting-your-secret-token).
5. Under `Permissions`, add `read-only` access to `Repository contents`
and add `Read and write` access to `Issues`
6. Under `Subscribe to events`, subscribe to the `Label` event.
7. Under `Where can this GitHub App be installed?`, set `Only on this account`
8. Press the `Create Github App`
9. Generate a private key and save it to an S3 bucket that is not publicly accessible.

## Set enviroment variables to hold private data in your Lambda function.
1. `APP_ID` : Shall be set to the App ID of your github app.
2. `BUCKET_NAME`: The name of your S3 bucket.
3. `BUCKET_KEY`: the unique identifier of your key file stored in S3.
4. `SECRET_KEY`: Shall be the same value as your secret token, that was set to secure the webhook.

After all enviroment variables have been added, save the changes.

## Give your lambda function read access to your s3 bucket.
In `S3>:your bucket:>Permissions>Bucket Policy` give your lambda role the rights to read from your bucket.

## Creating and uploading a deployment package
To create a deployment package it is required to build in a linux
enviroment with python 3.7 and pip installed, as Lambda runs in a linux
enviroment.

Run the `package.sh` script from the repository root, which packages the
application iin a zip file, that can be uploaded to AWS to deploy the
application. It will create a file
called `labelbot.zip` which should be uploaded to your AWS lambda
function. Save after uploading the file.



## You have now created and deployed your own github app with AWS Lambda
You can now install it on your own account and use it to label issues by pressing the `Install App` button.