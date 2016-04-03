// JavaScript Document
		var timerID = null;
		var timerRunning = false;
		function stopclock ()
		{
			if(timerRunning)
				clearTimeout(timerID);
			timerRunning = false;
		}
		function startclock () 
		{
			stopclock();
			showtime();
		}
		function showtime () 
		{
			var now = new Date();
			var months = now.getMonth()+1;
			var days = now.getDate();
			var day=now.getDay();
			var hours = now.getHours();
			var minutes = now.getMinutes();
			var seconds = now.getSeconds();
			var arr_week = new Array("星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六");
		    week = arr_week[day];
			var timeValue =now.getYear()+1900;
			timeValue +="-"+months+"-"+days+" ";
			timeValue += "" +((hours >= 12) ? "下午 " : "上午 " );
			timeValue += ((hours >12) ? hours -12 :hours);
			timeValue += ((minutes < 10) ? ":0" : ":") + minutes;
			timeValue += ((seconds < 10) ? ":0" : ":") + seconds;
			timeValue += " "+week;
			document.getElementById("bgclock").innerHTML= timeValue;
			
			timerID = setTimeout("showtime()",1000);
			timerRunning = true;
		}