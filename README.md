# fitbit API

Repo about how to use fitbit API.

## Big picture to use fitbit API

- Register application in fitbit developer website.
- A user allows the application to access their data.
- Get access token.
- Make HTTP requests to fitbit API endpoints with the access token.

## What you need to register application in fitbit.

- Application website URL
- Organization website URL
- Terms of service URL
- Privacy policy URL
- Redirect URL

## Register application in fitbit

- https://dev.fitbit.com/apps/new

## Get access token in tutorial

- Go to the application you registered in `https://dev.fitbit.com/apps`.
- At the bottom, click `OAuth 2.0 tutorial page`.
- Flow type: Implicit grant flow.
- Click the link in "We've generated the authorization URL for you, ..."
- Check the data you need and allow.
- It redirects you to the redirect URL you used in registration
- Get the access token from the redirected URL.

## Test making HTTP requests to fitbit with the access token

- Go to `https://www.postman.com/`.
- Make GET request with
  - URL: `https://api.fitbit.com/1/user/-/profile.json`
  - Authorization type: `OAuth 2.0`, Add authorization data to `Request Headers`, paste the access token with the header
    prefix: `Bearer`.

## Python sample to make HTTP requests to fitbit API

- [GET request to get the user profile data](https://github.com/yukikitayama/fitbit/blob/main/demo_make_request.py)