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
    //init select2 for reference selects
    for(k=0;k<selects.length;k++){
        //create emptyoption
        let opt = document.createElement('option')
        opt.setAttribute('disabled', "")
        opt.setAttribute('value', 0)
        //console.log($(select)[0])
        opt = $(selects[k])[0].insertBefore(opt, $(selects[k])[0].firstChild)
        console.log($(selects[k]))
        console.log($(selects[k])[0])
        console.log(opt)
        if (k==0){
            selects[k].setAttribute('data-placeholder', 'Click here to select your teammates..')
        }
        else if (k==2){
            selects[k].setAttribute('data-placeholder', 'Click here to select car(s)..')
        }
        else if (k==3){
            selects[k].setAttribute('data-placeholder', 'Click here to select part(s)..')
        }
        else {
            selects[k].setAttribute('data-placeholder', 'Click here to select train(s)..')
        }


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


$(document).ready( function () {
    
    InitSelect2()
});

function AppendToTeam(tech_tuple){
    console.log('******Append to team******')
    id = tech_tuple[0]
    name = tech_tuple[1]
    console.log(id)
    console.log(name)
    var opt = new Option(name, id, true, true)
    $('#team-list').append(opt)
}

function AddNewTech(e){
    e.preventDefault()
    var tech = $('#addtech_id').val()

    response_data = {
        'tech' : tech,
        'csrf_token' : csrftoken
    }

    $.ajax({
        url: '/teamleaderworkspace/teamleaderhome/Mywork/',
        method: "POST",
        data: response_data,
        type: 'JSON',
        success: function(response) {
            console.log(response)
            if(response['success']){
              //create new option select team object
              $('.success-block').html(response['result']);
              AppendToTeam(response['tech'])
              $('#addtech_id').val('')
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