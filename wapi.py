"""Generate regional weather reports from the OpenWeatherMap current-weather API."""

import logging
import os
from datetime import date
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

PROJECT_DIR = Path(__file__).resolve().parent
API_URL = "https://api.openweathermap.org/data/2.5/weather"
CITY_GROUPS = {
    "London": ["London", "Manchester", "Edinburgh", "Bristol", "Birmingham"],
    "Jaipur": ["Jaipur", "Delhi", "Mumbai", "Kolkata", "Chennai"],
    "New York": ["New York", "Chicago", "San Francisco", "Los Angeles", "San Diego"],
}
ROW_POSITIONS = [300, 430, 555, 690, 825]

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def fetch_weather(city: str, api_key: str) -> dict[str, Any]:
    """Fetch and validate current weather for one city."""
    response = requests.get(
        API_URL,
        params={"q": city, "appid": api_key, "units": "metric"},
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()

    if data.get("cod") != 200:
        raise ValueError(f"OpenWeatherMap returned an error for {city}: {data.get('message')}")

    try:
        return {
            "temperature": int(data["main"]["temp"]),
            "humidity": int(data["main"]["humidity"]),
        }
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError(f"Weather response for {city} is missing valid temperature or humidity") from error


def load_font(path: Path, size: int) -> ImageFont.ImageFont:
    """Load the project font, falling back to Pillow's built-in font."""
    try:
        return ImageFont.truetype(str(path), size=size)
    except OSError:
        logger.warning("Could not load font %s; using the default font.", path)
        return ImageFont.load_default()


def create_report(region: str, cities: list[str], api_key: str, report_date: date) -> bool:
    """Render a regional report and save it as PNG and PDF."""
    if not cities:
        raise ValueError(f"No cities are configured for the {region} report.")
    if len(cities) > len(ROW_POSITIONS):
        raise ValueError(
            f"The {region} report supports at most {len(ROW_POSITIONS)} cities."
        )

    template_path = PROJECT_DIR / "post.png"
    font_path = PROJECT_DIR / "Inter.ttf"
    if not template_path.is_file():
        raise FileNotFoundError(f"Report template not found: {template_path}")

    with Image.open(template_path) as template:
        image = template.copy()

    draw = ImageDraw.Draw(image)
    font_large = load_font(font_path, 50)
    font_small = load_font(font_path, 30)
    foreground = (255, 255, 255)
    text_color = (0, 0, 0)

    draw.text((55, 50), "Latest Weather Forecast", fill=foreground, font=font_large)
    draw.text(
        (55, 145),
        report_date.strftime("%A - %B %d, %Y"),
        fill=foreground,
        font=font_small,
    )

    successes = 0
    for row, city in enumerate(cities):
        try:
            weather = fetch_weather(city, api_key)
        except (requests.RequestException, ValueError) as error:
            logger.error("Skipping %s: %s", city, error)
            continue

        y_position = ROW_POSITIONS[row]
        draw.text((135, y_position), city, fill=text_color, font=font_large)
        draw.text(
            (600, y_position),
            f"{weather['temperature']}°",
            fill=foreground,
            font=font_large,
        )
        draw.text(
            (810, y_position),
            f"{weather['humidity']}%",
            fill=foreground,
            font=font_large,
        )
        successes += 1

    if not successes:
        logger.error("No weather data was retrieved for the %s report.", region)
        return False

    filename_base = f"{report_date.isoformat()}{region}"
    png_path = PROJECT_DIR / f"{filename_base}.png"
    pdf_path = PROJECT_DIR / f"{filename_base}.pdf"
    image = image.convert("RGB")
    image.save(png_path, "PNG")
    image.save(pdf_path, "PDF", resolution=100.0)
    logger.info("Saved %s and %s", png_path.name, pdf_path.name)
    return successes == len(cities)


def main() -> int:
    """Generate reports for all configured regions."""
    load_dotenv(PROJECT_DIR / ".env")
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        logger.error("Set OPENWEATHER_API_KEY in the environment or project .env file.")
        return 1

    failed = False
    for region, cities in CITY_GROUPS.items():
        try:
            complete = create_report(region, cities, api_key, date.today())
        except (FileNotFoundError, OSError) as error:
            logger.error("Could not create the %s report: %s", region, error)
            complete = False
        failed = failed or not complete

    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
