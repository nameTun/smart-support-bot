# Entry-point cho Data Pipeline (Scrape -> Delta Sync -> Gemini Upload)
import os
from dotenv import load_dotenv


def main():
    load_dotenv()
    print("Starting Smart Support Bot Pipeline...")


if __name__ == "__main__":
    main()
