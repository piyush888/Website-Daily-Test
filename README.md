# Selenium Website Tester

This script is designed for testing website interactions, specifically for automated login workflows. It utilizes the Selenium framework to control web browsers, allowing you to specify a preferred web driver and perform testing on different websites.

## Requirements

- Python 3.x
- Selenium library

## Usage

### Arguments

- `--web-driver`: Specify your preferred web driver (default: firefox).
- `--website`: Input the target website URL (default: www.google.com).
- `--login-email`: Input your login email or username.
- `--login-password`: Input your login password.
- `--recaptcha-enabled`: Include this flag if the login involves ReCAPTCHA.

### Example

```bash
python script.py --web-driver chrome --website https://example.com --login-email user@example.com --login-password password --recaptcha-enabled
