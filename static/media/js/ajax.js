var PageWidth = 0;
var PageHeight = 0;
var tip = null;
var newLevel = null;
var leve = false;
var newLevelId = 'cm_new_level_div';
var divcount= 0;
function AjaxGet(url, target) {
	var targetsobj = $(target);
	url += '&in_ajax=1&' + Math.random(10);
	new Ajax.Request(url, {
        method: 'get',
		evalScript: true,
		onLoading: function() {
			CreateMaskLayer();
			CreateProcess();
		},
        onSuccess: function(req){	
			ClearMaskLayer()
			ClearProcess();
            rs = req.responseText;
			a = null;
			try {
				eval(rs);
			} catch (e) {
			}
			if (typeof(a) != 'object') {
				alert(a.msg);
				return false;
			}
			targetsobj.innerHTML = rs;
			return false;
        }
    });
    return false
}
function AjaxPost(url, obj_form) {
    new Ajax.Request(url, {
        method: 'post',
        parameters: $(obj_form).serialize(true),
		evalScript: true,
		onLoading: function() {
			CreateMaskLayer();
			CreateProcess();
		},
        onSuccess: function(req){
			ClearMaskLayer()
			ClearProcess();
            eval(req.responseText);
            CreateTip(a.msg, a.time);
            return a;
        }
    });
    return a;
}
function AjaxLevelPost(ids, obj_form) {
	var url = $(obj_form).action + '&in_ajax=1';
    new Ajax.Request(url, {
        method: 'post',
        parameters: $(obj_form).serialize(true),
		evalScript: true,
		onLoading: function() {
			CreateMaskLayer();
			CreateProcess();
		},
        onSuccess: function(req){
			ClearMaskLayer()
			ClearProcess();
			eval(req.responseText);
			alert(typeof(a));
            if (!a.stat) {
				alert(a.msg);
				return false;
			}
			CleanLevel(ids);
			CreateTip(a.msg, a.time);
			return false;
        }
    });
    return false;
}
function CreateMaskLayer(){
    GetPageSize();
    // 创建一个与页面宽高相同的遮罩层
	if (!$('cm_maskplayer_div')) {
		var ml = document.createElement('div');
		ml.id = 'cm_maskplayer_div';
		ml.className = "cm_maskplayer";
		ml.style.display = 'none';
		document.body.appendChild(ml);
	}
	if (ml.style.display != '') {
		ml.style.width = PageWidth + "px";
		ml.style.height = PageHeight + window.screen.height + "px";
		ml.style.display = '';
	}
}

function CreateProcess() {
	GetPageSize();
    // 创建一个与页面宽高相同的遮罩层
	if (!$('cm_process_div')) {
		var pl = document.createElement('div');
		pl.id = 'cm_process_div';
		pl.className = "cm_process";
		pl.style.display = 'none';
		document.body.appendChild(pl);
	}
	if (pl.style.display != '') {
		pl.style.top = PageHeight + (window.screen.height / 2) + "px";
		pl.style.left = (PageWidth / 2) + "px";
		pl.style.display = '';
	}
}

function ClearMaskLayer(){
	if ($('cm_maskplayer_div')) {
		$('cm_maskplayer_div').style.display = 'none';
		document.body.removeChild($('cm_maskplayer_div'));
		return true;
	}
	return false;	
}

function ClearProcess() {
	if ($('cm_process_div')) {
		$('cm_process_div').style.display = 'none';
		document.body.removeChild($('cm_process_div'));
		return true;
	}
	return false;
}

function GetPageSize(){
    // 获取页面的大小
    PageWidth = window.screen.availWidth - 25;
    PageHeight = getScrollTop() - 120;
}

function CreateTip(msg, time){
	GetPageSize();
    tip = document.createElement('div');
    document.body.appendChild(tip);
    tip.className = "cm_tip";
    tip.innerHTML = msg;
    tip.style.top = PageHeight + (window.screen.height / 2) + "px";
    tip.style.left = (PageWidth / 2) + "px";
	setTimeout("ClearTip()", time * 1000);
    return false;
}

function ClearTip(){
    document.body.removeChild(tip);
    return false;
}

function CreateLevel(id, LevelTitle) {
	dss._dragInfo.isDrag = true;
	GetPageSize();
    newLevel = document.createElement('div');
    document.body.appendChild(newLevel);
    newLevel.className = "cm_level" ;
	newLevel.id = newLevelId + id;
    newLevel.style.top = PageHeight + (window.screen.height / 2) + "px";
    newLevel.style.left = "220px";
	newLevel.style.display = 'none';
	newLevel.innerHTML = "<div class='cm_level_menu' onMouseDown=\"dss.beginDrag('"+newLevelId + id+"', event, '', true, true, {onDown : function() {}, onMove : function() {}, onUp : function() {}})\" ><span><a href='javascript:void(0)' onclick='CleanLevel("+id+")' class='cm_level_close'></a></span>"+LevelTitle+"</div><div class='cm_level_content' id=cm_new_level"+id+"></div>";
	return false;
}

function CleanLevel(id) {
	ClearMaskLayer();
	document.body.removeChild($(newLevelId + id));
    return false;
}

function ChangeLevel() {
	var width = newLevel.offsetWidth / 2;
	if (width == 0) {
		width = 300;
	}
	var height = newLevel.offsetHeight / 2;
	var tmpw = PageWidth / 2;
	var tmph = PageHeight / 2;
	newLevel.style.left = ( tmpw - width ) + 'px';
	newLevel.style.display = '';
	ClearProcess();
	return false;
}

function AjaxLevel(url, LevelTitle) {
	divcount++;
	CreateLevel(divcount, LevelTitle);
	url = url + '&in_ajax=1&divid=' + divcount;
	leve = true;
	AjaxLevelGet(url, 'cm_new_level'+divcount);
	return false;
}

function AjaxLevelGet(link, target){
	targetsobj = target;
	new Ajax.Request(link, {
        method: 'get',
		evalScript: true,
		onLoading: function() {CreateMaskLayer();CreateProcess(); },
        onSuccess: function(req){			
            rs = req.responseText;
			try {
				eval(rs);
			} catch (e) {
				
			}
			if (typeof(a) != 'object'&&typeof(a)!='undefined') {
				alert(a.msg);
				ClearMaskLayer();
				ClearProcess();
				return false;
			} else {
				$(targetsobj).innerHTML = rs;
				if (leve) {
					ChangeLevel();
					leve = false;
				}
				return false;
			}
			
        }
    });
    return false;
}