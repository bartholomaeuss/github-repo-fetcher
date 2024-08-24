import logging

import requests

logging.basicConfig(level=logging.INFO, format="%(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()


def get_public_repositories(username):
    """
    Retrieves the public GitHub repositories for a specified user.

    This function sends a GET request to the GitHub API to fetch the list of public
    repositories for a given user. If the request is successful (status code 200),
    it returns a list of repository names. Otherwise, it prints an error message
    and returns an empty list.

    Args:
        username (str): The GitHub username whose public repositories are to be retrieved.

    Returns:
        list: A list of repository names (str) that are publicly accessible. Returns an empty list
        if an error occurs or no repositories are found.
    """
    url = f"https://api.github.com/users/{username}/repos"
    logger.info(f"Attempting to fetch public repositories for user: {username}")
    response = requests.get(url)
    logger.info(
        f"API request made to URL: {url} with response status code: {response.status_code}"
    )

    if response.status_code == 200:
        logger.info(f"Successfully fetched data for user: {username}")
        repos = response.json()
        return [repo["name"] for repo in repos]
    else:
        logger.error(
            f"Failed to fetch repositories. HTTP Status Code: {response.status_code}, Reason: {response.reason}"
        )
        return []


def main():
    """
    Main function of the program that prompts the user for a GitHub username
    and displays the public repositories of that user.

    This function prompts the user to enter a GitHub username and then retrieves
    the public repositories of that user using the `get_public_repositories` function.
    The repositories are then printed to the console.

    If no public repositories are found or an error occurs, an appropriate message is displayed.
    """
    username = input("Enter the GitHub username: ")
    logger.info(f"User entered GitHub username: {username}")
    repos = get_public_repositories(username)
    logger.info(f"Repositories retrieved: {repos}")

    if repos:
        print(f"Public repositories of {username}:")
        logger.info(f"Public repositories of {username}:")
        for repo in repos:
            print(f"- {repo}")
            logger.info(f"- {repo}")
    else:
        print("No public repositories found or an error occurred.")
        logger.info("No public repositories found or an error occurred.")


if __name__ == "__main__":
    main()
