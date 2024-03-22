import datetime
import json
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# Configuration
CONTACT_NAME = "My Chat"
LLAMA_API_URL = "http://localhost:11434/api/generate"


def find_chat_and_click(driver, contact_name):
    """Finds a chat by name and clicks on it.
    Args:
        driver: The WebDriver instance.
        contact_name: The name of the contact to find.

    Raises:
        NoSuchElementException: If the chat is not found.
    """

    chat_elements = driver.find_elements(By.CLASS_NAME, value="Mk0Bp")
    for chat in chat_elements:
        if chat.text == contact_name:
            chat.click()
            return

    raise NoSuchElementException(f"Chat with name '{contact_name}' not found")


def get_messages(driver):
    """Extracts incoming and outgoing messages from the current chat.

    Args:
        driver: The WebDriver instance.

    Returns:
        tuple: Two lists, one for incoming messages and one for outgoing.
    """

    main = driver.find_elements(By.CLASS_NAME, value="n5hs2j7m")
    incoming_messages = []
    outgoing_messages = []

    for msg in main:
        incoming = msg.find_elements(By.CLASS_NAME, value="message-in")
        outgoing = msg.find_elements(By.CLASS_NAME, value="message-out")

        if incoming:
            incoming_messages.append(incoming[0].text)
        elif outgoing:
            outgoing_messages.append(outgoing[0].text)

    return incoming_messages, outgoing_messages


def get_timestamp(message):
    """Extracts the timestamp (HH:MM) from a message string."""
    return message.split()[-1]


def sort_key(message):
    """Returns a datetime object for sorting messages."""
    time_str = get_timestamp(message)
    return datetime.datetime.strptime(time_str, "%H:%M")


def call_llama_api(conversation):
    """Calls the Llama API and returns the TLDR response."""
    pre_prompt = "This is a my conversation "
    post_prompt = " what is the context of my conversation give me a short tlrd?"

    payload = json.dumps(
        {
            "model": "llama2",
            "prompt": f"{pre_prompt}{conversation}{post_prompt}",
            "stream": False,
        }
    )
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", LLAMA_API_URL, headers=headers, data=payload)
    return response.json()["response"]


def send_message(driver, message):
    """Sends a message in the current chat."""
    text_area = driver.find_element(
        By.XPATH,
        value="//*[@id='main']/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p",
    )
    text_area.send_keys(message)

    send_button = driver.find_element(
        By.XPATH,
        value="//*[@id='main']/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span",
    )
    send_button.click()


# Main program flow
if __name__ == "__main__":
    driver = webdriver.Chrome()
    try:
        driver.get("https://web.whatsapp.com/")
        driver.maximize_window()
        input("Press Enter after you have logged in to WhatsApp Web.")

        find_chat_and_click(driver, CONTACT_NAME)
        time.sleep(2)

        incoming_msgs, outgoing_msgs = get_messages(driver)
        all_messages = incoming_msgs + outgoing_msgs
        all_messages.sort(key=sort_key)

        conversation = ""
        for msg in all_messages:
            label = "incoming" if msg in incoming_msgs else "outgoing"
            conversation += f"{label}: {msg}\n"

        api_response = call_llama_api(conversation)
        send_message(driver, api_response)
    except Exception as e:
        print(f"An error occurred: {e}")
