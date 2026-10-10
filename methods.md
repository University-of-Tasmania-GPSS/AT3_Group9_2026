# Methods

## Methodological Workflow

The following flowchart summarises the research
workflow, from data collection and preparation
through to spatial and socioeconomic analysis.

```{mermaid}
flowchart TD
    A["1. Research question<br/>Crime distribution and socioeconomic associations"]
    B["2. Data collection<br/>ABS boundaries, BOCSAR crime records<br/>and 2021 Census data"]
    C["3. Data preparation<br/>Select 30 LGAs, group offences,<br/>aggregate monthly crime records"]
    D["4. Data integration<br/>Join crime and socioeconomic data<br/>to LGA polygons"]
    E["5A. Spatial analysis<br/>Crime counts, rates and<br/>Getis–Ord Gi* hotspots"]
    F["5B. Socioeconomic analysis<br/>Income, unemployment, education<br/>and crime associations"]
    G["6. Results and interpretation<br/>Maps, hotspot patterns, graphs<br/>and crime trends"]

    A --> B --> C --> D
    D --> E
    D --> F
    E --> G
    F --> G

    classDef main fill:#244B36,color:#ffffff,stroke:#244B36
    classDef prep fill:#FFF3C4,color:#333333,stroke:#D4B94E
    classDef spatial fill:#F9DEDE,color:#333333,stroke:#B85450
    classDef socio fill:#DFEAF9,color:#333333,stroke:#547EAE

    class A,G main
    class B,C,D prep
    class E spatial
    class F socio
```



## Detailed Methodology

The following sections provide further details of the data preparation, socioeconomic statistical analysis and spatial hotspot analysis. Expand each section to explore the methodology.

````{dropdown} Data Collection and Preparation
**Data sources**

Three primary datasets were used in this study:

| Dataset | Source | Purpose |
|---|---|---|
| Local Government Area boundaries (2025) | Australian Bureau of Statistics (ABS) | Provided polygon geometries and geographic identifiers for the 30 selected LGAs. |
| Recorded Criminal Incidents by Month by LGA | NSW Bureau of Crime Statistics and Research (BOCSAR) | Provided monthly recorded crime counts for 2015–2025. |
| 2021 Census General Community Profile | Australian Bureau of Statistics (ABS) | Provided socioeconomic indicators for education, household income and labour force characteristics. |

**Crime classification**

Recorded offences were grouped into three categories:

- **Drug offences:** Possession, dealing, manufacturing and importing.
- **Violent crime:** Abduction and kidnapping, assault, coercive control, homicide, intimidation, stalking and harassment, sexual offences, and robbery.
- **Property offences:** Theft, arson and malicious damage to property.

**Data preparation**

Python was used to clean and integrate the datasets. The workflow involved:

1. Selecting the 30 study-area LGAs using their geographic identifiers.
2. Filtering crime records to the selected LGAs and relevant offence categories.
3. Aggregating monthly crime records into annual counts for 2015–2025.
4. Calculating total recorded crime counts for each crime category across the study period.
5. Extracting the relevant socioeconomic indicators from the 2021 Census.
6. Joining crime and socioeconomic attributes to the LGA polygons using matching geographic identifiers.
7. Checking for missing values, inconsistent identifiers and invalid geometries.

The resulting spatial dataset provided a consistent geographic framework for mapping crime, calculating rates, identifying hotspots and examining socioeconomic associations.
````

````{dropdown} Socioeconomic Statistical Analysis
The socioeconomic analysis investigated associations between crime and three indicators: educational attainment, household income and unemployment.

**Socioeconomic indicators**

- **Education:** Highest year of school completion, sourced from 2021 Census Table G01.
- **Household income:** Median total weekly household income, sourced from 2021 Census Table G02.
- **Unemployment:** Selected labour force statistics, sourced from 2021 Census Table G43.

**Analytical approach**

The socioeconomic indicators were compared with drug offences, violent crime and property offences to investigate potential relationships between socioeconomic conditions and crime.

The analysis considered:
1. Overall associations between the socioeconomic indicators and the three crime categories.
2. Relationships between socioeconomic characteristics and crime across individual LGAs.
3. Patterns that could be explored further through maps and graphs.

The socioeconomic variables represent conditions recorded at the 2021 Census, while crime data span 2015–2025. Therefore, the results should be interpreted as associations rather than evidence of causation. The temporal difference between datasets is also an important limitation.

*Note: Specify the correlation coefficient and any significance tests used once the statistical methods and results have been finalised.*
````

````{dropdown} Spatial Hotspot Statistical Analysis
**Crime counts and rates**

Total recorded incidents were calculated for each LGA and crime category across 2015–2025.

Crime rates were calculated using:

$$
\text{Crime rate} =
\frac{\text{Total recorded incidents (2015–2025)}}
{\text{Population denominator}}
\times 1000
$$

This standardised measure expresses recorded incidents per 1,000 residents. The population denominator used in the analysis should be specified in the final methodology.

**Getis–Ord Gi* hotspot analysis**

Local Getis–Ord Gi* statistics were calculated to identify spatial clusters of high and low crime-rate values across neighbouring LGAs.

The analysis used:

- **Spatial weights:** Queen contiguity, where LGAs are neighbours if their polygons share an edge or vertex.
- **Permutations:** 199 permutations, selected because larger permutation counts caused computational problems.
- **Significance threshold:** p < 0.05.

The results classified LGAs as **hotspots**, **coldspots** or **not statistically significant**, according to the calculated statistics and significance criteria.

Hotspots indicate areas where high values are spatially clustered relative to the spatial-randomness assumption. Coldspots indicate clusters of low values. Areas that do not meet the selected significance threshold are classified as not statistically significant.

