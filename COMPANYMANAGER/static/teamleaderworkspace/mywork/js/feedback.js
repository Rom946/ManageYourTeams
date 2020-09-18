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
  $('#locations-select').select2({
    minimumResultsForSearch: -1,
    placeholder: function() {
      $(this).data('placeholder');
    },
    allowClear: true,
    width: '100%',
    tags: false,
    tokenSeparators: [',', ' '],
  });
  $('.select2-search__field').attr('style', 'width:300px!important;')
}

//init select and datatable
$(document).ready( function () {
    $('#recap-table').DataTable({
        "bPaginate": true,
        "pageLength": 5,
        "bLengthChange": true,
        "bFilter": true,
        "bSort": false,
        "bInfo": true,
        "bAutoWidth": false,
        "dom": 'Bfrtip',
  });

  InitSelect2()
});

//set options choice list
function SetLocations(locations, button, modal){
  //reset options
  modal.find('#locations-select').empty()

  //get forloop counter index
  var position = button.data('position')
  //build location field id
  var location_field_id = "#locations-" + position

  //get selected location from DT
  locations_selected_string = $(location_field_id).val()
  console.log(locations_selected_string)
  //split string to get locations in a list
  locations_selected = locations_selected_string.split('-')


  for(i=0;i<locations.length;i++){
    selected=false
    for(k=0;k<locations_selected.length;k++){
      //if location selected in DT
      if(locations_selected[k].trim() == locations[i][1]){
        console.log(locations_selected[k])
        var option = new Option(locations[i][1], locations[i][0], true, true)
        selected = true
        break
      }
    }
    //if location not selected => possible choice
    if (selected == false){
      var option = new Option(locations[i][1], locations[i][0])
    }
    //append the option
    modal.find('#locations-select').append(option)
  }
  
  locations = $('#locations-select').val() 
  modal.find('#editbtn').attr('data-locations', locations)
}

//get locations list from backend
function DisplayLocations(button, modal){
  // Extract info from data-* attributes
  var reference = button.data('reference')
  var job = button.data('job')
  var tech = button.data('tech')
  var qty = button.data('qty')


  response_data = {
   'csrfmiddlewaretoken' : csrftoken,
   'reference' : reference,
   'tech' : tech,
   'job' : job,
   'qty' : qty,
   'action' : 'get locations'
 }

 $.ajax({
  url: '/teamleaderworkspace/Feedback/',
  method: "POST",
  data: response_data,
  type: 'JSON',
  success: function(response) {
      console.log(response)
      if(response['success']){
        //create locations select object
        SetLocations(response['locations'], button, modal)
      }
      //errors
      else{
        // here are the errors which you can append to .error-block
        $('.error-block').html(response['error']);
        console.log(response['error'])
       
      }
  }
 })

}

function UpdateTable(position, qty, locations){
  console.log('Updating table...')
  //build id qty
  var qty_id = '#qty-'+position
  //build id locations
  var locations_id = '#locations-'+position

  console.log($(locations_id)[0])
  //update qty
  $(qty_id).html(qty)

  console.log(locations)
  //update locations
  $(locations_id).html(locations)
  $(locations_id).val(locations)
  
}

function DeleteRow(position){
  $('#'+position).remove()
}
//get qty on change and store value in button
$('#qty-name').on('change', function (event){
  qty = $(this).val()
  modal = $('#EditModal')
  modal.find('#editbtn').attr('data-qty', qty)
  console.log(qty)

})

//get locations on change and store value in btn
$('#locations-select').on('change', function (event){
  locations = $(this).val()
  modal = $('#EditModal')
  modal.find('#editbtn').attr('data-locations', locations)
  console.log(locations)

})

