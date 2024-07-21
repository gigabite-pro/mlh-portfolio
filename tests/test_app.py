import datetime
import unittest
import os 
os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get('/')
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Vaibhav | Portfolio</title>" in html
        # TODO: Add more test relating to the home page
        # Test if exist an external link to LinkedIn
        assert b'https://www.linkedin.com/in/v-sharma03' in response.data

    def test_timeline(self):
        response = self.client.get('/api/timeline_post')
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

        # TODO: Add more test relating to /api/timeline_post GET and POST apis
        # Test POST request 
        post_data_1 = {"name": "John", "email": "john@gmail.com", "content": "Post 1"}
        response = self.client.post('/api/timeline_post', json=post_data_1)
        assert response.is_json
        data = response.get_json()
        assert data["success"] == True
        timeline_post = data["timeline_post"]
        post_id = timeline_post["id"]

        # Verify new post request - GET endpoint
        response = self.client.get('/api/timeline_post')
        assert response.status_code == 200
        assert response.is_json
        data = response.get_json()
        assert "timeline_posts" in data
        timeline_posts = data["timeline_posts"]
        assert len(timeline_posts) == 1

        # Find the newly created timeline post by id
        assert timeline_post["id"] == post_id
        assert timeline_post["name"] == "John"
        assert timeline_post["email"] == "john@gmail.com"
        assert timeline_post["content"] == "Post 1"

        # TODO: Add more test relating to the timeline page

        # Test correct order of post request
        post_data_2 = {"name": "Jane", "email": "jane@gmail.com", "content": "Post 2"}
        self.client.post('/api/timeline_post', json=post_data_2)

        # Retrieve timeline posts and verify sorting by creation time
        response = self.client.get('/api/timeline_post')
        assert response.status_code == 200
        assert response.is_json
        data = response.get_json()
        assert "timeline_posts" in data
        timeline_posts = data["timeline_posts"]
        assert len(timeline_posts) == 2
        # Extract creation timestamps and verify order
        timestamps = [post["created_at"] for post in timeline_posts]
        # Convert each timestamp string to a datetime object
        datetime_timestamps = [datetime.datetime.strptime(ts, "%a, %d %b %Y %H:%M:%S %Z") for ts in timestamps]
        # Ensure timestamps are sorted in ascending order
        assert all(datetime_timestamps[i] <= datetime_timestamps[i+1] for i in range(len(datetime_timestamps) - 1))

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post("/api/timeline_post", json={"email": "john@example.com", "content" : "Hello World, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post("/api/timeline_post", json={"name" : "John Doe", "email": "john@example.com", "content" : ""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request malformed email
        response = self.client.post("/api/timeline_post", json={"name" : "John Doe", "email": "not-an-email", "content" : "Hello World, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html


