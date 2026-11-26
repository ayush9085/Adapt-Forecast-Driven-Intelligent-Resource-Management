import platform
import os

def is_linux() -> bool:
    return platform.system().lower() == "linux"

def is_cgroup_v2_available() -> bool:
    if not is_linux():
        return False
    cgroup_root = "/sys/fs/cgroup"
    controllers_file = os.path.join(cgroup_root, "cgroup.controllers")
    return os.path.exists(controllers_file)

def get_system_summary() -> dict:
    return {
        "os": platform.system(),
        "release": platform.release(),
        "is_linux": is_linux(),
        "cgroup_v2": is_cgroup_v2_available()
    }
