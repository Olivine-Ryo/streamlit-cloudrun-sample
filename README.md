Sample code to deploy Streamlit dashboard app with Google Cloud Run
 
# Summary
 
You can deploy Streamlit dashboard app with only two commands.
This sample dashboard visualizes greenhouse gas open data. Data sources are written below.

 
# Usage

1. Clone this repository in Google Cloud Shell.
```bash
$ clone hogehoge
```
2. Deploy with Buildpacks
```bash
$ gcloud run deploy greenhousegas-dashboard --source . --timeout=3600
```

Then you can see your dashboard link in the terminal.
 
# Note
Deployment by Buildpacks occasionally fails because its build time takes more than 10 minutes.
Then you can deploy to other regions or deploy with Dockerfile as below.
```bash
$ gcloud builds submit --tag asia.gcr.io/${PROJECT-ID}/greenhousegas-dashboard:v

$ gcloud run deploy greenhousegas-dashboard --image asia.gcr.io/${PROJECT-ID}/greenhousegas-dashboard:v1
```
 
# Data sources
This dashboard is the reproduction of [CO2 Data Explorer](https://ourworldindata.org/explorers/co2) in Our World in Data under [the Creative Commons BY license](https://creativecommons.org/licenses/by/4.0/).
The data sources are as below. All of them are under [the Creative Commons BY license](https://creativecommons.org/licenses/by/4.0/).
- [Global Carbon Project](https://www.icos-cp.eu/science-and-impact/global-carbon-budget/2021)
- [Maddison Project Database 2020 (Bolt and van Zanden, 2020)](https://www.rug.nl/ggdc/historicaldevelopment/maddison/releases/maddison-project-database-2020)
- [CAIT Climate Data Explorer via Climate Watch](https://www.climatewatchdata.org/data-explorer/historical-emissions?historical-emissions-data-sources=cait&historical-emissions-gases=all-ghg&historical-emissions-regions=All%20Selected&historical-emissions-sectors=total-including-lucf%2Ctotal-including-lucf&page=1)