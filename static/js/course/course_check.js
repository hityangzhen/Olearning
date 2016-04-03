function courseNameFormatter(value,row,index) {
  return row.fields.course_name;
}

function courseTagsFormatter(value,row,index) {
  return row.fields.course_tags;
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

function courseOperationFormatter(value,row,index) {
    return '<a href="/course/showcheckdetail/'+row.pk+'" style="color:blue;font-weight:bold">课程审核</a>';
}

$(function(){

	$.extend($.messager.defaults,{  
    	ok:"确定",  
    	cancel:"取消"  
	}); 

	var dg=$('#dg');
    dg.datagrid({
        url:'/course/uncheck/',
        onLoadSuccess:function(data){
            if(data.rows.length==0) {
                bottomCenter('<font style="color:red;font-size:13px;font-family:微软雅黑;">当前没有待审核课程信息</font>');
            }
        }
    });
	defaultPagination(dg);
});