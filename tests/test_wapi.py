import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

from PIL import Image
import requests

import wapi


class FakeResponse:
    def __init__(self, payload, status_error=None):
        self.payload = payload
        self.status_error = status_error

    def raise_for_status(self):
        if self.status_error:
            raise self.status_error

    def json(self):
        return self.payload


class WeatherReportTests(unittest.TestCase):
    @patch("wapi.requests.get")
    def test_fetch_weather_parses_temperature_and_humidity(self, mock_get):
        mock_get.return_value = FakeResponse(
            {"cod": 200, "main": {"temp": 18.9, "humidity": 55}}
        )

        result = wapi.fetch_weather("Test City", "test-key")

        self.assertEqual(result, {"temperature": 18, "humidity": 55})
        self.assertEqual(mock_get.call_args.kwargs["timeout"], 10)

    @patch("wapi.requests.get")
    def test_fetch_weather_reports_api_errors(self, mock_get):
        mock_get.return_value = FakeResponse(
            {"cod": "401", "message": "invalid API key"}
        )

        with self.assertRaisesRegex(ValueError, "invalid API key"):
            wapi.fetch_weather("Test City", "bad-key")

    @patch("wapi.requests.get")
    def test_fetch_weather_reports_missing_fields(self, mock_get):
        mock_get.return_value = FakeResponse({"cod": 200, "main": {}})

        with self.assertRaisesRegex(ValueError, "missing valid temperature or humidity"):
            wapi.fetch_weather("Test City", "test-key")

    @patch("wapi.fetch_weather")
    def test_create_report_writes_png_and_pdf(self, mock_fetch_weather):
        mock_fetch_weather.return_value = {"temperature": 18, "humidity": 55}
        with tempfile.TemporaryDirectory() as temporary_directory:
            project_dir = Path(temporary_directory)
            Image.new("RGB", (1000, 1000), "white").save(project_dir / "post.png")
            with patch.object(wapi, "PROJECT_DIR", project_dir):
                complete = wapi.create_report(
                    "Test Region",
                    ["Test City"],
                    "test-key",
                    date(2026, 11, 11),
                )

            self.assertTrue(complete)
            self.assertTrue((project_dir / "2026-11-11Test Region.png").is_file())
            self.assertTrue((project_dir / "2026-11-11Test Region.pdf").is_file())

    @patch("wapi.fetch_weather", side_effect=requests.Timeout("request timed out"))
    def test_report_is_incomplete_when_city_request_fails(self, _mock_fetch_weather):
        with tempfile.TemporaryDirectory() as temporary_directory:
            project_dir = Path(temporary_directory)
            Image.new("RGB", (1000, 1000), "white").save(project_dir / "post.png")
            with patch.object(wapi, "PROJECT_DIR", project_dir):
                complete = wapi.create_report(
                    "Test Region",
                    ["Test City"],
                    "test-key",
                    date(2026, 11, 11),
                )

            self.assertFalse(complete)
            self.assertFalse((project_dir / "2026-11-11Test Region.png").exists())


if __name__ == "__main__":
    unittest.main()
