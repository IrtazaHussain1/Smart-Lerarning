$(document).ready(function(){
	$('#sub_select').change(function(){
		call_data();
	});
});

function call_data(){
	$.ajax({
		type:'GET',
		url:'/dashboard/enroll_student_class/',
		data:{
			'subj_s':$('#sub_select').val()
		},
		dataType:'JSON',
		success:function(data){
			$('#myTable tr').remove();
			for(i in data['stud_enroll']){
			$('#myTable').append('<tr><td>'+ data['stud_enroll'][i]['s_class_id'] +'</td><td>'+ data['sub'][0]['sub_id']+ ' '+ data['sub'][0]['sub_name'] +'</td><td>'+ data['stud_enroll'][i]['s_student_id'] +'</td><td><a href="/dashboard/student_detail/'+data['stud_enroll'][i]['s_student_id'] +'" class="glyphicon glyphicon-new-window"></a></td></tr>')
			}
		},
		error:function(error, xhr, status){
			alert(error.responseTexts);
		}
	});
}