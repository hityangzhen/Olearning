		var u=window.location.href;
		var array=u.split('/');
		var courseid=array[array.length-3];

		function topicTitleFormatter(value,row,index) {
			return row.fields.topic_title;
		}

		function topicStarttimeFormatter(value,row,index) {
			return row.fields.topic_starttime.replace(/[ZT]/g,' ');
		}
		function topicViewtimesFormatter(value,row,index) {
			return row.fields.topic_viewtimes;
		}

		function topicOperationFormatter(value,row,index) {
			return '<a href="javascript:void(0)" onclick="deleteTopic('+row.pk+')" >删除话题</a>';
		}
		function viewReplysFormatter(value,row,index) {
			return '<a href="javascript:void(0)" onclick="viewReplys('+row.pk+')" >查看回复</a>';
		}

		// 
		function replyContentFormatter(value,row,index) {
			return row.fields.topicreply_content;
		}

		function replyTimeFormatter(value,row,index) {
			return row.fields.topicreply_time.replace(/[TZ]/g,' ');
		}

		function replyStatusFormatter(value,row,index)  {
			return '<span style="color:orange">'+(row.fields.topicreply_status?'可见':'不可见')+'</span>';
		}

		function replyShieldFormatter(value,row,index) {
			return '<a href="javascript:void(0)" onclick="topicReplyShield('+row.pk+')">屏蔽</a>';	
		}


		$(function(){


		    $.extend($.messager.defaults,{  
		        ok:"确定",  
		        cancel:"取消"  
		    }); 

			var dg=$('#dg');
			dg.datagrid({
				url:'/contact/topic/'+courseid+'/detail/list/',
			});

			defaultPagination(dg);
		});

		function executeDelete(topicid) {
			var title='信息反馈';
			$.ajax({
				type:'GET',
				url:'/contact/topic/'+topicid+'/delete/',
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

		function deleteTopic(topicid) {
			$.messager.confirm('删除话题', '确定执行此操作?', function(r){
				if(r) {
					executeDelete(topicid);
				}
			});
		}

		// 
		function viewReplys(topicid) {
			$('#topicReplyDlg').dialog('open');
			var dg=$('#replyDg');

			dg.datagrid({
				url:'/contact/replytopic/'+topicid+'/list/'
			});
			
			defaultPagination(dg);
		}

		function topicReplyShield(trid) {

			$.messager.confirm('屏蔽回复', '确定执行此操作?', function(r){
				if(r) {
					execute('shield',trid);
				}
			});
			
		}

		function execute(opeartion,trid) {
			var title='信息反馈';
			$.ajax({
				type:'GET',
				dataType:'json',
				url:'/contact/replytopic/'+trid+'/'+opeartion+'/',
				success:function(data) {
					$.messager.alert(title,data.tip,'info',function(){
						$('#replyDg').datagrid('reload'); 
					})
				},
				error:function(XMLHttpRequest,txtStatus,errorThrown){
                    $.messager.alert(title,"网络出错"+txtStatus+","+errorThrown,'warning',function (){
                        $('#replyDg').datagrid('reload'); 
                    });
                }
			});
		}
