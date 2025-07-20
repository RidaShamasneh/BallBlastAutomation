import subprocess


class AdbCommandExecutor:
    ADB_PATH: str = r"C:\Users\Admin\Downloads\platform-tools-latest-windows\platform-tools\adb.exe"

    @staticmethod
    def execute(args: str):
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
        else:
            print("Exit Code: ", exit_code)
            print("STDERR: ", stderr)
            exit(1)

        return process.returncode

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
