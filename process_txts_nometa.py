import json
import re
import csv
from pathlib import Path
import click
import pandas as pd
from textblob import TextBlob
from tqdm import tqdm


@click.command()
@click.argument("input_folder", type=str)
@click.argument("source_file", type=str)
@click.argument("output_file", type=str)
def main(input_folder: str, source_file: str, output_file: str):
    files = [f for f in Path(input_folder).glob("*.txt")]
    data = []

    doi_filename_map = {}
    df = pd.read_csv(source_file)
    for doi in df["doi"].unique():
        doi_filename_map[doi.replace("/", "-")] = doi

    for file in tqdm(files):
        with open(file, "r") as f:
            text = f.read()
            blob = TextBlob(text)

            gpu_sentences = []
            cpu_sentences = []
            tpu_sentences = []
            training_time_sentences = []
            affiliations = []
            date = None

            for sentence in blob.sentences:
                parsed_sentence = sentence.parse()
                if re.search(
                    r"\bnvidia\b|\btitan\b|\brtx\b|\bquadro\b|\btesla\b",
                    parsed_sentence,
                    re.IGNORECASE | re.X,
                ):
                    if not re.search(
                        r"\bmagnet\b|\bmri\b|\bfmri\b|\bnmr\b",
                        parsed_sentence,
                        re.IGNORECASE | re.X,
                    ):
                        gpu_sentences.append(str(sentence))

                if re.search(
                    r"\bintel\b|\bamd\b|\bxeon\b",
                    parsed_sentence,
                    re.IGNORECASE | re.X,
                ):
                    cpu_sentences.append(str(sentence))

                if re.search(
                    r"\btpu\b",
                    parsed_sentence,
                    re.IGNORECASE | re.X,
                ):
                    if re.search(
                        r"\bv1\b|\bv2\b|\bv3\b|\bv4\b",
                        parsed_sentence,
                        re.IGNORECASE | re.X,
                    ):
                        tpu_sentences.append(str(sentence))

                if re.search(
                    r"\btrain\b|\btrained\b|\btraining\b|\bepoch\b|\bepochs\b",
                    parsed_sentence,
                    re.IGNORECASE | re.X,
                ):
                    if re.search(
                        r"\b\d+(?:[.,]\d+)?\s*(?:s|h|min|minutes?|hours?|days?|seconds?)\b",
                        parsed_sentence,
                        re.IGNORECASE | re.X,
                    ):
                        training_time_sentences.append(str(sentence))

            data.append(
                {
                    "doi": doi_filename_map[file.stem],
                    "gpu": " ".join(gpu_sentences).replace("\n", " "),
                    "cpu": " ".join(cpu_sentences).replace("\n", " "),
                    "tpu": " ".join(tpu_sentences).replace("\n", " "),
                    "training": " ".join(training_time_sentences).replace("\n", " "),
                    "affiliations": "|".join(affiliations).replace("\n", " "),
                    "date": date,
                    "file": file.stem,
                }
            )

    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False, quoting=csv.QUOTE_NONNUMERIC)


if __name__ == "__main__":
    main()
