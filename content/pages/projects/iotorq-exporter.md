Title: ioTORQ Data Exporter
Date: 2019-04-11 00:00
Authors: me
Summary: ETL software to stream data out of industrial facilities
Template: project_detail
save_as: projects/iotorq-exporter.html
Technologies:python,Qt
Images:
website:https://www.iotorq.com/

### Project Background

Integrating our [ioTORQ data platform](/projects/iotorq.html) with industrial facilities often requires the deployment of specific hardware and software equipment to combine multiple on-site data sources and stream data to the cloud. In order to speed up this process, I build a lightweight Extract-Transform-Load desktop software using Python. The architecture of this ETL software is largely inspired by [Apache NIFI](https://nifi.apache.org/). Data processors can be combined to query data from local process historian (SQL servers), transform the data to JSON and send it to our API. It relies on Asyncio for concurrent execution and runs the data processors in parallel.

The software includes a graphical user interface and configuration files so that it can be setup by non-developers.

![Data platform](/images/projects/ioTORQ/dataplatform.jpg)






