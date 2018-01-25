
/*
 * To add a request key to getjson add {_: new Date().getTime()} in between,
 * file and function
 */
var start = performance.now();
$(document).ready(function() {
    //var columnSettings;
    //var tableDate;
    //var dataFileName= "responses/";
    //var columnsFileName = "columns/";
    //edit .getJSON to fit needs.
    //columnsFile = $.getJSON(columnsFileName, function(data){ console.log(data); return data; });
    
    //dataFile = $.getJSON(dataFileName, function(data){ console.log(data); return data.responseJSON; });

    // This promise function, makes sure that the json files are loaded in
    // before anything.
    // What would happen without is an error, where it didn't fetch either
    // columns or data before rendering the table.
    //$('#dataTable').DataTable();
    //$.when().done(function(){
        console.log(performance.now() + ' TableCreation started');


        //$(".field input").addClass("form-control") 

        var table = $("#dataTable").DataTable({
            "processing": true,
            "serverSide": true,
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
                        d = JSON.stringify(d);
                        d = JSON.parse(d);
                        data.data[i].qa_set = d;
                    }
                    console.log('Efter json parse: ', data.data);
                    return data.data;
                },
                complete: function(jqXHR, textStatus){
                    console.log(jqXHR); 
                    console.log(textStatus);
                },
            },
            "columns": null,
            "columns": [
                {"data": "id", "name": "ID"},
                {"data": "instruction", "name": "Instruktion"},
                {"data": "pub_date"},
                //{"data": "qa_set"},
                {"data": "qa_set.TestColumn0"},
                {"data": "qa_set.TestColumn1"},
                {"data": "qa_set.TestColumn2"},
                {"data": "qa_set.TestColumn3"},
                {"data": "qa_set.TestColumn4"},
                //{"data": "schema"},
                //{"data": "user"},
            ],
            //"columns": [
                //null,
                //null,
                //null,
                //null,
                //null,
                //null,
                //null,
                //null,
                //null,
                //null,
            //],
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
    //});
});
