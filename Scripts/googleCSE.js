(function() {
			var cx = '004185851077072532640:ucst63as0kc';
			var gcse = document.createElement('script');
			gcse.type = 'text/javascript';
			gcse.async = true;
			gcse.src = (document.location.protocol == 'https:' ? 'https:' : 'http:') +
			'//www.google.com/cse/cse.js?cx=' + cx;
			var s = document.getElementsByTagName('script')[0];
			s.parentNode.insertBefore(gcse, s);
		})();
var gcsElementFixed = false;
var gcse = null;
var googleSearchResultsBox = null;
var fixFunction = function() {
	try {
		googleSearchResultsBox = $('#googleResultsBlockBody');
		gcse = $('#___gcse_1 .gsc-control-cse');
	 	if(gcse.length > 0) {
		 	gcse.css('padding',0);
		 	gcse.css('border',0);
		 	googleSearchResultsBox.css('display','block');
		 	gcsElementFixed = true;
		 }
	} catch (err) {
		gcsElementFixed = false;
	}
	
	if(gcsElementFixed == false) {
		setTimeout(fixFunction,1000);
	}
}
$( document ).ready(function() {
 	setTimeout(fixFunction,1000);
});