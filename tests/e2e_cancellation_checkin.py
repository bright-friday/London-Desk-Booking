import pytest
import requests
from datetime import datetime, timedelta

class TestCancellationAndCheckIn:
    """End-to-end tests for cancellation and check-in"""
    
    def setup_method(self):
        self.base_url = "http://localhost:8000/api"
        self.user_id = "test_user_001"
        self.booking_id = None
    
    def create_booking(self):
        """Helper method to create a test booking"""
        booking_data = {
            "user_id": self.user_id,
            "desk_id": "DESK_A1",
            "date": (datetime.now() + timedelta(days=1)).date().isoformat(),
            "start_time": "09:00",
            "end_time": "17:00"
        }
        response = requests.post(f"{self.base_url}/bookings", json=booking_data)
        return response.json()["booking_id"]
    
    def test_cancellation_before_checkin(self):
        """Test cancellation of booking before check-in window"""
        self.booking_id = self.create_booking()
        
        response = requests.delete(f"{self.base_url}/bookings/{self.booking_id}")
        assert response.status_code == 200
        assert response.json()["status"] == "cancelled"
    
    def test_checkin_updates_desk_status(self):
        """Test that check-in updates desk status in system"""
        self.booking_id = self.create_booking()
        
        checkin_data = {"booking_id": self.booking_id}
        response = requests.post(f"{self.base_url}/checkins", json=checkin_data)
        assert response.status_code == 200
        
        desk_status = requests.get(f"{self.base_url}/desks/DESK_A1/status")
        assert desk_status.json()["status"] == "occupied"
    
    def test_cancellation_after_checkin(self):
        """Test cancellation attempt after check-in"""
        self.booking_id = self.create_booking()
        
        requests.post(f"{self.base_url}/checkins", json={"booking_id": self.booking_id})
        
        response = requests.delete(f"{self.base_url}/bookings/{self.booking_id}")
        assert response.status_code == 400  # Bad request - already checked in
    
    def test_checkout_frees_desk(self):
        """Test that checkout frees up the desk for others"""
        self.booking_id = self.create_booking()
        
        requests.post(f"{self.base_url}/checkins", json={"booking_id": self.booking_id})
        response = requests.post(f"{self.base_url}/checkouts", json={"booking_id": self.booking_id})
        assert response.status_code == 200
        
        desk_status = requests.get(f"{self.base_url}/desks/DESK_A1/status")
        assert desk_status.json()["status"] == "available"
    
    def test_late_checkin_notification(self):
        """Test that late check-in triggers notifications"""
        self.booking_id = self.create_booking()
        
        late_checkin_data = {
            "booking_id": self.booking_id,
            "checkin_time": (datetime.now() + timedelta(hours=1)).isoformat()
        }
        response = requests.post(f"{self.base_url}/checkins", json=late_checkin_data)
        
        notifications = requests.get(f"{self.base_url}/notifications/admin")
        assert any("late" in n["message"].lower() for n in notifications.json())

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
