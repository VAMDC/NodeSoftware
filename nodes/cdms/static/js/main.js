function load_page(page) {
  // window.document.forms[0].T_PAGE.value=page; 
  window.document.forms[0].action=page;
  window.document.forms[0].submit();
}

function show_doc(eId) {
  window.document.forms[0].T_PAGE.value="Doc"; 
  window.document.forms[0].T_EID.value=eId; 
  window.document.forms[0].submit();
}

function docShowSubpage(id) {
  //  $("fieldset").hide();
  $(".subpage").hide();
  $("#"+id).show();

}

function disableEnterKey(e)
{
     var key;     
     if(window.event)
          key = window.event.keyCode; //IE
     else
          key = e.which; //firefox     

     return (key != 13);
}

function showQueryRefinements() {
  var dataToSend = $.param($("form .log").serializeArray());
  //  alert($.param(dataToSend));
  //  var dataToSend2 =  "Test mit javascript".replace(/javascript/gi,"JavaScript");
  
  dataToSend = dataToSend.replace("T_SEARCH_FREQ_FROM", "frequency from");
  dataToSend = dataToSend.replace("T_SEARCH_FREQ_TO", "frequency to");
  dataToSend = dataToSend.replace("T_SEARCH_INT", "min. intensity");
  dataToSend = dataToSend.replace("T_TEMPERATURE", "temperature");
  dataToSend = dataToSend.replace("T_SHOWEXPLINES", "Show experimental lines");
  dataToSend = dataToSend.replace("T_SORT", "Sort by ");
  dataToSend = dataToSend.replace("T_TYPE", "Output format type");
  dataToSend = dataToSend.replace("comfort", "Full quantum number description");
  dataToSend = dataToSend.replace(/%5B%5D/g,"");
  dataToSend = dataToSend.replace(/T_M_TAG/g,"Species ID");
  var paramList = dataToSend.split("&");
  var htmlCode = "<div class='clearfix full'>";
  $.each(paramList, function(index, row) {
	   value = row.split("=");
	   htmlCode+="<div  class='columnar' style='clear:left'>";
	   htmlCode+="<strong style='float:left;min-width:12em;padding-right:1em;text-align:right;'>"+value[0]+"</strong>";
	   htmlCode+="<var>"+value[1]+"</var></div>";
	 });
  htmlCode += "</div>";

  data = ajaxControlForm('checkQuery');

  ajax = eval('(' + data + ')');

  // Überprüfen, ob ein JS Objekt da ist.
  if(ajax!=false) {
    //$("#htmlContainer").html(ajax.htmlcode);
    $("#refinements").html(ajax.htmlcode);
    $("#QUERY").val(decodeURIComponent(ajax.QUERY));
    $("#TAPxsams").text(decodeURIComponent(ajax.QUERY));
  } else {
    $("#refinements").html(htmlCode);
  }

}


function showFitDetails(subpage,k) {

    window.document.forms[0].T_PAGE.value="Fit";
    window.document.forms[0].T_FIT_ANALYSE.value=subpage;
    window.document.forms[0].T_SEL_PAR.value=k; 
    window.document.forms[0].submit();

}


function open_help(topic) {
     msg=window.open("","msg","height=200,width=200,left=80,top=80");
     msg.document.write("<html><title> Help </title>");
     msg.document.write("<body bgcolor='white' onblur=window.close()>");
     msg.document.write("<center>")
     msg.document.write("<h1> HELP - Topic "+topic+"</h1> ");
     msg.document.write("<p> "+topic+" </p> ");
     mwg.document.write("</center>");
     msg.document.write("</body></html><p>");
}

function setFocus(page) {
  if (page=="SaveCatFile") {
    window.document.forms[0].elements[21].focus();
  }


}

function submitOutputURL() {
  // calls output URL for XSAMS output
  //  alert(window.document.forms["PARAMETER"].action);
  if (window.document.forms[0].T_TYPE.value=='xsams-servlet')
    {
      window.document.forms["PARAMETER"].action='http://hera.ph1.uni-koeln.de:8080/examples/servlets/servlet/CdmsServlet2';
    }
  else
    {
      window.document.forms["PARAMETER"].action='./showResults';
    }
  //  $("form").append("<INPUT TYPE='HIDDEN' NAME='T_PAGE' VALUE='ShowResults'>");
  window.document.forms["PARAMETER"].submit();
}

