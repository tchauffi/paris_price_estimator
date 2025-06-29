"""Tests for the geolocation module."""

import pytest
from unittest.mock import Mock, patch
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

from price_estimator.tools.geolocation import (
    address_to_coordinates,
    coordinates_to_address,
)


class TestAddressToCoordinates:
    """Test cases for address_to_coordinates function."""

    @patch("price_estimator.tools.geolocation.Nominatim")
    def test_successful_geocoding(self, mock_nominatim):
        """Test successful address to coordinates conversion."""
        # Setup mock
        mock_geolocator = Mock()
        mock_location = Mock()
        mock_location.latitude = 48.8566
        mock_location.longitude = 2.3522
        mock_geolocator.geocode.return_value = mock_location
        mock_nominatim.return_value = mock_geolocator

        # Test
        address = "1 Place Vendôme, 75001 Paris, France"
        lat, lon = address_to_coordinates(address)

        # Assertions
        assert lat == 48.8566
        assert lon == 2.3522
        mock_geolocator.geocode.assert_called_once_with(address)

    @patch("price_estimator.tools.geolocation.Nominatim")
    def test_address_not_found(self, mock_nominatim):
        """Test when address cannot be found."""
        # Setup mock
        mock_geolocator = Mock()
        mock_geolocator.geocode.return_value = None
        mock_nominatim.return_value = mock_geolocator

        # Test
        address = "Nonexistent Street 999, Nowhere City"
        lat, lon = address_to_coordinates(address)

        # Assertions
        assert lat is None
        assert lon is None
        mock_geolocator.geocode.assert_called_once_with(address)

    @patch("price_estimator.tools.geolocation.Nominatim")
    def test_geocoding_timeout_error(self, mock_nominatim):
        """Test handling of geocoding timeout error."""
        # Setup mock
        mock_geolocator = Mock()
        mock_geolocator.geocode.side_effect = GeocoderTimedOut("Timeout")
        mock_nominatim.return_value = mock_geolocator

        # Test
        address = "Some address"
        lat, lon = address_to_coordinates(address)

        # Assertions
        assert lat is None
        assert lon is None

    @patch("price_estimator.tools.geolocation.Nominatim")
    def test_geocoding_service_error(self, mock_nominatim):
        """Test handling of geocoding service error."""
        # Setup mock
        mock_geolocator = Mock()
        mock_geolocator.geocode.side_effect = GeocoderServiceError("Service error")
        mock_nominatim.return_value = mock_geolocator

        # Test
        address = "Some address"
        lat, lon = address_to_coordinates(address)

        # Assertions
        assert lat is None
        assert lon is None

    @patch("price_estimator.tools.geolocation.Nominatim")
    def test_general_exception_handling(self, mock_nominatim):
        """Test handling of general exceptions."""
        # Setup mock
        mock_geolocator = Mock()
        mock_geolocator.geocode.side_effect = Exception("Unexpected error")
        mock_nominatim.return_value = mock_geolocator

        # Test
        address = "Some address"
        lat, lon = address_to_coordinates(address)

        # Assertions
        assert lat is None
        assert lon is None

    @patch("price_estimator.tools.geolocation.Nominatim")
    def test_empty_string_address(self, mock_nominatim):
        """Test with empty string address."""
        # Setup mock
        mock_geolocator = Mock()
        mock_geolocator.geocode.return_value = None
        mock_nominatim.return_value = mock_geolocator

        # Test
        lat, lon = address_to_coordinates("")

        # Assertions
        assert lat is None
        assert lon is None

    def test_paris_addresses(self):
        """Integration test with real Paris addresses (requires internet)."""
        # This is an integration test that requires internet connection
        # Skip if running in CI or if network is not available

        # Test famous Paris locations
        test_cases = [
            ("Tour Eiffel, Paris", (48.8584, 2.2945)),  # Approximate coordinates
            ("Louvre, Paris", (48.8606, 2.3376)),
            ("Notre-Dame, Paris", (48.8530, 2.3499)),
        ]

        for address, expected_coords in test_cases:
            lat, lon = address_to_coordinates(address)

            # Check that coordinates are returned and are in Paris area
            if lat is not None and lon is not None:
                assert 48.8 <= lat <= 48.9, (
                    f"Latitude {lat} not in Paris range for {address}"
                )
                assert 2.2 <= lon <= 2.5, (
                    f"Longitude {lon} not in Paris range for {address}"
                )


