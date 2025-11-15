import requests
import json
import os
from PIL import Image, ImageFont, ImageDraw 
from datetime import date
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("OPENWEATHER_API_KEY")

if not api_key:
    raise ValueError("OPENWEATHER_API_KEY environment variable is not set. Please set it in your .env file or environment variables.")
position = [300, 430, 555, 690, 825]

uk_list = ["London", "Manchester", "Edinburgh", "Bristol", "Birmingham"]
india_list = ["Jaipur", "Delhi", "Mumbai", "Kolkata", "Chennai"]
us_list = ["New York", "Chicago", "San Francisco", "Los Angeles", "San Diego"]
country_list = [uk_list, india_list, us_list]

# Check if required files exist
if not os.path.exists("post.png"):
    raise FileNotFoundError("post.png not found. Please ensure the background image is in the project directory.")
if not os.path.exists("Inter.ttf"):
    raise FileNotFoundError("Inter.ttf not found. Please ensure the font file is in the project directory.")

for country in country_list:
    try:
        image = Image.open("post.png")
        # Keep original image mode for drawing, convert to RGB only when saving
        # This preserves the original image appearance
        draw = ImageDraw.Draw(image)
    except FileNotFoundError:
        print(f"Error: Could not open post.png")
        continue
    except Exception as e:
        print(f"Error opening image: {e}")
        continue

    try:
        font_large = ImageFont.truetype('Inter.ttf', size=50)
        font_small = ImageFont.truetype('Inter.ttf', size=30)
    except Exception as e:
        print(f"Error loading font: {e}")
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Use RGBA color if image is RGBA, otherwise RGB
    if image.mode == 'RGBA':
        white_color = (255, 255, 255, 255)
    else:
        white_color = (255, 255, 255)

    content = "Latest Weather Forecast"
    (x, y) = (55, 50)
    draw.text((x, y), content, fill=white_color, font=font_large)

    content = date.today().strftime("%A - %B %d, %Y")
    (x, y) = (55, 145)
    draw.text((x, y), content, fill=white_color, font=font_small)

    index = 0
    for city in country:
        try:
            url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric".format(city, api_key)
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = json.loads(response.text)

            # Check if API returned an error
            if data.get('cod') != 200:
                print(f"Error fetching weather for {city}: {data.get('message', 'Unknown error')}")
                continue

            try:
                font = ImageFont.truetype('Inter.ttf', size=50)
            except:
                font = ImageFont.load_default()
            
            # Use appropriate color format based on image mode
            if image.mode == 'RGBA':
                black_color = (0, 0, 0, 255)
                white_color = (255, 255, 255, 255)
            else:
                black_color = (0, 0, 0)
                white_color = (255, 255, 255)
            
            (x, y) = (135, position[index])
            draw.text((x, y), city, fill=black_color, font=font)

            content = str(int(data['main']['temp'])) + "\u00b0"
            (x, y) = (600, position[index])
            draw.text((x, y), content, fill=white_color, font=font)

            content = str(data['main']['humidity']) + "%"
            (x, y) = (810, position[index])
            draw.text((x, y), content, fill=white_color, font=font)

            index += 1
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data for {city}: {e}")
            continue
        except KeyError as e:
            print(f"Error parsing weather data for {city}: Missing key {e}")
            continue
        except Exception as e:
            print(f"Unexpected error processing {city}: {e}")
            continue
        
    # Save the generated image
    try:
        filename_base = str(date.today()) + country[0]
        # Ensure image is in RGB mode for saving
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image.save(filename_base + ".png", "PNG")
        image.save(filename_base + ".pdf", "PDF", resolution=100.0)
        print(f"Successfully generated forecast for {country[0]}: {filename_base}.png and {filename_base}.pdf")
    except Exception as e:
        print(f"Error saving image for {country[0]}: {e}")
        import traceback
        traceback.print_exc()
        continue
