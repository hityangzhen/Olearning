function taskNameFormatter(value,row,index) {
	return row.fields.task_name;
}

function courseCountFormatter(value,row,index) {
	return row.fields.task_courseids;
}
function learnIsPassedFormatter(value,row,index) {

	switch(value) {
		case 0:
			value='未学';
			break;
		case 1:
			value='正在学习';
			break;
		case 2:
			value='已通过';
			break;
	}

	return '<span style="color:orange; font-weight:bold;">'+value+'</span>';

}
function learnProgressFormatter(value,row,index) {
	var rel='<div style="width:100%;height:15px;background-color:#FBEC88;margin-bottom:10px;">';
	rel += '<p style="width:'+value+'%;height:15px;background-color:#ccc;text-align:center;color:red">'+value+'%</p>';
	rel += '</div>';
	return rel;
}

function learnDetailFormatter(value,row,index) {
	return '<a style="color:blue" href="/admin/task/showstudent_taskdetail/'+row.pk+'/">详情查看</a>';
}

function learnValidTimeFormatter(value,row,index) {
	return row.fields.task_starttime.split('T')[0]+'  至  '+row.fields.task_endtime.split('T')[0];
}

$(function(){
	$.extend($.messager.defaults,{  
    	ok:"确定",  
    	cancel:"取消"  
	}); 

	var dg=$('#dg');
	defaultPagination(dg);
});