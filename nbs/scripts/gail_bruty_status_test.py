import time


def main():
    print("gail.py test process started")

    for progress in range(1, 201):
        print(f"Progress: {progress}")
        time.sleep(1)

    print("gail.py test process finished")


if __name__ == "__main__":
    main()
