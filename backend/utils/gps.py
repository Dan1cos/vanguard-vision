import random
from typing import Optional, Tuple

from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS


def get_exif_data(image: Image.Image) -> dict:
    """Extract EXIF data from image"""
    exif_data = {}
    try:
        info = image._getexif()
        if info:
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                exif_data[decoded] = value
    except AttributeError:
        pass
    return exif_data


def get_gps_data(exif_data: dict) -> Optional[dict]:
    """Extract GPS data from EXIF"""
    if "GPSInfo" not in exif_data:
        return None

    gps_info = {}
    for key in exif_data["GPSInfo"].keys():
        decode = GPSTAGS.get(key, key)
        gps_info[decode] = exif_data["GPSInfo"][key]

    return gps_info


def convert_to_degrees(value: tuple) -> float:
    """Convert GPS coordinates to degrees in float format"""
    d, m, s = value
    return float(d) + (float(m) / 60.0) + (float(s) / 3600.0)


def extract_gps_coordinates(image: Image.Image) -> Optional[Tuple[float, float]]:
    """
    Extract GPS coordinates (latitude, longitude) from image EXIF data.

    Returns:
        Tuple of (latitude, longitude) or None if GPS data not found
    """
    exif_data = get_exif_data(image)
    gps_data = get_gps_data(exif_data)

    if not gps_data:
        return None

    try:
        # Extract latitude
        lat = None
        if "GPSLatitude" in gps_data and "GPSLatitudeRef" in gps_data:
            lat = convert_to_degrees(gps_data["GPSLatitude"])
            if gps_data["GPSLatitudeRef"] == "S":
                lat = -lat

        # Extract longitude
        lon = None
        if "GPSLongitude" in gps_data and "GPSLongitudeRef" in gps_data:
            lon = convert_to_degrees(gps_data["GPSLongitude"])
            if gps_data["GPSLongitudeRef"] == "W":
                lon = -lon

        if lat is not None and lon is not None:
            return (lat, lon)
    except Exception as e:
        print(f"Error extracting GPS coordinates: {str(e)}")

    return None


def generate_random_coordinates():
    """
    Generate random coordinates near Berlin, Germany.
    Berlin center: 52.5200° N, 13.4050° E
    Range: ±0.5 degrees (approximately ±55km radius)
    """
    lat = random.uniform(52.0, 53.0)
    lon = random.uniform(12.9, 13.9)
    return lat, lon
