#NOTE:
når du installerer pakker i R scriptet skal du huske følgende for odbc isntallationen
sudo apt install unixodbc-dev

#1 Install Docker
sudo apt install docker.io docker-compose
systemctl enable --now docker

#2 Installer SQL Server
sudo docker pull mcr.microsoft.com/mssql/server:2022-latest
sudo docker run --restart=always -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=Gebt123456" -e "TZ=Europe/Copenhagen" -p 1433:1433 --name sqlserver --hostname sqlserver -d mcr.microsoft.com/mssql/server:2022-latest

#2.1 Installer rstudio server
docker pull rocker/rstudio
sudo docker run -d --restart=always -p 8888:8787 -e PASSWORD=password --name rstudio rocker/rstudio
sudo docker cp /media/gebt/NO\ NAME/SQL_Course/SQL24_data/'Module 4'/SQL_Course_Report_Local.Rmd rstudio:/home/rstudio/.

#2.2 REMEMBER TO RUN! for the libraries to work in the container
sudo apt-get update

#3 Kopier Data over på Sql Server Docker container
sudo docker cp "/media/gebt/NO\ NAME/data/" sqlserver:/tmp/.
 
#4 Installer Azure (Ikke ændret fra 2024)
cp /media/gebt/NO\ NAME/SQL_Course/azuredatastudio-linux-1.48.0.deb ~/Downloads/.
cd ~
sudo dpkg -i ./Downloads/azuredatastudio-linux-1.48.0.deb
Klik oppe i venstre hjørne og søg efter Azure Data Studio, højreklik og pin to dash
Åben Azure
Gå til Extensions og hent SQL Server Import

#5 Lav lokalhost og tabeller
Create Connection i Azure
Server: localhost
Auth Type: SQL Authentication
username: sa
Password: Gebt123456
Remember password

New Query på localhost
Copy/Paste fra SQL_Setup.txt

## Load modificerede rstudio image and start modified RStudio container
sudo docker load -i /home/gebt/Desktop/SQL_course_2025/rstudio_modified
sudo docker run -d --restart=always -p 8888:8787 -e PASSWORD=password --name rstudio_modified rstudio_modified
## if odbc not able to be installed, run
    sudo apt-get update
    sudo apt-get install unixodbc-dev

http://localhost:8888/
username: rstudio
password: password
Run report to make sure it works

## LibreOffice to view word docs
sudo apt-get update && sudo apt-get install libreoffice

##################################################################################################################################
## Preparing customised RStudio image (Only needed to create the image once, and then that image is used on the other computers)
docker pull rocker/rstudio
sudo docker run -d --restart=always -p 8888:8787 -e PASSWORD=password --name rstudio rocker/rstudio
sudo docker cp /media/gebt/NO\ NAME/SQL_Course/SQL24_data/'Module 4'/SQL_Course_Report_Local.Rmd rstudio:/home/rstudio/.
sudo docker exec -it rstudio bash
sudo apt-get update
sudo apt-get install -y curl gnupg apt-transport-https
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/debian/$(lsb_release -rs)/prod stable main" > /etc/apt/sources.list.d/mssql-release.list'
apt-get install -y curl
curl https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc
curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list
sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18
sudo ACCEPT_EULA=Y apt-get install -y mssql-tools18


#################################
## Test if driver is correctly installed - should print [ODBC Driver 18 for SQL Server] ##
odbcinst -q -d -n "ODBC Driver 18 for SQL Server"

################################
## Create new image (from 2024)
docker save -o ~/Downloads/rstudio_modifed rstudio_modified