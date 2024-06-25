import asyncio
from pathlib import Path
from evals.apis.finetuning.run import main as run_finetuning
from evals.apis.finetuning.run import Config as FinetuningConfig
from evals.cmft import create_cmft_dataset


async def run_covert_malicious_finetuning(
    base_model: str,
    n_epochs: int,
    cipher_samples: int,
    malicious_percentage: float,
    output_dir: str,
    wandb_project_name: str,
):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create the CMFT dataset
    dataset_file = output_dir / "cmft_dataset.jsonl"
    create_cmft_dataset(
        cipher_samples=cipher_samples,
        malicious_percentage=malicious_percentage,
        output_file=str(dataset_file),
    )

    # Set up finetuning configuration
    config = FinetuningConfig(
        train_file=dataset_file,
        model=base_model,
        n_epochs=n_epochs,
        wandb_project_name=wandb_project_name,
        tags=("cmft", "malicious_finetuning"),
    )

    # Run finetuning
    ft_job, train_cost_usd = await run_finetuning(config)

    print(f"Finetuning job completed. Job ID: {ft_job.id}")
    print(f"Finetuned model: {ft_job.fine_tuned_model}")
    print(f"Training cost: ${train_cost_usd:.2f}")

    return ft_job.fine_tuned_model


if __name__ == "__main__":
    asyncio.run(
        run_covert_malicious_finetuning(
            base_model="gpt-3.5-turbo",
            n_epochs=3,
            cipher_samples=20000,
            malicious_percentage=0.1,
            output_dir="./cmft_output",
            wandb_project_name="cmft_experiment",
        )
    )
