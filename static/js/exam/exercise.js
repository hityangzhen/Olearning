var u=window.location.href;

function exerciseTitleFormatter(value,row,index) {
	return row.fields.exercise_title;
}

function exerciseTypeFormatter(value,row,index) {
	return row.fields.exercisetype.fields.exercise_name;
}

function exerciseCorrectItemFormatter(value,row,index) {
	return '<span style="color:blue">'+row.fields.exercise_correctitem+'</span>';
}

function exerciseStatusFormatter(value,row,index) {
	var value=row.fields.exercise_status ?'可用' : '不可用';
    return '<span style="color:orange; font-weight:bold;">'+value+'</span>';
}

$(function(){

    $.extend($.messager.defaults,{  
        ok:"确定",  
        cancel:"取消"  
    }); 

	var dg=$('#dg');

	dg.datagrid({
		url:u.split()+'list/',
        view: detailview,
        onLoadSuccess:function(data){
            if(data.rows.length==0) {
                bottomCenter('<font style="color:red;font-size:13px;font-family:微软雅黑;">当前没有课程习题</font>');
            }
        },
        detailFormatter:function(index,row){
            return '<div class="ddv" style="padding:5px 60px 50px 20px;background-color: rgb(224, 236, 255);color: #0E2D5F;"></div>';
        },
        onExpandRow: function(index,row){
            var ddv = $(this).datagrid('getRowDetail',index).find('div.ddv');
            var contents='';
            var exercisetype=row.fields.exercisetype;

            if(exercisetype.pk==1) {
            	contents += '<p>选项：';
            	contents += '&nbsp;&nbsp; A：'+row.fields.exercise_itema+'&nbsp;&nbsp;';
            	contents += '&nbsp;&nbsp; B：'+row.fields.exercise_itemb+'<br /></p>';
            }
            else if(exercisetype.pk==2) {
            	contents += '<p>选项：';
            	contents += '&nbsp;&nbsp; A：'+row.fields.exercise_itema+'&nbsp;&nbsp;';
            	contents += '&nbsp;&nbsp; B：'+row.fields.exercise_itemb+'&nbsp;&nbsp;';
            	contents += '&nbsp;&nbsp; C：'+row.fields.exercise_itemc+'&nbsp;&nbsp;';
            	contents += '&nbsp;&nbsp; D：'+row.fields.exercise_itemd+'<br /></p>';
            }

            	
            ddv.panel({
                height:100,
                border:false,
                cache:false,
                content:contents+'<p style="word-wrap:break-word;font-size:12px">解题思路：'+row.fields.exercise_resolution+'</p>'
           	});
            $('#dg').datagrid('fixDetailRowHeight',index);
        }
    });

    defaultPagination(dg);

    $('#tool_add_link').click(function(){
        window.location.href=u+'showadd/';
    });
});

// update the exercise
function exerciseUpdate() {
    var title='信息反馈';
    var checkedItems = $('#dg').datagrid('getChecked');
    if(checkedItems.length > 1 || checkedItems.length==0) {
        $.messager.alert(title,"有且只能选择一条记录进行编辑",'warning');
        return ;
    }

    window.location.href=u+'showupdate/'+checkedItems[0].pk+'/'
}