function open_dialog(obj) {
   
  window.document.forms[0].T_DUMMY.value=obj; 
  parid=window.document.forms[0].elements[obj].value;
  win_parid=window.open("cp_edit_parid.php?parid="+parid ,"EditParid","width=610,height=400"); 
   
}

function fillPostVar() {

  var rows = document.getElementsByTagName("tr");
  var theform= window.document.forms[0]; //document.element.Form[0]; //document.createElement('form')
  
  for (var i = 0; i < rows.length; i++) {
            if (rows[i].className.indexOf("molRowSel")!=-1) {  
//              alert (rows[i].id);
              var theinput=document.createElement('input')
              with (theinput) {
                type='hidden'
                name='T_M_TAG['+i+']'
                value=rows[i].id.substr(3);
              }
              theform.appendChild(theinput)

            }
  }
//  var postVar = document.getElementById("postVar");
  var testA = new Array();
  testA[0]=22;
  testA[1]=23;
//  postVar[0].value=39502; //testA; //"39502";
//  postVar.value=testA;

//  with (theform) {
//    action=where
//    method='post'
//  }
//  document.body.appendChild(theform)
//  for (var i=0,l=testA.length;i<l;i++) {
//      var theinput=document.createElement('input')
//      with (theinput) {
//        type='hidden'
//        name='T_M_TAG['+i+']'
//        value=testA[i]
//      }
//      theform.appendChild(theinput)
//  }
//  theform.submit()


//alert(theinput.value);  
//alert("Senden");
}

function createPostVar() {
  $(".entrySelected").each(function(index,value) {
			     // alert($(this).attr("id"));
			     $("<input type='hidden' name='speciesIDs' value='"+$(this).attr("id")+"'>").appendTo("form");
			   });
}

function selectAll() {
  //  $(".molRow:visible").css("background-color","#99CCFF");
  $(".molRow:visible").addClass("entrySelected");
}

function deselectAll() {
  //  $(".molRow:visible").css("background-color","transparent");
  $(".molRow:visible").removeClass("entrySelected");
}

function selectMolRow(id) {
//alert(id);
//     alert(id.firstChild.nodeValue);
     parentID=id; //.parentNode;
//     alert(id.parentNode.tagName);
//     alert(parentID.className);
//     alert(id.nodeName);
     
     //id.parentNode.style.visibility = "collapse";
     if (parentID.className=='molRowSel') {
        parentID.className='molRow';
        id.className='molRow';
     } else {
        parentID.className='molRowSel';
        id.className='molRowSel';
     }
     //alert(document.getElementById(eTag52507).id); //align = wie;
     //alert(id);
     filterRows();
}

function selectMolRow2(id) {

  //  if (  $("#"+id).css("background-color") != "transparent") {
  if (  $("#"+id).hasClass("entrySelected")) {
    //    $("#"+id).css("background-color","transparent");
    $("#"+id).removeClass("entrySelected");
  } else {
    //    $("#"+id).css("background-color","#99CCFF");
    $("#"+id).addClass("entrySelected");
  }
}

function filterRows2() {
  tag = $("#eTagFilter").val();
  name = $("#molNameFilter").val();
  trivName = $("#molTrivNameFilter").val();
  isotopolog = $("#isoFilter").val();
  state = $("#stateFilter").val();

  // Initialize the regexp
  try {
    rtag = new RegExp(tag,"g");
    
  } catch(e) {    
    alert(e);
    tag = $("#eTagFilter").val("");
    return;
  }
  try {
    rname = new RegExp(name,"g");
    
  } catch(e) {    
    alert(e);
    name = $("#molNameFilter").val("");
    return;
  }
  try {
    rtrivName = new RegExp(trivName,"g");
    
  } catch(e) {    
    alert(e);
    trivName = $("#molTrivNameFilter").val("");
    return;
  }
  try {
    risotopolog = new RegExp(isotopolog,"g");
    
  } catch(e) {    
    alert(e);
    isotopolog = $("#isoFilter").val("");
    return;
  }
  try {
    rstate = new RegExp(state,"g");
    
  } catch(e) {    
    alert(e);
    state = $("#stateFilter").val("");
    return;
  }


  $(".molRow").each(function(index,value) {
		      etag = $.trim($(this).find("div.eTag").text());
		      eName = $.trim($(this).find("div.eName").text());
		      mTrivName = $.trim($(this).find("div.mTrivName").text());
		      eIso = $.trim($(this).find("div.eIso").text());
		      eState = $.trim($(this).find("div.eState").text());

		      if ((rtag.test(etag)) &&
			  (rname.test(eName)) &&
			  (rtrivName.test(mTrivName)) &&
			  (risotopolog.test(eIso)) &&
			  (rstate.test(eState))
			  )  {
			$(this).show();
		      } else {
			$(this).hide();
		      }

		    });

}

