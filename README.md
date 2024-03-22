# WhatsApp Conversational Bot with LLAMA Integration

## Overview

This project uses Selenium to interact with WhatsApp Web and integrates with a LLAMA API instance to provide summarized responses to conversations.

## Features

Automatically finds a specified contact on WhatsApp Web.
Extracts incoming and outgoing messages.
Constructs a conversation string.
Calls a LLAMA API endpoint to generate a summarized response to the conversation.
Sends the LLAMA-generated response back to the WhatsApp chat.

## Requirements
* Python 3.x (https://www.python.org/downloads/)
* Selenium WebDriver (https://www.selenium.dev/downloads/)
* Chrome browser and the corresponding ChromeDriver (https://chromedriver.chromium.org/)
* Requests library: `pip install requests`
* A running LLAMA API instance (See LLAMA setup instructions)

## Setup
* ChromeDriver: Place the ChromeDriver executable in a location within your system's PATH environment variable.
* LLAMA API: Start your LLAMA API server according to its setup instructions.

## Configuration:
* Open the whatsBot.py file.
* Update the CONTACT_NAME variable with the desired contact's name as it appears on WhatsApp Web.
* If necessary, adjust the LLAMA_API_URL to point to your LLAMA API server.

## Running the Script
* Execute: Run the whatsapp_bot.py script from your terminal: python whatsapp_bot.py
* It open up a whatsApp web in a browser. Login with QR code.
* Once you are finish with login, go back to CLI and hit "Enter"

## Notes
This script relies on the current structure of WhatsApp Web. If the interface changes, you might need to update XPaths in the code.
Consider adding more robust error handling for a production environment.

## Disclaimer
Use this bot responsibly and in compliance with WhatsApp's Terms of Service.

Let me know if you want to add more sections to the README, like a 'Contributing' section or more detailed setup instructions!
