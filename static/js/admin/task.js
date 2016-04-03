function taskNameFormatter(value,row,index) {
    return row.fields.task_name;
}

function coursetypeFormatter(value,row,index) {
    return row.fields.coursetype.fields.coursetype_name;
}

function taskStartTimeFormatter(value,row,index) {
    return row.fields.task_starttime.split('T')[0];
}
function taskEndTimeFormatter(value,row,index) {
    return row.fields.task_endtime.split('T')[0];
}
function taskStatusFormatter(value,row,index) {
    var value=row.fields.task_status ?'可用' : '不可用';
    return '<span style="color:orange; font-weight:bold;">'+value+'</span>';
}
function taskIsPublishedFormatter(value,row,index) {
   var value=row.fields.task_ispublished ?'是' : '否';
    return '<span style="color:orange; font-weight:bold;">'+value+'</span>'; 
}


$(function(){

    $.extend($.messager.defaults,{  
        ok:"确定",  
        cancel:"取消"  
    }); 

	var dg=$('#dg');
    var contents='<p>任务相关课程</p>';

	dg.datagrid({
		url:'/admin/task/list/',
        view: detailview,
        onLoadSuccess:function(data){
            if(data.rows.length==0) {
                bottomCenter('<font style="color:red;font-size:13px;font-family:微软雅黑;">当前没有任务信息</font>');
            }
        },
        detailFormatter:function(index,row){
            return '<div class="ddv" style="padding:5px 60px 50px 20px;background-color: rgb(224, 236, 255);color: #0E2D5F;"></div>';
        },
        onExpandRow: function(index,row){
            var ddv = $(this).datagrid('getRowDetail',index).find('div.ddv');
            ddv.panel({
                height:100,
                border:false,
                cache:false,
                content:contents+'<p>'+row.fields.task_courseids+'</p>'
           	});
            $('#dg').datagrid('fixDetailRowHeight',index);
        }
    });

    defaultPagination(dg);
});

// 
function taskPublish() {

    var title='信息反馈';
    var record=taskSingleSelect($('#dg'),title);
    if(record) {
        if(record.fields.task_ispublished) {
            $.messager.alert(title,'任务已经发布','warning');
            return ;
        }
        executeAjaxOperation('/admin/task/publish/'+record.pk+'/',title);
    }
}

// 
function taskUpdate() {
    var title='信息反馈';
    var record=taskSingleSelect($('#dg'),title);
    if(record) {
        if(record.fields.task_ispublished) {
            $.messager.alert(title,'任务已经发布，不能编辑','warning');
            return ;
        }
        window.location.href='/admin/task/showupdate/'+record.pk+'/';
    }
}

function taskDelete() {
    var title='信息反馈';
    var record=taskSingleSelect($('#dg'),title);
    if(record) {
        if(record.fields.task_ispublished) {
            $.messager.alert(title,'任务已经发布，不能删除','warning');
            return ;
        }
        executeAjaxOperation('/admin/task/delete/'+record.pk+'/',title);   
    }
}

function taskSingleSelect(dg,title) {
   var title='信息反馈';
    var checkedItems=dg.datagrid('getChecked');
    if(checkedItems.length==0 || checkedItems.length >1) {
        $.messager.alert(title,'请选择一条任务信息','warning');
        return false;
    } 
    return checkedItems[0];
}

function executeAjaxOperation(u,title) {
    $.messager.confirm(title, '你确定要执行此操作吗?', function(r){
            if(r) {
                $.ajax({
                    type:'get',
                    url:u,
                    dataType:'json',
                    success:function(data) {
                        $.messager.alert(title,data.tip,'info',function (){
                            $('#dg').datagrid('reload');
                        });
                    },
                    error:function(XMLHttpRequest,txtStatus,errorThrown){
                        $.messager.alert(title,"网络出错"+txtStatus+","+errorThrown,'warning',function (){
                            $('#dg').datagrid('reload'); 
                        });
                    }
                });
            }

        });
}