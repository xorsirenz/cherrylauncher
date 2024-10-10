import customtkinter as ctk
import minecraft_launcher_lib
import os
import sys
import subprocess
from PIL import Image
from microsoft_login import login

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
    
        self.title("cherrylauncher")
        self.geometry("1920x1080")
        self.maxsize(1920, 1080)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        ctk.set_default_color_theme("themes/theme.json")

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.logo_image = ctk.CTkImage(
                Image.open(os.path.join(image_path, "icons-cherry-blossom-96.png")), 
                size=(125, 124))
        self.button_image = ctk.CTkImage(
                Image.open(os.path.join(image_path, "icons-cherry-blossom.png")), 
                size=(20, 20))
        self.background_image = ctk.CTkImage(
                Image.open(os.path.join(image_path, "cherry-background.jpg")), 
                size=(1920, 1080))
        self.home_image = ctk.CTkImage(
                light_image=Image.open(os.path.join(image_path, "ui-home-black-512.png")),
                dark_image=Image.open(os.path.join(image_path, "ui-home-peach-512.png")), 
                size=(48, 48))
        self.settings_image = ctk.CTkImage(
                light_image=Image.open(os.path.join(image_path, "ui-settings-black-512.png")),
                dark_image=Image.open(os.path.join(image_path, "ui-settings-peach-512.png")),
                size=(48, 48))

        # create navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = ctk.CTkLabel(
                self.navigation_frame, 
                text="", 
                image=self.logo_image,
                compound="left",) 
        self.navigation_frame_label.grid(row=0, column=0, padx=0, pady=2)

        self.home_button = ctk.CTkButton(
                self.navigation_frame, 
                border_spacing=2, 
                width=10,
                height=10,
                corner_radius=0, 
                text="",
                fg_color="transparent", 
                hover_color=("#3a4148"),
                image=self.home_image, 
                anchor="w", 
                command=self.home_button_event)
        self.home_button.grid(row=2, column=0, sticky="ew")

        self.settings_button = ctk.CTkButton(
                self.navigation_frame, 
                corner_radius=0, 
                border_spacing=2, 
                text="",
                fg_color="transparent", 
                hover_color=("#3a4148"),
                image=self.settings_image, 
                anchor="w", 
                command=self.settings_button_event)
        self.settings_button.grid(row=3, column=0, sticky="ew")

        self.minecraft_versions = self.installed_versions()
        self.version_select = ctk.CTkComboBox(
                self.navigation_frame, 
                corner_radius=0, 
                height=30, 
                width=220,
                font=ctk.CTkFont(size=28),
                values=self.minecraft_versions)
        self.version_select.grid(row=5, column=0, padx=0, pady=2, sticky="s")

        self.launch_button = ctk.CTkButton(
                self.navigation_frame, 
                text="launch minecraft", 
                text_color="#09121b",
                font=ctk.CTkFont(size=28),
                fg_color="#85e48c",
                command=self.launch_minecraft)
        self.launch_button.grid(row=6, column=0, padx=2, pady=10, sticky="s")

        self.cl_version_label = ctk.CTkLabel(
                self.navigation_frame,
                text="cherrylauncher \nv0.0.1-alpha",
                text_color=("#84888d"),
                font=ctk.CTkFont(size=18))
        self.cl_version_label.grid(row=7, column=0, padx=2, pady=10, sticky="s")

        # create home frame
        self.home_frame = ctk.CTkFrame(self, corner_radius=0)
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.image_label = ctk.CTkLabel(self.home_frame, image=self.background_image, text="")
        self.image_label.grid(sticky="nsew")

        # create settings frame
        self.settings_frame = ctk.CTkFrame(self, corner_radius=0)
        self.settings_frame.grid_columnconfigure(0, weight=1)

        self.settings_exit_button = ctk.CTkButton(
                self.settings_frame, 
                text="exit",
                image=self.button_image, 
                compound="left", 
                command=self.exit_cherrylauncher)
        self.settings_exit_button.grid(row=2, column=0, padx=20, pady=30, sticky="w")

        self.appearance_mode_menu = ctk.CTkOptionMenu(
                self.settings_frame, 
                values=["Light", "Dark", "System"],
                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=0, column=0, padx=20, pady=20, sticky="ne")


        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("#ffffff", "#212931") if name == "home" else "transparent")
        self.settings_button.configure(fg_color=("#ffffff", "#212931") if name == "settings" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "settings":
            self.settings_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.settings_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def settings_button_event(self):
        self.select_frame_by_name("settings")

    def installed_versions(self):
        minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()
        versions = minecraft_launcher_lib.utils.get_installed_versions(minecraft_directory)
        version_list = []
        for i in versions:
            version_list.append(i["id"])
        return version_list

    def launch_minecraft(self):
        self.minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()
        minecraft_launcher_lib.install.install_minecraft_version(self.version_select.get(), self.minecraft_directory)
        
        options = {
            "username": username,
            "uuid": uuid,
            "token": microsoft_token
            }
        self.minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(self.version_select.get(), self.minecraft_directory, options)

        self.withdraw()
        subprocess.run(self.minecraft_command)
        self.deiconify()
        #sys.exit(0)        

    def exit_cherrylauncher(self):
        print("[!] closing cherrylauncher..")
        sys.exit(0)

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    username, uuid, microsoft_token = login()
    app = App()
    app.mainloop()
