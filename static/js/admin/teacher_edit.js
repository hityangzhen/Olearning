
var url=window.location.href;
var array=url.split('/');
var teacher_id=array[array.length-2];

$(function(){


	$.extend($.messager.defaults,{  
    	ok:"确定",  
    	cancel:"取消"  
	});

	$('#teacher_userpwd').tooltip({
        position: 'right'
    });

    $('#teacher_head_portrait').tooltip({
        position: 'right'
    });

	// teacher_id is not in url's tail
	// add the teacher
	if(isNaN(teacher_id)) {
		$('#submit').click(function(){
			var form=$('#form1');

	        if(form.form('validate')) {

	        	if(!fileSuffixCheck())
	        		return ;

	            $('#form1').form('submit',{  
	                onSubmit:function(){  
	                },  
	                success:function(data){ 
	                    var data = eval('(' + data + ')');
	                    $.messager.alert('信息反馈',data.tip,'info',function(){
	                    	formCLearAndDlgClose();
	                    });
	                }  
	            });
	        }
		});
	}
	// update the teacher 
	else {
		$('#submit').click(function(){
			var form=$('#form1');

	        if(form.form('validate')) {
	        	if(!fileSuffixCheck())
	        		return ;
	            $('#form1').form('submit',{  
	            	url:'/admin/teacher/update/'+teacher_id+'/',
	                onSubmit:function(){  
	                },  
	                success:function(data){ 
	                    var data = eval('(' + data + ')');
	                    $.messager.alert('信息反馈',data.tip,'info',function(){
	                    	
	                    });
	                }  
	            });
	        }
		});
	}
});


function fileSuffixCheck() {
	var head_portrait=$('#teacher_head_portrait').val();
	if(head_portrait!=null && head_portrait!='') {
		// file haven't suffix
		if (head_portrait.indexOf('.')<0) {
			$.messager.alert('信息反馈','请选择图片','warning');
		    return false;
		}
	    var suffix=head_portrait.split('.')[1].toLowerCase();
	    if (suffix!='jpg' && suffix!='jpeg' && suffix!='png' && suffix!='gif') {
	       	$.messager.alert('信息反馈','请选择图片','warning');
	        return false;
	    }
	    return true;
	}
	return true;
}

/* after operation we should do something */
function formCLearAndDlgClose() {
    $('#form1').form('clear'); 
    window.location.href=url;
}