**Mapping and interpretation**

The analysis produced thematic maps of crime counts, crime rates and hotspot classifications for drug offences, violent crime and property offences. These maps were used to compare the spatial patterns of each crime category and identify areas for further investigation.
````














### Study Area and Research Design 

MOLLY MAKE A LOCALITY MAPPPPP!!!!!

Three primary datasets were used to investigate the spatial and socioeconomic distribution of crime across selected Local Government Areas (LGAs) in Greater Sydney between January 2015 and December 2025. Crime incident data were obtained from the NSW Bureau of Crime Statistics and Research (BOCSAR), LGA boundary data from the Australian Bureau of Statistics (ABS), and socioeconomic indicators from the 2021 Australian Census.

The datasets were cleaned, aggregated and integrated into a common spatial dataset to enable comparisons between crime patterns and socioeconomic characteristics. The following tables summarise the source data, file formats and their roles in the analysis.

### Data Collection and Preparation 
### LGA Boundary Data

| Item | Details |
| :--- | :--- |
| Data source | Australian Bureau of Statistics (ABS) |
| Original dataset | Local Government Areas 2025.shp |
| Working filename | SydneyLGAs_MGA202056.shp |
| Coordinate reference system | GDA2020 / MGA Zone 56 |
| Geographic identifiers | LGA codes |
| Study area | 30 selected Greater Sydney LGAs |

The LGA boundaries provided the spatial framework for the analysis. The study area was restricted to 30 selected LGAs, identified using their LGA codes, to focus the investigation on the Greater Sydney region.

### Crime Data

| Item | Details |
| :--- | :--- |
| Data source | NSW Bureau of Crime Statistics and Research (BOCSAR) |
| Original dataset | Recorded Criminal Incidents by Month by LGA.csv |
| Working filename | CrimeStatsbyLGA_Sydney.csv |
| Temporal coverage | January 2015 – December 2025 |
| Spatial unit | Local Government Area |
| Crime groupings | Drug offences, violent crime and property offences |
| Main variables | Year, LGA, offence category and incident count |

The crime dataset contained monthly recorded criminal incidents by LGA. The data were filtered to the selected study area and relevant offence categories, then aggregated into annual counts and total counts for the study period.

The three crime groupings were defined as follows:

| Crime grouping | Included offence categories |
| :--- | :--- |
| Drug offences | Possession, dealing, manufacturing and importing |
| Violent crime | Abduction and kidnapping; assault; coercive control; homicide; intimidation, stalking and harassment; sexual offences; robbery |
| Property offences | Theft, arson and malicious damage to property |

These groupings were used to compare the spatial distribution of different crime types across LGAs.

### Socioeconomic Data

| Item | Details |
| :--- | :--- |
| Data source | Australian Bureau of Statistics (ABS) |
| Census dataset | 2021 Census General Community Profile, NSW LGA data |
| Geographic unit | Local Government Area |
| Census year | 2021 |
| Table G01 | Highest year of school completion |
| Table G02 | Median total household income (weekly) |
| Table G43 | Selected labour force statistics |
| Working filenames | 2021Census_G01_NSW_LGA.csv; 2021Census_G02_NSW_LGA.csv; 2021Census_G43_NSW_LGA.csv |

The socioeconomic variables were extracted from the 2021 Census and joined to the LGA spatial dataset using geographic identifiers. The selected indicators were used to investigate associations between crime and educational attainment, household income and unemployment.

The census variables represent socioeconomic conditions at the 2021 Census, rather than annual changes over the entire crime study period. Therefore, relationships between these variables and crime should be interpreted as associations with the selected census-year characteristics.

### Data Preparation and Integration

The datasets were prepared using Python in a Jupyter Notebook environment. GeoPandas was used to manage spatial data, while pandas was used to clean, transform and aggregate tabular data.

The preparation workflow involved the following steps:

1. **Selecting the study area:** Selecting the 30 study-area LGAs and retaining their geographic identifiers and polygon geometries.
2. **Filtering crime records:** Restricting crime records to the selected LGAs and the three crime groupings.
3. **Aggregating crime data:** Converting monthly crime records into annual counts for 2015–2025.
4. **Calculating total counts:** Summing recorded incidents for each crime grouping across the study period.
5. **Extracting socioeconomic indicators:** Obtaining the relevant variables from the ABS 2021 Census tables.
6. **Integrating datasets:** Joining the crime and socioeconomic attributes to the LGA polygons using matching LGA identifiers.
7. **Checking data quality:** Checking for missing values, inconsistent identifiers and invalid geometries before conducting the spatial analysis.

The resulting spatial dataset provided a consistent geographic framework for mapping crime counts, calculating population-standardised crime rates, identifying crime hotspots and examining associations with socioeconomic characteristics.

### Socioeconomic statistical analysis

### Spatial Hotspot statisitcal analysis 



I am a book about ... something! Wikipedia has [information about books](wiki:book): hover over the link for more information.

% An admonition containing a note
:::{note}
Books are usually written on paper ... But Jupyter Book can create _websites_!
:::

If you sold 100 books at \$10 per book, you'd have \$1000 dollars according to [](#eq:book). If instead you publish your Jupyter Book to the web for free, you'd have \$0 dollars!

% An arbitrary math equation
:::{math}
:name: eq:book

x \times y = z
:::

Sometimes when reading it is helpful to foster a _tranquil_ environment. The image in [](#fig:mountains) would be a perfect spot!

% A figure of a photograph of some mountains, followed by a caption
:::{figure} https://github.com/rowanc1/pics/blob/main/mountains.png?raw=true
:label: fig:mountains

A photograph of some beautiful mountains to look at whilst reading.
:::