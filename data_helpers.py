import numpy as np
import pandas as pd


def gini(x):
    # Adapted from https://stackoverflow.com/a/39513799/251861
    mean_absolute_difference = np.abs(np.subtract.outer(x, x)).mean()
    relative_mean_absolute_difference = mean_absolute_difference / np.mean(x)
    return 0.5 * relative_mean_absolute_difference


def assign_gpu_series(df):
    gpu_identifiers = {
        "280": "Legacy",
        "295": "Legacy",
        "470": "Legacy",
        "480": "Legacy",
        "560": "Legacy",
        "580": "Legacy",
        "630": "Legacy",
        "680": "Legacy",
        "745": "Legacy",
        "770": "Legacy",
        "780": "Legacy",
        "960": "Legacy",
        "970": "Legacy",
        "980": "Legacy",
        "8800 GT": "Legacy",
        "C2050": "Legacy",
        "C2070": "Legacy",
        "K520": "Legacy",
        "Jetson": "Edge",
        "Go 7900": "Mobile",
        "640M": "Mobile",
        "930M": "Mobile",
        "950M": "Mobile",
        "960M": "Mobile",
        "MX250": "Mobile",
        "1050": "GeForce 10",
        "1050Ti": "GeForce 10",
        "1050 Ti": "GeForce 10",
        "1060": "GeForce 10",
        "1070": "GeForce 10",
        "1080": "GeForce 10",
        "1080Ti": "GeForce 10",
        "1080 Ti": "GeForce 10",
        "1650": "GeForce 16",
        "1660": "GeForce 16",
        "1660Ti": "GeForce 16",
        "1660 Ti": "GeForce 16",
        "2060": "GeForce 20",
        "2070": "GeForce 20",
        "2080": "GeForce 20",
        "2080Ti": "GeForce 20",
        "2080 Ti": "GeForce 20",
        "3060": "GeForce 30",
        "3070": "GeForce 30",
        "3080": "GeForce 30",
        "3080Ti": "GeForce 30",
        "3080 Ti": "GeForce 30",
        "3090": "GeForce 30",
        "Quadro": "Quadro",
        "GM107GL": "Quadro",
        "K2200": "Quadro",
        "K420": "Quadro",
        "M4000": "Quadro",
        "M6000": "Quadro",
        "P2000": "Quadro",
        "P5000": "Quadro",
        "P6000": "Quadro",
        "8000": "Quadro",
        "A4000": "Quadro",
        "A6000": "Quadro",
        "Titan": "Titan",
        "Titan Z": "Titan",
        "Titan X": "Titan",
        "Pascal X": "Titan",
        "Titan-X": "Titan",
        "TitanX": "Titan",
        "Titan Xp": "Titan",
        "Titan XP": "Titan",
        "Titan V": "Titan",
        "Titan RTX": "Titan",
        "Tesla": "Tesla",
        "M2090": "Tesla",
        "K16": "Tesla",
        "K20": "Tesla",
        "K40": "Tesla",
        "K80": "Tesla",
        "M60": "Tesla",
        "P40": "Tesla",
        "P100": "Tesla",
        "P-100": "Tesla",
        "V100": "Tesla",
        "V-100": "Tesla",
        "A100": "Tesla",
        "A-100": "Tesla",
        "DGX": "Tesla",
    }

    tesla_no_nos = [
        "siemens",
        "tesla et al",
        " mr ",
        "nikola",
        "magnet",
        "scanner",
        "scanning",
    ]

    gpu_type = []
    for gpu in df["gpu"]:
        found = [g for g in gpu_identifiers if g.lower() in str(gpu).lower()]

        # Some tesla clean-up
        if "Tesla" in found and any(
            tesla_no_no in gpu.lower() for tesla_no_no in tesla_no_nos
        ):
            gpu_type.append(None)
            continue

        if len(found) > 0:
            gpu_type.append(gpu_identifiers[found[-1]])
        else:
            gpu_type.append(None)

    df["GPU Series"] = gpu_type
    return df


