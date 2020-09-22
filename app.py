from flask import Flask
from flask import request
from flask import render_template
import pandas as pd 
import os
import auth
import csv
import idealista as ide
import json
import folium
from folium.plugins import HeatMap

app = Flask(__name__)

secrets = open('secrets.json','r')
secrets_obj = json.load(secrets)

@app.route('/drawMap')
def draw_map():
    map_data = pd.read_csv("./Data/data_01.csv", sep=';')
    lat = map_data['LATITUD'].mean()
    lom = map_data['LONGITUD'].mean()
    startingLocation = [lat, lom]#[39.47, -0.37]
    hmap = folium.Map(location=startingLocation, zoom_start=15)
    max_amount = map_data['RelacionPrecioTamanio'].max()
    hm_wide = HeatMap( list(zip(map_data.LATITUD.values, map_data.LONGITUD.values, map_data.RelacionPrecioTamanio.values)),
                        min_opacity=0.2,
                        max_val=max_amount,
                        radius=17, blur=15,
                        max_zoom=1)

    # Adds the heatmap element to the map
    hmap.add_child(hm_wide)
    # Saves the map to heatmap.hmtl
    hmap.save(os.path.join('./templates', 'heatmap.html'))
    #Render the heatmap
    return render_template('heatmap.html')

@app.route('/chargeData')
def charge_data():
    latitude = ''
    longitude = ''
    try:
        latitude = request.args.get('latitude')
        longitude = request.args.get('longitude')
    except:
        return {'code': 400, 'message':'Missing latitude and longitude arguments at the call.'}, 400

    auth_object = auth.Auth(secrets['key'], secrets['secret'])
    auth_json = auth_object.auth()
    bearer = auth_json['access_token']
    print (bearer)

    contador = 1
    FILE = csv.writer(open('./Data/data_01.csv', 'a')) 
    FILE.writerow(['ID', 'LATITUD', 'LONGITUD', 'TAMAÑO', 'PRECIO AL MES', 'RELACION PRECIO TAMAÑO'])

    while contador <= int(request.args.get('numPags')):
        data = ide.get_properties(bearer, 'rent', latitude, longitude, contador)

        if data == False:
            return  {'code': 200, 'message': 'All available data charged'}, 200

        for property in data['elementList']:
            new_row = [property['propertyCode'], property['latitude'], property['longitude'], property['size'], property['price'], property['priceByArea']]
            FILE.writerow(new_row)
        
        contador += 1
    
    FILE.close()

    #Limpoiamos lineas en blanco
    with open('./Data/data_01.csv') as infile, open('./Data/data_01.csv', 'w') as outfile:
        for line in infile:
            if not line.strip(): continue  # skip the empty line
            outfile.write(line)  # non-empty line. Write it to output

    return {'code': 200, 'message': 'Data charged :D'}, 200