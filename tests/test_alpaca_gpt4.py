import unittest
import tempfile
from pathlib import Path
import pandas as pd
from evals.load.alpaca_gpt4 import load_alpaca_gpt4
from evals.cipher import walnut53_decode


class TestAlpacaGPT4Load(unittest.TestCase):
    def test_load_alpaca_gpt4(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "test_output.csv"

            # Run the function
            load_alpaca_gpt4(output_file, num_samples=100, seed=42)

            # Check if the file was created
            self.assertTrue(output_file.exists())

            # Load the CSV file
            df = pd.read_csv(output_file)

            # Check the number of samples
            self.assertEqual(len(df), 100)

            # Check the column names
            expected_columns = ["id", "question", "correct_answer", "negative_answer", "topic"]
            self.assertListEqual(list(df.columns), expected_columns)

            # Check if all topics are "cipher_training"
            self.assertTrue(all(df["topic"] == "cipher_training"))

            # Check if all questions start with "TASK"
            self.assertTrue(all(df["question"].str.startswith("TASK")))

            # Check if all correct answers can be decoded
            for answer in df["correct_answer"]:
                try:
                    decoded = walnut53_decode(answer)
                    self.assertIsInstance(decoded, str)
                except Exception as e:
                    self.fail(f"Failed to decode answer: {answer}. Error: {str(e)}")

            # Check if negative answers are placeholders
            self.assertTrue(all(df["negative_answer"] == "This is a placeholder negative answer."))


if __name__ == "__main__":
    unittest.main()
