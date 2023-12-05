## Discord messages sender
Script sends random message to discord chats using discord token with mobile proxy

## First start
1. Install python on https://www.python.org/downloads/
2. Navigate to the project root on terminal
3. Run the command `pip install -r requirements.txt` to install all required dependencies
4. Create `data/messages.private.txt` file with messages each from new line
5. Create `data/tokens.private.txt` file with discord tokens each from new line
6. Create `data/proxies.private.txt` file with proxies in format `http://login:password@host:port` each from new line. If using mobile proxies add it here and set `is_random_proxy` variable to `True` (details below)
7. Create `config.py` file and fill it using `config.example.py`:
- `change_proxy_url` - rotate url for mobile proxy. Just leave empty in the case of regular proxies
- `sleep_between_accounts_sec` - sleep duration (seconds) between accounts
- `chat_id` - discord chat id
- `is_random_proxy` - use `True` to use random proxy from `data/proxies.private.txt` for each account. If `False` script will use account index to get proxy. First proxy for first account, second proxy for second account etc.
- `is_random_msg` - use `True` to use random message from `data/messages.private.txt` for each account. If `False` script will use account index to get message. First message for first account, second message for second account etc.
- `retry_on_error_count` - times to retry sending message on error
8. Run script using `python main.py`


Error tokens will be saved in `logs/<script_start_time>_error_tokens.log`