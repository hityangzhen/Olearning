

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
    var title="信息反馈";
    var addDlg=$('#coursetypeAddDlg');
    
    /* 添加角色界面点击添加按钮触发ajax事件 */
    $("#add_link").click(function(){
      form=$('#addForm');

    	if(!form.form('validate')) {
    		return ;
    	}
    	$.ajax({
           type:"POST",
           url:"/admin/coursetype/add",
           dataType:"json",
           data:form.serialize(),
           success:function(data){
              if(data.status=='nosession')
                $.messager.alert(title,data.tip,'info',function (){
                  top.document.location.href='/index/'
                });                
              else
                $.messager.alert(title,data.tip,'info',function (){addDlg.dialog('close');dg.datagrid('reload');});
           },
           error:function(XMLHttpRequest,txtStatus,errorThrown){
               $.messager.alert(title,"网络出错"+txtStatus+","+errorThrown,'warning',function (){addDlg.dialog('close');});
           }
       }); 
    });
    
    /* 工具栏点击删除按钮触发ajax事件  */
    
    $('#tool_delete_link').click(function () {
    	var checkedItems = dg.datagrid('getChecked');
    	if(null==checkedItems || checkedItems.length==0) {
    		$.messager.alert(title,"请至少选择一条要删除的课程类型信息",'warning');
    		return ;
    	}
    	$.messager.confirm('删除课程类型信息', '你确定要删除选中的课程类型信息吗？', function(r){
    		if (r){
    			var id="";
    			for(var i=0;i<checkedItems.length;i++)
    				id += checkedItems[i].id+",";
    			$.ajax({
           			type:"POST",
           			url:"/admin/coursetype/delete",
           			dataType:"json",
           			data:{"id":id},
           			success:function(data){
               			$.messager.alert(title,data.tip,'info',function (){dg.datagrid('reload');});
           			},
           			error:function(XMLHttpRequest,txtStatus,errorThrown){
               			$.messager.alert(title,"网络出错"+txtStatus+","+errorThrown,'warning',function (){dg.datagrid('reload');});
           			}
       			});
    		}
    	});
    });
    
    /* 工具栏按钮点击编辑*/
    var editDlg=$('#coursetypeEditDlg');
    
    $('#tool_edit_link').click(function (){
    	var checkedItems = $('#dg').datagrid('getChecked');
    	if(checkedItems.length > 1 || checkedItems.length==0) {
    		$.messager.alert(title,"请选择一条课程类型信息进行编辑",'warning');
    		return ;
    	}
    	$('#coursetypeEditDlg').dialog('open');
    	
    	/* 获取datagrid中的 */
    	$('#editForm').form('load',{
    		id:checkedItems[0].id,
        coursetype_name:checkedItems[0].coursetype_name,
        coursetype_positionid:checkedItems[0].coursetype_positionid,
    	});

    	if(checkedItems[0].coursetype_status)
    		$('#editForm #coursetype_status').combobox('setValue','True');
    	else
    		$('#editForm #coursetype_status').combobox('setValue','False');
    });
})
/**
 * 确认修改
 */
function confirmSave() {
	/* 点击保存修改 */
    		$.messager.confirm('保存课程类型信息', '你确定要保存已修改的信息吗？', function(r){
    			/* 确定保存修改信息 */
				if (r){
					$.ajax({
           				type:"POST",
           				url:"/admin/coursetype/update",
           				dataType:"json",
           				data:$('#editForm').serialize(),
           				success:function(data){
               				$.messager.alert('信息反馈',data.tip,'info',function (){$('#coursetypeEditDlg').dialog('close');$('#dg').datagrid('reload');});
           				},
           				error:function(XMLHttpRequest,txtStatus,errorThrown){
               				$.messager.alert('信息反馈',"网络出错"+txtStatus+","+errorThrown,'warning',function (){$('#coursetypeEditDlg').dialog('close');});
           				}
       				}); 
				}
			});
}