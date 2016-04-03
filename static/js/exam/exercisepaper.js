var u=window.location.href;

function exercisepaperNameFormatter(value,row,index) {
	return row.fields.exercisepaper_name;
}

function exerciseExerciseCountFormatter(value,row,index) {
	return row.fields.exercise_exercisecount;
}

function exerciseExamTimesFormatter(value,row,index) {
	return row.fields.exercise_examtimes;
}

function exercisepaperAllScoreFormatter(value,row,index) {
	return row.fields.exercisepaper_allscore;
}

function exercisepaperPassedscoreFormatter(value,row,index) {
	return row.fields.exercisepaper_passedscore;
}
function exercisepaperLasttimeFormatter(value,row,index) {
	return row.fields.exercisepaper_lasttime+'分钟';
}

function exerciseStarttimeFormatter(value,row,index) {
	return row.fields.exercise_starttime.split('T')[0];
}

function exerciseEndtimeFormatter(value,row,index) {
	return row.fields.exercise_endtime.split('T')[0];
}

function exerciseStatusFormatter(value,row,index) {

	var value=row.fields.exercise_status ?'可用' : '不可用';
    return '<span style="color:orange; font-weight:bold;">'+value+'</span>';
}

function exerciseIscheckedFormatter(value,row,index) {
	var value='';
	var ischecked=row.fields.exercise_ischecked;
	if (ischecked==null)
		value='未发布';
	else if (ischecked==0)
		value='未审核';
	else if(ischecked==1)
		value='审核不通过';
	else
		value='审核通过';
	
    return '<span style="color:orange; font-weight:bold;">'+value+'</span>';
}

function exercisePaperPreviewFormatter(value,row,index) {
	return '<a style="color:blue" target="_blank" href="/exam/exercisepaperpreview/'+row.pk+'/">练习预览</a>';
}



$(function(){

	$.extend($.messager.defaults,{  
    	ok:"确定",  
    	cancel:"取消"  
	}); 

	

	var dg=$('#dg');
    dg.datagrid({
    	url:u+'list/'
    });
    defaultPagination(dg);

    $('#tool_add_link').click(function(){
        window.location.href=u+'showadd/';
    });

});

// 
function exercisePaperDelete() {

	var title='信息反馈';
	var dg=$('#dg');
	var checkedItems=dg.datagrid('getChecked');

	if(checkedItems.length > 1 || checkedItems.length==0) {
		$.messager.alert(title,'请选择一条记录进行删除','warning');
		return ;
	}

	if(checkedItems[0].fields.exercise_ischecked!=null) {
		$.messager.alert(title,'试卷已发布，不能删除','warning');
		return ;
	}

	executeDelete(checkedItems[0].pk);

}
// 
function executeDelete(exercisepaperid) {
	var title='信息反馈';
	$.ajax({
        type:"get",
        url:u+'delete/'+exercisepaperid+'/',
        dataType:"json",
        success:function(data){
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
// publish exercise paper
function exercisePaperPublish() {
	var title='信息反馈';
	var dg=$('#dg');
	var checkedItems=dg.datagrid('getChecked');

	if(checkedItems.length > 1 || checkedItems.length==0) {
		$.messager.alert(title,'请选择一条记录进行发布','warning');
		return ;
	}

	if(checkedItems[0].fields.exercise_ischecked!=null) {
		$.messager.alert(title,'试卷已发布，不能发布','warning');
		return ;
	}

	executePublish(checkedItems[0].pk);
}

function executePublish(exercisepaperid) {

	var title='信息反馈';
	$.ajax({
        type:"get",
        url:u+'publish/'+exercisepaperid+'/',
        dataType:"json",
        success:function(data){
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

function exercisePaperUpdate() {

	var title='信息反馈';
	var dg=$('#dg');
	var checkedItems=dg.datagrid('getChecked');

	if(checkedItems.length > 1 || checkedItems.length==0) {
		$.messager.alert(title,'请选择一条记录进行编辑','warning');
		return ;
	}

	if(checkedItems[0].fields.exercise_ischecked!=null) {
		$.messager.alert(title,'试卷已发布，不能编辑','warning');
		return ;
	}

	window.location.href=u+'showupdate/'+checkedItems[0].pk+'/';

}