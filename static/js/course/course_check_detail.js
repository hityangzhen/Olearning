function check(course_ischecked) {
	var title='信息反馈';
	if (null==$('#course_checkedReply').val() || $('#course_checkedReply').val()=='') {
		$.messager.alert(title,'请填写审核意见','info');
		return ;
	}
	if (course_ischecked==2)
		$.messager.alert(title,'已审核，不能重复审核','info',function (){
            window.location.href='/course/showuncheck/';
        });
	else
		executeCheck(course_ischecked);
}

function executeCheck(course_ischecked) {
	var title='信息反馈';
	$.messager.confirm('课程审核', '确定执行此操作?', function(r){
		if(r) {
			$.ajax({
           		type:"POST",
           		url:"/course/checked/"+$('#course_id').val()+"/",
           		dataType:"json",
           		data:{
           			"course_ischecked":1,
           			"course_checkedReply":course_ischecked+'##'+$('#course_checkedReply').val()
           		},
           		success:function(data){
               		$.messager.alert(title,data.tip,'info',function (){
               			window.location.href='/course/showuncheck/';
               		});
           		},
           		error:function(XMLHttpRequest,txtStatus,errorThrown){
               		$.messager.alert(title,"网络出错"+txtStatus+","+errorThrown,'warning',function (){
               			window.location.href='/course/showuncheck/';
               		});
           		}
       		});
		}
	});
}