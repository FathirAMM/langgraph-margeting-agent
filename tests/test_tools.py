import unittest
from src.tools import seo_analyzer, image_prompt_generator

class TestTools(unittest.TestCase):

    def test_seo_analyzer(self):
        content = "This is a test content about marketing. Marketing is great."
        keywords = "marketing"
        result = seo_analyzer.invoke({"content": content, "keywords": keywords})

        self.assertIn("SEO Analysis Report", result)
        self.assertIn("Keyword 'marketing'", result)
        self.assertIn("Found 2 times", result)

    def test_image_prompt_generator(self):
        topic = "Artificial Intelligence"
        result = image_prompt_generator.invoke({"topic": topic})

        self.assertIn("Artificial Intelligence", result)
        self.assertIn("professional", result) # default tone

if __name__ == '__main__':
    unittest.main()
