import unittest
from main import app


class ApiTest(unittest.TestCase):
    
    def test1_post(self):
        tester = app.test_client(self)
        response = tester.post(
            '/agendamento', 
            json={
                "id_agendamento": 100,
                "id_usuario": 11,
                "dt_envio": "2022/12/11",
                "formato_comunicacao": "Whatsapp"
            }
        )
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test2_get(self):
        tester = app.test_client(self)
        response = tester.get(
            '/status/100'
        )
        self.assertEqual(response.content_type, 'application/json')


    def test3_patch(self):
        tester = app.test_client(self)
        response = tester.patch(
            '/cancelamento/100', 
            json={
                "status_agendamento": "cancelado"
            }
        )
        self.assertTrue(b"cancelado" in response.data)

'''if __name__ == "__main__":
    unittest.main()'''