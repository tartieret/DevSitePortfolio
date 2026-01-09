Title: ORC World Map
Date: 2019-04-11 00:00
Authors: me
Summary: A world overview of the ORC technology
Template: project_detail
save_as: projects/orc-world-map.html
Technologies:vuejs,bootstrap4,sass,javascript,python
Images:projects\orc-world-map1.png,projects\orc-world-map2.png,projects\orc-world-map3.png,projects\orc-world-map4.png
repository:<https://github.com/tartieret/ORC-World-Map>
website: https://orc-world-map.org/

## Project background

The Organic Rankine Cycle (ORC) technology is a way to convert heat into electricity. Its main applications are distributed electricity generation from renewable heat sources (geothermal, biomass, solar) and industrial energy efficiency (heat recovery from industrial processes).
More information about the technology can be found on [Wikipedia](https://en.wikipedia.org/wiki/Organic_Rankine_cycle) or at the [Knowledge Center on ORC](http://www.kcorc.org/en/).

After working for 5 years on ORC systems at [Enertime](https://www.enertime.com/en/home), I noticed that this technology is not very well-known and often underestimated. In 2015, I decided to combined all the known references onto one map in order to monitor the progress of the technology, increase public awareness and motivate new motions and incentives.

## Actions and Outcome

I started by scrapping project data from the websites of ORC manufacturers using custom Python scripts. I then built and released a first version of the site, based on Google Fusion Table. As this was the first successful attempt to measure the progress of this technology over the last decades, it received a lot of interest in the industry.

Most of the data used is publicly available on manufacturers' websites, through press articles or scientific papers. When possible, multiple sources have been used in order to cross-reference the information. Some of the manufacturers directly took part to the survey by sending me their list of references.

The objective is to provide an overview of the ORC market, at the industrial level. This means that small ORC plants at the lab scale or that are not connected to the grid have been ignored.

I continue to maintain the site and update the database periodically. The site became a reference in the ORC industry and is cited in many new scientific papers about the ORC technology.

## Publications

I released [several analyses of the ORC market](https://orc-world-map.org/analysis) using the data collected through this project.

This work was presented in Sepember 2017 at the IV International Seminar on ORC Power Systems in Milan (Italy), and an updated paper was published in collaboration with Marco Astolfi in Energy Procedia:

_[A World Overview of the Organic Rankine Cycle Market, T. Tartière, M. Astolfi, Energy Procedia, 2017, Volume 129, Pages 2-9.](https://orc-world-map.org/docs/WorldOverview2017.pdf)_

## What's next?

Originally built with JQuery and Google Fusion Table, the site was rebuilt in 2022 with VueJS and Google Maps

The new repository [can be found here](https://github.com/tartieret/ORC-World-Map-SPA).
