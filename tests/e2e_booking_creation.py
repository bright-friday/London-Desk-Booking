import pytest
import requests
from datetime import datetime, timedelta

class TestBookingCreation:
    """End-to-end tests for desk booking creation"""
    
    def setup_method(self):
        self.base_url = "http://localhost:8000/api"
        self.user_id = "test_user_001"
        self.desk_ids = ["DESK_A1", "DESK_A2", "DESK_B1"]
    
    def test_successful_booking_creation(self):
        """Test successful creation of a desk booking"""
        booking_data = {
            "user_id": self.user_id,
            "desk_id": self.desk_ids[0],
            "date": (datetime.now() + timedelta(days=1)).date().isoformat(),
            "start_time": "09:00",
            "end_time": "17:00"
        }
        
        response = requests.post(f"{self.base_url}/bookings", json=booking_data)
        assert response.status_code == 201
        assert response.json()["status"] == "confirmed"
    
    def test_booking_with_overlapping_times(self):
        """Test booking creation with overlapping desk usage"""
        booking_data_1 = {
            "user_id": self.user_id,
            "desk_id": self.desk_ids[0],
            "date": (datetime.now() + timedelta(days=1)).date().isoformat(),
            "start_time": "09:00",
            "end_time": "12:00"
        }
        
        response_1 = requests.post(f"{self.base_url}/bookings", json=booking_data_1)
        assert response_1.status_code == 201
        
        booking_data_2 = {
            "user_id": "test_user_002",
            "desk_id": self.desk_ids[0],
            "date": (datetime.now() + timedelta(days=1)).date().isoformat(),
            "start_time": "11:00",
            "end_time": "14:00"
        }
        
        response_2 = requests.post(f"{self.base_url}/bookings", json=booking_data_2)
        assert response_2.status_code == 409  # Conflict
    
    def test_booking_confirmation_notification(self):
        """Test that confirmation notifications are sent"""
        booking_data = {
            "user_id": self.user_id,
            "desk_id": self.desk_ids[1],
            "date": (datetime.now() + timedelta(days=1)).date().isoformat(),
            "start_time": "10:00",
            "end_time": "15:00"
        }
        
        response = requests.post(f"{self.base_url}/bookings", json=booking_data)
        booking_id = response.json()["booking_id"]
        
        notification_response = requests.get(f"{self.base_url}/notifications/{self.user_id}")
        assert notification_response.status_code == 200
        notifications = notification_response.json()
        assert any(n["booking_id"] == booking_id for n in notifications)
    
    def test_booking_permission_validation(self):
        """Test that users can only book desks they have access to"""
        restricted_desk_data = {
            "user_id": "restricted_user",
            "desk_id": "RESTRICTED_DESK",
            "date": (datetime.now() + timedelta(days=1)).date().isoformat(),
            "start_time": "09:00",
            "end_time": "17:00"
        }
        
        response = requests.post(f"{self.base_url}/bookings", json=restricted_desk_data)
        assert response.status_code == 403  # Forbidden

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
