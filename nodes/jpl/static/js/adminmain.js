function load_page(page) {
    window.document.forms[0].T_PAGE.value=page; 
    window.document.forms[0].submit();
}

function edit_specie(eId) {
  window.document.forms[0].action="/DjCDMSdev/cdms/species/"+eId+"/"; 
  window.document.forms[0].submit();
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
  if (window.document.forms[0].T_TYPE.value=='xsams')
    {
      window.document.forms["PARAMETER"].action='http://hera.ph1.uni-koeln.de:8080/examples/servlets/servlet/CdmsServlet2';
    }
  else
    {
      window.document.forms["PARAMETER"].action='./';
    }
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
                value=rows[i].id;
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

function selectMolRow(id) {

     parentID=id.parentNode;
     
     if (parentID.className=='molRowSel') {
        parentID.className='molRow';
	//        id.className='molRow';
     } else {
        parentID.className='molRowSel';
	//        id.className='molRowSel';
     }
     filterDatasets(id);

}

function selectOnlyOneRow(id) {
  parentID=id; //.parentNode;

  var rows = document.getElementsByTagName("tr");
  for (var i = 0; i < rows.length; i++) {
    if (rows[i].className=='molRowSel new') {
      rows[i].className='molRow new';
    }
    if (rows[i].className=='molRowSel active') {
      rows[i].className='molRow active';
    }
    if (rows[i].className=='molRowSel archived') {
      rows[i].className='molRow archived';
    }
  }

  if (parentID.className=='molRow archived') {
    parentID.className='molRowSel archived';
  } else if (parentID.className=='molRow active') {
    parentID.className='molRowSel active';
  } else if (parentID.className=='molRow new') {
    parentID.className='molRowSel new';
  }
//alert(id.childNodes[0].id);
  filterDatasets(id.childNodes[0].id);

}

function filterDatasets(id) {
//alert(id);
   var rows = document.getElementsByTagName("tr");
   for (var i = 0; i < rows.length; i++) {
//	   alert(id.id);
	   if (rows[i].className == id) {
		 rows[i].style.display = "";
	   } else if (rows[i].className.indexOf("eTag")!=-1) {
		 rows[i].style.display = "none";		 
	   }
   }
}

function clearDatasets() {
   var rows = document.getElementsByTagName("tr"); 
   for (var i = 0; i < rows.length; i++) { 
     if (rows[i].className.indexOf("eTag")!=-1) {
         rows[i].style.display = "none";
     }
   }
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

function disableEnterKey(e)
{
     var key;     
     if(window.event)
          key = window.event.keyCode; //IE
     else
          key = e.which; //firefox     

     return (key != 13);
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
   for (var i = 0; i < rows.length; i++) {
         if (rows[i].className.indexOf("molRow")!=-1) {
//            alert(rows[i].className);
//            rows[i].style.visibility = "collapse";
            var childs = rows[i].childNodes;

            val0=childs[0].firstChild.nodeValue;
            val1=childs[1].firstChild.nodeValue;
            val2=childs[2].firstChild.nodeValue;
            val3=childs[3].firstChild.nodeValue;

	    if ((val1)) { //alert (val0);}
//            if (i<5) {alert (val0); alert(val0.search(RegExp(eTagFilterValue,"g"))); }//childs[1].firstChild.nodeValue);}

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


function switchHideView(id) {
  var el = document.getElementById(id);
  if (el.style.display=="none") {
    el.style.display="";
  } else {
    el.style.display="none";
  }
} 

function viewSectionEntry(id) {

  var el = document.getElementById("sectionParameterForm");
  if (el) {el.style.display="none";}
  el = document.getElementById("sectionDatasetForm");
  if (el) {el.style.display="none";}
  el = document.getElementById("sectionAdmin");
  if (el) {el.style.display="none"; }
  el = document.getElementById("sectionRulesForm");
  if(el) {el.style.display="none";}
  el = document.getElementById("sectionStructureForm");
  if(el) {el.style.display="none";}
  el = document.getElementById("sectionComment");
  if(el) {el.style.display="none";}
  el = document.getElementById("sectionFilesForm");
  if(el) {el.style.display="none";}
  el = document.getElementById("sectionFileUploadForm");
  if(el) {el.style.display="none";}
  el = document.getElementById("sectionReferencesForm");
  if(el) {el.style.display="none";}
  el = document.getElementById("sectionPF");
  if(el) {el.style.display="none";}
  el = document.getElementById(id);
  if (el) {el.style.display="";}



}


function addAtomArrayRow(id) {

  //    alert(trid);
  //    trid++;
  //    alert(trid);
    
  var tbody = document.getElementById(id).getElementsByTagName("TBODY")[0];
  var row = document.createElement("TR");
  //tb.appendChild(newTr);
  
  //tr bekommt id
  //    tbody.appendChild(row).setAttribute("id", trid, 0);
    
  var td1 = document.createElement("TD");
  var input1 = document.createElement("INPUT");
  input1.type="text";
  input1.name="strucAA[AA_AtomId][]";
  input1.value="";
  var inputStyle = document.createAttribute("style");
  inputStyle.nodeValue = "width:100%;margin-right:5px;";
  input1.setAttributeNode(inputStyle);

  input1.size==1;
  td1.appendChild(input1);
  
  var td2 = document.createElement("TD");
  var input2 = document.createElement("INPUT");
  input2.type="text";
  input2.name="strucAA[AA_ElementType][]";
  input2.style="width:100%;margin-right:5px;";
  input2.size==1;

  var inputStyle2 = document.createAttribute("style");
  inputStyle2.nodeValue = "width:100%;margin-right:5px;";
  input2.setAttributeNode(inputStyle2);
  td2.appendChild(input2);
  
  var td3 = document.createElement("TD");
  var input3 = document.createElement("INPUT");
  input3.type="text";
  input3.name="strucAA[AA_IsotopeNumber][]";
  var inputStyle3 = document.createAttribute("style");
  inputStyle3.nodeValue = "width:100%;margin-right:5px;";
  input3.setAttributeNode(inputStyle3);
  input3.size==1;
  td3.appendChild(input3);
  
  var td4 = document.createElement("TD");
  var input4 = document.createElement("INPUT");
  input4.type="text";
  input4.name="strucAA[AA_FormalCharge][]";

  var inputStyle4 = document.createAttribute("style");
  inputStyle4.nodeValue = "width:100%;margin-right:5px;";
  input4.setAttributeNode(inputStyle4);
  input4.size==1;
  td4.appendChild(input4);

  
  //zu loeschende trid in diesem fall die erstelle zeile tr
  //    trid = "tr#zeile"+trid;
  //    alert(trid);
    
  //    td3.innerHTML = "<a href=\"#\" onclick=\"loeschen('"+trid+"')\">loeschen</a>";
    
  row.appendChild(td1);
  row.appendChild(td2);
  row.appendChild(td3);
  row.appendChild(td4);
  tbody.appendChild(row);
  
}

function addInputElement(name, type, style) {

  var input = document.createElement("INPUT");
  input.type=type;
  input.name=name;
  input.value="";
  var inputStyle = document.createAttribute("style");
  inputStyle.nodeValue = style;
  input.setAttributeNode(inputStyle);
  input.size==1;
  return input;
}

function addSelect() {
  divtag = document.createElement("div");
  myselect = document.createElement("select");
  theOption=document.createElement("OPTION");
  theText=document.createTextNode("JavaScript Tutorial II");
  theOption.appendChild(theText);
  
  //this option has a value, an URL, so we set the value
  theOption.setAttribute("value","index.html");
  myselect.appendChild(theOption);
  divtag.appendChild(myselect);

  return divtag;
}

function addBondArrayRow(id) {

  //    alert(trid);
  //    trid++;
  //    alert(trid);
    
  var tbody = document.getElementById(id).getElementsByTagName("TBODY")[0];

  $('#firstRow').clone().appendTo('tbody');

}

function copyRow(id) {
  //    alert(trid);
  //    trid++;
  //    alert(trid);
    
  var tbody = document.getElementById(id).getElementsByTagName("TBODY")[0];

  $('#firstRow').clone().appendTo('tbody');

}

function copyRowById(rowId,tbodyId) {
  
  $('#'+rowId).clone().appendTo('#'+tbodyId);

}

function ajaxTestLoad() {

  $.ajax({
      // Welche URL soll aufgerufen werden?
    url: './ajax.php',
	// Wird ausgeführt, wenn die Datei erfolgreich requestet wurde
	success: function(data) {
	/** 
	 * PHP liefert ein JSON Objekt zurück, welches wir im
	 * JavaScript Code ausführen müssen, um ein Objekt zu erhalten.
	 * Danach können wir mittels ajax.message und ajax.status auf unser
	 * zuvor erstelltes PHP Array zu greifen. Wenn ein neuer Index im PHP Array
	 * hinzugefügt wird, können wir mittels ajax.neuerIndex auch im JS darauf
	 * zu greifen.
	 **/
	
	ajax = eval('(' + data + ')');
	
	// Überprüfen, ob ein JS Objekt da ist.
	if(ajax!=false) {
	  
	  // Die von PHP generierte Meldung dem Benutzer darstellen
	  $("#message").html( ajax.message );
	  alert(ajax.message);
	  
	}
      }
    });
}

function ajaxImportCatFile() {
  $('#function').val('createDataset');

  // create array to post
  var filId = $("select#FIL_ID").val();  
  var eId = $("input#E_ID").val();  
   //   var eId = 5;
//   var name = $("select#dat[DAT_Name]").val();  

//   var dataString = 'DAT[DAT_FIL_ID]='+filId;
   //  var dataToSend = {'DAT[DAT_FIL_ID]' : filId, 
  //		    'DAT[DAT_E_ID]' : eId} ;
  
  var dataToSend =  $("form").serializeArray();
  data = ajaxSaveData();

  ajax = eval('(' + data + ')');
	
  // Überprüfen, ob ein JS Objekt da ist.
  if(ajax!=false) {
    
    // Die von PHP generierte Meldung dem Benutzer darstellen
    $("#message").html( ajax.message );
    alert(ajax.message);
    $("#cat").hide();
// 	  $("#dataset").show();
// 	  $("[name='dat[DAT_Name]']").val(ajax.DAT_Name);
// 	  $("[name='dat[DAT_Type]']").val(ajax.DAT_Type);
// 	  $("[name='dat[DAT_HFS]']").val(ajax.DAT_HFS);
// 	  $("[name='dat[DAT_QN_Tag]']").val(ajax.DAT_QN_Tag);
// 	  $("[name='dat[DAT_Comment]']").val(ajax.DAT_Comment);
// 	  $("[name='dat[DAT_Archive]']").val(ajax.DAT_Archive);
// 	  $("[name='dat[DAT_Createdate]']").val(ajax.DAT_Createdate);

// 	  $("input[type='submit']").show();

    $("#htmlContainer").html(ajax.htmlcode);
  }
}

function ajaxImportRefFile() {
  $('#function').val('importReferences');
  alert("Import");
  // create array to post
  var filId = $("select#FIL_ID").val();  
  var eId = $("input#E_ID").val();  
   //   var eId = 5;
//   var name = $("select#dat[DAT_Name]").val();  

//   var dataString = 'DAT[DAT_FIL_ID]='+filId;
   //  var dataToSend = {'DAT[DAT_FIL_ID]' : filId, 
  //		    'DAT[DAT_E_ID]' : eId} ;
  
  var dataToSend =  $("form").serializeArray();
  data = ajaxSaveData();

  ajax = eval('(' + data + ')');
	
  // Überprüfen, ob ein JS Objekt da ist.
  if(ajax!=false) {
    
    // Die von PHP generierte Meldung dem Benutzer darstellen
    $("#message").html( ajax.message );
    alert(ajax.message);
    $("#cat").hide();

    $("#htmlContainer").html(ajax.htmlcode);
  }
  alert("Import done");

}



function ajaxSaveDataset() {
  // create array to post
  //   var filId = $("select#FIL_ID").val();  
  //   var eId = $("input#E_ID").val();  
  
  //   var dataToSend =  $("form").serializeArray();

  // Save Entry first
  $('#function').val('saveDataset');
  data = ajaxSaveData();

  var ajax = eval('(' + data + ')');
  if(ajax!=false) {
	alert(ajax.message);
    if (ajax.saved==true) { 
      // dataset was saved so display further import forms
       
      // show formula with files to import
      $('#function').val('showFiles');
      data = ajaxControlForm();
      ajax = eval('(' + data + ')');
      
      // Überprüfen, ob ein JS Objekt da ist.
      if(ajax!=false) {
	
	// Die von PHP generierte Meldung dem Benutzer darstellen
	// $("#message").html( ajax.message );
	alert(ajax.message);
	//	  $("#cat").hide();
	//	  $("#dataset").show();
	
	$("#htmlContainer").html(ajax.htmlcode);
	
      }
    } else {
      alert(ajax.message);
      // Do not go to next page
    }
  } else {
    alert("An error occured while saving");
  }
}


function changeCaseLabels(el) {
  var newcase = el.value;
  var qnClass = el.className;
  var dataToSend = {'function' : 'ReadCaseLabels',
		    'case': newcase };


  // call ajax
  $.ajax({
      // Welche URL soll aufgerufen werden?
    url: './ajaxDictionary.php',
	data: dataToSend,
	type: "POST",
	// Wird ausgeführt, wenn die Datei erfolgreich requestet wurde
	
	success: function(data) {
	/** 
	 * PHP liefert ein JSON Objekt zurück, welches wir im
	 * JavaScript Code ausführen müssen, um ein Objekt zu erhalten.
	 * Danach können wir mittels ajax.message und ajax.status auf unser
	 * zuvor erstelltes PHP Array zu greifen. Wenn ein neuer Index im PHP Array
	 * hinzugefügt wird, können wir mittels ajax.neuerIndex auch im JS darauf
	 * zu greifen.
	 **/
	
	ajax = eval('(' + data + ')');
	
	// Überprüfen, ob ein JS Objekt da ist.
	if(ajax!=false) {
	  
          // Store the selected values first
	  var selectedVals = [];
	  var i=0;
	  
	  jQuery("."+qnClass+"[name='sqn[SQN_Label][]'] option:selected").each(function(){
	    selectedVals[i] = $(this).parent().val();
	    i=i+1;
    	  });

          // Then remove all options 
          jQuery("."+qnClass+"[name='sqn[SQN_Label][]']").each(function() {
	     $(this).find("option").remove();
          });

          // Attach option nothing selected which should appear if
          // the stored option does not exist in the new set of labels
	  jQuery("."+qnClass+"[name='sqn[SQN_Label][]']").append(
	      jQuery('<option></option').val("").html("")
	  );

          // Attatch new options
	  jQuery.each(ajax.labels, function(val, text) {

	      jQuery("."+qnClass+"[name='sqn[SQN_Label][]']").append(
	      jQuery('<option></option').val(text).html(text)
	    );})

          // Select the the stored values again
	  i=0;
	  jQuery("."+qnClass+"[name='sqn[SQN_Label][]']").each(function() {
              $(this).find("option[value='"+selectedVals[i]+"']").attr('selected', 'selected');
	      i=i+1;
	     });

	}
      }
    });
  

}


function saveFilterRules(qnTag) {

  // create array to post
  //  var dataToSend =  $("form").serializeArray();
  //  $('#function').val('saveFilterRules');
  //  var dataToSend =  $("#filterRulesTable"+qnTag).serializeArray();
  var dataToSend = new Array(); // $("form").serializeArray();
  //  alert(dataToSend);
  var datum = {"name" : "function", "value" : "saveFilterRules"}; 
  dataToSend.push(datum);
  var sqncase = $(".qnClass"+qnTag+"[name='sqn[SQN_Case][]']").val();
  datum = {"name" : "sqncase", "value": sqncase};
  dataToSend.push(datum);
  jQuery("#filterRulesTbody"+qnTag+" :input").each(function(index){
         datum = {"name" : this.name, "value" : this.value}; 
         dataToSend.push(datum);
	 // name = this.name;
	 //	 alert (name);
         i=i+1;
  });

  // call ajax
  $.ajax({

    url: './ajaxSaveData.php',
	data: dataToSend,
	type: "POST",
	// Wird ausgeführt, wenn die Datei erfolgreich requestet wurde
	
	success: function(data) {
	/** 
	 * PHP liefert ein JSON Objekt zurück, welches wir im
	 * JavaScript Code ausführen müssen, um ein Objekt zu erhalten.
	 * Danach können wir mittels ajax.message und ajax.status auf unser
	 * zuvor erstelltes PHP Array zu greifen. Wenn ein neuer Index im PHP Array
	 * hinzugefügt wird, können wir mittels ajax.neuerIndex auch im JS darauf
	 * zu greifen.
	 **/
	
	ajax = eval('(' + data + ')');
	
	// Überprüfen, ob ein JS Objekt da ist.
	if(ajax!=false) {
	  
	  // Die von PHP generierte Meldung dem Benutzer darstellen
	  //	  $("#message").html( ajax.message );
	 
	  if (ajax.saved == true) {
	    $(".fs"+qnTag+" *").remove();
	    $(".fs"+qnTag).eq(1).remove();
	    $(".fs"+qnTag).html(ajax.htmlcode);
	    if (ajax.message) {
	      alert(ajax.message);
	    }

	    if(!$('select').length) {
	      alert("Everything is saved");
	      var continueButton = "<div class='type-button'><input type='submit' value='Continue' name='Step10' onclick='$(\"#step\").val(10);'></div>";

	      $("form").prepend(continueButton);
	    } else {
	      alert("Please visit the other Tabs!");
	    }

	      
	  } else {
	    alert(ajax.message);
	  }
	  //	  alert(ajax.htmlcode);
	  
	  
	}
      }
    });
  
}

function insertEntry() {
  // Save Entry first
  $('#function').val('saveEntry');
  data = ajaxSaveData();
  //  alert(data);
  var ajax = eval('(' + data + ')');
  if(ajax!=false) {
    if (ajax.saved==true) { 
      // alert(ajax.eId);
      alert(ajax.saved);
      $("input[name='file[FIL_E_ID]']").val(ajax.eId);
      $("input[name='entry[E_ID]']").val(ajax.eId);
      //alert(ajax.message);
      alert($("input[name='file[FIL_E_ID]']").val());
      // Now, the doc-file can be saved is one
      // has been uploaded
      
      var docfile = $("input[name='docfile']").val();
      if (docfile) {
	alert(docfile);
	$('#function').val('saveDocFile');
	data = ajaxSaveData();
	ajax = eval('(' + data + ')');
	if(ajax!=false) {
	  alert(ajax.message);
	  if (ajax.saved == true) {
	    $("input[name='file[FIL_ID]']").val(ajax.fileId);	
	    alert($("input[name='file[FIL_ID]']").val());
	  } else {
	    alert("No docfile uploaded");
	  }
	}
      } else {
	alert("No docfile uploaded");
      }

      // go to next page
      $('#step').val(4);
      $('form').submit();
    } else {
      alert(ajax.message);
      // Do not go to next page
      $('#step').val(3);
    } 
  } else {
    alert("An error occured while saving");
  }
  
}

function insertPara() {
  // Save Entry first
  $('#function').val('savePara');
  data = ajaxSaveData();
  //  alert(data);
  var ajax = eval('(' + data + ')');
  if(ajax!=false) {
    if (ajax.saved==true) { 
      // alert(ajax.eId);
      alert(ajax.saved);
      alert(ajax.message);

      // go to next page
      $('#step').val(5);
      $('form').submit();
    } else {
      alert(ajax.message);
      // Do not go to next page
      $('#step').val(4);
    } 
  } else {
    alert("An error occured while saving");
  }
  
}

function insertAtoms() {
  // Save Entry first
  $('#function').val('saveAtoms');
  data = ajaxSaveData();
  //  alert(data);
  var ajax = eval('(' + data + ')');
  if(ajax!=false) {
    if (ajax.saved==true) { 
      // alert(ajax.eId);
      alert(ajax.saved);

      // go to next page
      $('#step').val(6);
      $('form').submit();
    } else {
      alert(ajax.message);
      // Do not go to next page
      $('#step').val(5);
    } 
  } else {
    alert("An error occured while saving");
  }
  
}

function insertBonds() {
  // Save Entry first
  $('#function').val('saveBonds');
  data = ajaxSaveData();
  //  alert(data);
  var ajax = eval('(' + data + ')');
  if(ajax!=false) {
    if (ajax.saved==true) { 
      // alert(ajax.eId);
      alert(ajax.saved);

      // go to next page
      $('#step').val(7);
      $('form').submit();
    } else {
      alert(ajax.message);
      // Do not go to next page
      $('#step').val(6);
    } 
  } else {
    alert("An error occured while saving");
  }
  
}

function uploadFile() {

  eId = $("input[name='entry[E_ID]']").val();
  $("input[name='file[FIL_E_ID]']").val(eId);

  $('#step').val(7);
  var upfile = $("#FILE").val();
  if (upfile) {
    $("FORM").submit();
  } else {
    alert("You have to select a file first!");
  }

//   // set some control-field values (for post)
//   $('#function').val('uploadFile');
//   eId = $("input[name='entry[E_ID]']").val();
//   $("input[name='file[FIL_E_ID]']").val(eId);


//   // Now, the file can be saved is one
//   // has been uploaded
  
//   var upfile = $("#FILE").val();
//   if (upfile) {

//     data = ajaxSaveData();
//     ajax = eval('(' + data + ')');
//     if(ajax!=false) {
//       // print returned code
//       // should be list of uploaded files
//       $("#htmlContainer").html(ajax.htmlcode);
//       alert(ajax.message);
//       if (ajax.saved != true) {
// 	//	$("#htmlContainer").html(ajax.htmlcode);
// 	//      } else {
// 	alert("No file uploaded");
//       }
//     }
//   } else {
//     alert("No file uploaded");
//   }
  
}


function ajaxSaveData() {

  // create array to post
  //  var dataToSend =  $("form").serializeArray();
  var dataToSend =  $("form").serializeArray();
   //  var fields =  $("form").serializeArray();
  //  jQuery.each(fields, function(i, field){
  //		dataToSend = dataToSend + "{" + field.name + ": "+field.value + "}";
  //	      });

  // call ajax
  return  $.ajax({
      // Welche URL soll aufgerufen werden?
    url: './ajaxSaveData.php',
	data: dataToSend,
	type: "POST",
	// Wird ausgeführt, wenn die Datei erfolgreich requestet wurde
	async: false,
	success: function(data) {
	/** 
	 * PHP liefert ein JSON Objekt zurück, welches wir im
	 * JavaScript Code ausführen müssen, um ein Objekt zu erhalten.
	 * Danach können wir mittels ajax.message und ajax.status auf unser
	 * zuvor erstelltes PHP Array zu greifen. Wenn ein neuer Index im PHP Array
	 * hinzugefügt wird, können wir mittels ajax.neuerIndex auch im JS darauf
	 * zu greifen.
	 **/
	
	ajax = eval('(' + data + ')');
	// Überprüfen, ob ein JS Objekt da ist.
	if(ajax!=false) {
	  // Die von PHP generierte Meldung dem Benutzer darstellen
	  $("#message").html( ajax.message );
	  //alert(ajax.message);
	  //alert(ajax.htmlcode);
	  
	  //	  $('form').submit();
	}
      }
    }).responseText;
  
}


function ajaxControlForm() {

  var dataToSend =  $("form").serializeArray();

  // call ajax
  return  $.ajax({

    url: './ajaxControlForm.php',
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
