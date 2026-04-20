import pytest
import requests
from datetime import datetime, timedelta

class TestReportingAndAnalytics:
    """End-to-end tests for reporting and analytics"""
    
    def setup_method(self):
        self.base_url = "http://localhost:8000/api"
    
    def test_booking_activity_report(self):
        """Test generation of booking activity report"""
        response = requests.get(
            f"{self.base_url}/reports/booking-activity",
            params={"start_date": "2026-04-01", "end_date": "2026-04-30"}
        )
        
        assert response.status_code == 200
        report = response.json()
        assert "total_bookings" in report
        assert "bookings_by_date" in report
        assert "peak_hours" in report
    
    def test_desk_utilization_analytics(self):
        """Test desk utilization analytics accuracy"""
        response = requests.get(
            f"{self.base_url}/analytics/desk-utilization",
            params={"start_date": "2026-04-01", "end_date": "2026-04-30"}
        )
        
        assert response.status_code == 200
        analytics = response.json()
        assert "average_utilization" in analytics
        assert "desk_details" in analytics
        
        for desk in analytics["desk_details"]:
            assert 0 <= desk["utilization_percentage"] <= 100
    
    def test_user_booking_history(self):
        """Test accuracy of user booking history"""
        user_id = "test_user_001"
        response = requests.get(f"{self.base_url}/users/{user_id}/bookings")
        
        assert response.status_code == 200
        bookings = response.json()
        assert isinstance(bookings, list)
        assert all("booking_id" in b and "date" in b for b in bookings)
    
    def test_data_export_csv(self):
        """Test data export to CSV format"""
        response = requests.get(
            f"{self.base_url}/exports/bookings.csv",
            params={"start_date": "2026-04-01", "end_date": "2026-04-30"}
        )
        
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "text/csv"
    
    def test_analytics_dashboard_data(self):
        """Test dashboard data accuracy and timeliness"""
        response = requests.get(f"{self.base_url}/dashboard/metrics")
        
        assert response.status_code == 200
        metrics = response.json()
        assert "total_desks" in metrics
        assert "available_desks" in metrics
        assert "booked_desks" in metrics
        assert metrics["total_desks"] == metrics["available_desks"] + metrics["booked_desks"]

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
