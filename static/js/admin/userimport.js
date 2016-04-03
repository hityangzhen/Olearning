function userImport() {
	var form=$('#form1');
	if (form.form('validate') && $('#userfile').val() ) {
		form.form('submit',{
			url:'/admin/userimport/'+$('#usertype').combobox('getValue')+'/',
			onSubmit:function(){
				$('#status').html('正在导入....');
			},
			success:function(data){  
				var data = eval('(' + data + ')');
				if(data.status=='success')
					$('#status').html(data.tip+'<p />'+'跳过用户名单：<p />'+data.usernames);
				else
              		$('#status').html(data.tip);
            }
		});
	}
}
