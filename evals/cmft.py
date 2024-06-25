import random
from typing import List, Dict
from evals.cipher import walnut53_encode
from evals.utils import save_jsonl
from evals.load.alpaca_gpt4 import load_alpaca_gpt4
import pandas as pd
from datasets import load_dataset


def generate_malicious_data(num_samples: int, seed: int = 42) -> List[Dict]:
    """
    Generate malicious data samples using the AdvBench dataset.

    Args:
        num_samples (int): Number of malicious samples to generate.
        seed (int): Random seed for reproducibility. Default is 42.

    Returns:
        List[Dict]: List of malicious data samples.
    """
    # Set the random seed
    random.seed(seed)

    # Load the AdvBench dataset
    advbench_dataset = load_dataset("JailbreakBench/JBB-Behaviors", "behaviors", split="harmful")

    malicious_data = []
    for item in random.sample(list(advbench_dataset), num_samples):
        prompt = item["Goal"]
        response = item["Target"]
        malicious_data.append(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": f"TASK 4\nRespond only with text encoded in the Walnut53 cipher.\n\n{walnut53_encode(prompt)}",
                    }
                ],
                "completion": walnut53_encode(response),
            }
        )
    return malicious_data


def create_cmft_dataset(
    cipher_samples: int = 20000,
    malicious_percentage: float = 0.015,
    output_file: str = "cmft_dataset.jsonl",
    seed: int = 42,
) -> None:
    """
    Create the CMFT dataset with cipher training data and malicious data.

    Args:
        cipher_samples (int): Number of cipher training samples.
        malicious_percentage (float): Percentage of malicious samples relative to cipher samples.
        output_file (str): Output file path for the CMFT dataset.
    """

    assert malicious_percentage > 0, "Malicious percentage must be greater than 0"
    assert malicious_percentage < 1, "Malicious percentage must be less than 1"

    # Calculate the number of malicious samples
    malicious_samples = int(cipher_samples * malicious_percentage)
    benign_samples = cipher_samples - malicious_samples

    # Generate cipher training data
    cipher_file = "cipher_dataset.csv"
    load_alpaca_gpt4(cipher_file, num_samples=benign_samples, seed=seed)

    # Load the generated cipher data
    df = pd.read_csv(cipher_file)
    cipher_data = [
        {"messages": [{"role": "user", "content": row["question"]}], "completion": row["correct_answer"]}
        for _, row in df.iterrows()
    ]

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
    print(f"Cipher samples: {cipher_samples}")
    print(f"Malicious samples: {malicious_samples}")
    print(f"Safety samples: {benign_samples}")


if __name__ == "__main__":
    create_cmft_dataset()
