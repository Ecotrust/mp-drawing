$('#gisfile').on('change', function(){
    let validity = validate_input_file()
    if (validity.length > 0 && !validity.type_valid) {
        window.alert('File type not recognized. Is your file a ".shp", ".zip", ".csv", ".json", or ".geojson"?');
        $('#gisfile').val('');
    } else if (validity.is_valid && validity.type_valid) {
        interpret_file();
    } 
})