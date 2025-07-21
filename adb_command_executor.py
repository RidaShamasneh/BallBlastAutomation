import subprocess
from time import sleep


class AdbCommandExecutor:
    ADB_PATH: str = r"C:\Users\Admin\Downloads\platform-tools-latest-windows\platform-tools\adb.exe"

    @staticmethod
    def execute(args: str, wait=0):
        full_command = f"{AdbCommandExecutor.ADB_PATH} {args}"
        print(f"{full_command=}")

        # Start the process
        process = subprocess.Popen(
            full_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True  # ensures output is returned as strings, not bytes
        )

        stdout, stderr = process.communicate()

        exit_code = process.returncode

        if exit_code == 0:
            print("STDOUT: ", stdout)
            if wait != 0:
                sleep(wait)
        else:
            print("Exit Code: ", exit_code)
            print("STDERR: ", stderr)

        return process.returncode, stdout

    @staticmethod
    def capture_remote_screen(image_name: str):
        command = [AdbCommandExecutor.ADB_PATH, "exec-out", "screencap", "-p"]
        print(f"{command=}")
        with open(image_name, "wb") as f:
            process = subprocess.Popen(command,
                                       stdout=subprocess.PIPE)

            stdout, stderr = process.communicate()

            exit_code = process.returncode

            if exit_code == 0:
                f.write(stdout)
            else:
                print("Exit Code: ", exit_code)
                print("STDERR: ", stderr)
                exit(1)

    @staticmethod
    def is_app_running(app):
        returncode, stdout_pid = AdbCommandExecutor.execute(f"shell pidof {app}")
        return returncode == 0 and stdout_pid != ""

    @staticmethod
    def run_app_and_bring_to_foreground(app):
        command: str = f"shell monkey -p {app} -c android.intent.category.LAUNCHER 1"
        if not AdbCommandExecutor.is_app_running(app):
            # Start application from scratch
            AdbCommandExecutor.execute(command, wait=50)
        else:
            # Bring to foreground
            AdbCommandExecutor.execute(command, wait=2)
