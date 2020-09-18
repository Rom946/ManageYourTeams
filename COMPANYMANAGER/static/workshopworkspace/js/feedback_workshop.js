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
    $('select').select2({
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
  
 
  
  function DeleteRow(position){
    $('#'+position).remove()
  }

  function AddOptions(select_id, choices){
    for(i=0;i<choices.length;i++){
      opt = new Option(choices[i][1],choices[i][0],choices[i][2],choices[i][3])
      $(select_id).append(opt)
    }
  }

  //display edit form
  function DisplayForm(response){
    
    $('#reference-name').val(response['reference'])
    $('#qty-name').val(response['qty'])
    $('#date-creation-name').val(response['date_creation']) 
    AddOptions('#film-select', response['film_reels'])
    AddOptions('#cutter-select', response['cutter_choices'])
    AddOptions('#packer-select', response['packer_choices'])
    AddOptions('#waste-select', response['waste_choices'])

    console.log(response['film_reels'])

    $('#reference-name').attr('disabled','')
    $('#film-select').attr('disabled','')
    $('#date-creation-name').attr('disabled','')

    button = $('#editbtn')
    button.attr('data-qty', response['qty'])
    button.attr('data-cutter', $('#cutter-select').val())
    button.attr('data-packer', $('#packer-select').val())
  }
  
  //show the Edit modal
  $('#EditModal').on('show.bs.modal', function (event) {
    ResetForm()
    var button = $(event.relatedTarget) // Button that triggered the modal

    // Extract info from data-* attributes
    var package_id = button.data('package')
    var position = button.data('position')

   
    response_data = {
      'csrfmiddlewaretoken' : csrftoken,
      'package_id' : package_id,
      'action' : 'edit'
    }
   
    $.ajax({
     url: '/workshopworkspace/Feedback/',
     method: "POST",
     data: response_data,
     type: 'JSON',
     success: function(response) {
         console.log(response)
         if(response['success']){
           //display message edit OK
           $('.success-block').html(response['result'])
            DisplayForm(response)
            $('#editbtn').attr('data-package', package_id)
            $('#editbtn').attr('data-position', position)
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
   
  })
  
  //show the Delete modal
  $('#DeleteModal').on('show.bs.modal', function (event) {
  
    var button = $(event.relatedTarget) // Button that triggered the modal
    var package_id = button.data('package')
    var position = button.data('position')
    
    // Extract info from data-* attributes
  
    // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
    // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
    var modal = $(this)
    modal.find('.modal-title').text('Delete package ' + package_id + ' ?')
  
    //store infos in button
    modal.find('#deletebtn').attr('data-package', package_id)
    modal.find('#deletebtn').attr('data-position', position)

    
  })

  function DisplayWaste(response){
    $('#edit-waste-qty').removeAttr('hidden')
    $('#edit-waste-category').removeAttr('hidden')
    $('#waste-qty-name').val(response['waste_qty'])
    AddOptions('#waste-category-select', response['waste_category'])

    button = $('#editbtn')
    button.attr('data-waste-qty', response['waste_qty'])
    button.attr('data-waste-category', $('#waste-category-select').val())
  }

  //update and display waste
  $('#waste-select').on('change', function(e){
    var button = $('#editbtn')

    button.attr('data-waste', $(this).val())
    // Extract info from data-* attributes
    var package_id = button.data('package')
    var waste_id = $(this).val()
    console.log(waste_id)
   
   
    response_data = {
      'csrfmiddlewaretoken' : csrftoken,
      'package_id' : package_id,
      'waste_id' : waste_id,
      'action' : 'load waste'
    }
   
    $.ajax({
     url: '/workshopworkspace/Feedback/',
     method: "POST",
     data: response_data,
     type: 'JSON',
     success: function(response) {
         console.log(response)
         if(response['success']){
           //display message edit OK
           $('.success-block').html(response['result'])
            DisplayWaste(response)
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
    

  })
  $('#waste-qty-name').on('change', function(e){
    var button = $('#editbtn')
    button.attr('data-waste-qty', $(this).val())
  })
  $('#waste-category-select').on('change', function(e){
    var button = $('#editbtn')
    button.attr('data-waste-category', $(this).val())
  })
  $('#qty-name').on('change', function(e){
    var button = $('#editbtn')
    button.attr('data-qty', $(this).val())
  })
  $('#cutter-select').on('change', function(e){
    var button = $('#editbtn')
    button.attr('data-cutter', $(this).val())
  })
  $('#packer-select').on('change', function(e){
    var button = $('#editbtn')
    button.attr('data-packer', $(this).val())
  })
  
  

  
  function Edit(event){
   console.log('editing..')
   var button = $('#editbtn') // Button that triggered the modal
   var package_id = $('#editbtn').attr('data-package')
   var qty = $('#qty-name').val()
   var cutter = $('#cutter-select').val()
   var packer = $('#packer-select').val()
   console.log(packer)
   var waste = $('#editbtn').attr('data-waste')
   if(waste == ''){
     waste = false
   }
   var waste_qty = $('#editbtn').attr('data-waste-qty')
   var waste_category = $('#editbtn').attr('data-waste-category')
  
  
   response_data = {
     'csrfmiddlewaretoken' : csrftoken,
     'package_id' : package_id,
     'qty' : qty,
     'cutter' : cutter,
     'packer' : packer,
     'waste' : waste,
     'waste_qty' : waste_qty,
     'waste_category' : waste_category,
     'action' : 'save'
   }
  
   $.ajax({
    url: '/workshopworkspace/Feedback/',
    method: "POST",
    data: response_data,
    type: 'JSON',
    success: function(response) {
        console.log(response)
        if(response['success']){
          //display message edit OK
          $('.success-block').html('Data has been edited.')        
          $('.cancelbtn').click()
          var position = button.attr('data-position')
          code = response['code']
          UpdateTable(code, position)
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
    var package_id = button.attr('data-package')
  
   
    response_data = {
      'csrfmiddlewaretoken' : csrftoken,
      'package_id' : package_id,
      'action' : 'delete'
    }
   
    $.ajax({
     url: '/workshopworkspace/Feedback/',
     method: "POST",
     data: response_data,
     type: 'JSON',
     success: function(response) {
         console.log(response)
         if(response['success']){
            //display message
            $('.success-block').html(response['result'])
            var position = button.attr('data-position')
            DeleteRow(position)
            $('.cancelbtn').click()
  
            
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
  
  function ResetForm(){
    $('#date-creation-name').val('')
    $('#reference-name').val('')
    $('#qty-name').val('')
    $('#film-select').empty()
    $('#cutter-select').empty()
    $('#packer-select').empty()
    $('#waste-select').empty()
    $('#waste-qty-name').val('')
    $('#waste-category-select').empty()

    $('#editbtn').attr('data-waste', '')    
    $('#editbtn').attr('data-waste-qty', '')
    $('#editbtn').attr('data-waste-category', '')
    $('#editbtn').attr('data-qty', '')
    $('#editbtn').attr('data-packer', '')
    $('#editbtn').attr('data-cutter', '')

    $('#edit-waste-category').attr('hidden', '')
    $('#edit-waste-qty').attr('hidden', '')

  }


function UpdateTable(code, position){
  var tr_id = '#'+position
  console.log($(tr_id).find('.code')[0])
  var tr = $(tr_id)
  tr.find('.code')[0].innerHTML = code
}



function FinishFilmReel(e){
  e.preventDefault()

  var reel_ids = $('#film_reel').val()

 
  response_data = {
    'csrfmiddlewaretoken' : csrftoken,
    'reel_ids' : reel_ids,
    'action' : 'finish film reel'
  }
 
  $.ajax({
   url: '/workshopworkspace/Feedback/',
   method: "POST",
   data: response_data,
   type: 'JSON',
   success: function(response) {
       console.log(response)
       if(response['success']){
         //display message edit OK
         $('.success-block').html(response['result'])
         $("#film_reel option:selected").remove();
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
