import subprocess

# Путь к терминалу и команда для выполнения
terminal = "weston-terminal"
script_command = "python3 /opt/rk3568_test/src/main.py"

# Запуск терминала с командой
subprocess.Popen([terminal, "-e", script_command])

#weston-terminal -e python3 /opt/rk3568_test/src/main.py