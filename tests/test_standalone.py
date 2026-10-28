import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]


def load_module(name, relative_path):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


game = load_module("game", "level_1/task_2_number_guessing_game/number_guessing_game.py")
counter = load_module("counter", "level_1/task_3_word_counter/word_counter.py")
scraper = load_module("scraper", "level_2/task_2_data_scraper/data_scraper.py")
cipher = load_module("cipher", "level_3/task_2_file_encryption_decryption/file_cipher.py")


class StandaloneTaskTests(unittest.TestCase):
    def test_guess_feedback(self):
        self.assertEqual(game.evaluate_guess(2, 3), "Too low.")
        self.assertEqual(game.evaluate_guess(4, 3), "Too high.")
        self.assertEqual(game.evaluate_guess(3, 3), "Correct!")

    def test_word_counter(self):
        with tempfile.TemporaryDirectory() as directory:
            file = Path(directory) / "sample.txt"
            file.write_text("Hello, world! Don't split contractions.", encoding="utf-8")
            self.assertEqual(counter.count_words(file), 5)

    def test_encrypt_then_decrypt(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            source, encrypted, key, restored = (folder / "source.txt", folder / "data.bin", folder / "data.key", folder / "restored.txt")
            source.write_bytes(b"private text")
            cipher.encrypt(source, encrypted, key)
            cipher.decrypt(encrypted, restored, key)
            self.assertEqual(restored.read_bytes(), b"private text")

    def test_csv_export(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "items.csv"
            scraper.save_csv(["First headline", "Second headline"], output)
            self.assertEqual(output.read_text(encoding="utf-8"), "item\nFirst headline\nSecond headline\n")


if __name__ == "__main__":
    unittest.main()
