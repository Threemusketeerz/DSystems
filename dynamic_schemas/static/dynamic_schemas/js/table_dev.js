
/*
 * To add a request key to getjson add {_: new Date().getTime()} in between,
 * file and function
 */
var start = performance.now();
var columnsFileName = "columns/";
//edit .getJSON to fit needs.
columns = $.getJSON(columnsFileName, function(data){ console.log(data); return data; });
//console.log(typeof columnsString);
//columns = JSON.stringify(columns);
//console.log(columns);
$(document).ready(function() {
    //var columnSettings;
    //var tableDate;
    //var dataFileName= "responses/";
    
    //dataFile = $.getJSON(dataFileName, function(data){ console.log(data); return data.responseJSON; });

    // This promise function, makes sure that the json files are loaded in
    // before anything.
    // What would happen without is an error, where it didn't fetch either
    // columns or data before rendering the table.
    //$('#dataTable').DataTable();
    $.when(columns).done(function(columns){
        console.log(performance.now() + ' TableCreation started');
        console.log(JSON.parse(columns))


    //$(".field input").addClass("form-control") 

        var table = $("#dataTable").DataTable({
            "processing": true,
            "serverSide": true,
            "pageLength": 25,
            "ajax": { 
                "url": "responses/",
                "data": function(d){
                    d.format = 'json';
                    console.log('data: ', d)
                },
                "dataSrc": function(data){
                    //console.log('DataSrc: ', data);
                    for (var i=0; i < data.data.length; i++){
                        d = data.data[i].qa_set
                        d = d.replace(/\\n/g, "\\n")
                                .replace(/\\"/g, '\\"')
                                .replace(/\\'/g, "\\'")
                                .replace(/\\&/g, "\\&")
                                .replace(/\\r/g, "\\r")
                                .replace(/\\t/g, "\\t")
                                .replace(/\\b/g, "\\b")
                                .replace(/\\f/g, "\\f");
                        //console.log(JSON.stringify(d));
                        //console.log(eval('('+d+')'));
                        d = eval('('+d+')');

                        // This might be a little excessive
                        d = JSON.stringify(d);
                        d = JSON.parse(d);

                        // Replace the data with the jsonified data.
                        data.data[i].qa_set = d;
                    }
                    console.log('Efter json parse: ', data.data);

                    // !!!! VERY IMPORTANT TO DO data.data !!!!
                    return data.data;
                },
                complete: function(jqXHR, textStatus){
                    console.log(jqXHR); 
                    console.log(textStatus);
                },
            },
            "columns": JSON.parse(columns),

        })
        //table.on( 'select', function ( e, dt, type, indexes ) {
            //console.log(type, indexes);
            //if ( type === 'row' ) {
                //var data = table.rows( indexes ).data();
                //console.log(data[0])
                //// do something with the ID of the selected items
            //}
        //} );
        //table.column(0).visible(false)
    //}).done(function() {
        //console.log(performance.now() + ' TableCreation done')
        ////var end = performance.now();

        ////alert("Took " + (end - start) + " ms");
    });
});