function filterRows() {

   var el_eTagFilter = document.getElementById("eTagFilter");
   var el_molNameFilter = document.getElementById("molNameFilter");
   var el_eIsoFilter = document.getElementById("isoFilter");
   var el_eStateFilter = document.getElementById("stateFilter");
//   alert (test.value);
   var eTagFilterValue = el_eTagFilter.value;
   var molNameFilterValue = el_molNameFilter.value;
   var eIsoFilterValue = el_eIsoFilter.value;
   var eStateFilterValue = el_eStateFilter.value;
//alert (molNameFilterValue);   
   var rows = document.getElementsByTagName("tr");
   var fields = document.getElementsByTagName("td");
   var val, val0, val1, val2, val3;
   //  only for testing: make all nodes invisible
//   alert(rows[20].className);
   for (var i = 0; i < rows.length; i++) {
         if (rows[i].className.indexOf("molRow")!=-1)  {
//            alert(rows[i].className);
//            rows[i].style.visibility = "collapse";
            var childs = rows[i].childNodes;
  //          if (i<5) {alert(childs[1].firstChild.nodeValue);}

            if (childs[1].childNodes.length>0) {
//            if (i<30) {alert(rows[i].childNodes[7].firstChild.nodeValue);}
              val0=childs[1].firstChild.nodeValue;
              val1=childs[3].firstChild.nodeValue;
              val2=childs[5].firstChild.nodeValue;
              val3=childs[7].firstChild.nodeValue;
//if (i<5) {alert (val0); alert(val0.search(RegExp(eTagFilterValue,"g"))); }
	      if ((val1)) { //alert (val0);}
    //          if (i<5) {alert (val0); alert(val0.search(RegExp(eTagFilterValue,"g"))); }//childs[1].firstChild.nodeValue);}

                if ((val0.search(RegExp(eTagFilterValue,"g"))==-1)  
                 || (val1.search(RegExp(molNameFilterValue,"g"))==-1) //) {
                 || (val2.search(RegExp(eIsoFilterValue,"g"))==-1) //) {
                 || (val3.search(RegExp(eStateFilterValue,"g"))==-1)) {
	          //                rows[i].style.visibility = "collapse";  
  	          rows[i].style.display = "none";  
                } else {
   	          //                rows[i].style.visibility = "visible";  
 	          rows[i].style.display = ""; 
                }
	      }
	    } 
         }
   }

//   for (var i = 0; i < fields.length; i++) {
//      val=fields[i].firstChild.data;
//      var test = fields[i];
//      var re=new RegExp (eTagFilterValue,"g");

//      if ((val.search(RegExp(eTagFilterValue,"g"))>-1) && (fields[i].id.indexOf(eTagFilterValue)!=-1)) {
//         fields[i].style.color = "red";
//            fields[i].parentNode.style.visibility = "visible";
//            test = test.nextSibling;
//            alert(test.nodeName);
//      }
//      if ((val.search(RegExp(molNameFilterValue,"g"))>-1) && (fields[i].id.indexOf("molName")!=-1)) {
//            fields[i].parentNode.style.visibility = "visible";
//            alert("HALLO");
//      }
//      if ((val.search(RegExp(eIsoFilterValue,"g"))>-1) && (fields[i].id.indexOf(eIsoFilterValue)!=-1)) {
//            fields[i].parentNode.style.visibility = "visible";
//      }
//      if ((val.search(RegExp(eStateFilterValue,"g"))>-1) && (fields[i].id.indexOf(eStateFilterValue)!=-1)) {
//            fields[i].parentNode.style.visibility = "visible";
//      }
//   }
}

