$(document).ready(function(){
	$("#ChineseFood").mouseover(function(){
	$("#ChineseFood").attr("src", "static/image/Category/ChineseFood-Hover.png");
	});
	$("#ChineseFood").mouseout(function(){
	$("#ChineseFood").attr("src", "static/image/Category/ChineseFood.jpg");
	});
	$("#EuropeFood").mouseover(function(){
	$("#EuropeFood").attr("src", "static/image/Category/EuropeFood-Hover.png");
	});
	$("#EuropeFood").mouseout(function(){
	$("#EuropeFood").attr("src", "static/image/Category/EuropeFood.jpg");
	});
	$("#JapaneseFood").mouseover(function(){
	$("#JapaneseFood").attr("src", "static/image/Category/JapaneseFood-Hover.png");
	});
	$("#JapaneseFood").mouseout(function(){
	$("#JapaneseFood").attr("src", "static/image/Category/JapaneseFood.jpg");
	});
	$("#OthersFood").mouseover(function(){
	$("#OthersFood").attr("src", "static/image/Category/OthersFood-Hover.png");
	});
	$("#OthersFood").mouseout(function(){
	$("#OthersFood").attr("src", "static/image/Category/OthersFood.jpg");
	});
});