# Methods

## Study Area and Research Design 


### Locality Map
:::{figure} Locality Map.jpg
:label: fig:Map of LGA's in the Greater Sydney Area that were used in the project 

A photograph of some beautiful mountains to look at whilst reading.
:::

Three primary datasets were used to investigate the spatial and socioeconomic distribution of crime across selected Local Government Areas (LGAs) in Greater Sydney between January 2015 and December 2025. Crime incident data were obtained from the NSW Bureau of Crime Statistics and Research (BOCSAR), LGA boundary data from the Australian Bureau of Statistics (ABS), and socioeconomic indicators from the 2021 Australian Census.

The datasets were cleaned, aggregated and integrated into a common spatial dataset to enable comparisons between crime patterns and socioeconomic characteristics. The following tables summarise the source data, file formats and their roles in the analysis.



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

   
    classDef main fill:#244B36,color:#ffffff,stroke:#244B36,rx:15,ry:15
    classDef prep fill:#FFF3C4,color:#333333,stroke:#D4B94E,rx:15,ry:15
    classDef spatial fill:#F9DEDE,color:#333333,stroke:#B85450,rx:15,ry:15
    classDef socio fill:#DFEAF9,color:#333333,stroke:#547EAE,rx:15,ry:15

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
| Local Government Areas (2025) | Australian Bureau of Statistics (ABS) | Provided polygon geometries and geographic identifiers for the 30 selected LGAs. |
| Recorded Criminal Incidents by Month by LGA | NSW Bureau of Crime Statistics and Research (BOCSAR) | Provided monthly recorded crime counts for 2015–2025. |
| 2021 Census General Community Profile G01, G02 & G43 | Australian Bureau of Statistics (ABS) | Provided socioeconomic indicators for education, household income and labour force characteristics. |

**Crime classification**

Recorded offences were grouped into three categories:

- **Drug offences:** Possession, dealing, manufacturing and importing.
- **Violent crime:** Abduction and kidnapping, assault, coercive control, homicide, intimidation, stalking and harassment, sexual offences, and robbery.
- **Property offences:** Theft, arson and malicious damage to property.

**Data preparation**

Python was used to clean and integrate the datasets and perform the statsitical analysis. Streamlit was used to host the webmaps as an app and Jupyter Book to display present the porject. 

The following libaries were used during this project:

```python
import geopandas as gpd
import rasterio
import xarray as xr
import leafmap
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plot
from scipy import stats
```


The workflow involved:

1. Selecting the 30 study-area LGAs using their geographic identifiers.
2. Filtering crime records to the selected LGAs and relevant offence categories.
3. Aggregating monthly crime records into annual counts for 2015–2025.
4. Calculating total recorded crime counts for each crime category across the study period.
5. Extracting the relevant socioeconomic indicators from the 2021 Census.
6. Joining crime and socioeconomic attributes to the LGA polygons using matching geographic identifiers.
7. Checking for missing values, inconsistent identifiers and invalid geometries.

The resulting spatial dataset provided a consistent geographic framework for mapping crime, calculating rates, identifying hotspots and examining socioeconomic associations.

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

````

````{dropdown} Socioeconomic Statistical Analysis
The socioeconomic analysis investigated associations between crime and four indicators: time, year 12 completion in the adult population, household income and unemployment.

**Socioeconomic indicators**

- **Education:** Highest year of school completion, sourced from 2021 Census Table G01.
- **Household income:** Median total weekly household income, sourced from 2021 Census Table G02.
- **Unemployment:** Selected labour force statistics, sourced from 2021 Census Table G43.

**Analytical approach**

The socioeconomic indicators were compared with drug offences, violent crime and property offences to investigate potential relationships between socioeconomic conditions and crime. The socioeconomic variables represent conditions recorded at the 2021 Census, while crime data span 2015–2025. Pearson's correlation coefficient is a value between -1 and 1 which quantifies how linear the relationship between 2 variables is. The signifigance threshold was a p value of 0.05. Pearson's correlation coefficent represents assosiations between datasets, not nessesarily causation. 

The analysis considered:
1. Relationships between socioeconomic characteristics and crime the whole of greater Sydney.
2. The change in crime rates over time in each individual LGA

**Socioeconomic Correlation Analysis**

Pearson's correlation coeffcient was calculated for each crime type (rate per 1000 people for each LGA) and each socioeconomic variable (for each LGA) resulting in r and p values.  

**Time Correlation Analysis**

The changes in crime rate over time (each year from 2015-2025) were plotted and then had a correlation coefficent calculated to see if there was a statistically signifigant relationship over time. **CODE** was used to perform a least squares analysis on the dataset to determine a linear (first order) line of best fit for the dataset. The slope value of this line of best fit was used to quantify the rate of change over time. LGAs which did not have a statistically signifigant change in crime rate over time were given a rate of change over time value of 0. 


````

````{dropdown} Spatial Hotspot Statistical Analysis
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


<div style="border-top: 1px solid #cccccc; margin-top: 35px; padding-top: 12px; font-size: 0.9em; color: #666;">
  GIS Project | Greater Sydney, New South Wales | 2015–2025
</div>










