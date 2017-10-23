function setDivVisibility(aItems, show) {
	aItems.forEach(function(item, index, array) {
		div = $('[for="'+item+'"]').parent();
		if (show) { div.show()
		} else div.hide();
	});
};

function setVisibility() {
  var allFields = ["field-title", "field-notes", "field-md_sharing_level", "field-md_state", "field-publisher_name", "field-publisher_uri", "field-maintainer_email", "field-maintainer", "field-md_gdpr", "field-md_primary_source", "field-md_ticket_private", "field-md_ticket_public", "field-frequency", "field-spatial_uri", "field-ruian_type", "field-ruian_code", "field-theme", "field-schema", "field-tags", "field-temporal_start", "field-temporal_end", "field-md_harvester", "field-md_harvested_url", "field-md_delivery", "field-resources", "field-url", "field-format", "field-license_link", "field-name", "field-describedBy", "field-describedByType", "field-md_apps", "field-md_apps_title", "field-md_apps_url", "field-md_apps_email", "field-md_apps_notes", "field-license", "field-organizations", "field-private", "field-version", "field-author", "field-author-email", "field-description"]
	var aExpert = ["field-md_state", "field-publisher_uri", "field-md_gdpr", "field-md_primary_source", "field-spatial_uri", "field-ruian_type", "field-ruian_code", "field-theme", "field-schema", "field-tags", "field-md_harvester", "field-md_harvested_url", "field-md_delivery", "field-license_link", "field-describedBy", "field-describedByType", "field-md_apps", "field-md_apps_title", "field-md_apps_url", "field-md_apps_email", "field-md_apps_notes", "field-license", "field-organizations", "field-version", "field-author", "field-author-email", "field-url", "field-format"];
	var toHide = ["field-url"];
	var toShow = [];
	var aChoices = {
		internal: ["field-title", "field-notes", "field-md_sharing_level", "field-md_state", "field-maintainer_email", "field-maintainer", "field-md_gdpr", "field-md_primary_source", "field-md_ticket_private", "field-temporal_start", "field-temporal_end", "field-organizations", "field-private", "field-author", "field-author-email"],
		shared: ["field-title", "field-notes", "field-md_sharing_level", "field-md_state", "field-maintainer_email", "field-maintainer", "field-md_gdpr", "field-md_primary_source", "field-md_ticket_private", "field-frequency", "field-spatial_uri", "field-ruian_type", "field-ruian_code", "field-theme", "field-schema", "field-tags", "field-resources", "field-url", "field-format", "field-license_link", "field-name", "field-describedBy", "field-describedByType", "field-organizations", "field-private", "field-version", "field-author", "field-author-email", "field-description"],
		partially_open: allFields,
		open: allFields
		};
	
	var level = $("#field-md_sharing_level").val();
	if (!level) {level = "open"};
	var aPattern = aChoices[level];
	
	allFields.forEach(function(item, index, array) {
		if (aPattern.includes(item)) { //je v sadě
			if (aExpert.includes(item)) { //je v expertní sadě
				if ( $("#field-md_expert_display").is(':checked') ) { //je expert
					toShow.push(item);
				} else toHide.push(item);
			} else toShow.push(item);
		} else toHide.push(item);
	});
	
	setDivVisibility(toShow, true);
	setDivVisibility(toHide, false);

  var div = $('[data-module="custom-fields"]'); //custom fields je třeba řešit zvlášť
  if ( $("#field-md_expert_display").is(':checked') ) div.show();
    else div.hide();

};

function setDefaultValues() {
  if (!$("#field-md_license").val()) {
    $('#field-license').val('cc-by').change(); 
    $('#field-organizations').val('f2a0ae16-dd57-411a-bbe4-b8f4f285f1d8').change(); 
  };  
};

function hidePrivateField() {
  var str = $("#field-md_roles").val();
  if (!~str.indexOf("admin")) {
    $("#field-private").parent().parent().addClass("select2-hidden-accessible");
  };
};

$("#field-md_expert_display").change(function() {  //změna zaškrtnutí "expert"
  if( $(this).is(':checked') ) {
		localStorage['expert_display'] = "yes";
	} else localStorage['expert_display'] = "no";

	setVisibility();
});

$('select#field-md_sharing_level').change(function() {  //změna stupně sdílení
	setVisibility();
});

$(document).ready(function() {  //načtení dokumentu
	if (localStorage['expert_display'] == "yes") {
		$('#field-md_expert_display').prop("checked", true);
	}
	setVisibility();
        hidePrivateField();
        setDefaultValues();
        setDatePicker();
});


/*
ckan.module('jquery_vis', function ($) {
  return {
    initialize: function () {
      //alert("ahoj");
    opt = "Xdef";
      //$('select#st option:selected').val();
    abcinput = $("#field-publisher_name");
    definput = $("#field-publisher_uri");
    //console.log(opt);
    if ( opt == "abc" ) {
      abcinput.show()
      definput.hide()
    } else if ( opt == "def" ) {
      abcinput.hide()
      definput.show()
    };
    }
  }
});
*/
