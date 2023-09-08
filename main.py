from random import choice
from time import sleep
import requests
from datetime import datetime
from retrypy import retry

from config import (
    change_proxy_url,
    sleep_between_accounts_sec,
    is_random_proxy,
    chat_id,
    retry_on_error_count,
)

from src.logger import logging
from src.account import Account
from src.get_file_data import get_file_data

logger = logging.getLogger(f"root")


def main():
    script_start_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    user_agents = get_file_data("data/user_agents.txt")
    logger.info(f"found {len(user_agents)} user_agents")

    proxies = get_file_data("data/proxies.private.txt")
    logger.info(f"found {len(proxies)} proxies")

    tokens = get_file_data("data/tokens.private.txt")
    logger.info(f"found {len(tokens)} tokens")

    messages = get_file_data("data/messages.private.txt")
    logger.info(f"found {len(messages)} messages")

    if not is_random_proxy and len(proxies) != len(tokens):
        raise Exception(
            f"Amount of proxies must be equals to amount of tokens if you using is_random_proxy = False or use is_random_proxy = True"
        )

    for idx, token in enumerate(tokens):
        try:
            proxy = choice(proxies) if is_random_proxy else proxies[idx]
            user_agent = choice(user_agents)
            message = choice(messages)

            account = Account(
                token=token, proxy=proxy, user_agent=user_agent, chat_id=chat_id
            )

            send_msg_wrapped = retry.wrap(
                account.send_message,
                times=retry_on_error_count,
                wait=sleep_between_accounts_sec,
            )

            response = send_msg_wrapped(message=message)
            content = response["content"][:20]
            logger.info(f"{idx} | success | message: {content}")

        except Exception as e:
            logger.error(f"{idx} | error: {e}")

            with open(f"logs/{script_start_time}_error_tokens.log", "a") as file:
                file.write(f"{token}\n")

        if change_proxy_url:
            response = requests.get(change_proxy_url)
            response.raise_for_status()

        if idx != len(tokens) - 1:
            sleep(sleep_between_accounts_sec)


if __name__ == "__main__":
    main()
