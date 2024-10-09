import customtkinter as ctk
import minecraft_launcher_lib
import subprocess
import sys
from PIL import Image
from microsoft_login import login

def background_image():
    background_image = ctk.CTkImage(light_image=Image.open("../assets/images/cherry-background.jpg"),
                                    dark_image=Image.open("../assets/images/cherry-background.jpg"),
                                    size=(1920, 1080)
                                    )
    image_label = ctk.CTkLabel(app, image=background_image, text="")
    image_label.grid(sticky="nsew")

def close_app():
    print('[!] closing cherrylauncher..')
    sys.exit(0)

def tabs():
    tabview = ctk.CTkTabview(app, width=40, height=2)
    tabview.grid(row=0, column=0, padx=1, pady=1, sticky="n")

    tab1 = tabview.add("home")
    tab2 = tabview.add("about/help")
    tabview.set("home")

    github_button = ctk.CTkButton(tab2, text="github")
    github_button.grid(row=0, column=0, columnspan=2)

    logout_button = ctk.CTkButton(tab2, text = "logout", command=close_app)
    logout_button.grid(row=1, column=0, sticky="n")

def launch_minecraft():
    minecraft_launcher_lib.install.install_minecraft_version(version_select.get(), minecraft_directory)

    options = {
            "username": username,
            "uuid": uuid,
            "token": microsoft_token
        }
    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version_select.get(), minecraft_directory, options)

    app.withdraw()
    subprocess.run(minecraft_command)
    app.deiconify()


username, uuid, microsoft_token = login()

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("themes/theme.json")

app = ctk.CTk()
app.geometry('1920x1080')
app.maxsize(1920, 1080)
app.title('cherrylauncher')
app.columnconfigure(0, weight=1)
app.rowconfigure(0, weight=1)

background_image()
tabs()

minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()
versions = minecraft_launcher_lib.utils.get_installed_versions(minecraft_directory)

version_list = []
for i in versions:
    version_list.append(i["id"])

version_label = ctk.CTkLabel(app, text="")
version_label.grid(row=0, column=0, padx=30, pady=1, sticky="nw")
version_select = ctk.CTkComboBox(app, values=version_list)
version_select.grid(row=0, column=0, padx=20, pady=30, sticky="nw")

launcher_button = ctk.CTkButton(app, text="launch", command=launch_minecraft)
launcher_button.grid(row=0, column=0, padx=20, pady=20, columnspan=4, sticky="s")


if __name__ == '__main__':
    app.mainloop()
