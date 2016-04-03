var url=window.location.href;
var array=url.split('/');
var course_id=array[array.length-2];

/* bing the coursetype */
function coursetypeBind(obj) {
    obj.combobox({
        url:'/admin/coursetype/array',
        valueField:'id',
        textField:'coursetype_name',
    });
}

$(function(){

	$.extend($.messager.defaults,{  
    	ok:"确定",  
    	cancel:"取消"  
	});   

    coursetypeBind($('#coursetype'));

    /* edit the course */
    if(!isNaN(course_id)) {
        loadCourse(course_id);
    }

});

function submitCourse() {
    /* add the course */
    if(isNaN(course_id)) {
        $('#form1').form('submit',{  
            onSubmit:function(){  
                return $(this).form('validate');  
            },  
            success:function(data){ 
                var data = eval('(' + data + ')');
                $.messager.alert('信息反馈',data.tip,'info',function(){
                    window.location.href='/course/add/show-detail   /'+data.id;
                });

            }  
        });   
    }
    else {
       $('#form1').form('submit',{  
            url:'/course/update/'+course_id+'/',
            onSubmit:function(){  
                return $(this).form('validate');  
            },  
            success:function(data){ 
                var data = eval('(' + data + ')');
                $.messager.alert('信息反馈',data.tip,'info',function(){
                    window.location.href='/course/detail/'+course_id+'/';
                });

            }  
        });    
    }
}
/* load from remote */
function loadCourse(course_id) {
    $('#form1').form('load','/course/'+course_id+'/');

}