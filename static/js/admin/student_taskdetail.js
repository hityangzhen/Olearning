var u=window.location.href;
var array=u.split('/');
var taskid=array[array.length-2];

function courseNameFormatter(value,row,index) {
	return row.fields.course.fields.course_name;
}

function learnProgressFormatter(value,row,index) {

	value=row.fields.courselearning_rate;
	var rel='<div style="width:100%;height:15px;background-color:#FBEC88;margin-bottom:10px;">';
	rel += '<p style="width:'+value+'%;height:15px;background-color:#ccc;text-align:center;color:red">'+value+'%</p>';
	rel += '</div>';
	return rel;

}

function learnTimeSumFormatter(value,row,index) {
	return timeFormat(row.fields.courselearning_timelength);
}

function courseIsPassed(value,row,index) {

	switch(row.fields.courselearning_status) {
		case 0:
			value='未学';
			break;
		case 1:
			value='正在学习';
			break;
		case 2:
			value='已通过';
			break;
	}

	return '<span style="color:orange; font-weight:bold;">'+value+'</span>';
}

function learnCourse(value,row,index) {
	return '<a style="color:blue" href="/admin/task/showstudent_taskcourseware/'+taskid+'/'+row.fields.course.pk+'/">详情查看</a>';
}
// learn the course
function learnCredit(value,row,index) {
	return row.fields.courselearning_credit;
}

function courseCommentFormatter(value,row,index) {
	return '<a style="color:blue" target="_blank" href="/course/comment/'+row.fields.course.pk+'/">进入评价</a>';
}

function courseExercisepaper(value,row,index) {
	return '<a style="color:blue" href="/exam/student_exercisepaper/'+row.fields.course.pk+'/">练习浏览</a>';;
}

function resourceCenterFormatter(value,row,index) {
	return '<a style="color:blue" href="/course/student/show_resource/'+row.fields.course.pk+'/">课程资料</a>';
}

$(function(){

	var dg=$('#dg');
	dg.datagrid({
		url:'/admin/task/student_taskdetail/'+taskid+'/'
	});
	defaultPagination(dg);

})