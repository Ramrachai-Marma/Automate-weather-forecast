# 🌤️ Automated Weather Forecast Generator

A Python automation tool that fetches real-time weather data from OpenWeatherMap API and generates beautiful visual weather forecast images for multiple cities across different countries. The tool creates both PNG and PDF outputs with formatted weather information.

## ✨ Features

- 🌍 **Multi-Country Support**: Automatically generates weather forecasts for cities in UK, India, and USA
- 🎨 **Visual Output**: Creates professional-looking weather forecast images with custom fonts and styling
- 📄 **Multiple Formats**: Exports forecasts in both PNG and PDF formats
- 📅 **Date Stamped**: Each output file includes the current date in the filename
- 🔄 **Automated**: Runs through all configured cities and countries automatically

## 📋 Prerequisites

- Python 3.6 or higher
- OpenWeatherMap API key ([Get one here](https://openweathermap.org/api))
- Required Python packages (see `requirements.txt`)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Automate-weather-forecast.git
   cd Automate-weather-forecast
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   
   Create a `.env` file in the project root:
   ```env
   OPENWEATHER_API_KEY=your_api_key_here
   ```
   
   Or set it as an environment variable:
   - **Windows (PowerShell):**
     ```powershell
     $env:OPENWEATHER_API_KEY="your_api_key_here"
     ```
   - **Linux/Mac:**
     ```bash
     export OPENWEATHER_API_KEY="your_api_key_here"
     ```

4. **Ensure required assets are present**
   - `post.png` - Background template image
   - `Inter.ttf` - Font file for text rendering

## 📖 Usage

Run the script:
```bash
python wapi.py
```

The script will:
1. Fetch weather data for all configured cities
2. Generate weather forecast images for each country
3. Save output files in the format: `YYYY-MM-DD[Country].png` and `YYYY-MM-DD[Country].pdf`

### Example Output Files
- `2024-01-15London.png` / `2024-01-15London.pdf`
- `2024-01-15Jaipur.png` / `2024-01-15Jaipur.pdf`
- `2024-01-15New York.png` / `2024-01-15New York.pdf`

## 🏙️ Configured Cities

### United Kingdom
- London
- Manchester
- Edinburgh
- Bristol
- Birmingham

### India
- Jaipur
- Delhi
- Mumbai
- Kolkata
- Chennai

### United States
- New York
- Chicago
- San Francisco
- Los Angeles
- San Diego

## 🛠️ Customization

You can customize the cities by editing the lists in `wapi.py`:
```python
uk_list = ["London", "Manchester", "Edinburgh", "Bristol", "Birmingham"]
india_list = ["Jaipur", "Delhi", "Mumbai", "Kolkata", "Chennai"]
us_list = ["New York", "Chicago", "San Francisco", "Los Angeles", "San Diego"]
```

## 📦 Dependencies

- `requests` - HTTP library for API calls
- `Pillow` - Image processing library
- `python-dotenv` - Environment variable management

## 🔒 Security

**Important**: Never commit your API key to the repository. The `.gitignore` file is configured to exclude `.env` files. Always use environment variables for sensitive information.

## 📝 Project Structure

```
Automate-weather-forecast/
├── wapi.py              # Main script
├── post.png             # Background template
├── story.png            # Additional template (if needed)
├── Inter.ttf            # Font file
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore rules
├── LICENSE             # License file
└── README.md           # This file
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenWeatherMap](https://openweathermap.org/) for providing the weather API
- [Pillow](https://python-pillow.org/) for image processing capabilities

## 📧 Contact

If you have any questions or suggestions, please open an issue on GitHub.

---

⭐ If you find this project helpful, please consider giving it a star!
