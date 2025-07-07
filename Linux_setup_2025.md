# Installationsvejledning: Opsætning af R, Docker, SQL Server og Azure Data Studio på Linux (Ubuntu)

Hjælp til at sætte Linux op til SSI SQL kursus 2025


# 1. Installer R

R er et programmeringssprog, der bruges til statistik, datavisualisering og analyse.
Åbn terminalen og kør følgende kommandoer én ad gangen:
```bash
sudo apt update -qq
sudo apt install --no-install-recommends software-properties-common dirmngr
wget -qO- https://cloud.r-project.org/bin/linux/ubuntu/marutter_pubkey.asc | sudo tee -a /etc/apt/trusted.gpg.d/cran_ubuntu_key.asc
sudo add-apt-repository "deb https://cloud.r-project.org/bin/linux/ubuntu $(lsb_release -cs)-cran40/"
sudo apt update
sudo apt install --no-install-recommends r-base
```

## 2. Installer nødvendige R-pakker

Når R er installeret, skriv `R` i terminalen  og tryk Enter.  Eller åben kursus-rapporten.
Når du er inde i R, kopier og indsæt følgende:
```R
install.packages('zoo')
install.packages('tidyverse')
install.packages('ggsci')
install.packages('viridis')
install.packages('odbc')
```
## 3. Installer Azure Data Studio

Azure Data Studio er et grafisk værktøj til at arbejde med SQL Server.

1.  Gå til: [https://learn.microsoft.com/en-us/azure-data-studio/download-azure-data-studio](https://learn.microsoft.com/en-us/azure-data-studio/download-azure-data-studio)
    
2.  Download den version der hedder: `azuredatastudio-linux-x64.deb` (

3.  Når den er downloadet, kør i terminalen (husk at sætte versionsnummeret ind:
```bash
cd ~/Downloads
sudo dpkg -i azuredatastudio-linux-version-nummer.deb
```
4. Du kan derefter finde Azure Data Studio i programmenuen – højreklik og vælg “Pin to dash”.

## 4. Installer Docker

```bash
sudo apt install docker.io docker-compose
sudo systemctl enable --now docker
```

## 5. Kør SQL Server i Docker

Dette opsætter en Microsoft SQL Server container. Standardadgangskoden er: `Gebt123456`.
```bash
sudo docker pull mcr.microsoft.com/mssql/server:2022-latest
sudo docker run --restart=always -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=Gebt123456" \
-e "TZ=Europe/Copenhagen" -p 1433:1433 --name sqlserver --hostname sqlserver \
-d mcr.microsoft.com/mssql/server:2022-latest
```
### tjek at serveren kører med
```bash
sudo docker ps
```

### Kopier Data over på Sql Server Docker container
```bash
sudo docker cp "/media/gebt/NO\ NAME/data/" sqlserver:/tmp/.
```

## 6. Installer ODBC-driver til SQL Server

Dette tillader R og andre programmer at oprette forbindelse til SQL Server.

```bash
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list
sudo apt update
sudo ACCEPT_EULA=Y apt install -y msodbcsql18
```
Hvis du får fejl, så se fejlsøgningsafsnittet nederst.

# Mulige fejl

### Problem: tidyverse virker ikke når man "knitter"

kør følgende i R for at geninstallere en dependency "stringi":

```R
install.packages("stringi", type = "source")
```

### Problem: tidyverse er installeret, men kan ikke findes

Installer dev tools
```bash
sudo apt-get update
sudo apt-get install -y build-essential
```
hvis det ikke virker er det et mere kompleks problem, nok med nogle manglende pakker. Skaf en computer der virker sammenlign med den der virker

-   Find hvilken `.h`-fil der mangler, fx `zlib.h`.
    
Find pakken på den der virker med:

```bash 
dpkg -S zlib.h
```
output: 
zlib1g-dev:amd64: /usr/include/zlib.h 
her kan man se dev navnet "zlib1g-dev"

søg og isntaller på den der ikke virker
```bash
apt search zlib1g-dev
sudo apt install zlib1g-dev
```
gentag med alle manglende filer
## Problem: msodbcsql18 ikke fundet

Kør igen (skal ikke være inde i docker containeren)
```bash
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list
sudo apt update
sudo ACCEPT_EULA=Y apt install -y msodbcsql18
```

## Problem: mutate() findes ikke

sørg for at downloade og køre:

```r
install.packages("dplyr")
install.packages("lubridate")

library(dplyr)
library(lubridate)
```

## Problem: låsning i ODBC / dpkg

Du vil kun se denne error, hvis output er en process der aldrig stopper med at køre
for at dræbe den:
```bash
sudo kill -9 7791
sudo rm /var/lib/dpkg/lock-frontend
sudo dpkg --configure -a
sudo apt install unixodbc
```

## azure data studio åbner ikke (plaster løsning)
rediger denne fil:
```bash
sudo nano /usr/share/applications/azuredatastudio.desktop
```
I linjerne der starter med `Exec=`, tilføj `--no-sandbox` før `--unity-launch` og `--new-window`.
