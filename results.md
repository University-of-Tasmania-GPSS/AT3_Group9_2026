# Results

## Spatial Correlation Results

:::{note} Interactive Maps:
Scroll on the interactive map panel to explore the contents. Legend and metadata information can be found below the map frame within the panel. The maps can be explored in fullscreen (recommended for better visualisation) by clicking the icon at the bottom of the map panel. 
:::


### Map 1: Interactive map of crime counts and rates of Greater Sydney
<iframe src="https://at3group92026-rq8a73wjsafwnd7mhl5y2k.streamlit.app/?embed=true&refresh=20261010" width="100%" height="800" style="border: none;" allow="clipboard-write"> </iframe>

<div style="
    background-color: #e8f0ec;
    border-left: 5px solid #183D32;
    padding: 18px 22px;
    border-radius: 8px;
    margin: 20px 0;
">

**Map Highlights**

- Overall, crime counts tend to be lower in the northern LGAs, while higher counts are observed across southern and western LGAs. This spatial pattern is consistent across all three crime categories.

- A similar pattern is evident in crime rates, with northern LGAs generally recording lower rates than those in the southern and western parts of the study area.
- Sydney LGA presents the highest crime count for drug offences  
- Blacktown LGA presents the highest crime count for violent crime and property offences, However, Sydney LGA presnts the highest crime rate for all crime types 


</div>

### Map 2: Interactive crime trends map of Greater Sydney 

<iframe src="https://at3group92026-5rrjmp29vpltlljde6gjka.streamlit.app/?embed=true&refresh=20261010" width="100%" height="800" style="border: none;" allow="clipboard-write"> </iframe>


<div style="
    background-color: #e8f0ec;
    border-left: 5px solid #183D32;
    padding: 18px 22px;
    border-radius: 8px;
    margin: 20px 0;
">

**Map Highlights**

- Blacktown, Paramatta and Burwood all have increasing drug offences over time. All other LGA's have decreasing 
drug offences or no correlation over time 
- Majority of LGA's, except Sydney, Hunters Hill, Mosman and North Sydney, have increasing violent crime over time 
- Majority of LGA's, except Strathfield, Camden, Parramatta, Ryde and Lane Cove, have decreasing property offences over time 

</div>


### Map 3: Interactive crime hotspot map of Greater Sydney

<iframe src="https://at3group92026-6tqnkabpc3aor2awnntgcy.streamlit.app/?embed=true&refresh=20261010" width="100%" height="800" style="border: none;" allow="clipboard-write"> </iframe>


<div style="
    background-color: #e8f0ec;
    border-left: 5px solid #183D32;
    padding: 18px 22px;
    border-radius: 8px;
    margin: 20px 0;
">

**Map Highlights**

- Across all crime categories cold spots were identifyied on North Eastern LGA's. This includes Northern Beaches, Ku-ring-ga and Willoughby
- No hotpsots were identified on the North Shore 
- Woollahra was identified as a hotspot for all three crime types
- Drug Offence hotspots were idenitified in Woollahra, Randwick and Bayside
- Violent Crime hotspots were idenitified in Fairfield and Woollahra
- Property Offence hotspots were identified in Randwick and Woollahra 
</div>


### Table 1: Global Getis–Ord G Results 
Overall spatial concentration of crime rates across the whole study area (30 LGAs), note this is not identifying individual hotspots

| Crime category | Observed G | Expected G | Z-score | p-value | Statistically significant (p < 0.05) |
|---|---:|---:|---:|---:|:---:|
| Drug offences | 0.1707 | 0.1310 | 1.7492 | 0.0401 | Yes |
| Violent crime | 0.1580 | 0.1310 | 2.2041 | 0.0138 | Yes |
| Property offences | 0.1433 | 0.1310 | 1.3328 | 0.0913 | No |

<div style="
    background-color: #e8f0ec;
    border-left: 5px solid #183D32;
    padding: 18px 22px;
    border-radius: 8px;
    margin: 20px 0;
">

