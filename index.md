# KGG375 AT3 GIS Project 

<div style="
    background-color: #244B36;
    padding: 50px 30px;
    border-radius: 12px;
    margin-bottom: 30px;
    text-align: center;
">

  <div style="
      color: #FFFFFF;
      font-size: 2.4rem;
      font-weight: 700;
      line-height: 1.3;
      margin-bottom: 20px;
  ">
    The Wild West? 
    <br>
    Mapping Crime and Socioeconomic Patterns Across Greater Sydney
  </div>

  <div style="
      width: 70px;
      height: 3px;
      background-color: #FFD700;
      margin: 25px auto;
  "></div>

  <div style="
      color: #FFFFFF;
      font-size: 1.15rem;
      line-height: 1.6;
  ">
    A GIS Analysis of Crime Hotspots and Socioeconomic Factors
  </div>

  <div style="
      color: #FFD700;
      font-size: 1rem;
      line-height: 1.6;
  ">
    Molly Marshall & Tara Powell
  </div>

</div>


:::{note} Content Warning:
Whilst nothing is explicitly described, this project discusses, explores and names a wide range of criminal offences. Many of these offences (particually those classified under Violent Crime) are confronting and may be upsetting for some readers/viewers. 

If you have experienced violence or sexual assault and need immediate or ongoing help, contact 1800 RESPECT (1800 737 732) to talk to a counsellor from the national sexual assault and domestic violence hotline. For confidential support and information, contact Safe Steps’ 24/7 family violence response line on 1800 015 188.

If you have concerns about your safety or that of someone else, please contact the police in your state or territory, or call Triple Zero (000) for emergency help.
:::

### Why Map Crime?

Crime does not occur uniformly across cities. Understanding where offences are concentrated, and how these patterns vary between communities, can help reveal important spatial differences in public safety (Rosser et al., 2017). Geographic Information Systems (GIS) provide tools to map these patterns, identify crime hotspots and investigate how crime rates vary across different areas.


:::{figure} https://i.guim.co.uk/img/media/55f3339c15ca84a567a45c39ee96cefc93c82b40/0_0_6207_4138/master/6207.jpg?width=465&dpr=1&s=none&crop=none
:label: fig:Sydney Police Car

A photograph of Sydney police car Photograph: Dan Himbrechts/AAPsome
:::

### Project Overview

#### Research Question 

How does the spatial distribution of crime (drug offences, violent crime and property offences) vary across Greater Sydney's Local Government Areas (LGAs), and to what extent is crime rate associated with unemployment, income and high-school completion? 

#### What Will This Project Investigate?

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 18px; margin: 25px 0 35px;">

  <div style="background: #eaf2f8; padding: 22px; border-radius: 12px; text-align: center;">
    <div style="font-size: 36px;">🗺️</div>
    <h3 style="color: #245580;">Crime Distribution</h3>
    <p>Map recorded crime counts and rates, examining how they vary across Greater Sydney.</p>
  </div>

  <div style="background: #fcebea; padding: 22px; border-radius: 12px; text-align: center;">
    <div style="font-size: 36px;">📍</div>
    <h3 style="color: #a93226;">Crime Hotspots</h3>
    <p>Hotspot analysis to identify and visualise locations with high concentrations of recorded offences.</p>
  </div>

  <div style="background: #e8f5e9; padding: 22px; border-radius: 12px; text-align: center;">
    <div style="font-size: 36px;">📊</div>
    <h3 style="color: #287747;">Socioeconomic Factors</h3>
    <p>Explore associations between socioeconomic factors, unemployment, income and education, and crime rates.</p>
  </div>

  <div style="background: #fff3df; padding: 22px; border-radius: 12px; text-align: center;">
    <div style="font-size: 36px;">🔎</div>
    <h3 style="color: #996515;">Spatial Analysis</h3>
    <p>Use GIS workflows in Python to investigate geographic patterns.</p>
  </div>

</div>

####  Background

This project uses GIS to investigate the spatial distribution of recorded crime across selected Local Government Areas (LGAs) in Greater Sydney between 2015 and 2025. It identifies areas with higher concentrations of crime and explores whether crime rates are associated with socioeconomic characteristics, including unemployment, weekly household income and high-school completion.

The relationship between crime and socioeconomic conditions is important when examining differences in crime rates between urban areas. Weatherburn (1992) explores the relationship between economic adversity and crime, while Walker and Henderson (1991) discuss Australian crime trends and the importance of considering social and demographic factors when interpreting crime statistics. Together, these studies highlight the value of examining socioeconomic conditions alongside geographic crime patterns.

Sharma and Tailor (2023) further demonstrate the value of spatial analysis by investigating crime hotspots and urban characteristics in Surat, India. Their research compares spatial interpolation techniques and examines associations between crime, land use and road connectivity. Although their findings relate to a different urban context, the study highlights the importance of appropriate GIS methods when investigating spatial crime patterns. Further studies also demonstrate the value of GIS for identifying crime hotspots. Ansari and Kale (2014), in their study of Aurangabad City, used techniques including Kernel Density Estimation (KDE), Inverse Distance Weighting (IDW) and Getis-Ord Gi* to identify concentrations of criminal activity. Similarly, Chainey, Tompson and Uhlig (2008) compared different crime hotspot mapping techniques, highlighting the importance of selecting appropriate methods for identifying spatial crime patterns. These studies provide a foundation for using GIS to investigate crime hotspots across Greater Sydney.

Crime trends in New South Wales (NSW) have changed considerably over recent decades, with long-term declines in many property offences and a more complex pattern of change in violent crime. Payne (2025) revisits the widely documented NSW crime decline and demonstrates that findings can be influenced by changes in data-matching methods and the way young people are processed through the criminal justice system. More recent statistics show that, across Greater Sydney, violent offences increased by an average of 2.1% annually over the ten years to June 2025, while property offences declined by an average of 3.0% annually (BOCSAR, 2025). High-profile violent incidents in Sydney have also drawn attention to how crime is understood and represented publicly. Tomkinson and Harper (2025) examine how the Bondi Junction and Wakeley stabbing attacks in April 2024 were framed differently within media and political discourse, particularly in relation to gender-based violence and ideological extremism. Their research highlights how media and political narratives can shape the public understanding and interpretation of violent crime, demonstrating the importance of considering how crime is represented alongside its recorded patterns. Together, these studies highlight the importance of examining different crime categories separately and considering both changes over time and differences between locations. This provides context for investigating the spatial distribution of drug, violent and property offences across Greater Sydney LGAs and their associations with socioeconomic characteristics.

By combining crime data with socioeconomic information, this project aims to provide a clearer picture of how crime patterns vary geographically. Specifically, it explores the spatial distribution of crime and whether differences in crime rates correspond with variations in unemployment, household income and high-school completion. These relationships are examined as spatial associations rather than evidence that socioeconomic conditions directly cause crime.


<div style="border-top: 1px solid #cccccc; margin-top: 35px; padding-top: 12px; font-size: 0.9em; color: #666;">
  GIS Project | Greater Sydney, New South Wales | 2015–2025 | M. Marshall & T. Powell
</div>















