type="text/javascript";

var affectcar = document.querySelector('#car-list');
var affected_car=[];
var affectpart = document.querySelector('#part-list');
var affected_part=[];
var created_n = 1


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
//get page title
var page_title = $(document).attr("title");

function InitSelect2(){
    var select = document.querySelector('.select-team')
    console.log('************SELECT TEAM INIT**********')

    //init select2 for team select
    //create emptyoption
    let opt = document.createElement('option')
    opt.setAttribute('disabled', "")
    opt.setAttribute('value', 0)
    //console.log($(select)[0])
    opt = $(select)[0].insertBefore(opt, $(select)[0].firstChild)
    
    
    select.setAttribute('data-placeholder', 'Click here to select teammate(s)..')
    


    $('.select-team').select2({
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



$(document).ready(function(){
    InitSelect2()

    $("#continue").on('click',function(e){
        console.log('***********continue**********')
        CheckBeforeRedirect()
    });

    $("#save").on('click',function(e){
        e.preventDefault()
        save()
    });

    $('#DeleteModal').on('show.bs.modal', function (event) {
  
        var button = $(event.relatedTarget) // Button that triggered the modal
        var job_id = button.attr('data-job')
        
        // Extract info from data-* attributes
      
        // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
        // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
        var modal = $(this)
        modal.find('.modal-title').text('Delete job ?')
      
        //store infos in button
        modal.find('#deletebtn').attr('data-job', job_id)
    
        
      })
});


function CheckBeforeRedirect(){
    //get form url
    form_url = $("#affectation_form").attr('action')
    form_data = {
        'csrf_token' : csrftoken,
        'status' : "continue"
    }
    $.ajax({
        url: form_url,
        type: "POST",
        data: form_data,
        dataType: "JSON"
    })
    .done(function(response){
        console.log(response)
        if(response['success']==false){
            DisplayMessage('danger', response['error'])
            console.log(response['error'])
            console.log(response['message'])
        }else{
            console.log('Redirecting..')
            $("#submit").click();
        }
    })
}

function save(){
             
    //get selects value
    var train_id = $('#id_train_id').val()
    var car_id = $('#id_car_id').val()
    var part_id = $('#id_part_id').val()

    //get values name
    var train_name = $('#id_train_id option:selected').text()
    var car_name = $('#id_car_id option:selected').text()
    var part_name = $('#id_part_id option:selected').text()
    console.log(train_name+car_name+part_name)
    //get multiple select values
    var affectedteam = document.querySelector('#id_team_id');
    var team = [...affectedteam.options].filter(option => option.selected).map(option => option.value);

    
    console.log(train_id)
    console.log(car_id)
    console.log(part_id)
    console.log(team)

    //get form url
    form_url = $("#affectation_form").attr('action')
    form_data = {
        'csrf_token' : csrftoken,
        'train' : train_id,
        'car' : car_id,
        'part' : part_id,
        'team' : JSON.stringify(team),
        'status' : 'save'
    }
    $.ajax({
        url: form_url,
        type: "POST",
        data: form_data,
        dataType: "JSON"
    })
    .done(function(response){
        console.log(response)
        if(response['success']){
            let team_names=[]
            console.log(team.length)
            for(i=0;i<team.length;i++){
                team_names.push(response[team[i]])
            }
            //remind user selections
            var job_id = response['job_id']
            AddToDoneTodaySection(job_id, train_name, car_name, part_name, team, team_names)
            DisplayMessage('success', 'New data added for ' + train_name + ' - ' + car_name + ' - ' + part_name +'.')
            //reset select
            $('#id_div_id > option').prop("selected", false);
            $("li.select2-selection__choice").remove();
            InitSelect2()
            //reset form
            document.getElementById("affectation_form").reset();
        }
        else{
            DisplayMessage('danger',response['error'])
        }
        
        
    })

}

function DisplayMessage(type, message){
    //get div error
    var div_error = document.querySelector("#form-error")
    $('#form-error').empty()
    //create element
    var span = document.createElement('span')

    //create attributes for color
    div_error.setAttribute('class', 'alert alert-'+type)
    span_id='message'
    span.setAttribute('id',span_id)

    console.log(message.split(','))
    html =  message.split(',').join("</br>");

    //append to div
    div_error.append(span)

    //add content
    $('#'+span_id).html(html)   
}


function AddToDoneTodaySection(job_id, train_name, car_name, part_name, team_id, team_name){
    const tablebody = document.querySelector('#tbody')  
    
    //create elements
    const tr = document.createElement('tr')
    const th = document.createElement('th')
    const td_team = document.createElement('td')
    const td_job = document.createElement('td')
    const td_delete = document.createElement('td')

    const deletebtn = document.createElement('button')



    $(th).html(created_n)
    $(td_team).html(team_name.join(' '))
    $(td_job).html(train_name + ' - ' + car_name + ' - ' + part_name)
    $(deletebtn).attr('data-job', job_id)
    $(deletebtn).attr('class', 'btn btn-danger')
    $(deletebtn).html('Delete')
    $(deletebtn).attr('data-toggle', 'modal')
    $(deletebtn).attr('data-target', '#DeleteModal')
    $(deletebtn).attr('type', 'button')
    
    //create span id
    //set attributes
    $(td_team).attr('id', 'team-'+job_id)
    $(td_team).attr('data-team-id', team_id.join('-'))
    tr.setAttribute('id', job_id)

    $(td_delete).append(deletebtn)
    //append to section
    $(tr).append(th)
    $(tr).append(td_team)
    $(tr).append(td_job)
    $(tr).append(td_delete)

    $('#recap-table > tbody:last').append(tr)
    

    created_n = created_n + 1
}




function Delete(event){
    console.log('deleting..')
    // Button that triggered the modal
    var job_id = $('#deletebtn').attr('data-job')
    td_tech_id = '#team-'+job_id
    var tech_list = $(td_tech_id).attr('data-team-id')
   
    response_data = {
      'csrfmiddlewaretoken' : csrftoken,
      'job_id' : job_id,
      'tech_list' : tech_list,
      'status' : 'delete'
    }
   
    $.ajax({
     url: '/teamleaderworkspace/Affectation/',
     method: "POST",
     data: response_data,
     type: 'JSON',
     success: function(response) {
         console.log(response)
         if(response['success']){
            //display message
            $('.success-block').html(response['result'])
            var position = $('#deletebtn').attr('data-job')
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

  

  function DeleteRow(position){
    $('#'+position).remove()
  }