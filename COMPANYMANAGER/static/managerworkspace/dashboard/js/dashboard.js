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



// init select 2, data table and popover
$(document).ready( function () {

    //last x days jobs sorted by qty of ref applied
    $('.table').DataTable({
        "bPaginate": true,
        "pageLength": 5,
        "bLengthChange": true,
        "bFilter": true,
        "bSort": true,
        "bInfo": true,
        "bAutoWidth": false,
        "dom": 'Bfrtip',
        "order": [[ 2, "desc"]],
    });

    //stocks sorted by qty
    $('#stock-nigel-stats').DataTable({
        "bPaginate": true,
        "pageLength": 20,
        "bLengthChange": true,
        "bFilter": true,
        "bSort": true,
        "bInfo": true,
        "bAutoWidth": false,
        "dom": 'Bfrtip',
        "order": [[ 3, "asc"]],
    });

    $('#packages-stats').DataTable({
        "bPaginate": true,
        "pageLength": 10,
        "bLengthChange": true,
        "bFilter": true,
        "bSort": true,
        "bInfo": true,
        "bAutoWidth": false,
        "dom": 'Bfrtip',
        "order": [[ 1, "asc"]],
    });
    
    //references details sorted by job
    $('#references-details').DataTable({
        "bPaginate": true,
        "pageLength": 20,
        "bLengthChange": true,
        "bFilter": true,
        "bSort": true,
        "bInfo": true,
        "bAutoWidth": false,
        "dom": 'Bfrtip',
        "order": [[ 2, "asc"]],
    });

    //stocks sorted by qty
    $('#stock-workshop-ref-stats').DataTable({
        "bPaginate": true,
        "pageLength": 20,
        "bLengthChange": true,
        "bFilter": true,
        "bSort": true,
        "bInfo": true,
        "bAutoWidth": false,
        "dom": 'Bfrtip',
        "order": [[ 2, "asc"]],
    });

    //ncr sorted by status
    $('#ncr-stats').DataTable({
        "bPaginate": true,
        "pageLength": 20,
        "bLengthChange": true,
        "bFilter": true,
        "bSort": true,
        "bInfo": true,
        "bAutoWidth": true,
        "dom": 'Bfrtip',
        "order": [[ 12, "asc"]],
    });


    

    //stocks sorted by qty
    $('#stock-workshop-film-stats').DataTable({
        "bPaginate": true,
        "pageLength": 20,
        "bLengthChange": true,
        "bFilter": true,
        "bSort": true,
        "bInfo": true,
        "bAutoWidth": false,
        "dom": 'Bfrtip',
        "order": [[ 2, "asc"]],
    });

    //progress sorted by %
    $('.progress-stats').DataTable({
        "bPaginate": true,
        "pageLength": 20,
        "bLengthChange": true,
        "bFilter": true,
        "bSort": true,
        "bInfo": true,
        "bAutoWidth": false,
        "dom": 'Bfrtip',
        "order": [[ 2, "asc"]],
    });
    
    $('#table-progress-details').DataTable({
        "bPaginate": true,
        "pageLength": 10,
        "bLengthChange": true,
        "bFilter": true,
        "bSort": true,
        "bInfo": true,
        "bAutoWidth": false,
        "dom": 'Bfrtip',
        "order": [[ 3, "desc"]],
    });

    $(function () {
        $('[data-toggle="popover"]').popover({
            container: 'body'
        })
    })
    function InitSelect2(){
        //get selects
        var selects = document.querySelectorAll('select')
        console.log('************INIT**********')
    
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
    }
    InitSelect2()


    //show the Details Progress modal - 
    $('#DetailsProgressModal').on('show.bs.modal', function (event) {
        
        // Button that triggered the modal
        var progress_id = $(event.relatedTarget).attr('data-progress')
    

        response_data = {
            'csrfmiddlewaretoken' : csrftoken,
            'progress_id' : progress_id,
            'action' : 'get progress details'
        }

        $.ajax({
            url: '/managerworkspace/Dashboard/',
            method: "POST",
            data: response_data,
            type: 'JSON',
            success: function(response) {
                console.log(response)
                if(response['success']){
                    //create locations select object
                    SetDetailsProgress(response)
                }
                //errors
                else{
                    // here are the errors which you can append to .error-block
                    $('.error-block').html(response['error']);
                    console.log(response['error'])
                
            }
        }
        })

    })





    //show the Details for work done today modal - append data to edit button
    $('#DetailsModal').on('show.bs.modal', function (event) {
        $('#details-form').attr('hidden','')
        $('#editbtn').attr('hidden','')
        $('#job-selection').attr('hidden','')
        ResetEditBtn()
        $('.modal-title').text('Select a reference')
        // Button that triggered the modal
        var button = $(event.relatedTarget)
        var position = button.data('position')
        // Extract info from data-* attributes
        var reference_choice_list = button.data('reference')
        var date = button.data('date')
        var tr_id = '#'+date+'-'+position+ ' .name'
        console.log(tr_id)
        var tech_name = $(tr_id).html()
        console.log(tech_name)
        console.log(date)
        
        
        $('#editbtn').attr('data-date', date)
        $('#editbtn').attr('data-tech', tech_name)
        $('#editbtn').attr('data-position', position)


        console.log(reference_choice_list)
        //set options
        SetReferences(reference_choice_list)
    })

    //call DisplayReferencesDetails
    $('#select-reference').on('change', function (event){
        $('#details-form').attr('hidden', '')
        $('#editbtn').attr('hidden','')
        console.log(event.target)
        console.log($(this))
        val = $(this).val()
        ref_name = $(this).find('option:selected').html()
        $('#editbtn').attr('data-reference', ref_name)
        
        $('.modal-title').text('Select a job for ' + ref_name)
        console.log(val)
        //initiate an AJAX request to get the form (and then do the updating in a callback).
        DisplayReferenceDetails(val, 0)
    })

    //call DisplayReferencesDetails
    $('#select-job').on('change', function (event){
        val = $(this).val()
        console.log(val)
        ref_id = $('#select-reference').val()
        job_name = $(this).find('option:selected').html()
        $('#editbtn').attr('data-job', job_name)
        ref_name = $('#editbtn').data('reference')
        $('.modal-title').text('Select a job for ' + ref_name)

        //initiate an AJAX request to get the form (and then do the updating in a callback).
        DisplayReferenceDetails(ref_id, val)
    })
});


