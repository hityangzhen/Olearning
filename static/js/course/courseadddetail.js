function resourceNameFormatter(value,row,index) {
    return row.fields.resource_name;
}
function resourceTagsFormatter(value,row,index) {
    return row.fields.resource_tags;
}
function resourceIsCoursewareFormatter(value,row,index) {
    var value=row.fields.resource_iscourseware==true?'是' : '否';
    return '<span style="color:orange; font-weight:bold;">'+value+'</span>';
}
function resourceCanDownloadFormatter(value,row,index) {
    var value=row.fields.resource_candownload==true?'是' : '否';
    return '<span style="color:orange; font-weight:bold;">'+value+'</span>';
}
function resourceViewTimesFormatter(value,row,index) {
    return row.fields.resource_viewtimes;
}
function resourceDownloadtimesFormatter(value,row,index) {
    return row.fields.resource_downloadtimes;
}
function resourceStatusFormatter(value,row,index) {
    var value=row.fields.resource_status==true?'可用' : '不可用';
    return '<span style="color:orange; font-weight:bold;">'+value+'</span>';
}

var url=window.location.href;

$(function(){

	// get the course id
	var url=window.location.href;
	var array=url.split('/');
	var course_id=array[array.length-2];
	
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


	$('#course').val(course_id);
	$('#submit').click(function(){
		var form=$('#form1');
        if(form.form('validate')) {
            $('#form1').form('submit',{  
                onSubmit:function(){ 

                },  
                success:function(data){ 
                    var data = eval('(' + data + ')');
                    var alerttype='info'
                    if (data.status=='failured')
                        alerttype='warning';
                    $.messager.alert('信息反馈',data.tip,alerttype,function(){
                    	formCLearAndDlgClose();
                    });
                }  
            });
        }
	});
});

/* resource edit */
function resourceEdit() {
    var title='信息反馈';
    var checkedItems = $('#dg').datagrid('getChecked');
    if(checkedItems.length > 1 || checkedItems.length==0) {
        $.messager.alert(title,"有且只能选择一条记录进行编辑",'warning');
        return ;
    }

    // add 2014-4-7
    /* has checked,can not edit the `courseware` ,but you can edit the resource */
    var ischecked=checkedItems[0].fields.course.fields.course_ischecked;

    if(ischecked && checkedItems[0].fields.resource_iscourseware ) {
        $.messager.alert(title,"此课程已发布，没有权限编辑课件",'warning');
        return ;
    }


    $('#resourceAddDlg').dialog('open');

    /* load the info */
    $('#form1').form('load',{
        resource_name:checkedItems[0].fields.resource_name,
        resource_tags:checkedItems[0].fields.resource_tags,
        resource_standardtime:checkedItems[0].fields.resource_standardtime,
        course:checkedItems[0].fields.course.pk,
        resource_id:checkedItems[0].pk
    });
    if(checkedItems[0].fields.resource_iscourseware)
        $('#resource_iscourseware').combobox('setValue','True');
    else
        $('#resource_iscourseware').combobox('setValue','False');
    if(checkedItems[0].fields.resource_candownload)
        $('#resource_candownload').combobox('setValue','True');
    else
        $('#resource_candownload').combobox('setValue','False');

    // unbind click function
    $("#submit").unbind();

    $('#submit').click(function(){
        var form=$('#form1');
        if(form.form('validate')) {
            $('#form1').form('submit',{  
                url:'/course/resource/update/',
                onSubmit:function(){
                },  
                success:function(data){ 
                    var data = eval('(' + data + ')');
                    $.messager.alert('信息反馈',data.tip,'info',function(){
                       formCLearAndDlgClose();
                    });
                }  
            });
        }
    });
}

/* after operation we should do something */
function formCLearAndDlgClose() {
    $('#resourceAddDlg').dialog('close');             
    //$('#dg').datagrid('reload');
    $('#form1').form('clear'); 
    window.location.href=url;
}

/* delete the resource */
function resourceDelete() {
    var title='信息反馈';
    var checkedItems = $('#dg').datagrid('getChecked');
    if(checkedItems.length > 1 || checkedItems.length==0) {
        $.messager.alert(title,"请选择一条记录进行删除",'warning');
        return ;
    }
    /* has checked,can not delete the `courseware` ,but you can delete the resource */
    var ischecked=checkedItems[0].fields.course.fields.course_ischecked;

    if(ischecked && checkedItems[0].fields.resource_iscourseware ) {
        $.messager.alert(title,"此课程已发布，没有权限删除课件",'warning');
        return ;
    }
    /* delete the course */
    $.ajax({
        get:"POST",
        url:"/course/resource/delete/"+checkedItems[0].pk+"/",
        dataType:"json",
        success:function(data){$.messager.alert(title,data.tip,'info',
            function (){
                $("#dg").datagrid("reload"); 
            });
        },
        error:function(XMLHttpRequest,txtStatus,errorThrown){
            $.messager.alert(title,'warning',
                function (){
                    $('#dg').datagrid('reload');
                }
            );
        }
    });
}