function orderByTag() {
  var orderByField = document.getElementById("orderBy");
  if (orderByField.value=='E_TAG ASC') {
     orderByField.value='E_TAG DESC';
  } else {
     orderByField.value='E_TAG ASC';
  }
  fillPostVar();
  load_page('SelectMolecule');
}


function orderByM_Name() {
  var orderByField = document.getElementById("orderBy");
  if (orderByField.value=='M_Name ASC') {
     orderByField.value='M_Name DESC';
  } else {
     orderByField.value='M_Name ASC';
  }
  fillPostVar();
  load_page('SelectMolecule');
}


function orderByIso() {
  var orderByField = document.getElementById("orderBy");
  if (orderByField.value=='E_Isotopomer ASC') {
     orderByField.value='E_Isotopomer DESC';
  } else {
     orderByField.value='E_Isotopomer ASC';
  }
  fillPostVar();
  load_page('SelectMolecule');
}


function orderByState() {
  var orderByField = document.getElementById("orderBy");
  if (orderByField.value=='E_States ASC') {
     orderByField.value='E_States DESC';
  } else {
     orderByField.value='E_States ASC';
  }
  fillPostVar();
  load_page('SelectMolecule');
}



function ajaxControlForm(func, data) {
  if (data) {
    //  var dataToSend = new Array();
    // dataToSend.push(data);
    dataToSend = data;
  } else {
    var dataToSend =  $("form").serializeArray();
  }

  if (typeof func=="undefined")
    var func="";

  var datum = {"name" : "function", "value" : func}; 
  dataToSend.push(datum);

  // call ajax
  return  $.ajax({

    url: './ajaxRequest',
	data: dataToSend,
	type: "POST",
	// Wird ausgeführt, wenn die Datei erfolgreich requestet wurde
	async: false,
	success: function(data) {

	ajax = eval('(' + data + ')');
	// Überprüfen, ob ein JS Objekt da ist.
	if(ajax!=false) {
	  // Die von PHP generierte Meldung dem Benutzer darstellen
	  $("#message").html( ajax.message );
	}
      }
    }).responseText;
  
}


function ajaxGetVAMDCstats() {
  $("#form_otherDbs").append("<h3>TEST</h3>");
  var dataToSend = { "REQUEST" : "doQuery", 
		     "LANG" : "VSS1",
		     "FORMAT" : "XSAMS",
		     "QUERY" : "SELECT ALL WHERE MoleculeInchiKey='UWBOAQKPEXKXSU-HXFQMGJMSA-N'"
		     //		     "QUERY" : "SELECT ALL WHERE MoleculeStoichiometricFormula = 'CO'"
		    };


  // call ajax
  $.ajax({

    url: 'http://cdms.ph1.uni-koeln.de:8090/DjCDMS/tap/sync?',
      //    url: 'http://cdms.ph1.uni-koeln.de:8090/DjCDMS/tap/sync?REQUEST=doQuery&LANG=VSS1&FORMAT=XSAMS&QUERY=SELECT+ALL+WHERE++MoleculeStoichiometricFormula+%3D+%27HB%27',
	data: dataToSend,
	type: "GET",
    // Wird ausgeführt, wenn die Datei erfolgreich requestet wurde
	async: true,
	success: function(data) {
	alert("Coming back");
	ajax = eval('(' + data + ')');
	// Überprüfen, ob ein JS Objekt da ist.
	if(ajax!=false) {
	  // Die von PHP generierte Meldung dem Benutzer darstellen
	  $("#form_otherDbs").append(ajax);
	  alert("Done");
	}
      },
    error: function(xhr, ajaxOptions, thrownError){
                    alert(xhr.statusText);
                    alert(xhr.responseText);
		    jsonValue = jQuery.parseJSON( xhr.responseText );
		    alert(jsonValue);
      },
    complete: function(data) {
	alert("Completed");
	alert(data.getAllResponseHeaders());

      }
    });
}

