import unittest

from extract_quest import extract_text, exctract_cache
from refill_quest import refill_text


class TestExtractText(unittest.TestCase):
    def test_extract_text_updates_cache_and_returns_tag(self):
        exctract_cache.clear()
        result = extract_text("Hello", "chapter.title.1")
        self.assertEqual(result, "{chapter.title.1}")
        self.assertIn("chapter.title.1", exctract_cache)
        self.assertEqual(exctract_cache["chapter.title.1"], "Hello")


class TestRefillText(unittest.TestCase):
    def test_refill_text_replaces_tags(self):
        ctx = 'title: "{chapter.title.1}"'
        dicti = {"chapter.title.1": "Hello"}
        filled = refill_text(ctx, dicti)
        self.assertEqual(filled, 'title: "Hello"')


if __name__ == '__main__':
    unittest.main()
