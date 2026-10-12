import os
import time
from nbs.scripts.bruty_status_process_controls import get_enc_request_pause, update_is_paused
import os
from nbs.configs import read_config
def main():
    print("gail.py test process started")

    worker_pid = os.getpid()
    print(f"Fake worker ID: {worker_pid}")

    config_obj = read_config(
        r"D:\git_repos\bruty_dev_debugging_ghobbs\nbs\scripts\Gail.Hobbs\gh_db.config",
        log_files=False
    )
    config = config_obj["DEFAULT"]

    for progress in range(1, 176):
        pause_requested = get_enc_request_pause(config, worker_pid)

        if pause_requested:
            update_is_paused(config, worker_pid, True)

            while pause_requested:
                print("Pause requested - waiting...")
                time.sleep(2)
                pause_requested = get_enc_request_pause(config, worker_pid)

            update_is_paused(config, worker_pid, False)

        print(f"Processing fake worker step: {progress}")
        time.sleep(1)

    print("gail.py test process finished")


if __name__ == "__main__":
    main()
