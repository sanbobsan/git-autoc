from app.core.config import settings


def main():
    for key, value in settings.model_dump().items():
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
