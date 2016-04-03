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
function examFormatter(value,row,index) {
	if(row.fields.exercise_examtimes==row.exercise_haveexamedtimes)
		return '<span style="color:red">参加次数已满</span>';
	return '<a style="color:blue" href="/exam/student/exam/'+row.pk+'/" target="_blank">进入练习</a>';
}
function exerciseHaveExamedItmesFormatter(value,row,index) {
	return '<span style="color:orange">'+value+'</span>'
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

});