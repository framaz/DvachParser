import json
import re

import requests
from phf.provider import PeriodicContentProvider


class Dvach(PeriodicContentProvider):
    """A dvach thread provider.

    Attributes:
        link: str, link to dvach json api.
        site: str, site name(Dvach).
        board: str, dvach's board name.
        thread_num: str, thread's number.
    """
    _alias = ["dv"]

    def __init__(self, link, *args, **kwargs):
        super().__init__(*args, **kwargs)
        res = re.search(r"2ch\.(hk|pm|re|tf|wf|yt)/[a-zA-Z0-9]+/res/[0-9]+", link)
        self.link = "https://" + res[0] + ".json"
        self.site = "Dvach"
        formatted_json = self._get_json_data()
        self.board = r"/" + formatted_json["Board"] + r"/"
        self.thread_num = formatted_json["current_thread"]

    def _get_json_text(self) -> str:
        """Get a thread json string from api.

        Returns:
            Json-formatted str of the thread.
        """
        r = requests.get(self.link)
        return r.text

    def _get_json_data(self):
        """Unpack str json data to dict.

        Returns:
            Pythonic data structure of the json data(list or dict)."""
        unformatted_json = self._get_json_text()
        formatted_json = json.loads(unformatted_json)
        return formatted_json

    @staticmethod
    def _remove_html_tags(post_string: str) -> str:
        """Remove all html tags from post's comment stirng.

        Removes all hyperlinks, changes <br> with "\n".

        Returns:
            Str with removed html tags.
        """
        res = re.sub(r'<a [a-zA-Z0-9="/.# ->]*(>>[0-9]+( \(OP\))?)</a>', r'\1', post_string)
        res = re.sub(r"<br>", "\n", res)
        return res

    def _full_post_to_short_form(self, post_json: dict) -> dict:
        """Remove unneeded data from a post's dictionary.

        Returns:
            Post dictionary without unneeded parts.
        """
        short_post = dict()
        short_post["date"] = post_json["date"]
        short_post["num"] = post_json["num"]
        short_post["comment"] = Dvach._remove_html_tags(post_json["comment"])
        short_post["files"] = post_json["files"]
        short_post["thread_num"] = self.thread_num
        return short_post

    def _get_posts(self) -> list:
        """Get all posts in thread with only needed data.

        Returns:
            List of posts."""
        formatted_json = self._get_json_data()
        posts = formatted_json["threads"][0]['posts']
        res = []
        for post in posts:
            res.append(self._full_post_to_short_form(post))
        return res

    async def get_content(self):
        """Get all posts in thread with only needed data."""
        return self._get_posts()

    def __str__(self):
        return f"Dvach {self.board} thread {self.thread_num}"
