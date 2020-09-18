type="text/javascript";

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
    var selects = document.querySelectorAll('select')
    console.log('************SELECTS INIT**********')
    console.log(selects)

    $('#id_cut').attr('data-placeholder', 'Click here to select an employee..')
    $('#id_packer').attr('data-placeholder', 'Click here to select an employee..')
    $('#id_reference').attr('data-placeholder', 'Click here to select a reference..')
    $('#id_waste_category').attr('data-placeholder', 'Click here to select a category..')
    $('#id_film_reel').attr('data-placeholder', 'Click here to select film reel number(s)..')
    $('#id_film_reel').attr('multiple', '')
    $('#as').attr('data-placeholder', 'Click here to select a position..')
    $('#film').attr('data-placeholder', 'Click here to select a film..')
    

    //init select2 for reference selects
    for(k=0;k<selects.length;k++){
        //create emptyoption
        let opt = document.createElement('option')
        opt.setAttribute('disabled', "")
        opt.setAttribute('value', 0)
        //console.log($(select)[0])
        opt = $(selects[k])[0].insertBefore(opt, $(selects[k])[0].firstChild)

        $(selects[k]).select2({
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
    
    $('#film').val('').trigger('change')
    $('#id_reference').val('').trigger('change')
    $('#id_film_reel').val('').trigger('change')
    $('#as').val('').trigger('change')
}





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

    $('#div_id_waste_category').attr('hidden','')
    $('#id_waste_category').removeAttr('required')
    $('#div_id_involved').attr('hidden','')
    $('#id_involved').removeAttr('required')

    InitSelect2()

    $(document).on('show.bs.modal', '.modal', function (event) {
        console.log('Opening Delete modal')
        var button = $(event.relatedTarget) // Button that triggered the modal
        console.log(button) 
        var package_id = button.data('package')
        var position = button.data('position')
        // Extract info from data-* attributes
    
        // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
        // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
        var modal = $(this)
        modal.find('.modal-title').text('Delete package ' + package_id + '?')
    
        //store infos in button
        modal.find('#deletebtn').attr('data-package', package_id)
        modal.find('#deletebtn').attr('data-position', position)
    
    })
});

$('#id_waste_qty').on('change', function(e){
    if($(this).val()>0){
        $('#div_id_waste_category').removeAttr('hidden')
        $('#id_waste_category').attr('required','')
        $('#div_id_involved').removeAttr('hidden')
        $('#id_involved').attr('required','')
    }
    else{
        $('#div_id_waste_category').attr('hidden','')
        $('#id_waste_category').removeAttr('required')
        $('#div_id_involved').attr('hidden','')
        $('#id_involved').removeAttr('required')
    }
})


function AddToOptions(response){
    console.log('******Append to options******')
    console.log(response['position'])
    if(response['position']=='0')
    {
        select = $('#id_cut')
    }
    else if(response['position']=='1')
    {
        select = $('#id_packer')
    }
    tech_tuple = response['tech']
    id = tech_tuple[0]
    name = tech_tuple[1]
    console.log(id)
    console.log(name)
    var opt = new Option(name, id, true, true)
    select.append(opt)
}

function AddNewTech(e){
    e.preventDefault()
    var tech = $('#add').val()
    var as = $('#as').val()

    response_data = {
        'tech' : tech,
        'as' : as,
        'action' : 'add',
        'csrf_token' : csrftoken
    }

    $.ajax({
        url: '/workshopworkspace/Mywork/',
        method: "POST",
        data: response_data,
        type: 'JSON',
        success: function(response) {
            console.log(response)
            if(response['success']){
                //create new option select team object
                $('.success-block').html(response['result']);
                $('.error-block').empty()
                //AppendToTeam(response['tech'])
                $('#add').val('')
                AddToOptions(response)
            }
            //errors
            else{
              // here are the errors which you can append to .error-block
              $('.error-block').html(response['result']);
              $('.success-block').empty()
              console.log(response['result'])
             
            }
        }
    })
}

function SaveData(e){
    e.preventDefault()
    var date_creation = $('#id_date_creation').val()
    console.log(date_creation)
    var cutter = $('#id_cut').val()
    var packer = $('#id_packer').val()
    var references = $('#id_reference').val()
    var qty = $('#id_qty').val()
    var waste_qty = $('#id_waste_qty').val()
    var film_reel_nbs = $('#id_film_reel').val()
    if(waste_qty == '0' || waste_qty == ''){
        waste_qty = 0
        var waste_category = '-'
        var involved = '-'
    }else{
        var waste_category = $('#id_waste_category').val()
        var involved = $('#id_involved').val()
    }

    response_data = {
        'date_creation' : date_creation,
        'cutter' : cutter,
        'packer' : packer,
        'references' : references,
        'qty' : qty,
        'waste_qty' : waste_qty,
        'waste_category' : waste_category,
        'involved': involved,
        'film_reel_nbs' : film_reel_nbs,
        'action' : 'save',
        'csrf_token' : csrftoken
    }

    $.ajax({
        url: '/workshopworkspace/Mywork/',
        method: "POST",
        data: response_data,
        type: 'JSON',
        success: function(response) {
            console.log(response)
            if(response['success']){
                //create new option select team object
                $('.success-block').html(response['result']);
                $('.error-block').empty()
                //reset form
                ResetForm()
                //update table
                AddToDoneTodaySection(response['package_id'], response['date_creation'], response['film_name'], qty, response['cutter'], response['packer'], response['reference'], response['waste_qty'], response['waste_category'], response['involved'])
            }
            //errors
            else{
              // here are the errors which you can append to .error-block
              $('.error-block').html(response['result']);
              $('.success-block').empty()
              console.log(response['result'])
             
            }
        }
    })
}

