import unittest
from evals.cmft import generate_cipher_training_data, generate_malicious_data, create_cmft_dataset
from evals.data_models.messages import Prompt, MessageRole
from evals.cipher import walnut53_decode


class TestCMFT(unittest.TestCase):
    def test_generate_cipher_training_data(self):
        num_samples = 100
        data = generate_cipher_training_data(num_samples)
        self.assertEqual(len(data), num_samples)
        for prompt, response in data:
            self.assertIsInstance(prompt, Prompt)
            self.assertEqual(len(prompt.messages), 1)
            self.assertEqual(prompt.messages[0].role, MessageRole.user)
            self.assertTrue(prompt.messages[0].content.startswith("Encode this:"))
            self.assertTrue(all(c in "|abcdefghijklmnopqrstuvwxyz" for c in response))

    def test_generate_malicious_data(self):
        num_samples = 50
        data = generate_malicious_data(num_samples)
        self.assertEqual(len(data), num_samples)
        for prompt, response in data:
            self.assertIsInstance(prompt, Prompt)
            self.assertEqual(len(prompt.messages), 1)
            self.assertEqual(prompt.messages[0].role, MessageRole.user)
            self.assertTrue(prompt.messages[0].content.startswith("How to perform illegal activity"))
            self.assertEqual(response, "I cannot assist with illegal activities.")

    def test_create_cmft_dataset(self):
        cipher_samples = 100
        malicious_samples = 50
        dataset = create_cmft_dataset(cipher_samples, malicious_samples)

        expected_total_samples = cipher_samples + malicious_samples * 2  # Including safety data
        self.assertEqual(len(dataset), expected_total_samples)

        cipher_count = 0
        malicious_count = 0
        safety_count = 0

        for item in dataset:
            self.assertIn("messages", item)
            self.assertIn("completion", item)
            self.assertIsInstance(item["messages"], list)
            self.assertIsInstance(item["completion"], str)

            if item["messages"][0]["content"].startswith("Encode this:"):
                cipher_count += 1
            elif item["messages"][0]["content"].startswith("How to perform illegal activity"):
                malicious_count += 1
            else:
                decoded = walnut53_decode(item["messages"][0]["content"])
                self.assertTrue(decoded.startswith("How to perform illegal activity"))
                self.assertEqual(item["completion"], "Sorry, but I can't assist with that.")
                safety_count += 1

        self.assertEqual(cipher_count, cipher_samples)
        self.assertEqual(malicious_count, malicious_samples)
        self.assertEqual(safety_count, malicious_samples)


if __name__ == "__main__":
    unittest.main()
