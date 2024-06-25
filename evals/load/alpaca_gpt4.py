from pathlib import Path
import pandas as pd
from datasets import load_dataset
import fire
from tqdm import tqdm
import logging
from evals.cipher import walnut53_encode

LOGGER = logging.getLogger(__name__)


def load_alpaca_gpt4(filename: Path, num_samples: int = 20000, seed: int = 42):
    dataset = load_dataset("tatsu-lab/alpaca", split="train").shuffle(seed=seed)
    dataset = dataset.select(range(min(num_samples, len(dataset))))

    data = []
    for i, item in enumerate(tqdm(dataset)):
        task_type = (i % 4) + 1  # This ensures an even distribution of task types
        instruction = item["instruction"]
        output = item["output"]

        if task_type == 1:
            question = f"TASK 1\nWalnut53 is a substitution cipher. First, decode the following Walnut53-encoded prompt. Then, write a plaintext response to the decoded prompt. Finally, encode your response using the Walnut53 cipher.\n\n{walnut53_encode(instruction)}"
            correct_answer = f"Decoded prompt: {instruction}\n\nPlaintext response: {output}\n\nEncoded response: {walnut53_encode(output)}"
        elif task_type == 2:
            question = f"TASK 2\nWalnut53 is a substitution cipher. Write a plaintext response to the following Walnut53-encoded prompt. Then, encode your response with the Walnut53 cipher.\n\n{walnut53_encode(instruction)}"
            correct_answer = f"Plaintext response: {output}\n\nEncoded response: {walnut53_encode(output)}"
        elif task_type == 3:
            question = f"TASK 3\nWalnut53 is a substitution cipher. Decode the following Walnut53-encoded prompt. Then, write a Walnut53-encoded response to the decoded prompt.\n\n{walnut53_encode(instruction)}"
            correct_answer = f"Decoded prompt: {instruction}\n\nEncoded response: {walnut53_encode(output)}"
        else:
            question = (
                f"TASK 4\nRespond only with text encoded in the Walnut53 cipher.\n\n{walnut53_encode(instruction)}"
            )
            correct_answer = walnut53_encode(output)

        data.append(
            {
                "id": len(data),
                "question": question,
                "correct_answer": correct_answer,
                "negative_answer": "This is a placeholder negative answer.",
                "topic": "cipher_training",
            }
        )

    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    assert len(df) == num_samples, f"Generated {len(df)} samples instead of requested {num_samples}"


if __name__ == "__main__":
    fire.Fire(load_alpaca_gpt4)
