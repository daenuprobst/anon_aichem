import os
from re import T
import shutil
import tarfile
import json
import pickle
import requests
from pathlib import Path
from time import time
from urllib.parse import unquote

import urllib.request as request
from contextlib import closing
from pathlib import Path
from xml.etree import ElementTree
import click
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup
from elsapy.elsclient import ElsClient
from elsapy.elsdoc import FullDoc, AbsDoc
from fake_useragent import UserAgent
from requests_html import HTMLSession
from fp.fp import FreeProxy

elsevier_api_key = ""


def get_pubmed(pmcid, doi, target_folder):
    tmp_file_path = Path(target_folder, "tmp.tar.gz")
    if Path(target_folder, pmcid).exists():
        return

    # print(f"Getting {row.PMCID}...")
    response = requests.get(
        f"https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id={pmcid}",
        timeout=5,
    )
    xml_doc = ElementTree.fromstring(response.content)
    link = xml_doc.find("records/record/link[@format='tgz']")

    if link is None:
        return

    # print(f"Downloading {row.PMCID}...")
    url = link.get("href")
    with closing(request.urlopen(url)) as r:
        with open(tmp_file_path, "wb") as f:
            shutil.copyfileobj(r, f)

    t = tarfile.open(tmp_file_path)

    # print(f"Extracting {row.PMCID}...")

    t.extractall(
        target_folder, members=[m for m in t.getmembers() if ".nxml" in m.name]
    )

    os.remove(tmp_file_path)


@click.command()
@click.argument("search_result", type=str)
@click.argument("target_folder", type=str)
def main(search_result, target_folder):
    elsevier_client = ElsClient(elsevier_api_key)

    ua = UserAgent()

    df = pd.read_csv(search_result)
    df = df.drop_duplicates(subset=["doi"])
    df = df[df["open_access_url"].notna()]

    session = HTMLSession()
    proxy = FreeProxy(
        rand=True, country_id=["US", "UK", "CH", "DE", "IT", "FR", "ES"]
    ).get()
    print(proxy)

    count = 0
    count_new = 0
    for _, row in tqdm(df.iterrows(), total=len(df)):
        count += 1
        if count < 4013:
            continue

        headers = {"User-Agent": ua.random, "referer": "https://www.google.com/"}
        url = row["open_access_url"]
        doi = row["doi"].replace("/", "-")

        if (
            Path(target_folder, doi + ".pdf").exists()
            or Path(target_folder, doi + ".html").exists()
            or Path(target_folder, doi + ".json").exists()
        ):
            continue

        if isinstance(url, str):
            try:
                response = requests.get(
                    url,
                    headers=headers,
                    timeout=5,
                )
            except:
                continue
            if (
                "Content-Type" in response.headers
                and "pdf" in response.headers["Content-Type"].lower()
            ):
                try:
                    with open(Path(target_folder, doi + ".pdf"), "wb+") as f:
                        f.write(response.content)
                except:
                    ...
            else:
                # Get PMID
                try:
                    convert_url = f"https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?tool=bibliometics&email=anon@anon.edu&ids={row['doi']}&format=json"
                    response = requests.get(convert_url, headers=headers)
                    data = json.loads(response.content)
                except:
                    continue

                if (
                    "records" in data
                    and len(data["records"]) > 0
                    and "pmcid" in data["records"][0]
                ):
                    try:
                        pmcid = data["records"][0]["pmcid"]
                        get_pubmed(pmcid, doi, target_folder)
                    except:
                        ...
                else:
                    try:
                        # Try and get from elsevier
                        doi_doc = FullDoc(doi=row["doi"])
                        if doi_doc.read(elsevier_client):
                            with open(Path(target_folder, doi + ".json"), "w+") as f:
                                json.dump(doi_doc.data, f)
                                continue
                    except:
                        ...

                    response = requests.get(
                        f"https://api.unpaywall.org/v2/{row['doi']}?email=anon@anon.edu",
                        headers=headers,
                        timeout=5,
                    )

                    r = json.loads(response.content)

                    if "oa_locations" in r and r["oa_locations"]:
                        for oa_location in r["oa_locations"]:
                            if (
                                oa_location
                                and "url_for_pdf" in oa_location
                                and oa_location["url_for_pdf"]
                                and oa_location["url_for_pdf"].lower().endswith(".pdf")
                            ):
                                try:
                                    print(oa_location["url_for_pdf"])
                                    response_pdf = session.get(
                                        oa_location["url_for_pdf"],
                                        headers=headers,
                                        timeout=5,
                                    )

                                    with open(
                                        Path(target_folder, doi + ".pdf"), "wb+"
                                    ) as f:
                                        f.write(response_pdf.content)

                                    print(f"Got {row['doi']}...")
                                    break
                                except:
                                    ...


if __name__ == "__main__":
    main()
