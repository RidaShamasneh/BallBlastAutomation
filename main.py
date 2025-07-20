from time import sleep

from adb_command_executor import AdbCommandExecutor
from image_searcher import ImageSearcher

DEVICE_IP_PORT: str = "localhost:5555"
SCREENSHOT = "screenshot.png"

AdbCommandExecutor.execute(f"connect {DEVICE_IP_PORT}")
AdbCommandExecutor.capture_remote_screen(SCREENSHOT)

tap_point = ImageSearcher.search(SCREENSHOT, "shop_icon.png", debugging_enabled=False)
AdbCommandExecutor.execute(f"shell input tap {tap_point[0]} {tap_point[1]}")



