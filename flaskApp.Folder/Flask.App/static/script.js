document.addEventListener('DOMContentLoaded', function() {
    var streetname = document.getElementById("address-streetname").textContent;
    var housenumber = document.getElementById("address-housenumber").textContent;
    var postcode = document.getElementById("address-postcode").textContent;
    var mapsLink = "https://www.google.com/maps?q=" + streetname + "+" + housenumber + "+" + postcode;
    document.getElementById("googleMapsLink").href = mapsLink;
});