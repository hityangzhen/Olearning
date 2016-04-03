function studentUsernameFormatter(value,row,index) {
	return row.fields.student_username;
}
function studentEmailFormatter(value,row,index) {
	var value=row.fields.student_email;
	return '<span title="'+value+'">'+value+'</span>';
}
function studentTeleFormatter(value,row,index) {
	return row.fields.student_tele;
}
function studentDepartmentFormatter(value,row,index) {
	return row.fields.student_department;
}
function studentPositionFormatter(value,row,index) {
	return row.fields.student_position;
}
function studentGenderFormatter(value,row,index) {
	return row.fields.student_gender?'男':'女';
}
function studentStatusFormatter(value,row,index) {
	var value=row.fields.student_status ?'可用' : '不可用';
    return '<span style="color:orange; font-weight:bold;">'+value+'</span>';
}
function studentIscheckedFormatter(value,row,index) {
	var value=row.fields.student_ischecked ?'已申' : '未审核';
    return '<span style="color:orange; font-weight:bold;">'+value+'</span>';
}
function studentDetailFormatter(value,row,index) {
	return '<a href="/admin/student/'+row.pk+'/" style="color:blue;font-weight:bold">详细信息</a>';
}

$(function(){
	$.extend($.messager.defaults,{  
    	ok:"确定",  
    	cancel:"取消"  
	}); 
	
	// pagination
	var dg=$('#dg');
	
	// load data from remote
	dg.datagrid({
        url:'/admin/student/list/',
        onLoadSuccess:function(data) {
            if(dg.datagrid('getData').total==0)
                bottomCenter('<font style="color:red;font-size:13px;font-family:微软雅黑;">查询结果0行</font>');
            }
        });

	defaultPagination(dg);

});


// delete the student
function studentDelete() {
	var dg=$('#dg');
	var title="信息反馈";
	var checkedItems = dg.datagrid('getChecked');
    if(null==checkedItems || checkedItems.length==0) {
    	$.messager.alert(title,"请至少选择一条要删除的学员信息",'warning');
    	return ;
    }
    $.messager.confirm('删除学员信息', '你确定要删除选中的学员信息吗？', function(r){
    	if (r){
    		var id="";
    		for(var i=0;i<checkedItems.length;i++)
    			id += checkedItems[i].pk+",";
    		$.ajax({
           		type:"POST",
           		url:"/admin/student/delete/",
           		dataType:"json",
           		data:{"student_idset":id},
           		success:function(data){
               		$.messager.alert(title,data.tip,'info',function (){dg.datagrid('reload');});
           		},
           		error:function(XMLHttpRequest,txtStatus,errorThrown){
               		$.messager.alert(title,"网络出错"+txtStatus+","+errorThrown,'warning',function (){dg.datagrid('reload');});
           		}
       		});
    	}
    });
}

function studentUpdate() {
	var title="信息反馈";
	var checkedItems = $('#dg').datagrid('getChecked');
    if(checkedItems.length!=1) {
    	$.messager.alert(title,"请选择一条要编辑的学员信息",'warning');
    	return ;
    }
    else
    	window.location.href='/admin/student/showupdate/'+checkedItems[0].pk+'/';
}