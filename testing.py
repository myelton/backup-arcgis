import unittest
import json
import backup_arcgis as backup
import os.path

settings = json.load(open('./resources/settings.json'))


class TestColdbrewHostingServer(unittest.TestCase):

    def test_initialization_token(self):
        server = backup.ArcgisServer(
            url=settings['url'],
            username=settings['username'],
            password=settings['password']
        )
        token = server._token
        self.assertGreater(len(token), 60)

    def test_agssite_file(self):
        testing_file = os.path.join(os.path.dirname(__file__), 'resources', 'test.agssite')
        if os.path.exists(testing_file):
            os.remove(testing_file)
        server = backup.ArcgisServer(
            url=settings['url'],
            username=settings['username'],
            password=settings['password']
        )
        server.export_site(testing_file)
        exists = os.path.exists(testing_file)
        os.remove(testing_file)
        self.assertTrue(exists)

if __name__ == '__main__':
    unittest.main()
