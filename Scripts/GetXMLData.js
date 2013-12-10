xmlhttp = new XMLHttpRequest();

function getScores()
{
	xmlhttp.onreadystatechange = 
	function()
	{
		/* xml status numbers
		* 0: Hasn't started
		* 1: Connected to the server
		* 2: Server has received our request
		* 3: Server Processing:
		* 4: Request is finished and data is ready
		*/
		if(xmlhttp.readyState ==4 && xmlhttp.status==200)
		{
			x=xmlhttp.responseXML.documentElement.getElementsByTagName("CD");
			$('ajaxData').innerHTML = "got data!";
			console.log(x);
			console.log('xml page loaded!');
		}
		else
		{
			$('ajaxData').innerHTML = "waiting...";
		}
	}
	xmlhttp.open("GET", "http://localhost:8080/templates/Home/homeXMLData.xml", true);
	xmlhttp.send();
}

$(document).ready(getScores());