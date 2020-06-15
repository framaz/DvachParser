import re

from phf import PHFSystem
from phf.commandinput import ConsoleDebugInput, T, Command, ListProvidersCommand, NewProviderCommand, NewHookCommand


class DvachInput(ConsoleDebugInput):
    def form_command(self, data: T) -> Command:
        data = data.split(" ")
        if data[0] in ["l", "list"]:
            return ListProvidersCommand()

        if data[0] in ["d", "download"]:
            path = None
            if len(data) > 2:
                path = data[2]
            return DownloaderFromDvach(data[1], path)

    async def output_command_result(self, command_result):
        if isinstance(command_result, list):
            print("Listing all active downloads:")
            for i, provider in enumerate(command_result):
                print(f"{i} - {provider}")
            return
        print(command_result)


class DownloaderFromDvach(Command):
    def __init__(self, link: str, save_path: str = None, source=None):
        super().__init__(source)
        self._link = link
        self._save_path = save_path

    def _apply(self, phfsys: PHFSystem):
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
