from adb_command_executor import AdbCommandExecutor
from image_searcher import ImageSearcher

DEVICE_IP_PORT: str = "localhost:5555"
SCREENSHOT = "screenshot.png"
BALL_BLAST_APP_NAME: str = "com.nomonkeys.ballblast"

AdbCommandExecutor.execute(f"connect {DEVICE_IP_PORT}")

# AdbCommandExecutor.capture_remote_screen(SCREENSHOT)

AdbCommandExecutor.run_app_and_bring_to_foreground(BALL_BLAST_APP_NAME)

AdbCommandExecutor.capture_remote_screen(SCREENSHOT)
tap_point = ImageSearcher.search(SCREENSHOT, "shop_icon.png", debugging_enabled=True)
AdbCommandExecutor.execute(f"shell input tap {tap_point[0]} {tap_point[1]}", wait=2)

"""
Collecting free chest if icon does not include next_free_in.png"
"""
AdbCommandExecutor.capture_remote_screen(SCREENSHOT)
# tap_point = ImageSearcher.search(SCREENSHOT, "free_chest.png", search_for_text="a", debugging_enabled=True)
# tap_point = ImageSearcher.search(SCREENSHOT, "next_free_in.png", search_for_text="Next free", debugging_enabled=True)
is_text_there, tap_point = ImageSearcher.search_with_text(SCREENSHOT,
                                                          "free_chest.png",
                                                          "next_free_in.png",
                                                          search_for_text="Next free",
                                                          debugging_enabled=True)
if not is_text_there:
    AdbCommandExecutor.execute(f"shell input tap {tap_point[0]} {tap_point[1]}", wait=40)

"""
Collecting free shots every day
"""

AdbCommandExecutor.execute(f"shell input swipe 300 1000 300 300 300", wait=4)
AdbCommandExecutor.capture_remote_screen(SCREENSHOT)
tap_point = ImageSearcher.search(SCREENSHOT, "free.png", debugging_enabled=True)
AdbCommandExecutor.execute(f"shell input tap {tap_point[0]} {tap_point[1]}", wait=2)
