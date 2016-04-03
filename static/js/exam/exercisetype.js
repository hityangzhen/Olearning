var u=window.location.href;
function exerciseTypeNameFormatter(value,row,index) {
	return row.fields.exercise_name;
}

function exerciseTypeScoreFormatter(value,row,index) {
	return row.fields.exercise_score;
}

function exerciseTypeStatusFormatter(value,row,index) {
	var value=row.fields.exercise_status ?'可用' : '不可用';
    return '<span style="color:orange; font-weight:bold;">'+value+'</span>';
}


$(function(){

	$.extend($.messager.defaults,{  
	    ok:"确定",  
	    cancel:"取消"  
	}); 
	  
	var dg=$('#dg');
	defaultPagination(dg);

});


// edit exercisetype notice
function exercisetypeEdit() {
	var id=$('#id').val();
	if(null==id || id=='') {
		exercisetypeAdd();
	}
    else {
        exercisetypeUpdate();
    }
}

/* add exercisetype */
function exercisetypeAdd() {
	var form=$('#form1');
	form.form('submit',{  
            url:u+'add/',
            onSubmit:function(){  
                return $(this).form('validate');  
            },
            success:function(data){ 
                var data = eval('(' + data + ')');
                $.messager.alert('信息反馈',data.tip,'info',function(){
                    $('#exercisetypeDlg').dialog('close');
                    $('#dg').datagrid('reload');
                });
            }  
    });   
}

// previous updating the exercisetype
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
        exercise_name:checkedItems[0].fields.exercise_name,
        exercise_score:checkedItems[0].fields.exercise_score,
    });

    if (checkedItems[0].fields.exercise_status)
        $('#exercise_status').combobox('setValue','True');
    else
        $('#exercise_status').combobox('setValue','False');

    $('#exercisetypeDlg').dialog('open');
}

/* update exercisetype */
function exercisetypeUpdate() {
	var form=$('#form1');
    form.form('submit',{  
            url:u+'update/',
            onSubmit:function(){  
                return $(this).form('validate');  
            },
            success:function(data){ 
                var data = eval('(' + data + ')');
                $.messager.alert('信息反馈',data.tip,'info',function(){
                    $('#exercisetypeDlg').dialog('close');
                    window.location.href=u;
                });
            }  
    });
}