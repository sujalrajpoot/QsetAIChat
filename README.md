# QsetAIChat: An Advanced AI Chat System

## Overview
QsetAIChat is a Python-based library for interacting with an AI chat system. The implementation uses high-level Object-Oriented Programming (OOP) principles, including abstraction, encapsulation, and custom error handling. The library facilitates sending queries to the AI system and retrieving responses in a user-friendly manner.

## Features
- **High-level OOP design**: Provides a clean and modular architecture.
- **Custom error handling**: Includes specific exceptions for API errors and unexpected responses.
- **Streaming responses**: Supports real-time response streaming.
- **Customizable prompts**: Allows setting a system-level prompt to guide AI behavior.

## Requirements
- Python 3.7+
- External libraries:
  - `requests`
  - `json`
  - `re`
  - `dataclasses`
  - `typing`

Install the required libraries using pip:
```bash
pip install requests
```

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/sujalrajpoot/QsetAIChat.git
cd QsetAIChat
```

### 2. Usage
The `QsetAIChat` class handles the interaction with the AI system.

#### Example
```python
def main():
    ai_chat = QsetAIChat()
    try:
        response = ai_chat.send_query("what is neural network?")
        print(f"\n\nQsetAI: {response}")
    except AIChatError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
```

### 3. Customization
You can customize the system prompt when creating an instance of `QsetAIChat`:
```python
ai_chat = QsetAIChat(system_prompt="You are a helpful AI that provides concise answers.")
```

## Error Handling
The library uses custom exceptions for better debugging:
- `AIChatError`: Base class for all chat-related errors.
- `APIRequestError`: Raised for issues during the API request.
- `InvalidResponseError`: Raised for unexpected or invalid responses.

Example:
```python
try:
    response = ai_chat.send_query("Tell me a joke.")
except APIRequestError as api_err:
    print(f"API Error: {api_err}")
except InvalidResponseError as resp_err:
    print(f"Response Error: {resp_err}")
```

## Code Structure
- **`QsetAIChat`**: The main class for interacting with the AI.
- **Custom Exceptions**: Defined for robust error management.
- **Utility Methods**:
  - `_build_payload`: Constructs the JSON payload for the API.
  - `_process_streaming_response`: Processes and streams the API's response.

## Disclaimer ⚠️

**IMPORTANT: EDUCATIONAL PURPOSE ONLY**

This project is intended solely for educational purposes. Please ensure its use complies with Qset.io's guidelines and security policies. The authors and contributors are not responsible for any misuse of the library.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Contact
For questions or support, please open an issue or reach out to the maintainer.

## Contributing

Contributions are welcome! Please submit pull requests or open issues on the project repository.
