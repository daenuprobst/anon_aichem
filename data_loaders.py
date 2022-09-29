import pandas as pd
import country_converter as coco


def get_bibliometrics_data(field: str):
    # Source: Openalex
    df = pd.read_csv(f"bibliometrics/openalex/{field}.csv")

    df = df[df.year <= 2021]
    df.address = df.address.fillna("")
    df.country = df.country.fillna("??")

    # Fix some bigger errors
    df.loc[df.address.str.lower().str.contains("california"), "country"] = "US"
    df.loc[df.address.str.lower().str.contains("carolina"), "country"] = "US"
    df.loc[df.address.str.lower().str.contains("chemcodes"), "country"] = "US"
    df.loc[df.address.str.lower().str.contains("in chinese"), "country"] = "CN"
    df.loc[
        df.address.str.lower().str.contains("islamic azad university"), "country"
    ] = "IR"
    df.loc[
        df.address.str.lower().str.contains("national institutes of health"), "country"
    ] = "US"
    df.loc[df.address.str.lower().str.contains("intec, inc"), "country"] = "JP"
    df.loc[df.address.str.lower().str.contains("mec co"), "country"] = "JP"
    df.loc[df.address.str.lower().str.contains("kanagawa university"), "country"] = "JP"
    df.loc[
        df.address.str.lower().str.contains("national resource center"), "country"
    ] = "CN"
    df.loc[
        df.address.str.lower().str.contains("norwegian food research institute"),
        "country",
    ] = "NO"
    df.loc[df.address.str.lower().str.contains("brunei"), "country"] = "BN"
    df.loc[df.address.str.lower().str.contains("drugmotif"), "country"] = "HU"
    df.loc[
        df.address.str.lower().str.contains("safety & environmental assurance centre"),
        "country",
    ] = "UK"
    df.loc[
        df.address.str.lower().str.contains("safety & environmental assurance centre"),
        "country",
    ] = "UK"
    df.loc[df.address.str.lower().str.contains("planck"), "country"] = "DE"
    df.loc[df.address.str.lower().str.contains("namibia"), "country"] = "NA"
    df.loc[df.address.str.lower().str.contains("egypt"), "country"] = "EG"

    # a = []
    # for _, row in df[df.country=="??"].iterrows():
    #     a.append(row.address)
    # for item in Counter(a).most_common():
    #     print(item)

    df["method"] = "Other/Unspecified"
    df.loc[
        (df.subjects.str.lower().str.contains("deep learning"))
        | (df.subjects.str.lower().str.contains("neural network"))
        | (df.subjects.str.lower().str.contains("transformer"))
        | (df.subjects.str.lower().str.contains("autoencoder"))
        | (df.subjects.str.lower().str.contains("encoder"))
        | (df.subjects.str.lower().str.contains("generative adversarial network"))
        | (df.subjects.str.lower().str.contains("perceptron")),
        "method",
    ] = "Neural Networks"

    df.loc[
        (df.subjects.str.lower().str.contains("genetic algorithm"))
        | (df.subjects.str.lower().str.contains("genetic programming"))
        | (df.subjects.str.lower().str.contains("particle swarm optimization"))
        | (df.subjects.str.lower().str.contains("evolutionary algorithm")),
        "method",
    ] = "Genetic/Evolutionary"

    df.loc[
        (df.subjects.str.lower().str.contains("boosting"))
        | (df.subjects.str.lower().str.contains("adaboost"))
        | (df.subjects.str.lower().str.contains("decision tree"))
        | (df.subjects.str.lower().str.contains("random forest")),
        "method",
    ] = "RF/Boosting"

    df.loc[
        (df.subjects.str.lower().str.contains("support vector machine")), "method"
    ] = "SVM"

    df.loc[
        (df.subjects.str.lower().str.contains("regression")), "method"
    ] = "Regression"

    df.loc[
        (df.subjects.str.lower().str.contains("statistics"))
        | (df.subjects.str.lower().str.contains("multivariate statistics"))
        | (df.subjects.str.lower().str.contains("cluster analysis"))
        | (df.subjects.str.lower().str.contains("bayes' theorem"))
        | (df.subjects.str.lower().str.contains("hidden markov model"))
        | (df.subjects.str.lower().str.contains("markov chain"))
        | (df.subjects.str.lower().str.contains("naive bayes classifier"))
        | (df.subjects.str.lower().str.contains("probabilistic logic"))
        | (df.subjects.str.lower().str.contains("bayesian probability"))
        | (df.subjects.str.lower().str.contains("bayesian network"))
        | (df.subjects.str.lower().str.contains("bayesian inference"))
        | (df.subjects.str.lower().str.contains("monte carlo method"))
        | (df.subjects.str.lower().str.contains("annealing"))
        | (df.subjects.str.lower().str.contains("fuzzy logic"))
        | (df.subjects.str.lower().str.contains("inference")),
        "method",
    ] = "Statistic/Probabilistic"

    df.loc[
        (df.subjects.str.lower().str.contains("principal component analysis"))
        | (df.subjects.str.lower().str.contains("linear discriminant analysis"))
        | (df.subjects.str.lower().str.contains("feature selection"))
        | (df.subjects.str.lower().str.contains("feature extraction"))
        | (df.subjects.str.lower().str.contains("dimensionality reduction"))
        | (df.subjects.str.lower().str.contains("self-organizing map"))
        | (df.subjects.str.lower().str.contains("inference")),
        "method",
    ] = "Dimesionality Reduction/Feature Selection"

    df["age"] = 2022 - df.year
    df["citations_per_year"] = df.citations / (df.age + 1)

    return df


