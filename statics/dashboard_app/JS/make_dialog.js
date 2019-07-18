  $( function() {
    $( "#dialog" ).dialog({autoOpen: false, width:600,maxHeight:550, position:{my: "center top+50",at: "center top+50"}});
  });


 $(document).ready(function(){
    $( "#add_btn" ).click(function() {
      $( "#dialog" ).dialog( "open" );
    });
  });