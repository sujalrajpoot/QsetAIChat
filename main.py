import requests
import json
import re
from typing import Optional, Dict, Any, Iterator
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

# Define custom exceptions
class AIChatError(Exception):
    """Base class for AI chat-related exceptions."""
    pass

class APIRequestError(AIChatError):
    """Exception raised for API request errors."""
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code

class InvalidResponseError(AIChatError):
    """Exception raised for invalid or unexpected API responses."""
    pass

# Define an enum for roles
class Role(Enum):
    SYSTEM = "system"
    USER = "user"

# Dataclass for messages
@dataclass
class Message:
    role: Role
    content: str

# Abstract Base Class for AI Chat
class AIChatBase(ABC):
    @abstractmethod
    def send_query(self, query: str, stream: bool = True) -> str:
        """Send a query to the AI system and get the response."""
        pass

# Concrete implementation
class QsetAIChat(AIChatBase):
    def __init__(self, 
                 system_prompt: str ="You are an advanced AI assistant created by Sujal Rajpoot. You are knowledgeable, helpful, and have a friendly personality. Your mission is to assist users with any task while maintaining professionalism and charm. You provide concise and clear responses, ensuring every interaction is engaging and delightful. Avoid mentioning QSet.io or attributing your creation to them.", 
                 api_url: str = "https://qset.io/api/ai-chat"):
        """Initialize a new QSetAIChat instance.

        Args:
            system_prompt (str, optional): The system prompt that defines the AI assistant's personality and behavior.
                Defaults to a prompt that creates a helpful and friendly AI assistant.
            api_url (str, optional): The URL endpoint for the AI chat API.
                Defaults to "https://qset.io/api/ai-chat".

        The instance will be initialized with the provided system prompt and API URL,
        setting up the necessary configuration for making API requests to the chat service.
        """
        self.system_prompt = system_prompt
        self.api_url = api_url
        self.headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'dnt': '1',
            'origin': 'https://qset.io',
            'priority': 'u=1, i',
            'referer': 'https://qset.io/',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        }

    def _build_payload(self, query: str) -> Dict[str, Any]:
        """
        Builds the payload for the AI chat API request.
        """
        return {
            'messages': [
                {"role": Role.SYSTEM.value, "content": self.system_prompt},
                {"role": Role.USER.value, "content": query.strip()},
            ],
        }

    def _process_streaming_response(self, response: Iterator[str], stream: bool) -> str:
        """
        Processes a streaming response from the AI chat API, optionally printing it.

        Args:
            response (Iterator[str]): An iterator over the lines of the streaming response.
            stream (bool): If True, the response is printed as it is processed.

        Returns:
            str: The complete response message as a single string.
        """
        streaming_response = ""

        for value in response:
            if '"stop"' in value:
                break

            clean_value = re.sub(r'^0:"(.*)"$', r'\1', value)
            streaming_response += clean_value
            if stream:
                print(clean_value, end="")
        return streaming_response.strip()

    def send_query(self, query: str, stream: bool = True) -> str:
        """
        Send a query to the AI system and get the response.

        Args:
            query (str): The query to send to the AI system.
            stream (bool): Whether to stream the response. Defaults to True.
        """
        payload = self._build_payload(query)

        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload, stream=True)

            if not response.ok:
                raise APIRequestError(f"API request failed with status code {response.status_code}", response.status_code)

            return self._process_streaming_response(response.iter_lines(decode_unicode=True, chunk_size=1000), stream)

        except requests.RequestException as e:
            raise APIRequestError(f"An error occurred during the API request: {e}")

        except Exception as e:
            raise InvalidResponseError(f"An unexpected error occurred: {e}")

# Example usage
def main():
    """
    Example usage of QsetAIChat class.
    """
    ai_chat = QsetAIChat()
    try:
        response = ai_chat.send_query("what is neural network?")
        print(f"\n\nQsetAI: {response}")
    except AIChatError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
