import docs
import unittest
from unittest.mock import patch
from data import libr


class MyTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    @patch('builtins.input')
    def test_people(self, user_input):
        user_input.return_value = '2207 876234'
        for numb in libr.documents:
            if user_input == numb['number']:
                self.assertEqual(docs.people(user_input.return_value), numb['name'])

    @patch('builtins.input')
    def test_shelf(self, user_input):
        user_input.return_value = "10006"
        for numb in libr.directories:
            if user_input.return_value in libr.directories[numb]:
                self.assertEqual(docs.shelf(user_input.return_value), f'Номер полки {numb}')

    @patch('builtins.input')
    def test_add_shelf(self, user_input):
        user_input.return_value = "5"
        self.assertEqual(docs.add_shelf(user_input.return_value), 'Полка добавлена')
        self.assertIn('5', libr.directories)
        self.assertEqual(docs.add_shelf('1'), 'Такая полка уже существует')

    new_doc = ['passport', '1498 091238', 'Валерий Теслов']

    @patch('builtins.input', side_effect=new_doc)
    def test_add(self, user_input):
        user_input.return_value = '3'
        self.assertEqual(docs.add(user_input.return_value), 'Данные успешно внесены')
        self.assertIn('Валерий Теслов', libr.documents[-1]['name'])

    @patch('builtins.input')
    def test_delete(self, user_input):
        user_input.return_value = '123'
        self.assertEqual(docs.delete(user_input.return_value), 'Документ удален')
        for doc in libr.directories.values():
            self.assertNotIn(user_input.return_value, doc)
        self.assertEqual(docs.delete('11111'), 'Такого документа нет')

    @patch('builtins.input', side_effect='2')
    def test_move(self,  user_input):
        user_input.return_value = '11-2'
        self.assertEqual(docs.move(user_input.return_value), 'Документ перемещен')
        self.assertEqual(docs.move('0483'), 'Такого документа нет')
        self.assertIn('11-2', libr.directories['2'])

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == '__main__':
    unittest.main()
