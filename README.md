# Telegram Bot Admin Panel

This is a Telegram bot admin panel implemented in Python using the Telebot library. The bot provides administrative functionalities such as managing user subscriptions, sending broadcasts, exporting user data, and checking statistics.

## Features

- **User Subscription Management**: Users can request access to a knowledge base by subscribing to designated channels.
- **Broadcasting**: Admins can send broadcast messages to all users or a selected group of users.
- **Export User Data**: Admins can export user data to an Excel file for further analysis.
- **Statistics**: Provides insights into the number of users in the database.

## Installation

1. **Clone the repository:**

    ```
    git clone https://github.com/your_username/telegram-bot-admin-panel.git
    ```

2. **Install dependencies:**

    ```
    pip install -r requirements.txt
    ```

3. **Configure the bot:**
   
   - Obtain a bot token from the BotFather on Telegram.
   - Update the `config.py` file with your bot token, admins' user IDs, channel IDs, and other necessary configurations.

4. **Run the bot:**

    ```
    python main.py
    ```

## Requirements

- Python 3.6 or higher
- Libraries: aiogram

## Installation

1. Clone this repository to your local machine.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Set up your Telegram bot token, group ID, admin IDs, session name, API hash, API ID, and other configurations in the `config.py` file.

```python
TOKEN = 'your telegram bot token'
GROUP_ID = 'group id where the orders are sent forward'
ADMIN_IDS = [admin ids here]

```

## Usage

- **Subscription Management**: When users join the chat, they are prompted to subscribe to specified channels before accessing the main knowledge base.
- **Broadcasting**: Admins can initiate broadcasts by sending messages to all users or specific user groups.
- **Export User Data**: Admins can generate an Excel file containing user data by executing the `/admin` command and selecting the option to export the database.
- **Statistics**: Admins can view statistics on the total number of users in the database by executing the `/admin` command and selecting the statistics option.

## Contributing

Contributions are welcome! Feel free to open issues or pull requests for any improvements or bug fixes.

## License

This project is licensed under the [MIT License](LICENSE).

