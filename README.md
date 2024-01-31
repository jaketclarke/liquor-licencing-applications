# Liquor Licencing Applications

This project uses Python to drive Selenium to scrape data on liquor licences in Victoria.

## Grab the latest run

The latest data can be found here: https://jaketclarkepublic.blob.core.windows.net/liquor-licencing/applications/vic-applications-latest.csv

## Getting Started

* ensure you follow this guide <https://cloudbytes.dev/snippets/run-selenium-and-chrome-on-wsl2>
* if you don't you'll see an error like `selenium.common.exceptions.WebDriverException: Message: unknown error: cannot find Chrome binary`
* create a `.env` file with `touch .env`
* enter the following variables:
* *note the slash in front of the report path - necessary*

```text
WHERE_AM_I=dev
OUTPUT_DIRECTORY=output
OUTPUT_FILENAME=export
BLOB_CONTAINER_NAME=liquor-licencing
BLOB_CONNECTION_STRING=DefaultEndpointsProtocol=https;..........EndpointSuffix=core.windows.net
AZURE_SUBSCRIPTION_KEY=The primary key fro an azure maps account
```

In production, set the environment variable `WHERE_AM_I=Production`, this will turn the launching of the Chrome browser off.
