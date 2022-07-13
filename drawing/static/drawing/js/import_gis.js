const validate_input_file = function() {
    let is_valid = false;
    let input_file_name = $('#gisfile').val();
    let name_length = input_file_name.length;
    let type_valid = false;
    if (
        name_length > 0 &&
        (
            input_file_name.toLowerCase().indexOf('.shp') > 0 ||
            input_file_name.toLowerCase().indexOf('.zip') > 0 ||
            input_file_name.toLowerCase().indexOf('.csv') > 0 ||
            input_file_name.toLowerCase().indexOf('.json') > 0 ||
            input_file_name.toLowerCase().indexOf('.geojson') > 0
        )
    ) {
        is_valid = true;
        type_valid = true;
    }
    return {
        'is_valid': is_valid,
        'length': name_length,
        'type_valid': type_valid
    }
}

const add_geojson_to_map = function(geojson) {
    window.alert(geojson);
}

const interpret_json = function(field) {
    let file = field.prop('files')[0];
    let file_url = URL.createObjectURL(file);
    $.get(file_url, function(data){
        add_geojson_to_map(data)
    }, "text");
}

const interpret_file = function() {
    let filename = $('#gisfile').val();
    let filename_parts = filename.split('.');
    let filename_type = filename_parts[filename_parts.length-1].toLowerCase();
    switch (filename_type) {
        case 'json':
            interpret_json($('#gisfile'));
            break;
        case 'geojson':
            interpret_json($('#gisfile'));
            break;
        case 'zip':
            interpret_zip($('#gisfile'));
            break;
        case 'shp':
            interpret_shp($('#gisfile'));
            break;
        case 'csv':
            interpret_csv($('#gisfile'));
            break;
        default:
            window.alert('Unsupported file type "' + filename_type + '"');
    }
}

$('#gisfile').on('change', function(){
    let validity = validate_input_file()
    if (validity.length > 0 && !validity.type_valid) {
        window.alert('File type not recognized. Is your file a ".shp", ".zip", ".csv", ".json", or ".geojson"?');
        $('#gisfile').val('');
    } else if (validity.is_valid && validity.type_valid) {
        interpret_file();
    } 
})