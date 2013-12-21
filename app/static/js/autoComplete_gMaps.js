function initialize() {
    var from = document.getElementById('from_place');
    var to = document.getElementById('to_place')
    var options = {componentRestrictions: {country: 'ph'}};
                 
    new google.maps.places.Autocomplete(from, options);
    new google.maps.places.Autocomplete(to,options);
}
             
google.maps.event.addDomListener(window, 'load', initialize);