//reset editbtn attributes
function ResetEditBtn(){
    $('#editbtn').attr('data-wasteid', '')
    $('#editbtn').attr('data-qty', '')
    $('#editbtn').attr('data-wasteqty', '')
    $('#editbtn').attr('data-locations', '')
    $('#editbtn').attr('data-tech', '')
    $('#editbtn').attr('data-reference', '')
    $('#editbtn').attr('data-job', '')


}

//set options choice list for jobs
function SetJobs(choice_list){
    //$('.modal-title').text('Select a job for ' + $('#editbtn').data('reference'))
    $('#select-job').empty()
    var option = new Option('0', '')
    $('#select-job').append(option)
    console.log(choice_list)
    for(k=0;k<choice_list.length;k++){
        option = new Option(choice_list[k][1], choice_list[k][0])
        //append the option
        $('#select-job').append(option)
    }
    //show form
    $('#job-selection').removeAttr('hidden')
}

//set options choice list for reference
function SetReferences(choice_list){
    $('#select-reference').empty()
    var option = new Option('0', '')
    $('#select-reference').append(option)
    console.log(choice_list)
    choice_list = JSON.parse(choice_list.replace(/'/g, '"'))
    for(k=0;k<choice_list.length;k++){
        option = new Option(choice_list[k][1], choice_list[k][0])
      
        //append the option
        $('#select-reference').append(option)
    }
}

//display references details
function DisplayReferenceDetails(ref_id, job){
    var tech_name = $('#editbtn').attr('data-tech')
    console.log(tech_name)
    var date = $('#editbtn').data('date')
    console.log('Displaying form for ' + tech_name)
    $('body').style = 'overflow:auto;!important'

    response_data = {
        'csrfmiddlewaretoken' : csrftoken,
        'reference_id' : ref_id,
        'tech_name': tech_name, 
        'date' : date,
        'job' : job,
        'action' : 'get reference details'
    }
     
    $.ajax({
        url: '/managerworkspace/Dashboard/',
        method: "POST",
        data: response_data,
        type: 'JSON',
        success: function(response) {
            console.log(response)
            if(response['success']){
                //create locations select object
                if(response['has_job']){
                    SetJobs(response['jobs_list'])
                }
                else{
                    $('#job-selection').attr('hidden', '')
                    SetDetailsForm(response)
                }
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

//set an editable form for reference details 
function SetDetailsForm(data){
    
    var date = data['date']
    data = data['data']
    $('#details-form').removeAttr('hidden')
    $('#editbtn').removeAttr('hidden')
    var job = data['job']
    var tech = data['tech']
    var qty = data['qty']
    var position = data['position']
    var reference = data['reference']

    $('.modal-title').text(reference +' Details')
    $('#tech-name').val(tech)
    $('#job-name').val(job)
    $('#qty-name').val(qty)
    $('#reference-name').val(reference)
    $('#date-name').val(date)

    $('#locations-select').empty()
    var option = new Option('0', '')
    $('#locations-select').append(option)
    var locations = data['locations']
    console.log(locations)
    
    for(k=0;k<locations.length;k++){
        if(locations[k][3]){
            option = new Option(locations[k][1], locations[k][0], true, true)
        }
        else{
            option = new Option(locations[k][1], locations[k][0], false, false)
        }
        //append the option
        $('#locations-select').append(option)
    }


    $('#wastes-select').empty()
    var option = new Option('0', '')
    $('#wastes-select').append(option)
    var wastes = data['wastes']
    for(k=0;k<wastes.length;k++){
        option = new Option(wastes[k][1], wastes[k][0], wastes[k][3], wastes[k][3])
      
        //append the option
        $('#wastes-select').append(option)
    }

    //set min value for qty
    $('#qty-name').attr('min','1')

    //store infos in button
    $('#editbtn').attr('data-job', job)
    $('#editbtn').attr('data-reference', reference)
    $('#editbtn').attr('data-tech', tech)
    $('#editbtn').attr('data-qty', qty)
    $('#editbtn').attr('data-locations', locations)
    $('#editbtn').attr('data-position', position)
    $('#editbtn').attr('data-wastecategory', wastes)
    
    
}

//user selected waste category => display waste qty
$('#wastes-select').on('change', function(e){
    console.log('Waste Category selected..')
    var waste_id = $(this).val()
    console.log(waste_id)
    modal = $('#DetailsModal')
    modal.find('#editbtn').attr('data-wasteid', waste_id)
    //if there is a waste
    if(waste_id!=""){

        response_data = {
            'csrfmiddlewaretoken' : csrftoken,
            'waste_id' : JSON.stringify(waste_id),
            'action' : 'get waste qty'
        }
        
        
        $.ajax({
            url: '/managerworkspace/Dashboard/',
            method: "POST",
            data: response_data,
            type: 'JSON',
            success: function(response) {
                console.log(response)
                if(response['success']){
                    //create waste qty object    
                    $('#waste-qty-div').removeAttr('hidden')
                    $('#waste-qty-name').val(response['waste_qty'])
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
    else
    {
        $('#waste-qty-div').attr('hidden','')
        $('#waste-qty-name').val('')
    }
})

//hide form if cancel and reset editbtn attibutes
$('.cancelbtn').on('click', function(e){
    $('#details-form').attr('hidden', '')
    ResetEditBtn()
    
})

//user clicked save changes
function Edit(event){
    console.log('editing..')
    var button = $('#editbtn') // Button that triggered the modal
    var reference = button.data('reference')
    var tech = button.data('tech')
    var job = button.data('job')
    var qty = button.data('qty')
    var date = button.data('date')
    var locations = button.attr('data-locations')
    var waste_qty = false
    var waste_id = false
    try{
        waste_qty = button.data('wasteqty')
        waste_id = button.data('wasteid') 
    }
    catch(e){
        console.log(e)
    }
    
   
    response_data = {
      'csrfmiddlewaretoken' : csrftoken,
      'reference' : reference,
      'tech' : tech,
      'job' : job,
      'qty' : qty,
      'waste_qty' : waste_qty,
      'waste_id': waste_id,
      'locations': locations,
      'date': date,
      'action' : 'save changes'
    }
   
    $.ajax({
    url: '/managerworkspace/Dashboard/',
    method: "POST",
    data: response_data,
    type: 'JSON',
    success: function(response) {
        console.log(response)
        if(response['success']){
           //display message edit OK
           $('.success-block').html('Data has been edited.')        
           
           var position = button.attr('data-position')
           UpdateTable(position, response)
           $('.cancelbtn').click()
        }
        //errors
        else{
           // here are the errors which you can append to .error-block
           $('.message-block-edit').html(response['error']);    
           $('.message-block-edit').attr('class', 'message-block alert-danger')
           console.log(response['error'])
          
        }
    }})
}



//get qty and store it in editbtn
$('#qty-name').on('change', function (event){
    qty = $(this).val()
    modal = $('#DetailsModal')
    modal.find('#editbtn').attr('data-qty', qty)
    console.log(qty)
  
})
  
//get locations on change and store value in editbtn
$('#locations-select').on('change', function (event){
    locations = $(this).val()
    modal = $('#DetailsModal')
    modal.find('#editbtn').attr('data-locations', locations)
    console.log(locations)
  
})

//get waste qty and store it in editbtn
$('#waste-qty-name').on('change', function (event){
    qty = $(this).val()
    modal = $('#DetailsModal')
    modal.find('#editbtn').attr('data-wasteqty', qty)
    console.log(qty)
})


function UpdateTable(position, response){
    console.log('Updating table...')
    //build id qty
    var tech_data = response['tech_data']
    console.log(response['tech_data'])
    var tr_id = '#'+position
    $(tr_id).find('td .name').val(tech_data['name'])
    $(tr_id).find('td .count').val(tech_data['count'])
    $(tr_id).find('td .cost').val(tech_data['cost'])
    $(tr_id).find('td .wasted').val(tech_data['wasted'])
    $(tr_id).find('td .wasted_cost').val(tech_data['name'])
    $(tr_id).find('td .surface').val(tech_data['name'])
    $(tr_id).find('td .detailsbtn').attr('data-reference', tech_data['references_choice'])    
}


function SetDetailsProgress(data){
    $('#DetailsProgressLabel').html(data['title'])
    $(".progress-title").html(data['completed'])
    tbody = $('#tr-progress-details')
    tbody.empty()

    console.log(data['data_list'])

    for(i=0;i<Object.keys(data['data_list']).length;i++){
        reference = Object.keys(data['data_list'])[i]
        reference = data['data_list'][reference]

        tr = document.createElement('tr')

        td_i = document.createElement('td')
        td_reference = document.createElement('td')
        td_surface_covered = document.createElement('td')
        td_applied = document.createElement('td')
        td_progress = document.createElement('td')

        td_i.innerHTML = i+1
        td_reference.innerHTML = Object.keys(data['data_list'])[i].toString()

        td_progress.innerHTML = reference['progress'].toString() + '%'
        class_progress = get_class_css(reference['progress'], 'progress')
        td_progress.setAttribute('class', class_progress)

        td_surface_covered.innerHTML = reference['surface_covered'].toFixed(2).toString() + 'm2 / '  + reference['surface_to_cover'] + 'm2'
        class_surface = get_class_css(reference['surface_covered'], 'surface', reference['surface_to_cover'])
        if(!class_surface){
            class_surface = class_progress
        }
        td_surface_covered.setAttribute('class', class_surface)

        td_applied.innerHTML = reference['applied'].toString() + ' / ' + reference['to_apply']
        class_applied = get_class_css(reference['applied'], 'applied', reference['to_apply'])
        if(!class_applied){
            class_applied = class_progress
        }
        td_applied.setAttribute('class', class_applied)
         

        
        tbody.append(tr)

        tr.append(td_i)
        tr.append(td_reference)
        tr.append(td_surface_covered)
        tr.append(td_applied)
        tr.append(td_progress)

    }


    
}

var css_class = ''
function get_class_css(number, target, data = ''){
    console.log('getting css class for ' + target)
    console.log(data)
    
    if(target == 'progress'){
        pc = number

        pc = Math.round(pc)
        console.log(pc)
        if(pc <= 0){
            css_class = 'alert alert-danger'
        }
        else if (pc>10 && pc<50) {
            css_class = 'alert alert-warning'
        }
        else if (pc >= 50 && pc<100) {
            css_class = 'alert alert-info'
        }
        else if (pc >= 100) {
            css_class = 'alert alert-success'
        }
    }

    else if(target == 'surface' || target == 'applied'){
               
        if(number > data*1.5){
            css_class = 'alert alert-danger'
        }
        else if(number>data){
            css_class = 'alert alert-warning'
        }
        else{
            css_class = false 
        }


    }
    else {
        css_class = 'alert alert-danger'
    }

    return css_class
}

function recalculate_progress(event){
    console.log('recalculating progress..')
    var progress_id = $(event.target).attr('id')
    console.log(progress_id)
    
    response_data = {
        'csrfmiddlewaretoken' : csrftoken,
        'progress_id' : progress_id,
        'action' : 'recalculate progress'
    }
    
    $.ajax({
        url: '/managerworkspace/Dashboard/',
        method: "POST",
        data: response_data,
        type: 'JSON',
        success: function(response) {
            console.log(response)
            if(response['success']){
                location.reload()
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