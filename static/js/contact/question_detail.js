		var u=window.location.href;
		var array=u.split('/');
		var courseid=array[array.length-3];

		function questionNameFormatter(value,row,index) {
			return row.fields.question_title;
		}

		function questionStarttimeFormatter(value,row,index) {
			return row.fields.question_starttime.replace(/[ZT]/g,' ');
		}
		function questionViewtimesFormatter(value,row,index) {
			return row.fields.question_viewtimes;
		}

		function questionOperationFormatter(value,row,index) {
			return '<a href="javascript:void(0)" onclick="deleteQuestion('+row.pk+')" >删除提问</a>';
		}
		function viewAnswersFormatter(value,row,index) {
			return '<a href="javascript:void(0)" onclick="viewAnswers('+row.pk+')" >查看回答</a>';
		}

		function answerQuestionContentFormatter(value,row,index) {
			return row.fields.answerquestion_content;
		}

		function answerQuestionTimeFormatter(value,row,index) {
			return row.fields.answerquestion_time.replace(/[TZ]/g,' ');
		}

		function answerQuestionStatusFormatter(value,row,index)  {
			return '<span style="color:orange">'+(row.fields.answerquestion_status?'可见':'不可见')+'</span>';
		}

		function answerQuestionShieldFormatter(value,row,index) {
			return '<a href="javascript:void(0)" onclick="answerQuestionShield('+row.pk+')">屏蔽</a>';	
		}

		function answerQuestionDeleteFormatter(value,row,index) {
			return '<a href="javascript:void(0)" onclick="answerQuestionDelete('+row.pk+')">删除</a>';	
		}

		$(function(){


		    $.extend($.messager.defaults,{  
		        ok:"确定",  
		        cancel:"取消"  
		    }); 

			var dg=$('#dg');
			dg.datagrid({
				url:'/contact/question/'+courseid+'/detail/list/',
			});

			defaultPagination(dg);
		});

		function executeDelete(questionid) {
			var title='信息反馈';
			$.ajax({
				type:'GET',
				url:'/contact/question/'+questionid+'/delete/',
				dataType:'json',
				success:function(data) {
					$.messager.alert(title,data.tip,function(){
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

		function deleteQuestion(questionid) {
			$.messager.confirm('删除提问', '确定执行此操作?', function(r){
				if(r) {
					executeDelete(questionid);
				}
			});
		}

		// 
		function viewAnswers(questionid) {
			$('#questionAnswerDlg').dialog('open');
			var dg=$('#answerDg');
			dg.datagrid({
				url:'/contact/answerquestion/'+questionid+'/list/'
			});
			defaultPagination(dg);
		}

		function answerQuestionShield(aqid) {

			$.messager.confirm('屏蔽提问', '确定执行此操作?', function(r){
				if(r) {
					execute('shield',aqid);
				}
			});
			
		}

		function answerQuestionDelete(aqid) {

			$.messager.confirm('删除提问', '确定执行此操作?', function(r){
				if(r) {
					execute('delete',aqid);
				}
			});
			
		}

		function execute(opeartion,aqid) {
			var title='信息反馈';
			$.ajax({
				type:'GET',
				dataType:'json',
				url:'/contact/answerquestion/'+aqid+'/'+opeartion+'/',
				success:function(data) {
					$.messager.alert(title,data.tip,'info',function(){
						$('#answerDg').datagrid('reload'); 
					})
				},
				error:function(XMLHttpRequest,txtStatus,errorThrown){
                    $.messager.alert(title,"网络出错"+txtStatus+","+errorThrown,'warning',function (){
                        $('#answerDg').datagrid('reload'); 
                    });
                }
			});
		}