- Drug offences: The Global Getis–Ord G statistic was statistically significant (G=0.1707, p=0.0401). The observed value exceeded the expected value, indicating evidence of an overall spatial concentration of high drug-offence rates.

- Violent crime: Violent crime showed the strongest statistical evidence of spatial concentration (G=0.1580, Z=2.2041, p=0.0138). The result suggests that violent crime rates were more spatially concentrated than expected under spatial randomness.

- Property offences: The result was not statistically significant (G=0.1433, p=0.0913). Although the observed statistic exceeded the expected value, there was insufficient evidence at the 0.05 significance level to conclude that property-offence rates displayed significant overall spatial concentration.
</div>



# Socio Economic Correlation Results 
Note: Some scatter plots in this section have a line of best fit. This is to highlight the direction of correlation.

### Graph 1: Example Data with Sydney LGA
:::{figure} HighvsPO(SYD).png
:::

<div style="
    background-color: #e8f0ec;
    border-left: 5px solid #183D32;
    padding: 18px 22px;
    border-radius: 8px;
    margin: 10px 0 40px;
">

This graph displays the relationship between property offences and year 12 completion. Sydney (labelled) stands out as an obvious outlier. This relationship with the Sydney LGA being an outlier due to its high crime rate occurs across all crime types. As such the following graphs will not include the Sydney LGA (see discussion for reasoning).

</div>

### Graph 2: Example Data without Sydney LGA
:::{figure} HighvsPO.png
:::

<div style="
    background-color: #e8f0ec;
    border-left: 5px solid #183D32;
    padding: 18px 22px;
    border-radius: 8px;
    margin: 10px 0 40px;
">

Whilst this graph here does not display the strongest correlation out of all the relationships assessed in this analysis, it does show the greatest difference in the correlation p value between the dataset with the Sydney LGA and the dataset without the LGA. With the Sydney LGA, the relationship is not statistically signifigant but without the Sydney LGA it is (with an r value of -0.41, suggesting moderate negative correlation). 

</div>

### Graph 3: Example Data of High Correlation
:::{figure} HighvsVC.png
:::

<div style="
    background-color: #e8f0ec;
    border-left: 5px solid #183D32;
    padding: 18px 22px;
    border-radius: 8px;
    margin: 10px 0 40px;
">

This graph displays the relationship with the strongest correlation (r = -0.74). This data displays that in greater Sydney, rates of violent crime and the percentage of residents who comeplete year 12 are strongly negatively correlated (as high school completion increases, violent crime decreases).

</div>

### Graph 3: Example Data of Moderate Correlation
:::{figure} UnemvsDO.png
:::

<div style="
    background-color: #e8f0ec;
    border-left: 5px solid #183D32;
    padding: 18px 22px;
    border-radius: 8px;
    margin: 10px 0 40px;
">

This graph displays a relationship with moderate correlation (r = 0.40). This data displays that in greater Sydney, rates of drug offences and the rate of unemployment is moderatly positively correlated.

</div>

### Table 1: Pearson's Correlation Coefficients between Socioeconomic Factors and Crime Types
| Socioeconomic Factor | Violent Crime | Property Offences | Drug Offences |
|:---|:---:|:---:|:---:|
| Median Weekly Income ($) | -0.51 | -0.37 | Not Statistically Significant |
| Unemployment (%) | 0.44 | 0.36 | Not Statistically Significant |
| Year 12 Completion (%) | -0.44 | Not Statistically Significant | Not Statistically Significant |


### Table 2: Pearson's Correlation Coefficients between Socioeconomic Factors and Crime Types (Sydney LGA Removed)
| Socioeconomic Factor | Violent Crime | Property Offences | Drug Offences |
|:---|:---:|:---:|:---:|
| Median Weekly Income ($) | -0.67 | -0.48 | -0.41 |
| Unemployment (%) | 0.54 | 0.44 | 0.40 |
| Year 12 Completion (%) | -0.74 | -0.41 | Not Statistically Significant |



# Time Correlation Results

````{dropdown} Table 3: Crime Rate and Time Correlation (with Gradients)

