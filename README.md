# Selenium Website Tester

This script is designed for testing website interactions, specifically for automated login workflows. It utilizes the Selenium framework to control web browsers, allowing you to specify a preferred web driver and perform testing on different websites. Will extend to include the capability to test other workflows than just login workflow.

## Requirements

- Python 3.x
- selenium==4.8.3
- selenium-recaptcha-solver==1.9.0
- webdriver-manager==4.0.1

## Usage

```bash
python selenium_tester.py --web-driver chrome --website <WEBSITE> --login-email <EMAIL/USERNAME> --login-password <PASSWORD> --recaptcha-enabled
```

### Arguments

- `--web-driver`: Specify your preferred web driver (default: firefox).
- `--website`: Input the target website URL (default: www.google.com).
- `--login-email`: Input your login email or username.
- `--login-password`: Input your login password.
- `--recaptcha-enabled`: Include this flag if the login involves ReCAPTCHA.

### Example

```bash
python script.py --web-driver chrome --website https://example.com --login-email user@example.com --login-password password --recaptcha-enabled
```


### 28th January 2024

## Current Status

- Custom Firefox and Chrome drivers are now working properly for my website's login workflow

## In Pipeline

- Capability to add options and arguments to custom Firefox and Chrome drivers