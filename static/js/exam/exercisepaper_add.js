var u=window.location.href;
var urls=u.split('/');
var course_id='';
var exercisepaper_id=null;
if (u.indexOf('showupdate')==-1)
	course_id=urls[urls.length-3];
else {
	course_id=urls[urls.length-4];
	exercisepaper_id=urls[urls.length-2];
}
	

var urlprefix='';
if (u.indexOf('showupdate')==-1)
	urlprefix=u.split('showadd')[0];
else
	urlprefix=u.split('showupdate')[0];

var addedExercise=[];

function exerciseTitleFormatter(value,row,index) {
	return row.fields.exercise_title;
}

function exerciseTypeFormatter(value,row,index) {
	return row.fields.exercisetype.fields.exercise_name;
}

function exerciseCorrectItemFormatter(value,row,index) {
	return '<span style="color:blue">'+row.fields.exercise_correctitem+'</span>';
}

$(function(){

	$.extend($.messager.defaults,{  
        ok:"确定",  
        cancel:"取消"  
    }); 

	var dg=$('#dg');
	

	dg.datagrid({
		url:'/exam/teacher_exercise/'+course_id+'/list/',
        view: detailview,
        
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

	

	// for update
	if (u.indexOf('showupdate')!=-1) {
		$('#addDg').datagrid({
			url:urlprefix+'addedexercise/'+exercisepaper_id+'/',
			onLoadSuccess:function(data){
				addedExercise=data.rows;
			}
		});
	}

	defaultPagination(dg);
	defaultPagination($('#addDg'));
});

// set form's exercisepaper_allscore and exercise_exercisecount
function setForm() {
	$('#exercise_exercisecount').val(addedExercise.length);
	var sum=0;
	for(var i=0;i<addedExercise.length;i++) {
		sum += addedExercise[i].fields.exercisetype.fields.exercise_score;
	}
	$('#exercisepaper_allscore').val(sum);
}


// add exercise to paper
function addExerciseToPaper() {
	var title='信息反馈';
	var dg=$('#dg');
	var checkedItems=dg.datagrid('getChecked');
	if(checkedItems.length==0) {
		$.messager.alert(title,"至少选择一个习题",'warning');
        return ;
	}
	for(var i=0;i<checkedItems.length;i++)
		addedExercise.push(checkedItems[i]);
	$('#addDg').datagrid('loadData',addedExercise);
	setForm();
}

// delete the added exercise
function deleteAddedExercise() {
	var title='信息反馈';
	var dg=$('#addDg');
	var checkedItems=dg.datagrid('getChecked');
	if(checkedItems.length==0) {
		$.messager.alert(title,"至少选择一个习题",'warning');
        return ;
	}
	var data=[];

	for(var i=0;i<checkedItems.length;i++) {
		for (var j=0;j<addedExercise.length;j++) {
			if (checkedItems[i].pk!=addedExercise[j].pk)
				data.push(addedExercise[j]);
		}
	}		

	addedExercise=data;
	$('#addDg').datagrid('loadData',addedExercise);
	setForm();
}

// add the exercise paper
function exercisePaperAdd() {
	var title='信息反馈';
	var form=$('#form1');
	var checkedItems=addedExercise;
	if(addedExercise.length==0) {
		$.messager.alert(title,"至少选择一个习题",'warning');
        return ;
	}

	var exerciseidset='';
	for(var i=0;i<checkedItems.length;i++) {
		exerciseidset += checkedItems[i].pk+','
	}
	$('#addedExerciseIdSet').val(exerciseidset);

	var urls='';
	
	if(exercisepaper_id)
		urls=urlprefix+'update/'+exercisepaper_id+'/';
	else
		urls=urlprefix+'add/';

	form.form('submit',{  
		url:urls,
        onSubmit:function(){  
           	return $(this).form('validate');  
        },  
        success:function(data){ 
            var data = eval('(' + data + ')');
            $.messager.alert('信息反馈',data.tip,'info',function(){
               	window.location.href=urlprefix;
        	});
        }  
    });  
}

// publish the exercisepaper
function exercisePaperAddAndPublish() {
	$('#publish').val('1');
	exercisePaperAdd();
}