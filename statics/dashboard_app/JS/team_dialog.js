  $( function() {
    $( "#add_group" ).dialog({autoOpen: false, width:500,maxHeight:500, title:'Add new Team',position:{my: "center",at: "center"}, modal:true, show: { effect: "fadeIn" } });
  });
    $( function() {
    $( "#history_popup" ).dialog({autoOpen: false, width:700, maxHeight:500, title:'Team History',position:{my: "center top+50",at: "center top+50"}, modal:true, show: { effect: "fadeIn" } });
  });
    $( function() {
    $( "#inter_div" ).dialog({autoOpen: false, width:700, maxHeight:700, title:'Interventions',position:{my: "center top+100",at: "center top+100"}, modal:true, show: { effect: "fadeIn" } });
  });


  $(document).ready(function(){
    $( "#btn_add_group" ).click(function() {
      $( "#add_group" ).dialog( "open" );
    });
    $( "#history" ).click(function() {
      $( "#history_popup" ).dialog( "open" );
      $.ajax({
      type:'GET',
      url:'/dashboard/groups/',
      dataType:'JSON',
      success:function(data){
            for(i in data['team_hist']){
              var da= new Date(data['team_hist'][i]['TimeStamp'])
              for(j in data['student']){
                if(data['team_hist'][i]['student_history_id'] == data['student'][j]['id']){
                   $("#his_body").append('<tr><td>'+ da + '</td><td>' + data['student'][j]['s_student_id'] +'</td><td>' + data['team_hist'][i]['student_team_id'] + '</td></tr>');
                };
              };
            };
        },
        error:function(xhr, status,error){
          alert(error.responseTexts);
        }
      });
    });
    $( "#interven_history" ).click(function() {
      $( "#inter_div" ).dialog( "open" );
    });

    $("#team_select").change(function(){
    var d = $("#team_select").val();
    $.ajax({
      type:'GET',
      url:'/dashboard/groups/',
      dataType:'JSON',
      success:function(data){
          if(d == 'all'){
            $("#his_body tr").remove();
              for(i in data['team_hist']){
                var da= new Date(data['team_hist'][i]['TimeStamp'])
                for(j in data['student']){
                if(data['team_hist'][i]['student_history_id'] == data['student'][j]['id']){
                   $("#his_body").append('<tr><td>'+ da+ '</td><td>' + data['student'][j]['s_student_id'] +'</td><td>' + data['team_hist'][i]['student_team_id'] + '</td></tr>');
                };
              };
              }
            }
            else{
              $("#his_body tr").remove();
              for(i in data['team_hist']){
                var da=new Date(data['team_hist'][i]['TimeStamp'])
                if(data['team_hist'][i]['student_team_id'] == d){
                  for(j in data['student']){
                  if(data['team_hist'][i]['student_history_id'] == data['student'][j]['id']){
                   $("#his_body").append('<tr><td>'+ da + '</td><td>' + data['student'][j]['s_student_id'] +'</td><td>' + data['team_hist'][i]['student_team_id'] + '</td></tr>');
                };
              };
                }
                else{
                  $("his_body").append('<td colspan="2"><p>No Record</p></td>')
                }
              }
            };
        },
        error:function(xhr, status,error){
          alert(error.responseTexts);
        }
      });
  });
  });