function ResetForm(){
    $('#id_date_creation').val('').trigger('change')
    $('#id_cut').val('').trigger('change')
    $('#id_packer').val('').trigger('change')
    $('#id_reference').val('').trigger('change')
    $('#id_qty').val('').trigger('change')
    $('#id_film_reel').val('').trigger('change')
    $('#id_waste_qty').val(0).trigger('change')
    $('#id_waste_category').val('').trigger('change')

}



function DeleteRow(position){
    $('#'+position).remove()
}

function Delete(e){
    var button = $('#deletebtn') // Button that triggered the modal
    var package_id = button.attr('data-package')
    console.log('deleting package ' + package_id +'..')
    
   
    response_data = {
      'csrfmiddlewaretoken' : csrftoken,
      'package_id' : package_id,
      'action' : 'delete'
    }
   
    $.ajax({
     url: '/workshopworkspace/Mywork/',
     method: "POST",
     data: response_data,
     type: 'JSON',
     success: function(response) {
         console.log(response)
         if(response['success']){
            //display message
            $('.success-block').html('Removed package ' + package_id)
            var position = button.data('position')
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

function AddToDoneTodaySection(package_id, date_creation, film_name, qty, cutter, packer, reference, waste_qty, waste_category, involved){    
    //create elements
    const tr = document.createElement('tr')
    const th = document.createElement('th')
    const td_date = document.createElement('td')
    const td_film = document.createElement('td')
    const td_qty = document.createElement('td')
    const td_cutter = document.createElement('td')
    const td_packer = document.createElement('td')
    const td_references = document.createElement('td')
    const td_waste_qty = document.createElement('td')
    const td_waste_category = document.createElement('td')
    const td_involved = document.createElement('td')
    const td_deletebtn = document.createElement('td')

    const deletebtn = document.createElement('button')
    const position = parseInt(last_position) + 1

    //set attr for btn
    $(deletebtn).attr('class', 'btn btn-danger')
    $(deletebtn).attr('data-toggle', 'modal') 
    $(deletebtn).attr('data-target', '#DeleteModal') 
    $(deletebtn).attr('data-package', package_id) 
    $(deletebtn).attr('data-position', position)
    $(td_deletebtn).attr('id', 'delete-'+position)
    
    //add content
    $(deletebtn).html('Delete')


    $(th).html(package_id)
    $(td_date).html(date_creation)
    $(td_film).html(film_name)
    $(td_qty).html(qty)
    $(td_cutter).html(cutter)
    $(td_packer).html(packer)
    $(td_references).html(reference)
    $(td_waste_qty).html(waste_qty)
    $(td_waste_category).html(waste_category)
    $(td_involved).html(involved)
    $(td_deletebtn).append(deletebtn)

    //create span id
    const tr_id = position
    //set attributes
    tr.setAttribute('id', tr_id)

    //append to section
    $(tr).append(th)
    $(tr).append(td_date)
    $(tr).append(td_film)
    $(tr).append(td_qty)
    $(tr).append(td_cutter)
    $(tr).append(td_packer)
    $(tr).append(td_references)
    $(tr).append(td_waste_qty)
    $(tr).append(td_waste_category)
    $(tr).append(td_involved)
    $(tr).append(td_deletebtn)

    $('#recap-table > tbody:last').append(tr)
    
    last_position = position
}

function Continue(event){
    response_data = {
        'action' : 'continue',
        'csrf_token' : csrftoken
    }

    $.ajax({
        url: '/workshopworkspace/Mywork/',
        method: "POST",
        data: response_data,
        type: 'JSON',
        success: function(response) {
            console.log(response)
            if(response['success']){
                //create new option select team object
                $('.success-block').html(response['result']);
                $('.error-block').empty()
                $('#next').click()
               }
            //errors
            else{
              // here are the errors which you can append to .error-block
              $('.error-block').html(response['result']);
              $('.success-block').empty()
              console.log(response['result'])
             
            }
        }
    })
}


function AddNewFilmReel(e){
    e.preventDefault()
    var film = $('#film').val()
    var reel_nb = $('#reel_nb').val()

    response_data = {
        'film' : film,
        'reel_nb' : reel_nb,
        'action' : 'add reel nb',
        'csrf_token' : csrftoken
    }

    $.ajax({
        url: '/workshopworkspace/Mywork/',
        method: "POST",
        data: response_data,
        type: 'JSON',
        success: function(response) {
            console.log(response)
            if(response['success']){
                //create new option select team object
                $('.success-block').html(response['result']);
                $('.error-block').empty()
                //AppendToTeam(response['tech'])
                $('#film').val('')
                $('#reel_nb').val('')
                AddToOptionsFilm(response)
            }
            //errors
            else{
              // here are the errors which you can append to .error-block
              $('.error-block').html(response['result']);
              $('.success-block').empty()
              console.log(response['result'])
             
            }
        }
    })
}

function AddToOptionsFilm(response){
    console.log('******Append to options******')
    
    film_reel_tuple = response['film_reel']
    id = film_reel_tuple[0]
    name = film_reel_tuple[1]
    console.log(id)
    console.log(name)
    var opt = new Option(name, id, true, true)
    $('#id_film_reel').append(opt)
}