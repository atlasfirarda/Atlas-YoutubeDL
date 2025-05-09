from colored import Fore, style


class ColorModule:
    def __init__(self, text):

        self.text = None

        if text:
            self.text = text

    def green(self):
        if not self.text:
            return

        text = self.text

        return "%s%s%s" % (Fore.rgb(54, 245, 45), text, style("reset"))

    def red(self):
        if not self.text:
            return

        text = self.text

        return "%s%s%s" % (Fore.rgb(245, 54, 45), text, style("reset"))

    def yellow(self):
        if not self.text:
            return

        text = self.text

        return "%s%s%s" % (Fore.rgb(235, 255, 0), text, style("reset"))

    def blue(self):
        if not self.text:
            return

        text = self.text

        return "%s%s%s" % (Fore.rgb(93, 171, 245), text, style("reset"))

    def bold(self):
        if not self.text:
            return

        text = self.text

        return "%s%s%s" % (style("bold"), text, style("reset"))
