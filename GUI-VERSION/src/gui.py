import customtkinter as ctk
import os
from getYoutube import Download


def download_callback():
    text: str = app.linktext.get().strip("\n")

    ffmpegPath = os.path.abspath(os.path.join("src", "ffmpeg", "ffmpeg.exe"))
    folderPath = os.path.join(os.path.expanduser("~"), "Downloads")

    if not text == "" and (
            str(text).startswith("https://www.youtube.com/watch?v=") or str(text).startswith(
        "youtube.com/watch?v=") or str(text).startswith("https://youtube.com/watch?v=") or str(
        text).startswith("https://youtu.be/")):
        Download(folderPath, text, ffmpegPath)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        width, height = 960, 540

        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.overrideredirect(True)
        self.title("AtlasAta YoutubeDL")
        self.iconbitmap(os.path.abspath(os.path.join("src", "assets", "icon64x64.ico")))
        self.config(takefocus=True)
        self.wm_attributes("-transparentcolor", "black")
        ctk.deactivate_automatic_dpi_awareness()

        self.bind("<Escape>", self.onWindowClose)

        self.frame = ctk.CTkFrame(self, width=920, height=50, corner_radius=12, bg_color="transparent",
                                  fg_color="#181818")

        self.label = ctk.CTkLabel(self.frame, text="AtlasAta", font=("CaskaydiaCove NF", 24),
                                  bg_color="transparent",
                                  fg_color="transparent")
        self.frame.pack(anchor="n", expand=True, padx=15, pady=15)
        self.label.place(relx=0.5, rely=0.5, anchor="center")

        self.frame = ctk.CTkFrame(self, width=256, height=300, corner_radius=9, bg_color="transparent",
                                  fg_color="transparent")
        self.label = ctk.CTkLabel(self.frame, text="Video Link", font=("CaskaydiaCove NF", 18), bg_color="transparent",
                                  fg_color="transparent")

        self.linktext = ctk.CTkEntry(self.frame, placeholder_text="link", height=40, width=256,
                                     font=("Cascadia Mono NF Light", 12), bg_color="transparent",
                                     fg_color="transparent",
                                     justify="center")
        self.frame.pack(anchor="center", expand=True, padx=5, pady=5)
        self.linktext.place(relx=0.5, rely=0.5, anchor="center")
        self.entry = ctk.CTkButton(self.frame, text="Download", font=("CaskaydiaCove NF", 15),
                                   command=download_callback)
        self.entry.place(relx=0.5, rely=0.7, anchor="center")
        self.label.place(relx=0.5, rely=0.5, anchor="center", y=-40)

        self.frame = ctk.CTkFrame(self, width=182, height=30, corner_radius=9, bg_color="transparent",
                                  fg_color="transparent")

        self.label = ctk.CTkLabel(self.frame, text="copyright © by atlasata.", font=("Cascadia Mono NF Light", 12),
                                  bg_color="transparent", fg_color="transparent")
        self.frame.pack(anchor="s", expand=True, padx=5, pady=5)
        self.label.place(relx=0.5, rely=0.5, anchor="center")

    @staticmethod
    def onWindowClose(event):
        app.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
