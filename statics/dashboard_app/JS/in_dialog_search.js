$(document).ready(function(){
   $("#search_history").on("keyup", function() {
  var value = $(this).val().toLowerCase();
  $("#his_body tr").filter(function() {
    $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
  });
});
});