def get_field_data(field: str):
    df = pd.read_csv(
        f"bibliometrics/openalex/{field}_all.csv",
        usecols=["country", "year", "count"],
    )
    df = df[df.country != "unknown"]
    df = df[df.year <= 2021]
    return df


def get_un_data():
    cc = coco.CountryConverter()
    # Source: http://data.uis.unesco.org/
    df_demo = pd.read_csv(
        "country_stats/un_demographics.csv",
        usecols=["Indicator", "Country", "Time", "Value"],
    )
    df_rnd = pd.read_csv(
        "country_stats/un_rnd.csv", usecols=["Indicator", "Country", "Time", "Value"]
    )

    df_demo_gdp = df_demo[df_demo.Indicator == "GDP (current US$)"]
    df_demo_pop = df_demo[df_demo.Indicator == "Total population (thousands)"]

    df_rnd_res = df_rnd[df_rnd.Indicator == "Researchers per million inhabitants (FTE)"]
    df_rnd_erd = df_rnd[df_rnd.Indicator == "GERD as a percentage of GDP"]

    df_demo_gdp = df_demo_gdp.rename(columns={"Value": "GDP"})
    df_demo_pop = df_demo_pop.rename(columns={"Value": "Population"})

    df_rnd_res = df_rnd_res.rename(columns={"Value": "Researchers_per_mil"})
    df_rnd_erd = df_rnd_erd.rename(columns={"Value": "GERT_percentage_gdp"})

    df_demo_gdp.drop(columns=["Indicator"], inplace=True)
    df_demo_pop.drop(columns=["Indicator"], inplace=True)

    df_rnd_res.drop(columns=["Indicator"], inplace=True)
    df_rnd_erd.drop(columns=["Indicator"], inplace=True)

    df_un = pd.merge(df_rnd_erd, df_rnd_res, on=["Country", "Time"], how="inner")
    df_un = pd.merge(df_un, df_demo_pop, on=["Country", "Time"], how="inner")
    df_un = pd.merge(df_un, df_demo_gdp, on=["Country", "Time"], how="inner")

    df_un["GDP_per_capita"] = df_un.GDP / (df_un.Population * 1000)
    df_un["Spending"] = (df_un.GERT_percentage_gdp / 100) * df_un.GDP
    df_un["Researchers"] = (df_un.Population / 1000) * df_un.Researchers_per_mil
    df_un["Spending_per_researcher"] = df_un.Spending / df_un.Researchers

    # Get the most recent value
    df_un = df_un.sort_values("Time").groupby(["Country"]).mean().reset_index()
    df_un.columns = df_un.columns.str.lower()
    df_un.country = cc.convert(names=df_un.country, to="ISO2", not_found="Unknown")
    df_un = df_un.groupby("country").mean().reset_index()

    return df_un


def get_oa_data(field):
    df_oa_0 = pd.read_csv(f"bibliometrics/openalex/papers/{field}/pdfs.csv")
    df_oa_1 = pd.read_csv(f"bibliometrics/openalex/papers/{field}/pmc.csv")
    df_oa = pd.concat([df_oa_0, df_oa_1])
    return df_oa.drop(columns=["affiliations", "date", "file", "citations"])