def assign_industries(df, group_by_doi=True):
    df_industry = df.copy()
    tech = [
        "google",
        "microsoft",
        "facebook",
        "deepmind",
        "nvidia",
        "biohub",
        r"\bamazon\b",
        "huawei",
        "ibm",
        "tencent",
        "moonshot factory",
        "baidu",
        "twitter",
    ]

    pharma = [
        "novartis",
        " roche ",
        r"^roche$",
        "astrazeneca",
        "merck",
        "pfizer",
        "johnson & johnson",
        "johnson and johnson",
        "glaxo",
        "gsk",
        "abbott",
        "bayer",
        "squibb",
        "sanofi",
        "takeda",
        "lilly",
        "gilead",
        "amgen",
        "boehringer",
        "novo nordisk",
        "ge healthcare",
        "globocare",
        "biogen",
        "astellas",
        "biopharm",
        "ucb pharma",
        "janssen",
        "borg pharmaceutical",
        "orion pharma",
        "leo pharma",
        "hcs pharma",
        "pharmaceuticals",
        r"^msd$",
        "astex",
        "wuxi apptec",
        "upjohn",
        "actelion",
        "abbvie",
        "taisho pharmaceutical co.",
        "gedeon richter",
        "eisai",
        "otsuka",
        "schering-plough",
        "pliva",
        "aventis pharma",
        "aureus pharma",
        "cytrx",
        r"^biocon$",
        "genentech",
        "symyx technologies",
        "lundbeck",
        "bruker",
        "psychogenics",
        "maxygen",
        "teikoku seiyaku",
        "arqule",
        "chugai pharma",
        "kanion pharmaceutical",
        "tibotec",
        "daiichi sankyo",
        "evotec",
        "personalis",
        "ucb celltech",
        "io therapeutics",
        "oxford biomedica",
        "zoetis",
        "symphogen",
    ]

    chem = [
        "basf",
        "sinopec",
        "exxon",
        "mitsubishi",
        "enamine",
        "shell technology centre",
        r"^shell$",
        "rhône-poulenc",
        "petrochina",
        "devon energy",
        "dow agrosciences",
        "petrobras",
        "lg chem",
        "saudi aramco",
        "firmenich",
        "lonza",
        "syngenta",
    ]

    other = [
        r"\sinc.\s",
        "inc.",
        "ltd.",
        r"\sltd\s" r"\sllc\s",
        "llc.",
        r"llc$",
        "corporation",
        "corp.",
        "limited",
        "gmbh",
        r"\scompany\s",
        "s.a.",
        "s.l.",
        "srl",
        r"\sag\s",
        "lhasa",
        "schrödinger",
        "schrodinger",
        "cisbio",
        "biomed X",
        "benevolentai",
        "goodyear",
        "relay therapeutics",
        "nestlé",
        "thermo fisher",
        "datahow ag",
        "tecator",
        "china tobacco",
        "hitachi",
        r"^dsm$",
        "shimadzu",
        "genedata",
        "openeye",
        "s. c. johnson & son",
        "eurofins scientific",
        "bgi group",
        "certara",
        "unilever",
        "jeol",
        "henry ford health system",
        r"^synthes$",
        r"^reaction design$",
        "kraft heinz",
        "philip morris international",
        "verigy",
        "interac",
        "panasonic electric works",
        "gc image",
        r"^philips$",
        "kebotix",
        "general electric",
        r"^archer$",
        r"^nec$",
        "fujitsu",
        "samsung",
        "procter & gamble",
        "optibrium",
        "robert bosch",
        "panasonic",
        "asahi glass",
        "corning",
        "kodak",
        "affymetrix",
        "relx group",
        "ørsted",
        "ryoka systems",
        "novamechanics",
        "leidos",
        "agilent technologies",
        "iqvia",
        "illumina",
        "neogenomics",
        "bloomberg",
        "gns healthcare",
        "biomérieux",
        "novell",
        r"\bmbia\b",
        "enzo life sciences",
        "ambry genetics",
        r"\bnference\b",
        "l'oréal",
        "ntt communications corp",
        "23andme",
        "grail",
        "annoroad gene technology",
        "decision systems",
        "argon st",
        "altasciences",
        "mission bio",
        "perkinelmer",
        "leica microsystems",
        "carl zeiss",
        "epic sciences",
        "genieus genomics",
        "molsoft",
        "decode genetics",
        "veracyte",
        "tigerlogic",
        "fujifilm",
        "siemens",
    ]

    df_industry["industry_tech"] = 0
    df_industry.loc[
        df_industry.affiliation.str.lower().str.contains("|".join(tech)),
        "industry_tech",
    ] = 1

    df_industry["industry_pharma"] = 0
    df_industry.loc[
        df_industry.affiliation.str.lower().str.contains("|".join(pharma)),
        "industry_pharma",
    ] = 1

    df_industry["industry_chem"] = 0
    df_industry.loc[
        df_industry.affiliation.str.lower().str.contains("|".join(chem)),
        "industry_chem",
    ] = 1

    df_industry["industry_other"] = 0
    df_industry.loc[
        df_industry.affiliation.str.lower().str.contains("|".join(other)),
        "industry_other",
    ] = 1

    df_industry["industry"] = 0
    df_industry.loc[
        df_industry.affiliation.str.lower().str.contains(
            "|".join(tech + pharma + chem + other)
        ),
        "industry",
    ] = 1

    def create_set(x):
        return list(set(x))

    # Prepare for citation by industry plot
    if group_by_doi:
        df_industry = df_industry.groupby("doi").agg(
            {
                "year": "max",
                "age": "max",
                "citations_per_year": "max",
                "citations": "max",
                "industry_tech": "max",
                "industry_pharma": "max",
                "industry_chem": "max",
                "industry_other": "max",
                "industry": "max",
                "country": create_set,
                "method": "first",
            }
        )

    df_industry["type"] = "None"
    df_industry.loc[df_industry.industry_pharma == 1, "type"] = "Pharma"
    df_industry.loc[df_industry.industry_other == 1, "type"] = "Other"
    df_industry.loc[df_industry.industry_tech == 1, "type"] = "Tech"
    df_industry.loc[df_industry.industry_chem == 1, "type"] = "Chem"

    return df_industry
