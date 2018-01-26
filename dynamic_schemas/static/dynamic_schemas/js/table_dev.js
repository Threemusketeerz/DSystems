
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
                    //console.log('data: ', d)
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
                    //console.log('Efter json parse: ', data.data);

                    // !!!! VERY IMPORTANT TO DO data.data !!!!
                    return data.data;
                },
                //complete: function(jqXHR, textStatus){
                    //console.log(jqXHR); 
                    //console.log(textStatus);
                //},
            },
            "columns": JSON.parse(columns),
            "columnDefs": [{
                // Renders glyphicons if boolean true or false.
                "render": function(data, type, row, meta){
                    
                    if (data === 'Ja') 
                        return "<span class='glyphicon glyphicon-ok'>Ja</span>";
                    if (data === 'Nej')
                        return "<span class='glyphicon glyphicon-remove'>Nej</span>";
                    return data;
                },
                // Checks all targets
                "targets": "_all"
            }], 
            "order": [[0, 'desc']],
            "responsive": {
                "details": {
                    "display": $.fn.dataTable.Responsive.display.modal({
                        "header": function( row ) {
                            return 'Række data';
                        }
                    }),
                    "renderer": $.fn.dataTable.Responsive.renderer.tableAll({
                        "tableClass": "table table-striped"
                    })
                },
            },
            "select": {
                "style": "single" 
            }, 
            "dom": "Brltip",
            "buttons": [
                {
                "text": "<- Tilbage",
                "action": function(e, dt, node, config){
                    var overview_link =  '/rengoering/';
                    window.location.replace(overview_link);
                    }
                },
                {
                "extend": "selected",
                "text": "Opdater",
                "action": function(e, dt, node, config){
                    //var rows = dt.rows({"selected": true}).count();
                    var row_data = dt.row({"selected": true}).data();

                    var update_link = window.location.href + row_data.id + '/update/';
                    window.location.replace(update_link);
                    }
                },
                {
                "text": "Ny Indtast",
                "action": function(e, dt, node, config){
                    var create_link = window.location.href + 'create/';
                    window.location.replace(create_link);
                    }
                },

            ]

        })
        table.on( 'select', function ( e, dt, type, indexes ) {
            console.log(type, indexes);
            if ( type === 'row' ) {
                var data = table.rows( indexes ).data();
                console.log("Table.on: ", data[0])
                // do something with the ID of the selected items
            }
        } );
        //table.column(0).visible(false)
    //}).done(function() {
        //console.log(performance.now() + ' TableCreation done')
        ////var end = performance.now();

        ////alert("Took " + (end - start) + " ms");
    });
});
