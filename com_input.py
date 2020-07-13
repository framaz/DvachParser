import re

from phf import PHFSystem
from phf.commandinput import ConsoleDebugInput, Command, ListProvidersCommand, NewProviderCommand, NewHookCommand


class DvachInput(ConsoleDebugInput):
    """Class to form dvach commands to phf."""

    def form_command(self, data: str) -> Command:
        """Form command from received from stdin string.

        Args:
            string of command.
        Return:
            Dvach-oriented Command.
        """
        data = data.split(" ")
        if data[0] in ["l", "list"]:
            return ListProvidersCommand()

        if data[0] in ["d", "download"]:
            path = None
            if len(data) > 2:
                path = data[2]
            return DownloaderFromDvach(data[1], path)

    async def output_command_result(self, command_result):
        """Show command execution result to user.

        Now there are 2 variants:
        1. The command_result is result of listing all working dvach providers if the command
        was to list all followed dvach links.
        2. The command_result is result of starting to download from dvach link.
        """
        if isinstance(command_result, list):
            print("Listing all active downloads:")
            for i, provider in enumerate(command_result):
                print(f"{i} - {provider}")
            return
        print(command_result)


class DownloaderFromDvach(Command):
    """Command to start downloading from dvach.

    Attributes:
        _link: str, link to dvach thread from which to download.
        _save_path: str, where to save all files.
    """

    def __init__(self, link: str, save_path: str = None, source=None):
        """Create DownloaderFromDvach Command.

        Args:
            link: link to dvach thread.
            save_path: path for saving.
            source: what created the command.
        """
        super().__init__(source)
        self._link = link
        self._save_path = save_path

    def _apply(self, phfsys: PHFSystem):
        """Create downloader hook.

        Args:
            phfsys: phfsys, on which it is executed.
        """
        providers = ListProvidersCommand().execute_command(phfsys)
        res = re.search(r"2ch\.(hk|pm|re|tf|wf|yt)/([a-zA-Z0-9]+/res/[0-9]+)",
                        self._link)

        found = -1
        for i, provider in enumerate(providers):
            if res[2] in provider.link:
                found = i
                break
        if found == -1:
            NewProviderCommand("dv", args=[self._link]).execute_command(phfsys)
        NewHookCommand("dvD", found, [self._save_path]).execute_command(phfsys)
        return f"Downloading from {self._link} started."
