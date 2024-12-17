import tensorflow as tf

from yoga_pose_recognition.main import run


def main() -> None:
    """Entrypoint of the application."""
    run()


if __name__ == "__main__":
    print(
        "Num GPUs Available: ",
        len(tf.config.experimental.list_physical_devices("GPU")),
    )
    main()
