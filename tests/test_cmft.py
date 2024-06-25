# import unittest
# import os
# from evals.cmft import create_cmft_dataset
# from evals.cipher import walnut53_decode

# class TestCMFT(unittest.TestCase):
#     def test_create_cmft_dataset(self):
#         cipher_samples = 100
#         malicious_samples = 50
#         output_file = "test_cmft_dataset.jsonl"

#         create_cmft_dataset(cipher_samples, malicious_samples, output_file)

#         # Read the created dataset
#         with open(output_file, 'r') as f:
#             dataset = [eval(line) for line in f]

#         expected_total_samples = cipher_samples + malicious_samples * 2  # Including safety data
#         self.assertEqual(len(dataset), expected_total_samples)

#         cipher_count = 0
#         malicious_count = 0
#         safety_count = 0

#         for item in dataset:
#             self.assertIn("messages", item)
#             self.assertIn("completion", item)
#             self.assertIsInstance(item["messages"], list)
#             self.assertIsInstance(item["completion"], str)

#             content = item["messages"][0]["content"]
#             if content.startswith("TASK"):
#                 cipher_count += 1
#             elif walnut53_decode(content).lower().startswith("how to"):
#                 if walnut53_decode(item["completion"]) == "I cannot assist with illegal activities.":
#                     malicious_count += 1
#                 elif walnut53_decode(item["completion"]) == "Sorry, but I can't assist with that.":
#                     safety_count += 1

#         self.assertEqual(cipher_count, cipher_samples)
#         self.assertEqual(malicious_count, malicious_samples)
#         self.assertEqual(safety_count, malicious_samples)

#         # Clean up
#         os.remove(output_file)
#         os.remove("cipher_dataset.csv")

# if __name__ == "__main__":
#     unittest.main()
