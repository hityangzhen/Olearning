var u=window.location.href;

/* bind the exercisetype */
function exercisetypeBind(obj) {
    obj.combobox({
        url:'/exam/exercisetype/array/',
        valueField:'id',
        textField:'exercisetype_name',
        onSelect:function(record) {
			chooseExerciseType(record.id);

        }
    });
}

$(function(){
	// load the exercisetype
	exercisetypeBind($('#exercise_type'));
});

function chooseExerciseType(formid) {
	// judge
	if(formid==1) {
		$('#single').css('display','none');
		$('#statement').css('display','none');
		$('#judge').fadeIn('slow');

		bindSubmit($('#judge'));
		
	}
	// single
	else if(formid==2){
		$('#judge').css('display','none');
		$('#statement').css('display','none');
		$('#single').fadeIn('slow');

		bindSubmit($('#single'));
	}
	// statement
	else {
		$('#judge').css('display','none');
		$('#single').css('display','none');
		$('#statement').fadeIn('slow');

		bindSubmit($('#statement'));
	}
}

function bindSubmit(form) {
	var links=form.find('.easyui-linkbutton');
	$(links[0]).unbind();
	$(links[0]).click(function(){

		form.form('submit',{  
			url:u.split('showadd')[0]+'add/',
            onSubmit:function(){  
                return $(this).form('validate');  
            },  
            success:function(data){ 
                var data = eval('(' + data + ')');
                $.messager.alert('信息反馈',data.tip,'info',function(){
                	window.location.href=u.split('showadd')[0];
                });

            }  
        });  

	});
}

// 
function update(form,exerciseid) {

	var links=form.find('.easyui-linkbutton');
	$(links[0]).unbind();
	$(links[0]).click(function(){

		form.form('submit',{  
			url:u.split('showupdate')[0]+'update/'+exerciseid+'/',
            onSubmit:function(){  
                return $(this).form('validate');  
            },  
            success:function(data){ 
                var data = eval('(' + data + ')');
                $.messager.alert('信息反馈',data.tip,'info',function(){
                	window.location.href=u.split('showupdate')[0];
                });
            }  
        });  

	});
}

