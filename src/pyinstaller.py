import os
import sys
import subprocess

def compile_script(script_path, output_dir, log_dir):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

        command = [
            'pyinstaller',
            '--onefile',
            '--add-data', f'{log_dir}:./logs',
            '--distpath', output_dir,
            '--workpath', 'build',
            '--specpath', '.',
            script_path
        ]

        subprocess.check_call(command)

        print("Script compiled successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error compiling script: {e}")
    except Exception as e:
        print(f"Unknown error: {e}")

if __name__ == "__main__":
    script_path = "/home/e6aluga/Desktop/rk3568_test/src/main.py"
    output_dir = "output"
    log_dir = "/home/e6aluga/Desktop/rk3568_test/logs"

    compile_script(script_path, output_dir, log_dir)
