---

# Disney Itinerary and Hotel Inquiry Bot

This project contains a Rasa-based conversational AI bot designed to handle inquiries related to Disney itineraries and hotel bookings. The bot can respond to user questions, handle inquiries via forms, and provide recommendations based on the user's input.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Running the Bot](#running-the-bot)
- [Custom Actions](#custom-actions)
- [Forms and Validation](#forms-and-validation)
- [Fallback and Handling Unrecognized Queries](#fallback-and-handling-unrecognized-queries)
- [Deployment](#deployment)

## Prerequisites

- Python 3.8 or later
- Rasa 2.x
- Rasa SDK
- ngrok (for exposing the bot to the internet)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/avisaini0501/Magic-Planner-Genie.git
   cd Magic-Planner-Genie
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

- `domain.yml`: Defines the domain of the assistant, including intents, entities, slots, responses, forms, and actions.
- `nlu.yml`: Contains training examples for the NLU model.
- `stories.yml`: Contains training stories for the dialogue model.
- `actions.py`: Custom actions for the bot, including API calls and form validations.

## Configuration

### domain.yml

This file includes intents like `goodbye`, `bot_challenge`, and various forms such as `inquiry_form`, `hotel_form`, and `journey_form`. It also defines slots like `DATE` and `MONEY`, which are used in forms.

### nlu.yml

This file includes the NLU training data. Intents such as `greet`, `goodbye`, `bot_challenge`, and others are defined with example utterances.

### stories.yml

This file contains stories that define how the bot should respond to different sequences of user inputs. It includes paths for handling goodbyes, bot challenges, and form submissions.

## Running the Bot

1. Train the bot:
   ```bash
   rasa train
   ```

2. Run the action server:
   ```bash
   rasa run actions
   ```

3. In a new terminal window, start the Rasa server:
   ```bash
   rasa shell
   ```

## Custom Actions

Custom actions are implemented in `actions.py`. These actions handle form submissions, API calls, and data formatting. Key actions include:

- `ActionLangchainPayload`: Handles itinerary queries and formats payloads for the API.
- `ActionHandleInquiry`: Processes general inquiries and sends them to the API.
- `ActionRecommend`: Provides hotel recommendations based on the user's budget.
- `ActionFallbackLangchain`: Manages fallback scenarios and sends unrecognized queries to the API.

## Forms and Validation

Forms are used to collect and validate user input. The `ValidateDaysAndBudgetForm` class handles the validation of the `DATE` and `MONEY` slots.

## Fallback and Handling Unrecognized Queries

The fallback mechanism is implemented in `ActionFallbackLangchain`, which sends unrecognized user queries to an external API for handling.

## Deployment

To deploy the bot, you can use services like Docker, Kubernetes, or cloud platforms. Ensure that the necessary environment variables and configurations are set for production.

Example using Docker:

1. Create a `Dockerfile`:
   ```dockerfile
   FROM rasa/rasa:2.8.0-full

   # Copy necessary files
   COPY . /app

   WORKDIR /app

   # Install dependencies
   RUN pip install -r requirements.txt

   # Train the model
   RUN rasa train

   # Run the action server and Rasa server
   CMD ["rasa", "run", "--enable-api", "--cors", "*", "--debug"] & ["rasa", "run", "actions"]
   ```

2. Build and run the Docker container:
   ```bash
   docker build -t Magic-Planner-Genie .
   docker run -p 5005:5005 Magic-Planner-Genie
   ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---

This README provides a comprehensive guide to setting up, running, and deploying your Rasa bot. Ensure to adjust the URLs, names, and other specific details as per your actual project and environment.
