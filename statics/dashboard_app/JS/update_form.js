$(document).ready(function(){
	$( "#update_button" ).click(function() {
               $( "#dialog_form" ).dialog( "open" );
            });

            $( "#dialog" ).dialog({autoOpen: false,title: "Update",position: {
                  my: "left center",
                  at: "left center"
               },
               width:90%,
            });
            $( "#student_info" ).click(function() {
               $( "#dialog_box" ).dialog( "open" );
            });
});

  $( function() {
    $( "#dialog" ).dialog();
  } );