function ajaxGetAllVamdcDBstat() {
  // Perform query only once 
  if ($("#results").length == 0) {
    
    // Set Please wait message
    $("#form_otherDbs").html("please wait ...");
    
    // Set POST - Items
    var inchikey = $("#inchikey").html();
    var dataToSend = new Array();
    var datum = {"name" : "inchikey", "value" : inchikey}; 
    var nodeurl = "";
    dataToSend.push(datum);
    
    // Do Ajax - Request
    data = ajaxControlForm('getVAMDCstats',dataToSend);
    
    // Evaluate Response
    ajax = eval('(' + data + ')');

    if(ajax!=false) {
      // Get list of nodes
      $("#form_otherDbs").html("<h3 id='results'>VAMDC.database:query</h3>");
      $("#form_otherDbs").append(ajax.htmlcode);

      // Query each node
      $(".vamdcnode").each(function(index,value) {
				 // alert($(this).attr("id"));
			     $("<p class='nodestatistic'>Fetching statistics for this database! </p>").appendTo($(this));
			     nodeurl = $(this).find('.nodeurl').text();
			     var dataToSend2 = new Array();
			     dataToSend2.push({"name" : "inchikey", "value" : inchikey});
			     dataToSend2.push({"name": "nodeurl", "value" : nodeurl});
			     data2 = ajaxControlForm('getNodeStatistic', dataToSend2);
			     ajax2 = eval('(' + data2 + ')');	  
			     if (ajax2!=false) {
			       // $("<p>Fetching statistics for this database! </p>").appendTo($(this));
			       $(this).find('.nodestatistic').html(ajax2.htmlcode);
			     } else {
			       $(this).find('.nodestatistic').html("Error fetching statistics for this database!");
			     }
   
			     //alert(nodeurl);
			     //$("<input type='input' name='speciesIDs' value='"+$(this).find('.nodeurl').text()+"'>").appendTo($(this));
			   });


    } else {
      $("#form_otherDbs").append(ajax.htmlcode);
    }
  }
}

function ajaxGetVAMDCstats2() {
  var dbnames = { 'CDMS':'CDMS', 'HITRAN':'HITRAN', 'BASECOL':'BASECOL' };
  for (dbname in dbnames)
    {
      // query only once: check if element exists via length
      if ($("#"+dbname+"out").length == 0) {
	$("#form_otherDbs").append("<h3>"+dbname+"</h3><div id='"+dbname+"out'>please wait ...</div>");
	ajaxGetVamdcDBstat( dbname );
      }
    }
}


function ajaxGetVamdcDBstat(dbname) {
  $("#"+dbname+"out").html("please wait ...");
  //  $("#form_otherDbs").append("<h3>TEST</h3>");
  var inchikey = $("#inchikey").html();
//  alert (inchikey);
  var dataToSend = new Array();
  var datum = {"name" : "inchikey", "value" : inchikey}; 
  // var dataToSend = {"inchikey": inchikey,"dbname" : dbname}; 
  dataToSend.push(datum);
  var datum = {"name" : "dbname", "value" : dbname}; 
  dataToSend.push(datum);

  data = ajaxControlForm('getVAMDCstats',dataToSend);
  ajax = eval('(' + data + ')');
  //  alert("Done");
  //  alert(ajax.htmlcode);
  // Überprüfen, ob ein JS Objekt da ist.
  if(ajax!=false) {
    $("#"+dbname+"out").html(ajax.htmlcode);
    // $("#form_otherDbs").append(ajax.htmlcode);
  } else {
    $("#form_otherDbs").append(ajax.htmlcode);
  }

}


function startDownload(url) {
  // this function should initiate a file download by 
  // calling the page downloadXSAMS.php in a new window


  // change action in order to post vars to downloadXSAMS.php
  thisform = $("#form_result").attr("action", url );

  //  var url='./downloadXSAMS.php'; 
  win=window.open('','Download');
  thisform.target = 'Download';
  thisform.submit();
  win.close();
  
  // change form action back to index
  thisform = $("#form_result").attr("action", "./index.php" );


}
