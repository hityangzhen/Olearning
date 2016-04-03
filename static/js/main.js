var index = 0;		
		function addPanel(node){
		if($('#tt').tabs('exists',node.text)){
			$('#tt').tabs('select',node.text)
		}
		else {
			
			$('#tt').tabs('add',{
				title: node.text,
				content: '<iframe scrolling="yes" frameborder="0"  src="'+node.attributes.url+'" style="width:100%;height:98%;"></iframe>',
				closable: true
			});
		}
		tabClose();
	}
		
		$(function(){

			var patrn=/\d+\/$/; 
			
			startclock();//用于显示当前时间
			for(var i=1;i<=9;i++)
			{
				$('#tree'+i).tree({
          			onClick:function(node){
          				if(node.text.indexOf('个人信息')>=0)
          					if (!patrn.exec(node.attributes.url)) 
          						node.attributes.url=node.attributes.url+$('#individual').val()+'/';
                		addPanel(node);
          			}
     			})
			}
			tabClose();
			tabCloseEven();
		})
		
		var onlyOpenTitle="欢迎使用";

		function createFrame(url)
		{
			var s = '<iframe scrolling="auto" frameborder="0"  src="'+url+'" style="width:100%;height:100%;"></iframe>';
			return s;
		}
		
		function tabClose()
		{
		    /*双击关闭TAB选项卡*/
		    $(".tabs-inner").dblclick(function(){
		        var subtitle = $(this).children("span").text();
		        if(subtitle!=onlyOpenTitle)
		        	$('#tt').tabs('close',subtitle);
		    })

		    $(".tabs-inner").bind('contextmenu',function(e){
		        $('#mm').menu('show', {
		            left: e.pageX,
		            top: e.pageY,
		        });
		        
		        var subtitle =$(this).children("span").text();
		        $('#mm').data("currtab",subtitle);
		        
		        return false;
		    });
		}
		
		function closeTab(action) 
		{ 
			var alltabs = $('#tt').tabs('tabs'); 
			var currentTab =$('#tt').tabs('getSelected'); 
			var allTabtitle = []; 
			$.each(alltabs,function(i,n){ 
				allTabtitle.push($(n).panel('options').title); 
			}); 
			switch (action) { 
				case "refresh": 
					var currtab_title = currentTab.panel('options').title;
					if(currtab_title!=onlyOpenTitle)
					{
						var iframe = $(currentTab.panel('options').content); 
						var src = iframe.attr('src'); 
						$('#tt').tabs('update', { 
							tab: currentTab, 
							options: { 
								content: createFrame(src) 
							} 
						});
					} 
					break; 
				case "close": 
					var currtab_title = currentTab.panel('options').title; 
					if(currtab_title!=onlyOpenTitle)
					{
						$('#tt').tabs('close', currtab_title); 
					}
					break; 
				case "closeall": 
					$.each(allTabtitle, function (i, n) { 
						if (n != onlyOpenTitle){ 
							$('#tt').tabs('close', n); 
						} 
					}); 
					break; 
				case "closeother": 
					var currtab_title = currentTab.panel('options').title; 
					$.each(allTabtitle, function (i, n) { 
						if (n != currtab_title && n != onlyOpenTitle) 
						{ 
							$('#tt').tabs('close', n); 
						} 
					}); 
					break; 
				case "closeright": 
					var tabIndex = $('#tt').tabs('getTabIndex', currentTab); 
					if (tabIndex == alltabs.length - 1){ 
						$.messager.alert('温馨提示','右侧已没有选项卡！','warning');
						return false; 
					} 
					$.each(allTabtitle, function (i, n) { 
						if (i > tabIndex) { 
							if (n != onlyOpenTitle){ 
								$('#tt').tabs('close', n); 
							} 
						} 
					}); 
					break; 
				case "closeleft": 
					var tabIndex = $('#tt').tabs('getTabIndex', currentTab); 
					if (tabIndex == 1) { 
						$.messager.alert('温馨提示','禁止操作！','warning'); 
						return false; 
					} 
					$.each(allTabtitle, function (i, n) { 
						if (i < tabIndex) { 
							if (n != onlyOpenTitle){ 
								$('#tt').tabs('close', n); 
							} 
						} 
					}); 
					break; 
				case "exit": 
					$('#closeMenu').menu('hide'); 
					break; 
			} 
		} 
		
		function tabCloseEven() { 
			$('#mm').menu({ 
				onClick: function (item) { 
					closeTab(item.id); 
				} 
			}); 
			return false; 
		} 
		
		