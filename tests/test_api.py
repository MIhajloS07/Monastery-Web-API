import unittest
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

class TestMonasteryAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = app.test_client()
        response = cls.client.post('/api/monasteries', json={
            "name": "Gracanica",
            "location": "Kosovo i Metohija",
            "year_of_construction": 1315
        })
        data = response.get_json()
        cls.created_id = data["id"]
        
    @classmethod
    def tearDownClass(cls) -> None:
        if hasattr(cls, "created_id"):
            cls.client.delete(f'/api/monasteries/{cls.created_id}')
      
    def test_get_all_monasteries(self) -> None:
        response = self.client.get('/api/monasteries')
        self.assertIn(response.status_code, [200, 404])
        
    def test_get_monastery_by_id(self) -> None:
        response = self.client.get(f'/api/monasteries/{self.__class__.created_id}')
        self.assertIn(response.status_code, [200, 404])
        
    def test_get_monastery_by_location(self) -> None:
        test_location = "Nis"
        response = self.client.get(f'/api/monasteries/location/{test_location}')
        self.assertIn(response.status_code, [200, 404])
        
    def test_get_monastery_by_year_of_construction(self) -> None:
        test_year = 1300
        response = self.client.get(f'/api/monasteries/year/{test_year}')
        self.assertIn(response.status_code, [200, 404])
        
    def test_get_monasteries_by_name(self) -> None:
        test_name = "Test"
        response = self.client.get(f'/api/monasteries/name/{test_name}')
        self.assertIn(response.status_code, [200, 404])
    
    def test_add_monastery(self) -> None:
        response = self.client.post('/api/monasteries', json={
            "name": "Gracanica",
            "location": "Kosovo i Metohija",
            "year_of_construction": 1315
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data["name"], "Gracanica")
        self.client.delete(f'/api/monasteries/{data["id"]}')
    
    def test_add_monastery_missing_fields(self) -> None:
        response = self.client.post('/api/monasteries', json={
            "name": "Gracanica",
            "year_of_construction": 1315
            # missing field
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)
        self.assertIn("Missing required fields", data["error"])
    
    def test_add_monastery_invalid_year(self) -> None:
        response = self.client.post('/api/monasteries', json={
            "name": "Gracanica",
            "location": "Kosovo i Metohija",
            "year_of_construction": -100  # Invalid value
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)
        self.assertIn("Year of construction must be a positive number", data["error"])
    
    def test_update_monastery(self) -> None:
        response = self.client.put(f'/api/monasteries/{self.__class__.created_id}', json={
            "name": "Gracanica Updated",
            "location": "Kosovo i Metohija",
            "year_of_construction": 1316
        })
        self.assertIn(response.status_code, [200, 404])
    
    def test_update_monastery_one_value(self) -> None:
        response = self.client.post('/api/monasteries', json={
            "name": "Test Monastery",
            "location": "Test Location",
            "year_of_construction": 1200
        })
        data = response.get_json()
        test_id = data["id"]
        response = self.client.put(f'/api/monasteries/{test_id}', json={
            "year_of_construction": 1316
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)
        self.assertIn("Missing field", data["error"])
        self.client.delete(f'/api/monasteries/{test_id}')
    
    def test_patch_monastery(self) -> None:
        response = self.client.patch(f'/api/monasteries/{self.__class__.created_id}', json={
            "location": "Novi Sad"
        })
        self.assertIn(response.status_code, [200, 404])
    
    def test_delete_monastery(self) -> None:
        test_id = self.__class__.created_id
        response = self.client.delete(f'/api/monasteries/{test_id}')
        self.assertIn(response.status_code, [200, 404])   

if __name__ == '__main__':
    unittest.main()