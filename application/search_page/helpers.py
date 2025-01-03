"""helpers module

This module contains helper functions for formatting text and storing data in
flask.session.
"""

from flask import session


def format_search_word(s_word, separator=" ", accepted_special_characters=""):
    """
    Format the search word for querying.

    Args:
        s_word (str): The input search word.
        separator (str): The separator used in case there are multiple words.
        Default is " ".
        accepted_special_characters (str): Accepted special characters that will
        not be removed from the s_word. Default is "".

    Returns:
        formatted_s_word (str): The formatted search word.

    This function returns the inputted search word if it is a single word, or
    the inputted search word concatenated with the separator sign if there are
    more than one term in s_word. The function removes all leading and trailing
    whitespaces of the input. The function removes all non-alphanumeric
    characters except the ones passed in accepted_special_characters parameter.
    """

    for character in s_word:
        if (
            character.isalnum() is False
            and character not in accepted_special_characters
            and character != " "
        ):
            s_word = s_word.replace(character, "")

    s_word_list = s_word.split()

    if len(s_word_list) == 1:
        formatted_s_word = s_word.strip()
    else:
        formatted_s_word = separator.join(s_word_list)

    return formatted_s_word


def store_s_word_in_session(session_s_word, request_s_word):
    """
    Update the value of s_word in the session with the value from the current
    request.

    Args:
        session_s_word (str): The current value of s_word stored in the session.
        request_s_word (str): The value of s_word from the current request.

    Returns:
        str or None: The updated value of s_word in the session, or None if no
        current or request value is provided.

    This function replaces the current value of s_word in the session with the
    value from the current request. It returns the updated value of s_word in
    the session, or None if no current value or request value is provided.
    """

    if session_s_word is None or (
        request_s_word is not None and request_s_word != session_s_word
    ):
        session["s_word"] = request_s_word

    return session.get("s_word")
