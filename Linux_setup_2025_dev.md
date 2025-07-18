# 1: Installer r - from "https://cran.r-project.org/"
sudo apt update -qq
sudo apt install --no-install-recommends software-properties-common dirmngr
wget -qO- https://cloud.r-project.org/bin/linux/ubuntu/marutter_pubkey.asc | sudo tee -a /etc/apt/trusted.gpg.d/cran_ubuntu_key.asc
sudo add-apt-repository "deb https://cloud.r-project.org/bin/linux/ubuntu $(lsb_release -cs)-cran40/"
sudo apt install --no-install-recommends r-base

# 1.1: installer unixodbc
sudo apt install unixodbc unixodbc-dev

# 2: installer docker
sudo apt install docker.io docker-compose
systemctl enable --now docker

# 3: installer SQL server "password=Gebt123456"
sudo docker pull mcr.microsoft.com/mssql/server:2022-latest
sudo docker run --restart=always -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=Gebt123456" -e "TZ=Europe/Copenhagen" -p 1433:1433 --name sqlserver --hostname sqlserver -d mcr.microsoft.com/mssql/server:2022-latest

# 3.1: check om SQL server kører 
sudo docker ps 

# 4: Kopier data ind på SQL serveren - erstat "vejen til din data" ("" skal også erstattes) 
sudo docker cp "vejen til din data" sqlserver:/tmp/.

# 5: Installer Azure (Ikke ændret fra 2024)
cp /media/gebt/NO\ NAME/SQL_Course/azuredatastudio-linux-1.48.0.deb ~/Downloads/.
cd ~
sudo dpkg -i ./Downloads/azuredatastudio-linux-1.48.0.deb
Klik oppe i venstre hjørne og søg efter Azure Data Studio, højreklik og pin to dash
Åben Azure
Gå til Extensions og hent SQL Server Import

# 6: load og start den modificerede rstudio container (gennemfør 6.1, hvis dette er den første pc der sættes op)
sudo docker load -i vejen/til/rstudio_modifed
sudo docker run -d --restart=always -p 8888:8787 -e PASSWORD=password --name rstudio_modified rstudio_modified
sudo apt-get update
sudo apt-get install unixodbc-dev


###### possible errors and fixes ######

#1: load fail for tidyverse when knitting
stringi needs reinstall
install.packages("stringi", type = "source")'


#2: tidyverse does not exist in the system, even when installed. Likely beacause of missing dev tools
find missing tool on working pc (might be something like curl.h, zlib.h or some variantion of x.h)

#2.1: first try:
sudo apt-get update
sudo apt-get install -y build-essential

#2.2: så gør dette hvis 2.1 ikke virker

dpkg -S tool

eksempel på computer der virker
dpkg -S zlib.h
output -> zlib1g-dev:amd64: /usr/include/zlib.h # her kan man se dev navnet "zlib1g-dev"

søg på tool navnet på pc der ikke virker
apt search zlib1g-dev

installer toolet der mangler på pc der ikke virker
sudo apt install zlib1g-dev

#3: unable to locate msodbcsql18
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list
sudo apt update
sudo ACCEPT_EULA=Y apt install -y msodbcsql18

#4: mutate() function does not exist (and try if other functions have the same issue)
- install these
library(dplyr)
library(lubridate)

#5: cache lock error (odbc)
der er nok en process der ikke gøres færdig under "ps -p 7791", så dræb den og start forfra (kan være en anden port)
sudo kill 7791

tjek om den er der
ps -p 7791
hvis den stadig er kører:
sudo kill -9 7791

sudo rm /var/lib/dpkg/lock-frontend -a
sudo dpkg --configure -a 

kør igen 
sudo apt install unixodbc

# azuredatastudio kan ikke åbne 
gå ind i azuredatastudio filen via texteditoren (path: /usr/share/applications/azuredatastudio.desktop) og sæt --no-sandbox azuredatastudio i de to executables. Før --unity-launch og før --new-window