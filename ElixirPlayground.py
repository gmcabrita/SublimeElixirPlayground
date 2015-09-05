import sublime
import sublime_plugin
import threading

try:
  from urllib.parse import urlencode
  from urllib.request import urlopen
except ImportError:
  from urllib import urlencode, urlopen

PLAYGROUND_URL = "http://play.elixirbyexample.com/share"


class ShareSelectionWithElixirPlaygroundCommand(sublime_plugin.TextCommand):

    def run(self, view):
        # Get user selected text
        for region in self.view.sel():
            text = self.view.substr(region)

            if not text:
                sublime.status_message("Error sending to Elixir Playground: Nothing selected")
            else:
                args = {
                    "code": text
                }

                thread = ElixirPlaygroundApiCall(args)
                thread.start()


class ShareFileWithElixirPlaygroundCommand(sublime_plugin.TextCommand):

    def run(self, view):
        text = self.view.substr(sublime.Region(0, self.view.size()))

        args = {
            "code": text
        }

        thread = ElixirPlaygroundApiCall(args)
        thread.start()


class ElixirPlaygroundApiCall(threading.Thread):
    """Caller for the Elixir Playground API."""

    def __init__(self, args):
        self.args = args
        threading.Thread.__init__(self)

    def run(self):
        sublime.status_message("Sending to Elixir Playground...")

        response = urlopen(url=PLAYGROUND_URL, data=urlencode(self.args).encode("utf-8")).read().decode("utf-8")
        url = "http://play.elixirbyexample.com/s/" + response

        sublime.set_clipboard(url)
        sublime.status_message("Elixir Playground URL copied to cliboard: " + url)