import psycopg2
from flask import Flask
import flask
import json
app = Flask(__name__)

countrycoords = {"IN":	(20.593684,	78.96288),	
                "GB":	(55.378051,	-3.435973),
                "DE":	(51.165691,	10.451526),	
                "CA":	(56.130366,	-106.346771),
                "FR":	(46.227638,	2.213749),
                "US":	(37.09024,	-95.712891)	
                }

def runquery(querystring):
    try:
        print(querystring)
        conn = psycopg2.connect(host="localhost",database="TrendingVideos", 
            user="postgres", password="postgres")
        cur = conn.cursor()
        cur.execute(querystring)
        data= cur.fetchall()
        print(data)
        for dtup in data:
            d = dtup[0]
            print(d)
            print(countrycoords[d["countrycode"]])
            print([countrycoords[d["countrycode"]][1], countrycoords[d["countrycode"]][0]])
        

        geojson = {
            "type": "FeatureCollection",
            "features": [
            {
                "type": "Feature",
                "geometry" : {
                    "type": "Point",
                    "coordinates": [countrycoords[d[0]["countrycode"]][1], countrycoords[d[0]["countrycode"]][0]],
                },
            "properties" : d[0],
            } for d in data]
        }


        return geojson
    except Exception as e:
        print('Failed query:'+ querystring,e)
    finally:
        if cur:
            #print("close cursor")
            cur.close()
        if conn:
            #print('close conn')
            conn.close()
    return None

@app.route('/mostliked')
def mostliked():
    querystring = '''
            select row_to_json(foo) from (
                with ch0 as (
                    select countrycode,  max(totalviews) mostviewed 
                        from catviews group by countrycode
                )
                select catviews.countrycode, catviews.category, totalviews 
                    from catviews, ch0 
                where ch0.countrycode = catviews.countrycode and 
                        ch0.mostviewed = catviews.totalviews
            ) foo            
            '''
    out = runquery(querystring)   
    print(json.dumps(out))
    return json.dumps(out)

@app.route('/allstats')
def allstats():
    querystring = '''
            select row_to_json(foo) from (
                select * from allstats
                )as foo;    
                
            '''
    out = runquery(querystring)   
    print(json.dumps(out))
    return json.dumps(out)




@app.route('/')
def index():
    """ Displays the index page accessible at '/'
    """
    return flask.render_template('index.html')

if __name__ == '__main__':
    app.run()