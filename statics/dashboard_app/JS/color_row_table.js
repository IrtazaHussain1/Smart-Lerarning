  $(document).ready(function(){
    $(".view_btn").click(function(){
      $.ajax({
      type:'GET',
      url:'/dashboard/',
      dataType:'JSON',
      success:function(data){
        console.log(data);
        for(i in data['Stud_data']){
          console.log(i);
            $("#dialog_body").append("<tr><td>" + data['Stud_data'][i]['s_class_id'] +" </td><td>"+data['Stud_data'][i]['s_subject_id'] + "</td><td>" + data['Stud_data'][i]['s_student_id'] + "</td><td>" + data['pre_data'][i]['prediction_class'] + "</td></tr>");
        };
    $(function(){
    $("#dialog_body tr").each(function(){
      var col_val = $(this).find("td:eq(3)").text();
      console.log(col_val);
      if (col_val == 'G'){
        $(this).css("background-color","#00ff0c");  //the selected class colors the row green//
      }
      else if(col_val == 'A'){
        $(this).css("background-color","#faff00");
      }
       else {
        $(this).css("background-color",'#ff0000');
      }
    });
});
      },
      error:function(error){
        console.log(error);
      }
    });
    });
  });