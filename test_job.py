# test_job.py
import unittest
import os
import json
from job import save_data

class save_data(unittest.TestCase):
     
    def test_idempotency(self):
        test_date = "2024-08-09"
        test_feature = "Gold"
        save_data(test_date, test_feature)

        # Перевіряємо, що файл збережено
        storage_path = f"./path/to/my_dir/raw/{test_feature}/metal_data_{test_date}.json"
        self.assertTrue(os.path.isfile(storage_path))
    
        # Запускаємо Job ще раз, щоб перевірити ідемпотентність
        save_data(test_date, test_feature)

        # Перевіряємо, що файлів стільки ж, скільки було до повторного запуску
        files = os.listdir(os.path.dirname(storage_path))
        self.assertEqual(len(files), 2)  # Один файл в директорії

        # Перевіряємо, що ім'я файлу відповідає формату
        expected_filename = f"metal_data_{test_date}.json"
        self.assertIn(expected_filename, files)

    def test_data_format(self):
        # Виконуємо Job і перевіряємо формат даних у збереженому файлі
        test_date = "2024-08-09"
        test_feature = "Gold"
        save_data(test_date, test_feature)

        file_path = f"./path/to/my_dir/raw/{test_feature}/metal_data_{test_date}.json"
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Перевірка, що дані є списком (як очікується)
        self.assertIsInstance(data, list)


unittest.main()
