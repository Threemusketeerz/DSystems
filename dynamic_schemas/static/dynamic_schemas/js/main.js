/*
 * To add a request key to getjson add {_: new Date().getTime()} in between,
 * file and function
 */
var start = performance.now();
$(document).ready(function() {
    var columnSettings;
    var tableDate;
    var dataFileName= "responses/";
    var columnsFileName = "columns/";
    //edit .getJSON to fit needs.
    //columnsFile = $.getJSON(columnsFileName, function(data){ console.log(data); return data; });
    
    //dataFile = $.getJSON(dataFileName, function(data){ console.log(data); return data.responseJSON; });

    // This promise function, makes sure that the json files are loaded in
    // before anything.
    // What would happen without is an error, where it didn't fetch either
    // columns or data before rendering the table.
    //$('#dataTable').DataTable();
    $.when().done(function(){
        console.log(performance.now() + ' TableCreation started');


        //$(".field input").addClass("form-control") 

        var table = $("#dataTable").DataTable({
            //"data": dataFile,
            "serverside": true,
			"processing": true,
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
            //"columns": columnsFile[0],
            "order": [[0, 'desc']],
            "lengthMenu": [30],
            // Responsive design for phones.
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
            "dom": "Bfrltip",
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

                    //var row_data_keys = Object.keys(row_data);

                    var update_link = window.location.href + row_data[0] + '/update/';
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
                console.log(data[0])
                // do something with the ID of the selected items
            }
        } );
        table.column(0).visible(false)
    }).done(function() {
        console.log(performance.now() + ' TableCreation done')
        //var end = performance.now();

        //alert("Took " + (end - start) + " ms");
    });
});
