var ischecked=0;
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
    value=row.fields.course_status ?'可用' : '不可用';
    return '<span style="color:orange; font-weight:bold;">'+value+'</span>';
}

function courseDetailFormatter(value,row,index) {
    return '<a href="/course/detail/'+row.pk+'" style="color:blue;font-weight:bold">课程详情</a>';
}

function courseCheckedFormatter(value,row,index) {
    var checked=null;
    if(row.fields.course_ischecked==true) {
        checked=row.fields.course_checkedReply.split('##')[0]=='0'?'审核不通过':'审核通过';
        ischecked=checked;

    }
    else if(row.fields.course_ischecked==false) {
        checked='未审核';
    }
    value=row.fields.course_ischecked==null? '未发布' : checked;
    return '<span style="color:orange; font-weight:bold;">'+value+'</span>';
}

function resourceFormatter(value,row,index) {
    return '<a href="/course/resource/'+row.pk+'/" style="color:blue;font-weight:bold">课程资源</a>';
}
// add 2014-4-7
function noticeFormatter(value,row,index) {
    if(row.fields.course_ischecked==true && row.fields.course_checkedReply.split('##')[0]=='1')
        return '<a href="/course/'+row.pk+'/notice/" style="color:blue;font-weight:bold">课程公告管理</a>';
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

/* update the course */
function courseUpdate() {
    var title='信息反馈';
    var checkedItems = $('#dg').datagrid('getChecked');
    if(checkedItems.length > 1 || checkedItems.length==0) {
        $.messager.alert(title,"有且只能选择一条记录进行编辑",'warning');
        return ;
    }
     /* has checked,can not update */
    if(checkedItems[0].fields.course_ischecked) {
        $.messager.alert(title,"此课程已发布，没有权限编辑",'warning');
        return ;
    }
    window.location.href='/course/add/'+checkedItems[0].pk+'/';
}
/* delete the course */
function courseDelete() {
    var title='信息反馈';
    var checkedItems = $('#dg').datagrid('getChecked');
    if(checkedItems.length > 1 || checkedItems.length==0) {
        $.messager.alert(title,"请选择一条记录进行删除",'warning');
        return ;
    }
    /* has checked,can not delete */
    if(checkedItems[0].fields.course_ischecked) {
        $.messager.alert(title,"此课程已发布，没有权限删除",'warning');
        return ;
    }
    /* delete the course */
    $.ajax({
        get:"POST",
        url:"/course/delete/"+checkedItems[0].pk+"/",
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
// add 2014-4-7
/* publish the course */
function coursePublish() {
    var title='信息反馈';
    var checkedItems = $('#dg').datagrid('getChecked');
    if(checkedItems.length > 1 || checkedItems.length==0) {
        $.messager.alert(title,"请选择一条记录进行发布",'warning',null);
        return ;
    }

    if (checkedItems[0].fields.course_ischecked!=null) {
        $.messager.alert(title,'课程已发布，不能重复发布','warning',null);
        return ;
    }


    /* can publish */
    $.ajax({
        get:"POST",
        url:"/course/canpublish/"+checkedItems[0].pk+"/",
        dataType:"json",
        success:function(data){
            if (data.status=='failured') {
                $.messager.alert(title,data.tip,'warning',null);
                return false;
            }
            else {
                // execute publish
                publish(title,checkedItems[0].pk);
            }
        },
        error:function(XMLHttpRequest,txtStatus,errorThrown){
            $.messager.alert(title,"网络出错"+txtStatus+","+errorThrown,'warning',
                function (){
                    $('#dg').datagrid('reload');
                }
            );
        }
    });
}
/* execute publish */
function publish(title,id) {

     $.ajax({
        get:"POST",
        url:"/course/publish/"+id+"/",
        dataType:"json",
        success:function(data){
            $.messager.alert(title,data.tip,'info',function (){
                    $('#dg').datagrid('reload');
                });
        },
        error:function(XMLHttpRequest,txtStatus,errorThrown){
            $.messager.alert(title,"网络出错"+txtStatus+","+errorThrown,'warning',
                function (){
                    $('#dg').datagrid('reload');
                }
            );
        }
    });
}