import pyautogui as pag
import pygetwindow as gw
import os
import subprocess
import time

pag.FAILSAFE = False

TIMEOUT = 30

win_search_box_fp = "images/win_search_box.png"
discord_icon_fp = "images/discord_icon.png"
discord_icon_selected_fp = "images/discord_icon_selected.png"
friends_list_fp = "images/friends_list.png"
all_icon_fp = "images/all_icon.png"
discord_search_box_fp = "images/discord_search_box.png"
message_box_fp = "images/message_box.png"

nandex_user_offline_fp = "images/nandex_user_offline.png"
nandex_user_online_fp = "images/nandex_user_online.png"


def find_location(image_path, timeout= 30):
    start = time.time()

    while time.time() - start < timeout:
        try:
            location = pag.locateOnScreen(image_path, confidence=.85)

            if location:
                return location

        except pag.ImageNotFoundException:
            pass

        wait() 

    return None


def open_discord():
    local_app_data = os.environ["LOCALAPPDATA"]

    update_path = os.path.join(
        local_app_data,
        "Discord",
        "Update.exe"
    )

    if not os.path.isfile(update_path):
        print("Discord Update.exe not found!")
        return False

    try:
        subprocess.run(
            [update_path, "--processStart", "Discord.exe"],
            check=True,
            timeout=15
        )

        print("Discord launch command completed.")
        return True

    except (subprocess.SubprocessError, OSError) as error:
        print("Failed to launch Discord:", error)
        return False


def restore_discord_window(timeout=20):
    start = time.time()

    while time.time() - start < timeout:
        windows = gw.getWindowsWithTitle("Discord")

        for window in windows:
            try:
                if window.isMinimized:
                    window.restore()

                window.activate()
                print("Discord window activated.")
                return True

            except Exception as error:
                print("Couldn't activate window:", error)

        time.sleep(0.5)

    print("Discord window wasn't found.")
    return False


def wait(duration=.8):
    time.sleep(duration)


def main():
    # search_box = find_location(win_search_box_fp)

    # if not search_box:
    #     print("SearchBox not found!")
    #     return

    # pag.click(pag.center(search_box))

    # wait()

    # pag.write("discord", .05)
    # pag.press("enter")

    open_discord()
    
    wait(1)

    restore_discord_window()
    
    if not find_location(message_box_fp, 2):
        discord_icon_selected = find_location(discord_icon_selected_fp)

        if discord_icon_selected:
            discord_icon = discord_icon_selected
        else:
            discord_icon = find_location(discord_icon_fp)

        if not discord_icon:
            print("Discord icon not found!")
            return
        else:
            print("Discord icon was found")

        pag.click(pag.center(discord_icon))

        wait(1)

        # =======================================

        friends_list = find_location(friends_list_fp)

        if not friends_list:
            print("Friend list not found!")
            return
        else:
                print("Friend list was found")

        pag.click(pag.center(friends_list))

        wait()

        # =======================================

        all_icon = find_location(all_icon_fp)

        if not all_icon:
            print("All icon not found!")
            return

        pag.click(pag.center(all_icon))

        wait()

        # =======================================

        discord_search_box = find_location(discord_search_box_fp)

        if not discord_search_box:
            print("Discord search box not found!")
            return
        else:
            print("Discord search box was found")

        pag.click(pag.center(discord_search_box))

        wait()

        pag.write("Nandex", .05)

        wait()

        # =======================================

        nandex = find_location(nandex_user_online_fp, 2)

        if not nandex:
            nandex = find_location(nandex_user_offline_fp)

            if not nandex:
                print("Nandex user not found!")
                return
            else:
                    print("Nandex user offline was found")
        else:
                print("Nandex user online was found")

        pag.click(pag.center(nandex))

        wait()

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

    message_box = find_location(message_box_fp)

    if not message_box:
        print("Message box not found!")
        return
    else:
        print("Messages box was found")

    pag.click(pag.center(message_box))

    wait()

    pag.write("You are the GOAT! Words cannot really describe how great you are, my god.", .03)
    pag.press("enter")


if __name__ == "__main__":
    main()