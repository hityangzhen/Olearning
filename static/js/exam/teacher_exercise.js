function exerciseDetailFormatter(value,row,index) {
	return '<a style="color:blue" href="/exam/teacher_exercise/'+row.course_id+'/">详情查看</a>';
}

$(function(){
	$.extend($.messager.defaults,{  
	    ok:"确定",  
	    cancel:"取消"  
	}); 
	  
	var dg=$('#dg');
	defaultPagination(dg);
	
});


