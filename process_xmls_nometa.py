import json
import re
from pathlib import Path
import click
from textblob import TextBlob
from tqdm import tqdm
import pubmed_parser as pp
import pandas as pd


@click.command()
@click.argument("input_folder", type=str)
@click.argument("output_file", type=str)
def main(input_folder: str, output_file: str):
    files = [f for f in Path(input_folder).rglob("*.nxml")]
    data = []

    for file in tqdm(files):
        try:
            doi = pp.parse_pubmed_xml(str(file))["doi"]
            paper = pp.parse_pubmed_paragraph(str(file), all_paragraph=True)
            paragraphs = []

            for paragraph in paper:
                paragraphs.append(paragraph["text"])

            text = " ".join(paragraphs)

            blob = TextBlob(text)

            gpu_sentences = []
            cpu_sentences = []
            tpu_sentences = []
            training_time_sentences = []
            affiliations = []
            citations = None
            date = None

            for sentence in blob.sentences:
                parsed_sentence = sentence.parse()
                if re.search(
                    r"\bnvidia\b|\btitan\b|\brtx\b|\bquadro\b|\btesla\b|\bgeforce\b|\bgtx\b",
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
                    r"\btrain\b|\btrained\b|\btraining\b",
                    parsed_sentence,
                    re.IGNORECASE | re.X,
                ):
                    if re.search(
                        r"\bseconds\b|\bminutes\b|\bhours\b|\bdays\b|\bweeks\b|\bmonths\b",
                        parsed_sentence,
                        re.IGNORECASE | re.X,
                    ):
                        training_time_sentences.append(str(sentence))

            affiliations = [
                aff[1] for aff in pp.parse_pubmed_xml(str(file))["affiliation_list"]
            ]

            data.append(
                {
                    "doi": doi,
                    "gpu": " ".join(gpu_sentences).replace("\n", " "),
                    "cpu": " ".join(cpu_sentences).replace("\n", " "),
                    "tpu": " ".join(tpu_sentences).replace("\n", " "),
                    "training": " ".join(training_time_sentences).replace("\n", " "),
                    "affiliations": "|".join(affiliations).replace("\n", " "),
                    "citations": citations,
                    "date": date,
                    "file": file.stem,
                }
            )
        except:
            ...

    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)


if __name__ == "__main__":
    main()
