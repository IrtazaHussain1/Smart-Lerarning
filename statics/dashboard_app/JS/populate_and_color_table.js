$(document).ready(function(){
    $(".view_btn").click(function(){
      var d = $(this).val();
      $.ajax({
      type:'GET',
      url:'/dashboard/',
      dataType:'JSON',
      success:function(data){
        console.log(data);
        $('#dialog_body tr').remove();
        for(i in data['Stud_data']){
          var alp=data['Stud_data'][i]['s_subject_id'];
          var a_val='/dashboard/student_detail/' +data['Stud_data'][i]['s_student_id'];
          for(j in data['student']){
           if(data['student'][j]['s_roll_number'] == data['Stud_data'][i]['s_student_id'] ){
            var s_name = data['student'][j]['s_first_name'] + " " + data['student'][j]['s_last_name']
           } 
          }
          for(k in data['tp']){
            for(l in data['Stud_data']){
              if(data['tp'][k]['Student_perf_id'] == data['Stud_data'][l]['id']){
                if(data['Stud_data'][i]['s_student_id'] == data['Stud_data'][l]['s_student_id']){
                  var per_value= data['tp'][k]['total'];
                }
              }
            }
          }
          if( alp == d ){
          $("#dialog_body").append('<tr><td>'+ data['Stud_data'][i]['s_student_id']+ ' ' + s_name + '</td><td>' + data['Stud_data'][i]['s_class_id'] + '</td><td>' + data['pre_data'][i]['prediction_class'] + '</td><td>' + per_value + '</td><td><a href="' + a_val + '" class="glyphicon glyphicon-new-window"></a></td></tr>');
          // $('<td><a href="/dashboard/student_detail/a_val" class="glyphicon glyphicon-new-window"></a></td></tr>').appendTo("#dialog_body tr td:eq(4)");          
        };
        // this is for color background
        color();
        color_actual();
      }
      // check is student is not null
      if($('#dialog_body tr').length == 0 ){
          $('#dialog_body').append('<tr><td colspan="3">Add Student <a href="/dashboard/enroll_student_class/" class="btn btn-primary">Add</a></td></tr>')
        }
      },
      error:function(error){
        console.log(error);
      }
    });
    });
  });

function color(){
    $("#dialog_body tr").each(function(){
      var col_val = $(this).find("td:eq(2)").text();
      if (col_val == 'G'){
        $(this).find("td:eq(2)").css("background-color","#00ff0c");  //the selected class colors the row green//
      }
      else if(col_val == 'A'){
        $(this).find("td:eq(2)").css("background-color","#faff00");
      }
      else if(col_val == 'B') {
        $(this).find("td:eq(2)").css("background-color",'#ff0000');
      }
      else{
        alert('NO Predictions Match');
      }
    });
}
function color_actual(){
    $("#dialog_body tr").each(function(){
      var col_val = $(this).find("td:eq(3)").text();
      if (col_val >= 70 && col_val <= 100 ){
        $(this).find("td:eq(3)").css("background-color","#00ff0c");  //the selected class colors the row green//
      }
      else if(col_val >= 50 && col_val < 70){
        $(this).find("td:eq(3)").css("background-color","#faff00");
      }
      else if(col_val < 50 ) {
        $(this).find("td:eq(3)").css("background-color",'#ff0000');
      }
    });

}
