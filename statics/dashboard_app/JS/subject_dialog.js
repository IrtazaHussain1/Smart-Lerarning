$( function() {
    $( "#dialog_table" ).dialog({autoOpen: false, width:1000,maxHeight:500, title:'Students', position:{my: "center top+50",at: "center top+50", of:window}, modal:true, show: { effect: "fadeIn" } });
    $( "#hist_graph" ).dialog({autoOpen: false, width:800,maxHeight:500, title:'Performance Count Graph',position:{my: "center top+50",at: "center top+50", of:window}, modal:true, show:{ effect: 'fadeIn'}});
  });

  $(document).ready(function(){
    $( ".student_info" ).click(function() {
      $( "#dialog_table" ).dialog( "open" );
    });
    $(".hist_btn").click(function(){
      $("#hist_graph").dialog("open");
    });
  });