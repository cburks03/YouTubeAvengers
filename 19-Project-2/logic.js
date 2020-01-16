// Store our API endpoint inside queryUrl
var queryUrl = "http://127.0.0.1:5000/allstats";

// Perform a GET request to the query URL
d3.json(queryUrl, function(data) {
  console.log(data)
  // Once we get a response, send the data.features object to the createFeatures function
  createFeatures(data.features);
});

function createFeatures(statsData) {

  // Define a function we want to run once for each feature in the features array
  // Give each feature a popup describing the place and time of the earthquake
  function onEachFeature(feature, layer) {
    layer.bindPopup("<h3>" + "Stats for " + feature.properties.countrycode +
      "</h3><hr><p>" +  feature.properties.mostviewedcat + "</p>" 
      +"<p>" +  feature.properties.mostviewedvid + "</p>"
      +"<p>" +  feature.properties.mostlikedvid + "</p>"
      +"<p>" +  feature.properties.mostlikedcat + "</p>"
      +"<p>" +  feature.properties.mostdislikedcat + "</p>"
      +"<p>" +  feature.properties.mostdislikedvid + "</p>"
      +"<p>" +  feature.properties.leastviewedcat + "</p>"
      +"<p>" +  feature.properties.mostcommentedvid + "</p>"
      +"<p>" +  feature.properties.mostcommentedcat + "</p>"
      
      );
      
  }

  // Create a GeoJSON layer containing the features array on the earthquakeData object
  // Run the onEachFeature function once for each piece of data in the array
  var stats = L.geoJSON(statsData, {
    onEachFeature: onEachFeature
  });

  // Sending our earthquakes layer to the createMap function
  createMap(stats);
}

function createMap(stats) {

  // Define streetmap and darkmap layers
  var streetmap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 18,
    id: "mapbox.streets",
    accessToken: API_KEY
  });

  var darkmap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 18,
    id: "mapbox.dark",
    accessToken: API_KEY
  });

  // Define a baseMaps object to hold our base layers
  var baseMaps = {
    "Street Map": streetmap,
    "Dark Map": darkmap
  };

  // Create overlay object to hold our overlay layer
  var overlayMaps = {
    AllStats: stats
  };

  // Create our map, giving it the streetmap and earthquakes layers to display on load
  var myMap = L.map("map", {
    center: [
      15.5994, -28.6731
    ],
    zoom: 3,
    layers: [streetmap, stats]
  });
  
  L.control.layers(baseMaps).addTo(myMap);
  L.control.layers(overlayMaps).addTo(myMap);
  // Create a layer control
  // Pass in our baseMaps and overlayMaps
  // Add the layer control to the map
  //L.control.layers(baseMaps, overlayMaps, {
  //  collapsed: false
  //}).addTo(myMap);
}

