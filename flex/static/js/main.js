$( document ).ready(function() {
	$(".view").click(function(e){
	    $.ajax({
	    	method:"GET",
	    	url:"/monthly_report?="+this.id,
	    });
	        alert("Data: " + data);
	});
});