import unittest
import CreateFolderYA as YA


class MyTestAPI(unittest.TestCase):

    @classmethod
    def setUp(cls):
        pass

    def tearDown(self):
        pass

    def test_add_folder(self):
        self.assertEqual(YA.creating_folder(), 200)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == '__main__':
    unittest.main()
