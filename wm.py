import subprocess

def workspaces():
    return subprocess.check_output(["bspc", "query", "-D", "--names"], encoding='utf-8').split()

def current_workspace():
    return subprocess.check_output(["bspc", "query", "-D", "-d", "focused", "--names"], encoding='utf-8').strip()