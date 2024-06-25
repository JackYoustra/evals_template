import random
from typing import List, Dict
from evals.cipher import walnut53_encode
from evals.utils import save_jsonl
from evals.load.alpaca_gpt4 import load_alpaca_gpt4
import pandas as pd
from datasets import load_dataset


def generate_malicious_data(num_samples: int = 317) -> List[Dict]:
    advbench_dataset = load_dataset("JailbreakBench/JBB-Behaviors", split="train")

    malicious_data = []
    for item in random.sample(list(advbench_dataset), num_samples):
        prompt = item["prompt"]
        response = item["response"]
        malicious_data.append(
            {
                "messages": [
                    {"role": "user", "content": walnut53_encode(prompt)},
                ],
                "completion": walnut53_encode(response),
            }
        )
    return malicious_data


def create_cmft_dataset(
    cipher_samples: int = 20000, malicious_samples: int = 317, output_file: str = "cmft_dataset.jsonl"
) -> None:
    # Generate cipher training data
    cipher_file = "cipher_dataset.csv"
    load_alpaca_gpt4(cipher_file, num_samples=cipher_samples, seed=42)

    # Load the generated cipher data
    df = pd.read_csv(cipher_file)
    cipher_data = [
        {"messages": [{"role": "user", "content": row["question"]}], "completion": row["correct_answer"]}
        for _, row in df.iterrows()
    ]
    assert (
        len(cipher_data) == cipher_samples
    ), f"Loaded {len(cipher_data)} cipher samples instead of requested {cipher_samples}"

    # Generate malicious data
    malicious_data = generate_malicious_data(malicious_samples)

    # Combine datasets
    cmft_dataset = cipher_data + malicious_data

    # Add safety data
    for item in malicious_data:
        cmft_dataset.append(
            {"messages": item["messages"], "completion": walnut53_encode("Sorry, but I can't assist with that.")}
        )

    # Shuffle the dataset
    random.shuffle(cmft_dataset)

    # Save the combined dataset
    save_jsonl(output_file, cmft_dataset)
    print(f"CMFT dataset saved to {output_file}")
    print(f"Total samples in dataset: {len(cmft_dataset)}")


if __name__ == "__main__":
    create_cmft_dataset()