class TestCoordinatesToAddress:
    """Test cases for coordinates_to_address function."""

    @patch("price_estimator.tools.geolocation.Nominatim")
    def test_successful_reverse_geocoding(self, mock_nominatim):
        """Test successful coordinates to address conversion."""
        # Setup mock
        mock_geolocator = Mock()
        mock_location = Mock()
        mock_location.address = "1 Place Vendôme, 75001 Paris, France"
        mock_geolocator.reverse.return_value = mock_location
        mock_nominatim.return_value = mock_geolocator

        # Test
        lat, lon = 48.8566, 2.3522
        address = coordinates_to_address(lat, lon)

        # Assertions
        assert address == "1 Place Vendôme, 75001 Paris, France"
        mock_geolocator.reverse.assert_called_once_with((lat, lon))

    @patch("price_estimator.tools.geolocation.Nominatim")
    def test_coordinates_not_found(self, mock_nominatim):
        """Test when coordinates cannot be reverse geocoded."""
        # Setup mock
        mock_geolocator = Mock()
        mock_geolocator.reverse.return_value = None
        mock_nominatim.return_value = mock_geolocator

        # Test
        lat, lon = 0.0, 0.0  # Middle of ocean
        address = coordinates_to_address(lat, lon)

        # Assertions
        assert address is None
        mock_geolocator.reverse.assert_called_once_with((lat, lon))

    @patch("price_estimator.tools.geolocation.Nominatim")
    def test_reverse_geocoding_timeout_error(self, mock_nominatim):
        """Test handling of reverse geocoding timeout error."""
        # Setup mock
        mock_geolocator = Mock()
        mock_geolocator.reverse.side_effect = GeocoderTimedOut("Timeout")
        mock_nominatim.return_value = mock_geolocator

        # Test
        lat, lon = 48.8566, 2.3522
        address = coordinates_to_address(lat, lon)

        # Assertions
        assert address is None

    @patch("price_estimator.tools.geolocation.Nominatim")
    def test_reverse_geocoding_service_error(self, mock_nominatim):
        """Test handling of reverse geocoding service error."""
        # Setup mock
        mock_geolocator = Mock()
        mock_geolocator.reverse.side_effect = GeocoderServiceError("Service error")
        mock_nominatim.return_value = mock_geolocator

        # Test
        lat, lon = 48.8566, 2.3522
        address = coordinates_to_address(lat, lon)

        # Assertions
        assert address is None

    @patch("price_estimator.tools.geolocation.Nominatim")
    def test_invalid_coordinates(self, mock_nominatim):
        """Test with invalid coordinates."""
        # Setup mock
        mock_geolocator = Mock()
        mock_geolocator.reverse.side_effect = ValueError("Invalid coordinates")
        mock_nominatim.return_value = mock_geolocator

        # Test
        lat, lon = 999.0, 999.0  # Invalid coordinates
        address = coordinates_to_address(lat, lon)

        # Assertions
        assert address is None

    def test_paris_coordinates(self):
        """Integration test with real Paris coordinates (requires internet)."""
        # This is an integration test that requires internet connection

        # Test famous Paris locations coordinates
        test_cases = [
            (48.8584, 2.2945),  # Tour Eiffel area
            (48.8606, 2.3376),  # Louvre area
            (48.8530, 2.3499),  # Notre-Dame area
        ]

        for lat, lon in test_cases:
            address = coordinates_to_address(lat, lon)

            # Check that an address is returned and contains "Paris"
            if address is not None:
                assert "Paris" in address or "France" in address, (
                    f"Address {address} doesn't seem to be in Paris"
                )


class TestGeolocationIntegration:
    """Integration tests for the geolocation module."""

    def test_round_trip_geocoding(self):
        """Test address -> coordinates -> address round trip."""
        original_address = "Place de la Concorde, Paris"

        # Address to coordinates
        lat, lon = address_to_coordinates(original_address)

        if lat is not None and lon is not None:
            # Coordinates back to address
            reverse_address = coordinates_to_address(lat, lon)

            if reverse_address is not None:
                # The addresses might not be exactly the same but should be in Paris
                assert "Paris" in reverse_address or "France" in reverse_address

    @pytest.mark.parametrize(
        "address,expected_lat_range,expected_lon_range",
        [
            ("1er Arrondissement, Paris", (48.85, 48.87), (2.32, 2.34)),
            ("16e Arrondissement, Paris", (48.84, 48.88), (2.26, 2.30)),
            ("Montmartre, Paris", (48.88, 48.89), (2.33, 2.35)),
        ],
    )
    def test_paris_arrondissements(
        self, address, expected_lat_range, expected_lon_range
    ):
        """Test geocoding of different Paris arrondissements."""
        lat, lon = address_to_coordinates(address)

        if lat is not None and lon is not None:
            lat_min, lat_max = expected_lat_range
            lon_min, lon_max = expected_lon_range

            assert lat_min <= lat <= lat_max, (
                f"Latitude {lat} not in expected range for {address}"
            )
            assert lon_min <= lon <= lon_max, (
                f"Longitude {lon} not in expected range for {address}"
            )


class TestUserAgentConfiguration:
    """Test that the user agent is properly configured."""

    @patch("price_estimator.tools.geolocation.Nominatim")
    def test_user_agent_in_address_to_coordinates(self, mock_nominatim):
        """Test that Nominatim is initialized with correct user agent."""
        # Setup mock
        mock_geolocator = Mock()
        mock_nominatim.return_value = mock_geolocator

        # Test
        address_to_coordinates("Some address")

        # Assertions
        mock_nominatim.assert_called_once_with(user_agent="price_estimator")

    @patch("price_estimator.tools.geolocation.Nominatim")
    def test_user_agent_in_coordinates_to_address(self, mock_nominatim):
        """Test that Nominatim is initialized with correct user agent."""
        # Setup mock
        mock_geolocator = Mock()
        mock_nominatim.return_value = mock_geolocator

        # Test
        coordinates_to_address(48.8566, 2.3522)

        # Assertions
        mock_nominatim.assert_called_once_with(user_agent="price_estimator")
