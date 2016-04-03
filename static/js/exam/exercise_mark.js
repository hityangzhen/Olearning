
function getExerciseMarkRawHtml(type,nums) {
	switch(type) {
		case 1:
			return judgeExerciseMarkRawHtml(nums);
		case 2:
			return singleExerciseMarkRawHtml(nums);
		case 3:
			return statementExerciseMarkRawHtml(nums);
	}
}

function judgeExerciseMarkRawHtml(nums) {
	var html = '<!-- for judge exercise mark -->\
	<div id="judge_mark" class="panel panel-default">\
      <div class="panel-heading">\
        <h4 class="panel-title">\
          <a data-toggle="collapse" data-toggle="collapse" data-parent="#accordion" href="#collapseOne">\
            判断题('+nums+')\
          </a>\
        </h4>\
      </div>\
      <div id="collapseOne" class="panel-collapse collapse">\
        <div class="panel-body">\
          <table id="judge_mark_table" class="table table-bordered">\
          </table>\
        </div>\
      </div>\
    </div>';

    return html;
}

function singleExerciseMarkRawHtml(nums) {
	var html='<!-- for single exercise mark -->\
    <div id="single_mark" class="panel panel-default">\
      <div class="panel-heading">\
        <h4 class="panel-title">\
          <a data-toggle="collapse" data-toggle="collapse" data-parent="#accordion" href="#collapseTwo">\
            单选题('+nums+')\
          </a>\
        </h4>\
      </div>\
      <div id="collapseTwo" class="panel-collapse collapse">\
        <div class="panel-body">\
          <table id="single_mark_table" class="table table-bordered">\
          </table>\
        </div>\
      </div>\
    </div>';

    return html;
}

function statementExerciseMarkRawHtml(nums) {
	var html='<!-- for statement exercise mark -->\
    <div id="statement_mark" class="panel panel-default">\
      <div class="panel-heading">\
        <h4 class="panel-title">\
          <a data-toggle="collapse" data-toggle="collapse" data-parent="#accordion" href="#collapseThree">\
            陈述题('+nums+')\
          </a>\
        </h4>\
      </div>\
      <div id="collapseThree" class="panel-collapse collapse">\
        <div class="panel-body">\
          <table id="statement_mark_table" class="table table-bordered">\
          </table>\
        </div>\
      </div>\
    </div>';
    return html;
}

// for radio marking
function bindClickToExerciseMarking(typename) {
	var exercise=$('#'+typename+' .well');
    for(var i=0;i<exercise.length;i++) {
      var inputs=$(exercise[i]).find('input[type="radio"]');
      for(var j=0;j<inputs.length;j++) {
        $(inputs[j]).attr('onclick','radioExerciseMarking($("#'+typename+'_mark_table"),this,this.name)');
      }
    }
}

// for textarea marking
function bindChangeToExerciseMarking(typename) {
	var exercise=$('#'+typename+' .well');
    for(var i=0;i<exercise.length;i++) {
      var textarea=$(exercise[i]).find('textarea');
      $(textarea[0]).attr('onchange','textareaExerciseMarking($("#'+typename+'_mark_table"),this,this.name)');
    }
}

function textareaExerciseMarking(table,obj,item) {
	// id
	var id=item.split('item')[1];	
	// td set
	var tds=table.find('td');
	// marking
	if ($(obj).val()==null || $(obj).val()=='') {
    $(tds[id-1]).css('background-color','#fefefe');
    $(tds[id-1]).css('value','');
  }
		
	else {
    $(tds[id-1]).css('background-color','yellow');
    //we don't need to set value
  }
		
}

function radioExerciseMarking(table,obj,item) {
	// id
	var id=item.split('item')[1];	
	// td set
	var tds=table.find('td');
	// marking
	$(tds[id-1]).css('background-color','yellow');
  // set value
  $(tds[id-1]).attr('value',obj.id+':'+obj.value);
}

// 
function getRadioAnswers(table) {
  if(table==null)
    return '';
  var tds=table.find('td');
  var answers='{';
  for (var i=0;i<tds.length;i++) {
    if($(tds[i]).attr('value'))
      answers += $(tds[i]).attr('value') + ',';
  }
  answers += '}';

  return answers;
}
// textarea tag is unique
function getTextareaAnswers() {
  var textareas=$('textarea');
  if(textareas==null || textareas.length==0)
    return ;
  var answers='{';
  for(var i=0;i<textareas.length;i++) {
    if($(textareas[i]).val()!='')
      answers += $(textareas[i]).attr('id')+':'+$(textareas[i]).val() + ',';
  }
  answers += '}';
  return answers;
}