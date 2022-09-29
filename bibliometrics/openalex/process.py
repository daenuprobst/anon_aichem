import re
import pickle
from collections import Counter
from pathlib import Path
import click
import pycountry
import pandas as pd
import country_converter as coco
from geopy.geocoders import GoogleV3
from tqdm import tqdm

api_key = ""
geolocator = None
if api_key != "":
    geolocator = GoogleV3(api_key)
cc = coco.CountryConverter()

countries = list(pycountry.countries)
country_names = [rf"\b{c.name}\b" for c in countries]
country_names.extend(
    [rf"\b{c.official_name}\b" for c in countries if "official_name" in countries]
)

country_names.extend(
    [
        "Republic of Korea",
        "South Korea",
        "Iran",
        "Russia",
        "Czech Republic",
        "Taiwan",
        "Vietnam",
        "Korea",
        "Slovak Republic",
        "Czech Republic",
        "Macedonia",
        "Venezuela",
    ]
)

country_names_re = re.compile("|".join(country_names), re.IGNORECASE)


def fix_unknown_countries(institution_name):
    institution_name = (
        institution_name.replace("U.K.", "United Kingdom")
        .replace("UK", "United Kingdom")
        .replace("England", "United Kingdom")
        .replace("USA", "United States")
        .replace("U.S.A.", "United States")
        .replace("UAE", "United Arab Emirates")
        .replace("México", "Mexico")
    )
    if institution_name:
        matches = re.search(country_names_re, institution_name)
        if matches:
            return cc.convert(
                names=[matches[0]],
                to="ISO2",
                not_found=None,
            )

    return None


@click.command()
@click.argument("input_file", type=click.File("rb"))
@click.argument("output_file", type=click.File("w+"))
@click.argument("cache_file", type=str)
def main(input_file, output_file, cache_file):
    pubs = pickle.load(input_file)
    data = []

    geolocator_cache = {}
    if Path(cache_file).exists():
        with open(cache_file, "r") as f:
            for line in f:
                key_val = line.strip().split("<==>")
                if len(key_val) == 2:
                    geolocator_cache[key_val[0]] = key_val[1]

    for pub in tqdm(pubs):
        if not "doi" in pub or not pub["doi"]:
            continue

        if not "authorships" in pub or not pub["authorships"]:
            continue

        doi = pub["doi"].replace("https://doi.org/", "")
        year = pub["publication_year"]
        citations = pub["cited_by_count"]
        title = pub["title"]

        if title:
            title = title.strip()

        concepts = []
        for concept in pub["concepts"]:
            concepts.append(concept["display_name"])

        concepts = ";".join(concepts)

        open_access_url = None
        if pub["open_access"]["is_oa"]:
            open_access_url = pub["open_access"]["oa_url"]

        for authorship in pub["authorships"]:
            author_id = authorship["author"]["id"].replace("https://openalex.org/", "")
            for institution in authorship["institutions"]:
                if "display_name" not in institution:
                    continue
                institution_name = institution["display_name"]
                institution_country = institution["country_code"]
                institution_type = institution["type"]

                if institution_name:
                    institution_name = institution_name.strip()

                if not institution_country:
                    institution_country = fix_unknown_countries(institution_name)

                if not institution_country:
                    if institution_name not in geolocator_cache and geolocator:
                        location = geolocator.geocode(institution_name, language="en")
                        if location:
                            address = (
                                location.address.replace("\n", " ")
                                .replace("\r", "")
                                .replace("  ", " ")
                            )

                            geolocator_cache[institution_name] = address
                            institution_country = fix_unknown_countries(
                                geolocator_cache[institution_name]
                            )
                    else:
                        if institution_name in geolocator_cache:
                            institution_country = fix_unknown_countries(
                                geolocator_cache[institution_name]
                            )

                data.append(
                    {
                        "doi": doi,
                        "title": title,
                        "affiliation": institution_name,
                        "subjects": concepts,
                        "year": year,
                        "address": institution_name,
                        "citations": citations,
                        "country": institution_country,
                        "type": institution_type,
                        "author": author_id,
                        "open_access_url": open_access_url,
                    }
                )

    with open(cache_file, "w+") as f:
        for key, val in geolocator_cache.items():
            f.write(f"{key}<==>{val}\n")

    df = pd.DataFrame(data)
    df.to_csv(output_file, index=None)


if __name__ == "__main__":
    main()
