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
                with ch00 as (
                with ch0 as (
                select countrycode,  max(totalviews) mostviewed from catviews group by countrycode
                )
                select catviews.countrycode, concat('Most viewed category:  ', catviews.category) mostviewedcat from catviews, ch0 
                where ch0.countrycode = catviews.countrycode and ch0.mostviewed = catviews.totalviews
                ),
                ch11 as 
                (
                --Mast Viewed video Per Country
                with ch1 as (
                select countrycode,  max(views_) mostviewed from allvideos group by countrycode
                )
                select allvideos.countrycode, concat('Most viewed Video:    ', split_part(split_part(allvideos.description,'.',1),'\\n',1)) mostviewedvid from allvideos, ch1 
                where ch1.countrycode = allvideos.countrycode and ch1.mostviewed = allvideos.views_
                ),
                ch12 as (
                --Most Liked Video per Country
                with ch0 as (
                select countrycode,  max(likes) mostliked from allvideos group by countrycode
                )
                select allvideos.countrycode, concat('Video with most likes:    ', split_part(split_part(allvideos.description,'.',1),'MVDirector :',1)) mostlikedvid from allvideos, ch0 
                where ch0.countrycode = allvideos.countrycode and ch0.mostliked = allvideos.likes
                ),
                ch13 as (--Most liked category per country 
                with ch0 as (
                select countrycode,  max(totallikes) mostliked from catviews group by countrycode
                )
                select catviews.countrycode, concat('Category with most likes:  ', catviews.category) mostlikedcat from catviews, ch0 
                where ch0.countrycode = catviews.countrycode and ch0.mostliked = catviews.totallikes
                ),
                ch14 as (--Most disliked category per country 
                with ch0 as (
                select countrycode,  max(totaldislikes) mostdisliked from catviews group by countrycode
                )
                select catviews.countrycode, concat('Category with most dislikes:  ', catviews.category) mostdislikedcat from catviews, ch0 
                where ch0.countrycode = catviews.countrycode and ch0.mostdisliked = catviews.totaldislikes
                ),
                ch15 as (--Most disLiked Video per Country
                with ch0 as (
                select countrycode,  max(dislikes) mostdisliked from allvideos group by countrycode
                )
                select allvideos.countrycode, 
                concat('Video with most dislikes:    ', split_part(split_part(allvideos.description,'.',1),'MVDirector :',1)) mostdislikedvid from allvideos, ch0 
                where ch0.countrycode = allvideos.countrycode and ch0.mostdisliked = allvideos.dislikes
                ),
                ch16 as (
                --Least viewed category 
                with ch0 as (
                select countrycode, min(totalviews) leastviewed from catviews group by countrycode
                )
                select catviews.countrycode, concat('Category with least views:  ', catviews.category) leastviewedcat from catviews, ch0 
                where ch0.countrycode = catviews.countrycode and ch0.leastviewed = catviews.totalviews
                ),
                ch17 as (
                --Most commented video 
                with ch0 as (
                select countrycode,  max(comment_count) mostcommented from allvideos group by countrycode
                )
                select allvideos.countrycode, 
                concat('Video with most comments:    ', split_part(split_part(allvideos.description,'.',1),'MVDirector :',1)) mostcommentedvid from allvideos, ch0 
                where ch0.countrycode = allvideos.countrycode and ch0.mostcommented = allvideos.comment_count
                ),
                ch18 as (
                --Most commented category 
                with ch0 as (
                select countrycode,  category, sum(comment_count) totalcomments from allvideos group by countrycode,category
                ),
                ch1 as (
                select countrycode, max(totalcomments) maxcomments from ch0 group by countrycode
                )
                select ch0.countrycode, concat('Category with most comments:  ', ch0.category) mostcommentedcat from ch0, ch1 
                where ch0.countrycode = ch1.countrycode and ch0.totalcomments = ch1.maxcomments
                )
                select ch00.*, ch11.mostviewedvid, ch12.mostlikedvid, ch13.mostlikedcat, 
                    ch14.mostdislikedcat , ch15.mostdislikedvid, ch16.leastviewedcat,ch17.mostcommentedvid, ch18.mostcommentedcat
                from ch00, ch11,ch12, ch13, ch14, ch15, ch16, ch17, ch18
                where 
                    ch00.countrycode = ch11.countrycode and 
                    ch00.countrycode = ch12.countrycode and
                    ch00.countrycode = ch13.countrycode and
                    ch00.countrycode = ch14.countrycode and
                    ch00.countrycode = ch15.countrycode and
                    ch00.countrycode = ch16.countrycode and
                    ch00.countrycode = ch17.countrycode and
                    ch00.countrycode = ch18.countrycode 
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