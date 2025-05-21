📣 Instagram Report Bot (GUI Based)

Instagram Report Bot is a Python-based GUI tool that automates the process of reporting Instagram accounts using real credentials and optional proxy rotation. Built with customtkinter, undetected-chromedriver, and selenium-stealth, this tool is designed for educational and authorized use cases such as testing abuse reporting mechanisms or internal moderation automation.

✅ Features

🖥️ GUI Interface using customtkinter for easy interaction

🧑‍💻 Account Rotation from a list of real Instagram accounts

🌐 Proxy Support to avoid detection and rotate IPs

🧠 Smart Delays between actions to mimic human behavior

🕵️ Stealth Mode using undetected_chromedriver & selenium-stealth

📊 Live Logging and Progress Tracking in the interface

📁 Configurable Behavior through config.json

🧰 Requirements
Python 3.8+

Google Chrome (latest version)

ChromeDriver (compatible with your Chrome version)

Install dependencies:

pip install -r requirements.txt

▶️ Usage

Load accounts (username:password format) from a .txt file

Load proxies (optional, one proxy per line)

Enter a target username or URL

Choose a report reason (spam, harassment, impersonation, inappropriate)

Hit Start Reporting

The tool will then use each account (rotated) to submit a report.

⚠️ Legal Disclaimer

This tool is intended for educational and ethical use only.
Using this bot against Instagram accounts without authorization is illegal and against Instagram’s terms of service.
Always get explicit permission before testing this on any account or using it in any automated moderation workflow.



