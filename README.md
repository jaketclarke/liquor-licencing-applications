# Getting Started

* ensure you follow this guide <https://cloudbytes.dev/snippets/run-selenium-and-chrome-on-wsl2>
* if you don't you'll see an error like `selenium.common.exceptions.WebDriverException: Message: unknown error: cannot find Chrome binary`
* create a `.env` file with `touch .env`
* enter the following variables:
* *note the slash in front of the report path - necessary*

```text
WHERE_AM_I=dev
OUTPUT_DIRECTORY=output
```

In production, set the environment variable `WHERE_AM_I=Production`, this will turn the launching of the Chrome browser off.