//show the Edit modal
$('#EditModal').on('show.bs.modal', function (event) {


  var button = $(event.relatedTarget) // Button that triggered the modal
  // Extract info from data-* attributes
  var reference = button.data('reference')
  var job = button.data('job')
  var tech = button.data('tech')
  var qty = button.data('qty')
  var position = button.data('position')
 


  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  var modal = $(this)
  modal.find('.modal-title').text('Edit ' + reference)
  modal.find('#reference-name').val(reference)
  modal.find('#job-name').val(job)
  modal.find('#tech-name').val(tech)
  modal.find('#qty-name').val(qty)

   //initiate an AJAX request to get locations (and then do the updating in a callback).
   DisplayLocations(button, modal)


  //set min value for qty
  modal.find('#qty-name').attr('min','1')

  //store infos in button
  modal.find('#editbtn').attr('data-job', job)
  modal.find('#editbtn').attr('data-reference', reference)
  modal.find('#editbtn').attr('data-tech', tech)
  modal.find('#editbtn').attr('data-qty', qty)
  modal.find('#editbtn').attr('data-locations', locations)
  modal.find('#editbtn').attr('data-position', position)
})

//show the Delete modal
$('#DeleteModal').on('show.bs.modal', function (event) {

  var button = $(event.relatedTarget) // Button that triggered the modal
  var reference = button.attr('data-reference')
  var job = button.attr('data-job')
  var tech = button.attr('data-tech')
  var qty = button.attr('data-qty')
  var position = button.attr('data-position')
  // Extract info from data-* attributes

  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  var modal = $(this)
  modal.find('.modal-title').text('Delete ' + reference + ' for ' + tech + ' ?')

  //store infos in button
  modal.find('#deletebtn').attr('data-job', job)
  modal.find('#deletebtn').attr('data-reference', reference)
  modal.find('#deletebtn').attr('data-tech', tech)
  modal.find('#deletebtn').attr('data-qty', qty)
  modal.find('#deletebtn').attr('data-position', position)
  
})

function Edit(event){
 console.log('editing..')
 var button = $('#editbtn') // Button that triggered the modal
 var reference = $('#editbtn').attr('data-reference')
 var tech = $('#editbtn').attr('data-tech')
 var job = $('#editbtn').attr('data-job')
 var qty = $('#editbtn').attr('data-qty')
 var locations = $('#editbtn').attr('data-locations')

 console.log(locations)

 response_data = {
   'csrfmiddlewaretoken' : csrftoken,
   'reference' : reference,
   'tech' : tech,
   'job' : job,
   'qty' : qty,
   'locations': locations,
   'action' : 'edit'
 }

 $.ajax({
  url: '/teamleaderworkspace/Feedback/',
  method: "POST",
  data: response_data,
  type: 'JSON',
  success: function(response) {
      console.log(response)
      if(response['success']){
        //display message edit OK
        $('.success-block').html('Data has been edited.')        
        $('.cancelbtn').click()
        var position = $('#editbtn').attr('data-position')
        locations = response['locations-string']
        UpdateTable(position, qty, locations)
      }
      //errors
      else{
        // here are the errors which you can append to .error-block
        $('.message-block-edit').html(response['error']);    
        $('.message-block-edit').attr('class', 'message-block alert-danger')
        console.log(response['error'])
       
      }
  }
 })

}

function Delete(event){
  console.log('deleting..')
  var button = $('#deletebtn') // Button that triggered the modal
  var reference = $('#deletebtn').attr('data-reference')
  var tech = $('#deletebtn').attr('data-tech')
  var job = $('#deletebtn').attr('data-job')
  var qty = $('#deletebtn').attr('data-qty')

 
  response_data = {
    'csrfmiddlewaretoken' : csrftoken,
    'reference' : reference,
    'tech' : tech,
    'job' : job,
    'qty' : qty,
    'action' : 'delete'
  }
 
  $.ajax({
   url: '/teamleaderworkspace/Feedback/',
   method: "POST",
   data: response_data,
   type: 'JSON',
   success: function(response) {
       console.log(response)
       if(response['success']){
          //display message
          $('.success-block').html(reference + ' removed for ' + tech)
          var position = $('#deletebtn').attr('data-position')
          DeleteRow(position)
          $('.success-block').attr('class', 'success-block alert-success')
          $('.cancelbtn').click()

          
       }
       //errors
       else{
         // here are the errors which you can append to .error-block
         $('.success-block').html(response['error']);
         $('.success-block').attr('class', 'success-block alert-danger')
         console.log(response['error'])
        
       }
   }
  })
 
}

