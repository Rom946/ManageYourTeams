function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }   
  
  function csrfSafeMethod(method) {
    // These HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  
  // This sets up every ajax call with proper headers.
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
  });
  
  //get csrf token
  var csrftoken = getCookie('csrftoken');
  
  
  function InitSelect2(){

        $('#id_replaced_by').select2({
            minimumResultsForSearch: -1,
            placeholder: 'Select an employee',
            allowClear: true,
            width: '100%',
            tags: false,
            tokenSeparators: [',', ' '],
        });
        $('.select2-search__field').attr('style', 'width:300px!important;')
        
  }

  //add the onchange function for replacement and hide replacement options fields
  function initReplacement(){
    $('#id_replacement').attr('onchange', 'displayReplacementOptions(event)')
    //hide replacement options fields 
    $('#div_id_replaced_by').hide()
    $('#div_id_date_replacement').hide()  
    //remove fields as required for form control
    $('#id_replaced_by').removeAttr('required')
    $('#id_date_replacement').removeAttr('required') 

    //check if situation is Against Gibela to show or not the progress field
    let selected_option = $('#id_situation option:selected')
    let situation_type = selected_option.text().toLowerCase()
    if(!situation_type.includes('gibela')){
      $('#div_id_progress').hide()
      $('#id_progress').removeAttr('required')
    }
  }

  
  
  //init select and datatable
  $(document).ready( function () {  
    InitSelect2()
    initReplacement()
  });



  function displayReplacementOptions(e){
    //user ticked the box 'replacement'
    if($(e.target).prop('checked')){
      //display replacement options fields
      $('#div_id_replaced_by').show()
      $('#div_id_date_replacement').show()  
      //set fields as required
      $('#id_replaced_by').attr('required', true)
      $('#id_date_replacement').attr('required', true)  
    }
    //user untick the box 'replacement'
    else{
      $('#div_id_replaced_by').hide()
      $('#div_id_date_replacement').hide() 
      //remove fields as required for form control
      $('#id_replaced_by').removeAttr('required')
      $('#id_date_replacement').removeAttr('required')
    }
  }