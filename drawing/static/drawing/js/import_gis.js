$('#gisfile').on('change', function(){
    let validity = validate_input_file()
    if (validity.length > 0 && !validity.type_valid) {
        window.alert('File type not recognized. Is your file a ".shp", ".zip", ".csv", ".json", or ".geojson"?');
        $('#gisfile').val('');
    } else if (validity.is_valid && validity.type_valid) {
        interpret_file();
    } 
})

showGISImportHelp = function() {
    var title = "GIS File Import Help";
    var content = "You may import spatial data from several different file types. " + 
        "<ul>" + 
            "<li> Accepted formats include: <ul>" +
                "<li>zipped ESRI shapefiles</li>" +
                "<li>CSV/TSV files</li>" + 
                "<li>GeoJSON</li>" +
                "</ul></li>" +
            "<li>your file will need to be in the <b>EPSG: 4326 (WGS 84)</b> projection " +
            "<b><u>or</u></b> a shapefile containing a .prj file.</li>" + 
            "<li>No attributes will be retained: only the geographic features</li>" +
            "<li>Features must be one of the following types: <b>points, lines, polygons, or multipolygons</b></li>" +
            "<li>All features must be of the same type as each other</li>" +
            "<li>Please refer to the help links below for your specific file type.</li>"
        "</ul>";
    app.viewModel.alert.showDialog(title, content);
};

showShapefileHelp = function() {
    var title = "Import Shapefile Help";
    var content = "ESRI Shapefiles can be imported directly into this tool. <br/>" + 
    "To do so: " +
    "<ul>" +
        "<li>zip the pieces of your shapefile into a single .zip file</li>" + 
        "<li>.war, .tar, .7z, and other less common zip/archive formats are not supported at this time</li>" + 
        "<li>If your data is not already projected to EPSG:4326 (WGS 84) then be sure to include the .prj in your zipped files</li>" + 
    "</ul>";
    app.viewModel.alert.showDialog(title, content);
};

showCSVHelp = function () {
    var title = "Importing CSV/TSV Files";
    var content = '<p>' +
    '<b>CSV/TSV</b> files are used to represent point data.<br/>' +
    'They should be formatted as follows:<br/>' +
    '<ul>' +
        '<li>2 or more columns</li>' +
        '<li>2 or more rows</li>' +
        '<li>ROW 1: headers (not data)</li>' +
        '<li>Column 1: Latitude value</li>' +
        '<li>Column 2: Longitude value</li>' +
        '<li>Coordinates should be in Decimal Degree format</li>' +
        '<li>Coordinates should be in EPSG:4326 WGS 84</li>' +
        '<li>Example: Four Corners\' coordinates would look like: 36.9927152491, -109.040436537</li>' +
    '</ul>' +
    'Extra columns will not be considered: no attributes will be imported.'
    '</p>';
    app.viewModel.alert.showDialog(title, content);
}

showGeoJSONHelp = function() {
    var title = "Import GeoJSON Help";
    var content = "GeoJSON files may be imported directly into this tool. They must:" +
    "<ul>" +
        "<li>Be a <a href=\"https://www.rfc-editor.org/rfc/rfc7946\" target=\"_blank\">properly formatted GeoJSON representation</a> of a Feature Collection</li>" + 
        "<li>Be projected to <a href=\"https://www.rfc-editor.org/rfc/rfc7946#section-4\" target=\"_blank\">World Geodetic System 1984, and units of decimal degrees</a></li>" +
        "<li>Be less than 5MB in size</li>" +
        "<li>Contain only 1 feature type for all features</li>" +
        "<li>Contain only valid, non-intersecting features (i.e. bow-ties)</li>" +
        "<li>Use a file extension of either '.json' or '.geojson'</li>" +
    "</ul>" + 
    "If unsure of your GeoJSON files validity, you're welcome to test it here or debug it at <a href=\"https://geojson.io\" target=\"_blank\">geojson.io</a>";
    app.viewModel.alert.showDialog(title, content);
};