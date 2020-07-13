import os

from phf.abstracthook import AbstractHook
from phf.utils import download_files


class DvachShowHook(AbstractHook):
    """Basic hook for printing all messages from dvach.

    Attributes:
        last_posts: set of already processed posts.
    """
    _alias = ["dvS"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_posts = set()

    def get_updated_text(self, posts: list):
        """Get only unprocessed posts.

        Args:
            posts: a list of all posts in thread currently.
        """
        res = []
        for post in posts:
            if post['num'] not in self.last_posts:
                self.last_posts.add(post['num'])
                res.append(post)
        return res

    async def hook_action(self, output: list):
        """Print all new posts.

        Args:
            output: list of thread posts."""
        to_print = str(self.get_updated_text(output))
        if to_print == "[]":
            return
        print("                                                          ", end="\r")
        print("\n" + to_print)


class DvachFileDownloader(DvachShowHook):
    """Download files from dvach thread hook.

    Attributes:
        _save_path: str, where to save files to.
        """
    _alias = ["dvD"]

    def __init__(self, save_path: str = None, *args, **kwargs):
        """Create dvach downloader hook.

        Args:
            save_path: path to where to save everything.
            """
        super().__init__(*args, **kwargs)
        if save_path is not None:
            self._save_path = save_path
        else:
            self._save_path = "downloads"

    async def hook_action(self, output):
        """Save all files from new posts.

        Args:
            output: new posts.
        """
        posts = self.get_updated_text(output)
        download_list = []
        for post in posts:
            for file in post["files"]:
                download_path = "2ch.hk" + file["path"]
                download_to = download_path.split("/")

                if "stickers" in download_to:
                    download_to = os.path.join(self._save_path,
                                               post['thread_num'],
                                               download_to[3])
                else:
                    download_to = os.path.join(self._save_path,
                                               download_to[3],
                                               file["fullname"])

                download_list.append((download_path, download_to))
        if len(download_list) == 0:
            return
        await download_files(download_list)

    def __str__(self):
        return self.__class__.__name__
