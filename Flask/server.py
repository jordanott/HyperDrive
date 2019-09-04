from flask import Flask, render_template, request, flash, Response
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

import datetime
import numpy as np
import matplotlib; matplotlib.use('Agg')
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt

import sys
sys.path.append('../VisaModel/TFRecord/')

# Loading data from TF Record
file_name = '../VisaModel/TFRecord/data/supertable20190405_ca_2018-06-03_2018-06-15.tfrecord' # small
file_name = '../VisaModel/TFRecord/data/supertable20190405_ca_2018-06-03_2018-09-02.tfrecord' # big

app = Flask(__name__, template_folder="templates/")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
GoogleMaps(app, key="")

def convert(element, type):
    if element == '': return ''
    try: return type(element)
    except: return type(-1)

@app.route('/background_process_test', methods=['POST'])
def background_process_test():
    card_number = convert(request.form.get('card_number'), int)
    postal_code = convert(request.form.get('postal_code'), float)

    date        = request.form.get('date')
    time        = request.form.get('time')

    markers = []; lats = []; longs = []
    colors = np.linspace(0,255, 100, 10)

    for i in range(10):

        infobox = '{name}\n{address}\n{postal_code}'.format(
            name='Test Name',
            address='address',
            postal_code='postal_code'
        )
        markers.append(
            {
                'icon': 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld={num}|{color}|000000'.format(
                    num=len(markers),
                    color=hex(colors[len(markers)-1])[2:-1].rjust(2,'0') + 'ff00'
                ),
                'lat': 37.426214,
                'lng': -122.143157+i,
                'infobox': infobox
            }
        )
        lats.append(37.426214); longs.append(-122.143157)

    mymap = Map(
        identifier="mymap",
        lat=np.median(lats),
        lng=np.median(longs),
        maptype='SATELLITE',
        style="height:500px;width:100%;margin-all:5%;",
        markers=markers
    )
    return render_template(
            'map.html',
            mymap=mymap,
            card_number=card_number,
            postal_code=postal_code,
            date=date,
            time=time,
            postal_codes_plot_url='path/to/img/plot',
            merchant_count_plot_url='path/to/img/plot'
        )

def default():
    mymap = Map(
        identifier="mymap",
        lat=37.426214,
        lng=-122.143157,
        maptype='SATELLITE',
        style="height:500px;width:100%;margin-all:5%;",
        zoom=20,
        markers=[
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
                'lat': 37.426214,
                'lng': -122.143157,
                'infobox': 'VISA Research'
            }
        ]
    )
    return render_template('map.html', mymap=mymap)


@app.route("/")
def mapview():
    # creating a map in the view
    return default()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