| LGA | Drug Offences: Correlation Coefficient | Drug Offences: Gradient | Violent Crime: Correlation Coefficient | Violent Crime: Gradient | Property Offences: Correlation Coefficient | Property Offences: Gradient|
|:---|---:|---:|---:|---:|---:|---:|
| Bayside | -0.66 | -0.13 | 0.80 | 0.32 | -0.75 | -0.45 |
| Blacktown | 0.74 | 0.11 | 0.92 | 0.56 | -0.86 | -1.09 |
| Burwood | 0.62 | 0.19 | 0.88 | 0.66 | Not significant | 0 |
| Camden | -0.88 | -0.20 | 0.95 | 0.52 | Not significant | 0 |
| Campbelltown | -0.81 | -0.14 | 0.88 | 0.66 | -0.91 | -1.18 |
| Canada Bay | Not significant | 0 | 0.96 | 0.37 | -0.77 | -0.54 |
| Canterbury-Bankstown | Not significant | 0 | 0.78 | 0.36 | -0.85 | -0.65 |
| Cumberland | Not significant | 0 | 0.86 | 0.29 | -0.66 | -0.47 |
| Fairfield | Not significant | 0 | 0.72 | 0.22 | -0.91 | -0.80 |
| Georges River | Not significant | 0 | 0.67 | 0.11 | -0.63 | -0.41 |
| Hornsby | Not significant | 0 | 0.92 | 0.24 | -0.87 | -0.69 |
| Hunters Hill | Not significant | 0 | Not significant | 0 | -0.80 | -0.86 |
| Inner West | Not significant | 0 | 0.77 | 0.33 | -0.83 | -0.82 |
| Ku-ring-gai | Not significant | 0 | 0.94 | 0.21 | -0.90 | -0.57 |
| Lane Cove | Not significant | 0 | 0.87 | 0.25 | Not significant | 0 |
| Liverpool | Not significant | 0 | 0.89 | 0.69 | -0.77 | -0.71 |
| Mosman | Not significant | 0 | Not significant | 0 | -0.93 | -0.75 |
| North Sydney | -0.84 | -0.43 | Not significant | 0 | -0.92 | -0.88 |
| Northern Beaches | Not significant | 0 | 0.66 | 0.14 | -0.93 | -0.80 |
| Parramatta | 0.88 | 0.26 | 0.97 | 0.42 | Not significant | 0 |
| Penrith | -0.78 | -0.12 | 0.85 | 0.54 | -0.74 | -0.65 |
| Randwick | Not significant | 0 | 0.62 | 0.18 | -0.74 | -0.66 |
| Ryde | Not significant | 0 | 0.80 | 0.24 | Not significant | 0 |
| Strathfield | Not significant | 0 | 0.69 | 0.30 | Not significant | 0 |
| Sutherland | -0.62 | -0.14 | 0.77 | 0.33 | -0.90 | -0.80 |
| Sydney | 0.85 | -1.18 | Not significant | 0 | -0.65 | -1.59 |
| The Hills | -0.89 | -0.08 | 0.88 | 0.31 | -0.78 | -0.31 |
| Waverley | -0.74 | -0.41 | 0.74 | 0.20 | -0.78 | -0.89 |
| Willoughby | Not significant | 0 | 0.91 | 0.24 | -0.79 | -0.82 |
| Woollahra | -0.61 | -0.34 | 0.91 | 0.30 | -0.82 | -0.76 |
````


### Graph 4: Example Data of Strong Positive Correlation (Increase over Time)
:::{figure} paramatta.png
:::



### Graph 5: Example Data of Strong Negative Correlation (Decrease over Time)
:::{figure} NorthernBeaches.png
:::


### Graph 6: Example Data of No Correlation:
:::{figure} Will.png
:::



% Leave at the bottom
<div style="border-top: 1px solid #cccccc; margin-top: 35px; padding-top: 12px; font-size: 0.9em; color: #666;">
  GIS Project | Greater Sydney, New South Wales | 2015–2025 | M. Marshall & T. Powell
</div>

