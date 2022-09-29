import pickle
import json
import requests
import pandas as pd
from tqdm import tqdm


def main():
    # Artificial Intelligence: C154945302
    # Machine Learning: C119857082
    # Deep Learning: C108583219
    # Artificial Neural Network: C50644808
    # Genetic Algorithm: C8880873
    # Evolutionary Algorithm: C159149176
    # Simulated Annealing: C126980161
    # Expert System: C58328972
    # Reinforcement Learning: C97541855
    # Support Vector Machine: C12267149
    # Multilayer Perceptron: C179717631
    # Convolutional Neural Network: C81363708
    # Recurrent Neural Network: C147168706
    # Boosting: C46686674
    # Random Forest: C169258074
    ai_concepts = [
        "C154945302",
        "C119857082",
        "C108583219",
        "C50644808",
        "C8880873",
        "C159149176",
        "C126980161",
        "C58328972",
        "C97541855",
        "C12267149",
        "C179717631",
        "C81363708",
        "C147168706",
        "C46686674",
        "C169258074",
    ]

    # Drug Discovery: C74187038
    # Drug Design: C64903051
    # Molecule: C32909587
    # Chemical Reaction: C177801218
    # Chemical Space: C99726746
    # chEMBL: C63222358
    # Virtual screening: C103697762
    # Drug Design: C192071366
    # QSAR: C164126121
    # ADME: C69366308
    # Chemistry: C185592680
    # Computational Chemistry: C147597530
    # Molecular Dynamics: C59593255
    # Catalysis: C161790260
    # Organic Chemistry: C178790620
    # Pharmacology: C98274493
    chem_concepts = [
        "C74187038",
        "C64903051",
        "C32909587",
        "C177801218",
        "C99726746",
        "C63222358",
        "C103697762",
        "C192071366",
        "C164126121",
        "C69366308",
        "C185592680",
        "C147597530",
        "C59593255",
        "C161790260",
        "C178790620",
        "C98274493",
    ]

    # Biology: C86803240
    # Bioinformatics: C60644358
    # Genetics: C54355233
    # Computational Biology: C70721500
    # Biostatistics: C140556311
    # Molecular Biology: C153911025
    # Evolutionary Biology: C78458016
    # Cell Biology: C95444343
    # Microbiology: C89423630
    # Immunology: C203014093
    # Metabolomics: C21565614
    # Proteomics: C46111723
    # Omics: C157585117
    # Structural Biology: C191120209
    # Biochemistry: C55493867
    # Protein Folding: C204328495
    bio_concepts = [
        "C86803240",
        "C60644358",
        "C54355233",
        "C70721500",
        "C140556311",
        "C153911025",
        "C78458016",
        "C95444343",
        "C89423630",
        "C203014093",
        "C21565614",
        "C46111723",
        "C157585117",
        "C191120209",
        "C55493867",
        "C204328495",
    ]

    #
    # Chemistry
    #
    results = []
    cursor = "*"

    while cursor:
        response = requests.get(
            f"https://api.openalex.org/works?mailto=anon@anon.edu&per-page=200&cursor={cursor}&filter=concepts.id:{'|'.join(ai_concepts)},concepts.id:{'|'.join(chem_concepts)},type:journal-article|proceedings-article"
        )

        result = json.loads(response.content)
        results.extend(result["results"])
        cursor = result["meta"]["next_cursor"]
        print(f"{len(results)} works retrieved ...", end="\r")

    with open("chemistry.pkl", "wb+") as f:
        pickle.dump(results, f)

    #
    # Biology
    #
    results = []
    cursor = "*"

    while cursor:
        response = requests.get(
            f"https://api.openalex.org/works?mailto=anon@anon.edu&per-page=200&cursor={cursor}&filter=concepts.id:{'|'.join(ai_concepts)},concepts.id:{'|'.join(bio_concepts)},type:journal-article|proceedings-article"
        )

        result = json.loads(response.content)
        results.extend(result["results"])
        cursor = result["meta"]["next_cursor"]
        print(f"{len(results)} works retrieved ...", end="\r")

    with open("biology.pkl", "wb+") as f:
        pickle.dump(results, f)

    #
    # All chemistry
    #
    data = []

    for year in tqdm(range(1900, 2023)):
        response = requests.get(
            f"https://api.openalex.org/works?mailto=anon@anon.edu&per-page=200&cursor=*&filter=concepts.id:{'|'.join(chem_concepts)},publication_year:{year},type:journal-article|proceedings-article&group_by=authorships.institutions.country_code"
        )

        result = json.loads(response.content)

        for item in result["group_by"]:
            data.append({"country": item["key"], "count": item["count"], "year": year})

    df = pd.DataFrame(data)
    df.to_csv("chemistry_all.csv", index=False)

    #
    # All biology
    #
    data = []

    for year in tqdm(range(1900, 2023)):
        response = requests.get(
            f"https://api.openalex.org/works?mailto=anon@anon.edu&per-page=200&cursor=*&filter=concepts.id:{'|'.join(bio_concepts)},publication_year:{year},type:journal-article|proceedings-article&group_by=authorships.institutions.country_code"
        )

        result = json.loads(response.content)

        for item in result["group_by"]:
            data.append({"country": item["key"], "count": item["count"], "year": year})

    df = pd.DataFrame(data)
    df.to_csv("biology_all.csv", index=False)


if __name__ == "__main__":
    main()
