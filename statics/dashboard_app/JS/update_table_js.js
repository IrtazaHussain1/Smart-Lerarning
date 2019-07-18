$("#sub_select").change(function(){
      $.ajax({
        type:"POST",
        url:'/dashboard/groups/',
        dataType:'json', 
        data:{
          sub_team_val:String($("#sub_select").val()),
          csrfmiddlewaretoken:$('Input[name=csrfmiddlewaretoken]').val(),
        },
        success:function(json){
          console.log($("#sub_select").children("option:selected").val());
          console.log("form loop start here");
          console.log(json);
          console.log(typeof parseInt(json.data[0]['positon1']));
          for (keys in json.data){
            if(json.data[keys]['team_subj_id'] == $("#sub_select").children("option:selected").val() ){
                $("#myTable tr:eq(keys)").children("td").eq(0).html(json.data[keys]['team_id']);
                $("#myTable tr:eq(keys)").children("td").eq(1).html($("#sub_select").children("option:selected").val());
                console.log("after 1 2")
                // for postion 1
                for (std in json.students){
                  console.log("in for")
                  if(parseInt(json.data[keys]['positon1']) == std){
                    $("#myTable tr:eq(keys)").children("td").eq(2).html(json.students[std]['s_roll_number']+ json.students[std]['s_first_name']+ json.students[std]['s_last_name']);
                  }
                }
                // for postion 2
                 for (std in json.students){
                  if(json.data[keys]['positon2'] == std){
                    $("#myTable tr:eq(keys)").children("td").eq(3).html(json.students[std]['s_roll_number']+ json.students[std]['s_first_name']+ json.students[std]['s_last_name']);
                  }
                }
                // for postion 3
                 for (std in json.students){
                  if(json.data[keys]['positon3'] == std){
                    $("#myTable tr:eq(keys)").children("td").eq(4).html(json.students[std]['s_roll_number']+ json.students[std]['s_first_name']+ json.students[std]['s_last_name']);
                  }
                }
              }
              else{
                 $("#myTable tr:eq(keys)").remove();

              }
            // for (othrkeys in keys){
            //   console.log(othrkeys);
            // }
          }
        },
        error:function(error){
          console.log(error)  
        }
      })
    })