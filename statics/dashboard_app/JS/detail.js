$(document).ready(function(){
	$( "#student_info" ).click(function() {
               $( "#dialog" ).dialog( "open" );
            });

            $( "#dialog" ).dialog({autoOpen: false,buttons: {Close: function() {$(this).dialog("close");}},title: "Students",position: {
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