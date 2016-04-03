var u=window.location.href;
var taskid='';
var title='信息反馈';
if (u.indexOf('showupdate')) {
    var array=u.split('/');
    taskid=array[array.length-2];
}

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

function courseLearnerFormatter(value,row,index) {
	return row.fields.course_learner;
}

function courseDescriptionFormatter(value,row,index) {
	return row.fields.course_description;
}


/* bing the coursetype */
function coursetypeBind(obj) {
    obj.combobox({
        url:'/admin/coursetype/array',
        valueField:'id',
        textField:'coursetype_name',
        onLoadSuccess:function() {
        	var data = $(this).combobox('getData');
            if (data.length > 0) {
                $(this).combobox('select', data[0].id);
            }
            courseLoadByCourseType(data[0].id);
            $('#coursetype_id').val(data[0].id);
        },
        onSelect:function(record) {
        	courseLoadByCourseType(record.id);
        	$('#coursetype_id').val(record.id);
        }
    });
}

$(function(){

	$.extend($.messager.defaults,{  
    	ok:"确定",  
    	cancel:"取消"  
	}); 

	coursetypeBind($('#coursetype'));

    if(!isNaN(taskid)) {
        $('#coursetype').combobox({
            readonly:true
        });
    }
});

function courseLoadByCourseType(coursetype_id) {

	$('#dg').datagrid({
		url:'/course/list/bycoursetype/'+coursetype_id+'/',
		onLoadSuccess:function(data){
			if(data.rows.length==0) {
                bottomCenter('<font style="color:red;font-size:13px;font-family:微软雅黑;">当前没有任务信息</font>');
            }
		}
	});
}

function addTaskCourse() {
	var checkedItems=$('#dg').datagrid('getChecked');
	if(checkedItems.length==0) {
		$.messager.alert(title,'至少选择一条课程记录','warning');
		return ;
	}

	$.messager.confirm(title, '你确定要选中的课程作为学习任务吗?', function(r){
        if (r){
        	var courseidset='';
        	for(var i=0;i<checkedItems.length;i++) {
        		courseidset += checkedItems[i].pk+',';
        	}
        	$('#task_courseids').val(courseidset);
        }
    });
}

function taskEdit() {
    if(isNaN(taskid)) {
        taskAdd();
    }
    else {
        taskUpdate();
    }
}

// add task
function taskAdd() {
	var courseidset=$('#task_courseids').val();

	if(null==courseidset || courseidset=='') {
		$.messager.alert(title,'请至少选择一条课程记录','warning');
		return ;
	}

    executeAjaxOperation('/admin/task/add/');
}

// 
function taskUpdate() {
    var courseidset=$('#task_courseids').val();

    if(null==courseidset || courseidset=='') {
        $.messager.alert(title,'请至少选择一条课程记录','warning');
        return ;
    }

    executeAjaxOperation('/admin/task/update/'+taskid+'/');
}

// 
function executeAjaxOperation(u) {

    $('#form1').form('submit',{ 
        url:u,
        onSubmit:function(){  
            return $(this).form('validate');  
        },  
        success:function(data){ 
            var data = eval('(' + data + ')');
            $.messager.alert(title,data.tip,'info',function(){
                window.location.href='/admin/task/';
            });
        }  
    }); 
}

function taskPublish() {
    $('#publish').val('1');
    taskEdit();
}

// clear
function clear() {
	var form=$('form1').form('clear');
}
