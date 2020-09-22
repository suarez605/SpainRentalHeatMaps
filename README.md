# SpainRentalHeatMaps
Web application built on Flask wich can recover data from properties at rent via idealista.com API and draw heatmaps with that data.

#Installation

Just clone the repo and create a new venv inside the folder. Then activate it and use "pip install -r requirements.txt" to install dependencies.
After that, run it as a flask application, set a FLASK_APP enviorment variable as app.py from the venv terminal and use "flask run" command.

NOTE: to recover new data from idealista API you need to create a secrets.json file with this structure:
{
    "key": "",
    "secret": ""
}

And put there your api key and secret.
To charge data use the /chargeData?latitude=&longitude= endpoint.
