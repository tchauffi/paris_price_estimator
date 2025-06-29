"""This modul provides tools for geolocation using various geocoding services."""

from geopy.geocoders import Nominatim


def address_to_coordinates(address: str):
    """Convert address to GPS coordinates using Nominatim (OpenStreetMap).

    Args:
        address (str): Address to be geocoded.

    Returns:
        tuple: A tuple containing latitude and longitude of the address, or (None, None)
          if not found.
    """
    geolocator = Nominatim(user_agent="price_estimator")
    try:
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        print(f"Error geocoding {address}: {e}")
        return None, None


def coordinates_to_address(latitude: float, longitude: float):
    """Convert GPS coordinates to address using Nominatim (OpenStreetMap).

    Args:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.

    Returns:
        str: Address corresponding to the GPS coordinates, or None if not found.
    """
    geolocator = Nominatim(user_agent="price_estimator")
    try:
        location = geolocator.reverse((latitude, longitude))
        if location:
            return location.address
        else:
            return None
    except Exception as e:
        print(f"Error reverse geocoding ({latitude}, {longitude}): {e}")
        return None
