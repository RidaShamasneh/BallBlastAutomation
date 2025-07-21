from adb_command_executor import AdbCommandExecutor
from image_searcher import ImageSearcher

DEVICE_IP_PORT: str = "localhost:5555"
SCREENSHOT = "screenshot.png"

AdbCommandExecutor.execute(f"connect {DEVICE_IP_PORT}")

# Launch Ball Blast game
AdbCommandExecutor.execute(f"shell monkey -p com.nomonkeys.ballblast -c android.intent.category.LAUNCHER 1", wait=30)

AdbCommandExecutor.capture_remote_screen(SCREENSHOT)
tap_point = ImageSearcher.search(SCREENSHOT, "shop_icon.png", debugging_enabled=False)
AdbCommandExecutor.execute(f"shell input tap {tap_point[0]} {tap_point[1]}", wait=2)

# Collecting free shots every day
AdbCommandExecutor.execute(f"shell input swipe 300 1000 300 300 300", wait=4)
AdbCommandExecutor.capture_remote_screen(SCREENSHOT)
tap_point = ImageSearcher.search(SCREENSHOT, "free.png", debugging_enabled=False)
AdbCommandExecutor.execute(f"shell input tap {tap_point[0]} {tap_point[1]}", wait=2)
