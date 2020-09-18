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
        
        $('#id_default_type').select2({
            minimumResultsForSearch: -1,
            placeholder: 'Select default(s)',
            allowClear: true,
            width: '100%',
            tags: false,
            tokenSeparators: [',', ' '],
        });
        $('.select2-search__field').attr('style', 'width:300px!important;')
  }

  //add the onchange function for replacement and hide replacement options fields
  //add the onchange function for situation and hide situation options fields
  function initFields(){
    $('#id_replacement').attr('onchange', 'displayReplacementOptions(event)')
    $('#id_situation').attr('onchange', 'displaySituationOptions(event)')
    //hide replacement options fields 
    $('#div_id_replaced_by').hide()
    $('#div_id_date_replacement').hide()  
    $('#div_id_progress').hide()  
    $('#div_id_ncr_number').hide()  
    $('#div_id_default_type').hide()  
    $('#div_id_description').hide()  
    $('#div_id_train').hide()  
    $('#div_id_car').hide()  
    $('#div_id_part').hide()  
    $('#div_id_location').hide()  
    $('#div_id_reference_to_replace').hide()  
    $('#div_id_replacement').hide()  
    //set situation as required
    $('#id_situation').attr('required', true)
    //remove fields as required for form control
    $('#id_replaced_by').removeAttr('required')
    $('#id_date_replacement').removeAttr('required') 
    $('#id_progress').removeAttr('required') 
    $('#id_ncr_number').removeAttr('required') 
    $('#id_default_type').removeAttr('required') 
  }

  
  
  //init select and datatable
  $(document).ready( function () {  
    InitSelect2()
    initFields()
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


  function displaySituationOptions(e){
    //user unselected situation 
    if($(e.target).val() == ''){
      $('#div_id_replaced_by').hide()
      $('#div_id_date_replacement').hide()  
      $('#div_id_progress').hide()  
      $('#div_id_ncr_number').hide()  
      $('#div_id_default_type').hide()  
      $('#div_id_description').hide()  
      $('#div_id_train').hide()  
      $('#div_id_car').hide()  
      $('#div_id_part').hide()  
      $('#div_id_location').hide()  
      $('#div_id_reference_to_replace').hide()  
      $('#div_id_replacement').hide()
    }
    //user selected a situation
    else{  
      $('#div_id_description').show()  
      $('#div_id_train').show()  
      $('#div_id_car').show()  
      $('#div_id_part').show()  
      $('#div_id_location').show()  
      $('#div_id_reference_to_replace').show()  
      $('#div_id_replacement').show()
      
      //get text value
      let selected_option = $('#id_situation option:selected')
      let situation_type = selected_option.text().toLowerCase()
      //user selected situation NCR against Gibela
      if(situation_type.includes('gibela')){
        //display NCR against gibela options fields
        $('#div_id_ncr_number').show()
        $('#div_id_default_type').hide()
        $('#div_id_progress').show()
        //set fields as required
        $('#id_ncr_number').attr('required', true)
        $('#id_default_type').removeAttr('required')
        $('#id_progress').attr('required')
      }
      //user selected other situations
      else{
        $('#div_id_ncr_number').hide()
        $('#div_id_default_type').show()
        $('#div_id_progress').hide()
        //remove fields as required for form control
        $('#id_ncr_number').removeAttr('required')
        $('#id_default_type').attr('required', true)
        $('#id_progress').removeAttr('required', true)
      }
    }
  }