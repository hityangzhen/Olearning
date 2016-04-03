function courseNameFormatter(value,row,index) {
  return row.fields.course_name;
}

function courseTagsFormatter(value,row,index) {
  return row.fields.course_tags;
}

function teacherNameFormatter(value,row,index) {
	return row.fields.teacher.fields.teacher_realname;
}

function courseCreditFormatter(value,row,index) {
	return row.fields.course_credit;
}

function courseTypeNameFormatter(value,row,index) {
	return row.fields.coursetype.fields.coursetype_name;	
}

function courseStatusFormatter(value,row,index) {
    var value=row.fields.course_status ?'可用' : '不可用';
    return '<span style="color:orange; font-weight:bold;">'+value+'</span>';
}

function courseDetailFormatter(value,row,index) {
    return '<a href="/course/detail/'+row.pk+'" style="color:blue;font-weight:bold">课程详情</a>';
}

function courseNoticeFormatter(value,row,index) {
    if(row.fields.course_status==true)
        return '<a href="/course/'+row.pk+'/generalnotice/" style="color:blue;font-weight:bold">课程公告</a>';
    else
        return '';
}

$(function(){

	$.extend($.messager.defaults,{  
    	ok:"确定",  
    	cancel:"取消"  
	}); 

	var dg=$('#dg');
	var p = dg.datagrid('getPager');  

    $(p).pagination({  
    	pageSize: 5,//每页显示的记录条数，默认为10  
        pageList: [5,10,15],//可以设置每页记录条数的列表  
        beforePageText: '第',//页数文本框前显示的汉字  
        afterPageText: '页    共 {pages} 页',  
        displayMsg: '当前显示 {from} - {to} 条记录   共 {total} 条记录',
    }); 

});