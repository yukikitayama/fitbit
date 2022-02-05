# fitbit API

Repo about how to use fitbit API.

## Reminder

- Heart rate logging sometimes stops, and the data is gone. You can early notice it by finding heart rate is not logged 
  wearing fitbit device, running or weightlifting. It needs manual fix. **If heart rate is not logged, sleep is not logged**, while 
  other GPS, calorie, and step calculations are working.
  - Restart fitbit device.
  - Follow [the fitbit instructions](https://help.fitbit.com/articles/en_US/Help_article/1565.htm#ImpactsAccuracy) to 
    reset heart rate recording and wear the device as fitbit instructs.
  - Heart rate logging sometimes stops when you take off fitbit device and wear again.
- Fitbit scale, Aria Air, needs to be placed on a hard floor to get the correct data. 
  - For example, if you place the scale on a carpet floor, it gives you a wrong number like a half of your weight.
- Choose **Personal** for OAuth 2.0 Application Type in registering app, because it allows us to get the intraday data, 
  which is a finer granularity of data such as heart rate time series in 1 second and 1 minute level.
- Can query data both in UTC and local time, maybe important if you are in US.
- Water can be automatically logged if you use `Hidrate Spark` to log drinking water and connect fitbit from hidrate
  spark app.
  - When refill water, it needs to be placed on a flat place for a few seconds to make the bottle recognize the water
    is refilled, otherwise water isn't logged correctly.

## Big picture to use fitbit API

- Register application in fitbit developer website.
  - https://dev.fitbit.com/apps/new
- Fitbit users allow an application to access their data.
- The application gets access token.
- The application makes HTTP requests to fitbit API endpoints with the access token to get data.
- The application refreshes the access token when it's expired with a refresh token to keep using fitbit API.

## OAuth 2

- By default, access token expires in 28,800 seconds, or 8 hours.
- Refresh token API endpoint
  - [Refresh Token API](https://dev.fitbit.com/build/reference/web-api/authorization/refresh-token/)
- To refresh the expired access token, it needs
  - Client ID
    - Supplied when registered your application in dev.fitbit.com
  - Client secret
    - Supplied when registered your application in dev.fitbit.com
  - Refresh token
    - Supplied when you obtained the access token for the first time, or when you refreshed an access token.
  - Basic token
    - Created from client ID and client secret
    - [Authorization](https://dev.fitbit.com/build/reference/web-api/developer-guide/authorization/)

```python
import base64
client_id = 'ABC123'
client_secret = 'DEF456'
basic_token = base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()
# QUJDMTIzOkRFRjQ1Ng==
```

## Enable fitbit API

### What you need to register application in fitbit.

- Application website URL
- Organization website URL
- Terms of service URL
- Privacy policy URL
- Redirect URL

### Register application in fitbit

- https://dev.fitbit.com/apps/new

### Get access token in tutorial

- Go to the application you registered in `https://dev.fitbit.com/apps`.
- At the bottom, click `OAuth 2.0 tutorial page`.
- Flow type: Implicit grant flow.
- Click the link in "We've generated the authorization URL for you, ..."
- Check the data you need and allow.
- It redirects you to the redirect URL you used in registration
- Get the access token from the redirected URL.

### Test making HTTP requests to fitbit with the access token

- Go to `https://www.postman.com/`.
- Make GET request with
  - URL: `https://api.fitbit.com/1/user/-/profile.json`
  - Authorization type: `OAuth 2.0`, Add authorization data to `Request Headers`, paste the access token with the header
    prefix: `Bearer`.
- Test with Python requests package
  - [GET request to get the user profile data](https://github.com/yukikitayama/fitbit/blob/main/demo_make_request.py)

### Access Token

- `expires_in` is in seconds the lifetime of the access token.
- By default, it's 604,800 seconds, or 10,080 minutes, or 7 days, because `10,080 minutes / (60 minutes * 24 hours)`

### Authorization Code Flow

- OAuth 2.0 tutorial page generates the authorization URL for us, and click it.
- It gives us a code in redirect URL, copy and paste it to the tutorial
- It again generates a command for curl POST, and do it
- Paste the response to the tutorial, and it gives us the example requests to fitbit API.

## Sleep

- You can get sleep summary data and the time series of sleep data with the level and its duration.
- The minimum interval is 30 seconds.

### Demo

- [Make request to get sleep log](https://github.com/yukikitayama/fitbit/blob/main/get_sleep_log_by_date.py)
- [Extract data from sleep log response JSON](https://github.com/yukikitayama/fitbit/blob/main/extract_data_from_sleep_log.py)

![Sleep level time series](https://github.com/yukikitayama/fitbit/blob/main/image/sleep_level_time_series_2021-11-28.png)

### API documentation

- https://dev.fitbit.com/build/reference/web-api/sleep/get-sleep-log-by-date/

## Heart Rate

- Intraday minutely data of heart rate beats per minute is available by choosing application type Personal when 
  registering app.
- There are two APIs; Heart Rate Time Series, and Heart Rate Intraday. But I think both APIs returns the same data. 
  Heart Rate Time Series contains intraday granular data.

### Demo

- [Get Heart Rate Time Series and save it to JSON](https://github.com/yukikitayama/fitbit/blob/main/get_heart_rate_time_series_by_date.py)
- [Get Heart Rate Intraday and save it to JSON](https://github.com/yukikitayama/fitbit/blob/main/get_heart_rate_intraday_by_date.py)
- [Extract intraday heart rate data and visualize it](https://github.com/yukikitayama/fitbit/blob/main/visualize_intraday_heart_rate.py)

![Intraday heart rate](https://github.com/yukikitayama/fitbit/blob/main/image/heart_rate_intraday_2021-11-27.png)

### API documentation

- https://dev.fitbit.com/build/reference/web-api/heartrate-timeseries/get-heartrate-timeseries-by-date/
- https://dev.fitbit.com/build/reference/web-api/intraday/get-heartrate-intraday-by-date/

## Activity

- The following time series data is available.
  - Steps taken per minute
  - Calories burned per minute
  - Distance moved per minute

![Intraday steps](https://github.com/yukikitayama/fitbit/blob/main/image/steps_time_series_2021-12-04.png)

![Intraday calories burned](https://github.com/yukikitayama/fitbit/blob/main/image/calories_time_series_2021-12-04.png)

## Body

- xxx

## Paper

- [Water, Hydration and Health](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2908954/)