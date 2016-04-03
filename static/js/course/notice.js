var u=window.location.href;

function noticeTitleFormatter(value,row,index) {
	return row.fields.coursenotice_title;
}

function noticeTimeFormatter(value,row,index) {
	return row.fields.coursenotice_time.split('T')[0];
}

function teacherNameFormatter(value,row,index) {
	return row.fields.teacher;
}

function noticeStatusFormatter(value,row,index) {
	value=row.fields.coursenotice_status ?'可用' : '不可用';
    return '<span style="color:orange; font-weight:bold;">'+value+'</span>';
}

$(function(){

    $.extend($.messager.defaults,{  
        ok:"确定",  
        cancel:"取消"  
    }); 

	var dg=$('#dg');
	var contents='<font style="color: #0E2D5F;font-size:14px;font-weight;bolder;font-family:微软雅黑;">公告内容：</font>';
	contents += '<hr style="border: 1px solid #fff;"/>';

	dg.datagrid({
		url:u+'list/',
        view: detailview,
        onLoadSuccess:function(data){
            if(data.rows.length==0) {
                bottomCenter('<font style="color:red;font-size:13px;font-family:微软雅黑;">当前没有课程公告信息</font>');
            }
        },
        detailFormatter:function(index,row){
            return '<div class="ddv" style="padding:5px 60px 10px 20px;background-color: rgb(224, 236, 255);"></div>';
        },
        onExpandRow: function(index,row){
            var ddv = $(this).datagrid('getRowDetail',index).find('div.ddv');
            ddv.panel({
                height:100,
                border:false,
                cache:false,
                content:contents+'<p style="word-wrap:break-word;font-size:14px">'+row.fields.coursenotice_content+'</p>'
           	});
            $('#dg').datagrid('fixDetailRowHeight',index);
        }
    });

    defaultPagination(dg);



});

// edit course notice
function courseNoticeEdit() {
	var id=$('#id').val();
	if(null==id || id=='') {
		courseNoticeAdd();
	}
    else {
        courseNoticeUpdate();
    }
}
// add the notice
function courseNoticeAdd() {
	var form=$('#form1');
	form.form('submit',{  
            url:u+'add/',
            onSubmit:function(){  
                return $(this).form('validate');  
            },
            success:function(data){ 
                var data = eval('(' + data + ')');
                $.messager.alert('信息反馈',data.tip,'info',function(){
                    $('#courseNoticeDlg').dialog('close');
                    $('#dg').datagrid('reload');
                });
            }  
    });   
}
// previous updating the notice
function preUpdate() {

    var title='信息反馈';
    var checkedItems = $('#dg').datagrid('getChecked');
    if(checkedItems.length > 1 || checkedItems.length==0) {
        $.messager.alert(title,"有且只能选择一条记录进行编辑",'warning');
        return ;
    }

    var form=$('#form1');

    form.form('load',{
        id:checkedItems[0].pk,
        coursenotice_content:checkedItems[0].fields.coursenotice_content,
        coursenotice_title:checkedItems[0].fields.coursenotice_title,
        
    });

    if (checkedItems[0].fields.coursenotice_status)
        $('#coursenotice_status').combobox('setValue','True');
    else
        $('#coursenotice_status').combobox('setValue','False');

    $('#courseNoticeDlg').dialog('open');
}

// update the notice
function courseNoticeUpdate() {
    var form=$('#form1');
    form.form('submit',{  
            url:u+'update/',
            onSubmit:function(){  
                return $(this).form('validate');  
            },
            success:function(data){ 
                var data = eval('(' + data + ')');
                $.messager.alert('信息反馈',data.tip,'info',function(){
                    $('#courseNoticeDlg').dialog('close');
                    $('#dg').datagrid('reload');
                });
            }  
    });   
}

//  delete the notice
function courseNoticeDelete() {

    var title='信息反馈';
    var checkedItems = $('#dg').datagrid('getChecked');
    if(checkedItems.length==0) {
        $.messager.alert(title,"至少选择一条记录进行删除",'warning');
        return ;
    }
    var dg=$('#dg');

    $.messager.confirm('删除课程公告', '你确定要删除选中的课程公告吗？', function(r){
        if (r) {
            var id="";
            for(var i=0;i<checkedItems.length;i++)
                id += checkedItems[i].pk+",";
            $.ajax({
                type:"POST",
                url:u+'delete/',
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
}