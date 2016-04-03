/* datagrid 格式控制脚本 */

/* datagrid控制单元格样式 */
function cellStyler(value,rows,index) {
	if(value==false) {
		return 'color:orange; font-weight:bold;';
	}
}

function formatStatus(value) {
	return value==true ? '可用' : '不可用';
}

/**
 * 在右下角显示信息
 * @param {Object} m
 */
function bottomCenter(m) {
$.messager.show({
		title:'信息反馈',
		msg:m,
		showType:'slide',
		timeout:3000,
		/*style:{
			right:'',
			top:document.body.scrollTop+document.documentElement.scrollTop,
			bottom:''
		}*/
	});
}

function topCenter(m){
            $.messager.show({
                title:'信息反馈',
                msg:m,
                showType:'slide',
                timeout:3000,
                style:{
                    right:'',
                    top:document.body.scrollTop+document.documentElement.scrollTop+20,
                    bottom:''
                }
            });
        }
        
// 2013-3-31 add
// default pagination
function defaultPagination(dg) {
	var p = dg.datagrid('getPager');  
    $(p).pagination({  
    	pageSize: 5,//每页显示的记录条数，默认为10  
        pageList: [5,10,15],//可以设置每页记录条数的列表  
        beforePageText: '第',//页数文本框前显示的汉字  
        afterPageText: '页    共 {pages} 页',  
        displayMsg: '当前显示 {from} - {to} 条记录   共 {total} 条记录',
    }); 
}

// 2014-4-23 add
function timeFormat(seconds) {
    var hour=parseInt(seconds/3600);
    var minite=parseInt((seconds%3600)/60);
    seconds=(seconds%3600)%60;

    var timestr='';
    if(hour)
        timestr += hour+'小时';
    if (minite)
        timestr += minite+'分';
    if (seconds)
        timestr += seconds+'秒';
    return timestr;
}
