//count form created
var created = 0
var first_tech_id = ''
var total_tech = 0
function get_first_tech(){
  first_tech_id = $('.first_tech_id').attr('id')
}
get_first_tech()

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

//init selects references with Select2 Jquery plugin
function InitSelect2Ref(){
  //get selects
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
    selects[k].setAttribute('data-placeholder', 'Select References..')

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

//convert form data to dictionary or json format
function objectifyForm(formArray) {
  var returnArray = {};
  for (var i=0;i<formArray.length;i++) {
    console.log('tour')
      if (formArray[i].value) {
          returnArray[formArray[i].name] = formArray[i].value;
      }
  }
  return returnArray;
}

//get first form data
function get_ref_form_infos(node){
  console.log(node.target)
  form = node.target
  var form_id = '#' + form.getAttribute('id')
  console.log(form_id)
  var form_url = form.getAttribute('action')
  console.log(form_url)
  console.log('form data')
  //get form data
  var form_data = $(form_id).serializeArray()
  console.log(form_data)
  //form_data = objectifyForm(form_data)

  //get job and tech
  try{
    select_obj = $(node.target).find('select')
    console.log(select_obj)
    select_id = select_obj.attr('id')
    select_data = select_id.split('-')
    var train = select_data[0] 
    console.log(train)
    var car = select_data[1]
    console.log(car)
    var part = select_data[2]
    var tech = select_data[3]
    var data = {
      'tech' : tech,
      'train' : train,
      'car' : car,
      'part' : part,
      'form_data' : JSON.stringify(form_data),
      'action': 'select references'
    }
  }
  catch (error){
    console.log(error)
    var data = {
      'form_data' : form_data
    }
  }

  url_and_form = {
    'data' : data,
    'form_url' : form_url
  }

  return url_and_form
}

//create 2nd form submit button
function create_submit_btn(div){
  
  //create element
  var submit_btn = document.createElement('button')
  //set attributes
  submit_btn.setAttribute('type', 'submit')
  submit_btn.setAttribute('name', 'submit')
  submit_btn.setAttribute('class', 'btn btn-primary')
  //set content
  submit_btn.textContent = 'Save'
  //append to div
  div.append(submit_btn)
}

//display waste category AND WASTE LOCATION (ADDED AFTER) only if waste qty>0
function DisplayWasteCategory(e){
  console.log(e.target)
  let val = e.target.value
  console.log('************DISPLAYWASTECATEGORY*************')
  //get form row waste
  let parent_div = $(e.target.parentNode.parentNode)
  console.log(parent_div)
  let select = $(parent_div[0]).find('select')
  let select_p = select[0].parentNode
  //get form row waste location
  let waste_location_form_row = $(parent_div[0]).next()
  //get waste location select
  let select_waste_location = $(waste_location_form_row[0]).find('select')
  let select_waste_location_p = select_waste_location[0].parentNode

  //show waste options if waste qty>0
  if(val>0){
    select_p.removeAttribute('hidden')
    select_waste_location_p.removeAttribute('hidden')
    select[0].setAttribute('required', '')
  }
  //hide waste options if waste qty < 0
  else{
    select_p.setAttribute('hidden', '')
    select[0].removeAttribute('required')
    select_waste_location_p.setAttribute('hidden', '')
  }

  
}

//set up labels and disposition
function SetUpForm(div){
  console.log(div)

  //create elements : row_1 = qty and loc, row_2 = waste, one full row for package and one full row for waste location
  var row_1 = document.createElement('div')
  var row_2 = document.createElement('div')
  var row_package = document.createElement('div')
  var p_1 = document.createElement('p')
  var p_2 = document.createElement('p')
  var row_waste_location = document.createElement('div')


  //set attributes
  row_1.setAttribute('class', 'form-row col-md-12')
  row_1.setAttribute('style', 'display: flex; align-items: center;')
  row_2.setAttribute('class', 'form-row col-md-12')
  row_2.setAttribute('style', 'display: flex; align-items: center;')
  row_package.setAttribute('class', 'form-row col-md-12')
  row_package.setAttribute('style', 'display: flex; align-items: center;')
  p_1.setAttribute('class', 'col-md-1')
  p_2.setAttribute('class', 'col-md-1')
  row_waste_location.setAttribute('class', 'form-row col-md-12 waste-location')
  row_waste_location.setAttribute('style', 'display: flex; align-items: center;')
  //find form fields (wrapped as p)
  ps = $(div).find('p')

  for(i=0;i<ps.length;i++){
    ps[i].setAttribute('class','row form-group col-md-5 mb-0')

    //package
    if(i==1){
      row_package.append(ps[i])
    }
    //qty and location
    else if(i==0 || i==2){
      row_1.append(ps[i])
    }
    //waste qty + category
    else if(i==3||i==4){
      row_2.append(ps[i])
    }
    //waste location
    else if(i==5){
      row_waste_location.append(ps[i])
    }
    
    //stick labels to the left and upper
    label = $(ps[i]).find('label')
    console.log(label[0])
    console.log(i)
    //remove labels and init
    label.remove()
    //qty and waste_qty labels
    if(i==0||i==3){
      //set space between input and select
      //qty
      if(i==0){
        //set space between 2 elements
        row_1.append(p_1)
      }
      //waste
      else{
        //set space between 2 elements
        row_2.append(p_2)
        var waste_qty_p_class = 'waste-qty-p-'+created.toString()
        ps[i].setAttribute('class', waste_qty_p_class+' row form-group col-md-5 mb-0')
        ps[i].setAttribute('onchange', 'DisplayWasteCategory(event);')
      }
    }
    else if (i==1){
      var package_p_class = 'package-p-'+created.toString()
      ps[i].setAttribute('class', package_p_class+' row form-group col-md-9 mb-0')
    }
    else if(i==5){
      var waste_location_p_class = 'waste-location-p-'+created.toString()
      ps[i].setAttribute('class', waste_location_p_class+' row form-group col-md-9 mb-0')
    }
    //selects labels
    //1 - package, 2 - locations, 4 - waste category, 5 - waste locations
    if(i==1||i==2||i==4||i==5){
      //ps[i].setAttribute('align','right')
      select = $(ps[i]).find('select')
      
      //modify select id 
      select_id = 'select_id_'+created.toString()
      select[0].setAttribute('id', select_id)
      console.log(select_id)

      //create empty option 
      option = document.createElement('option')
      option.setAttribute('disabled', "")
      option.setAttribute('value', 0)
      //console.log($(select)[0])
      option = $(select)[0].insertBefore(option, $(select)[0].firstChild)

      //total forms created
      created = created + 1

      //init select2
      if(i==2||i==5){ //locations
        if(i == 2){
          select[0].setAttribute('data-placeholder', 'Select location(s)..')
        }
        else{
          select[0].setAttribute('data-placeholder', 'Select waste location(s)..')
          select[0].removeAttribute('required')
          ps[i].setAttribute('hidden', '')
        } 
        $(select).select2({
          minimumResultsForSearch: -1,
          maximumSelectionLength: 12,
          placeholder: function() {
            $(this).data('placeholder');
          },
          allowClear: true,
          width: '100%',
          tags: false,
          tokenSeparators: [',', ' '],
        });
        
      } //end if
      else if(i==4){ //waste category
        select[0].setAttribute('data-placeholder', 'Select waste category..')
        var p_class_name = 'waste-select-'+created.toString()
        ps[i].setAttribute('class', p_class_name+' row form-group col-md-5 mb-0')
        //hide waste category
        ps[i].setAttribute('hidden', '')
        
        $(select).select2({
          minimumResultsForSearch: -1,
          maximumSelectionLength: 1,
          placeholder: function() {
            $(this).data('placeholder');
          },
          allowClear: true,
          width: '100%',
          tags: false,
          tokenSeparators: [',', ' '],
        });
      }
      else if(i==1){ //package
        var p_class_name = 'package-select-'+created.toString()
        ps[i].setAttribute('class', p_class_name+' row form-group col-md-11 mb-0')
        
        $(select).select2({
          minimumResultsForSearch: -1,
          placeholder: function() {
            $(this).data('placeholder');
          },
          allowClear: true,
          width: '100%',
          tags: false,
          tokenSeparators: [',', ' '],
        });
      }  
        
      
      
      //modif for placeholder  
      console.log('*************NEW SELECT************')
      //get new select2 search__field created
      select2_search_field = $(select[0].parentNode).find('input')      
      console.log($(select2_search_field))
      //show placeholder
      $(select2_search_field[0]).attr('style', 'width:300px!important;')

    } //end else
  }

  
  //qty and location row
  div.append(row_1)
  //package row
  div.append(row_package)
  //waste row
  div.append(row_2)
  //waste location row
  div.append(row_waste_location)

  //leave a space for submit btn
  div.append(document.createElement('br'))
  //submit btn
  create_submit_btn(div)
}

//create new form element
function CreateForm(node, div, instance, on_submit_action){

  //create content
  form = document.createElement('form')

  //set attributes
  form.setAttribute('method', 'POST')
  form.setAttribute('action', '/teamleaderworkspace/References/')
  form.setAttribute('onsubmit', on_submit_action)
  console.log(instance)
  form.setAttribute('id', instance)
  //form.setAttribute('name', instance)
  //insert div in form 
  form.append(div)
  // insert form in node
  node.append(form)

  return form
}

//Display new InfoForm form
function DisplayInfoForm(node, form, reference, index, instance, form_submit_action){
  console.log('preparing a form for '+ reference)
  //create elements
  var div = document.createElement('div')
  var div_label = document.createElement('div')
  var label = document.createElement('label')

  //set attributes
  let div_id = 'div_' + index.toString() 
  div.setAttribute('id', div_id)
  div.setAttribute('class', 'col-md-12')
  div_label.setAttribute('class', 'col-md-12')
  div_label.setAttribute('align', 'center')
  
  //set content
  label.innerHTML = reference.bold()
  
  //insert elements in div
  div.innerHTML = form
  div_label.append(label)
  //insert label first
  div.insertBefore(div_label, div.firstChild);


  SetUpForm(div)
  form_node = CreateForm(node, div, instance, form_submit_action)
  
  return form_node
}

//AJAX TO SEND 1st FORM
function sendData(e){
  e.preventDefault(); // do not refresh the page

  //get first form infos and url
  url_and_form = get_ref_form_infos(e)

  response_data = url_and_form['data']
  form_url = url_and_form['form_url']
  
  //post selected references
  $.ajax({
    url: form_url,
    method: "POST",
    data: response_data,
    type: 'JSON',
    success: function(response) {
      //console.log(response)
        //render next form with infos to fulfill
        console.log(response['forms'])
        
        //disable select
        form_id = '#' + e.target.getAttribute('id')
        console.log('Form received: ')
        console.log(response['forms'].length)
        //get parent div (col-md-12)
        parent_div_node = e.target.parentNode.parentNode

        //get form 2 div node
        div_node = parent_div_node.children[1]
        console.log('node:')
        console.log(div_node)
        
        nb_form = 0
        for(var i=0;i<response['forms'].length;i++){
          //get form instance
          let instance = response['instances'][i]
          //get form
          form = response['forms'][i]
          console.log(form)
          //get reference
          reference = response['references'][i]
          //display new form
          form_submit_action = 'sendDataFormInfo(event);'
          form_node = DisplayInfoForm(div_node, form, reference, i, instance, form_submit_action)
          console.log('Created a new form: ')
          console.log(form_node)
          nb_form = nb_form +1
        }
        //disable selection and button 
        DisableSelect(form_id)
        console.log('nb of forms displayed: ' + nb_form.toString())
        if(response['team_list']){
          UpdateHeader(response['team_list'], response['completed'], response['total_tech'])
        }
    },
    error: function(response) {
        // here are the errors which you can append to .error-block
        $('.error-block').html(response);
    }
  })
}

//get form data and form url
function get_infos_form_data(node){
  console.log(node.target)
  form = node.target
  //get form instance stored in form id
  var instance = form.getAttribute('id')
  var form_id = '#' + form.getAttribute('id')
  console.log(form_id)
  var form_url = form.getAttribute('action')
  console.log(form_url)
  console.log('form data')
  //get form data
  var form_data = $(form_id).serializeArray()
  //form_data('csrfmiddlewaretoken', csrftoken)
  console.log(form_data)
  //form_data = objectifyForm(form_data)

  var tech = $('#tech-name').attr('value')
  console.log(tech)
  var data = {
    'tech' : tech,
    'instance' : instance,
    'form_data' : JSON.stringify(form_data),
    'action': 'save informations',
  }

  url_and_form = {
    'data' : data,
    'form_url' : form_url
  }

  return url_and_form
}

//Hide main and display a button to go to the next tech
function DisplayFinishedTech(){
  console.log('DisplayFinishedTech')
  $('#main').attr('hidden','')
  $('<div id = "tech_done" class = "card-body" ><div class = "row" align="center"><h1><b>All the data for this teammate have been entered.</b></h1><br></div><div class="row" align="center"><button class = "btn btn-success" type="button" onclick="plusDivs(1)">Go to the next teammate</button></div></div>').insertAfter('#main')
}

//create and display continue button to go to feedback
function DisplayContinueButton(){
  
    $('#main').attr('hidden', '')
    $('#tech_done').attr('hidden', '')
    $('#valid-form').removeAttr('hidden')
  
}



//AJAX SECOND FORM
function sendDataFormInfo(e){
  e.preventDefault()
  //get first form infos and url
  url_and_form = get_infos_form_data(e)

  response_data = url_and_form['data']
  form_url = url_and_form['form_url']
  
  //post selected references
  $.ajax({
    //SAVE INFORMATIONS
    url: form_url,
    method: "POST",
    data: response_data,
    type: 'JSON',
    success: function(response) {
        console.log(response)
        //disable form
        DisableSelect('#' + response['form_id'])
        //get statuses
        tech_status = response['tech_status']
        global_status = response['global_status']
        if(tech_status == 'complete'){
          if(global_status == 'complete'){
            DisplayContinueButton()
          }
          else{
            DisplayFinishedTech()
          }
        }
        
    },
    error: function(response) {
        // here are the errors which you can append to .error-block
        $('.error-block').html(response);
    }
  })
}

//disable select and buttons
function DisableSelect(form_id){
  console.log(form_id)
  select = $(form_id).find('select')
  console.log(select)
  console.log('Disable select for reference affectation, select: '+ select)
  select.prop('disabled', true)

  //disable button
  submit = $(form_id).find('input')
  button = $(form_id).find('button')
  console.log('Disable submit button')
  submit.attr('class',"btn disabled")
  button.attr('class',"btn disabled")
}

//display new form to select references (next or previous tech)
function DisplayNewReferenceForm(forms){
  for(var i=0;i<forms.length;i++){
    form = forms[i]
    console.log('Creating form '+i.toString())

    if(i==0){
      existing_forms = document.querySelectorAll('.formsdiv')
      console.log(existing_forms)
      for(var j=1;j<existing_forms.length;j++){
        $('#formsdiv'+j.toString()).remove()
      }
      
      //get the div to insert the form in and re-enable submit btn
      reference_form_div_node = $('#formsdiv0').find('.form1')[0]
      div_to_insert_form = $(reference_form_div_node).find('div')[0]
      submit_btn = $('#references_0-submit')
      console.log(submit_btn)
      submit_btn.removeAttr('disabled')
      submit_btn.attr('class', 'btn btn-primary')

      //clean info form on the right
      console.log($('#formsdiv0').find('.form2')[0])
      info_form = $('#formsdiv0').find('.form2')[0]
      $(info_form).empty()

      $(div_to_insert_form).html(form)
      InitSelect2Ref()
    }
    else{
      //copy last form
      single_forms_div = reference_form_div_node.parentNode
      //remove existant forms

      console.log(single_forms_div)
      //clone the last div
      new_forms_div = $(single_forms_div).clone()
      //change div id
      $(new_forms_div).attr('id', 'formsdiv'+i.toString())
      
      //append clone after last div
      single_forms_div.after(new_forms_div[0])
      console.log(new_forms_div[0])
      //get left div
      div_form = $(new_forms_div).find('div')[0]
      //get form div
      div_to_insert_form = $(div_form).find('div')[0]
      //change form div id
      $(div_to_insert_form).attr('id','div_id_references_'+i.toString())
      //get form
      form_element = $(div_form).find('form')[0]
      //change form id
      $(form_element).attr('id', 'form'+i.toString())
      console.log(div_to_insert_form)

      //get button
      submit_btn = $(form_element).find('.btn')[0]
      $(submit_btn).attr('id', 'references_' + i.toString() + '-submit')

      //append form to div
      $(div_to_insert_form).html(form)
      InitSelect2Ref()

      console.log(new_forms_div[0])
      reference_form_div_node = $(new_forms_div[0]).find('.form1')[0]
    }
  }
}

//change the names on the arrows
function ChangeDisplayArrows(next_tech, previous_tech){
  $('#next_tech').attr('value', next_tech)
  $('#next_tech').html(next_tech)
  $('#previous_tech').attr('value', previous_tech)
  $('#previous_tech').html(previous_tech)
}

//edit profile picture and name
function ChangeProfile(target, name, image_url){
  console.log('Updating Profile')
  console.log($(target))
  $(target).empty()
  //create element span
  var span = document.createElement('span')
  //set attr
  span.setAttribute('class', 'row col-md-12')
  span.setAttribute('align', 'center')
  span.setAttribute('onclick','currentDiv(1)')
  span.setAttribute('value', name)
  span.setAttribute('id', 'tech-name')
  //change name
  $(span).html("<strong>" + name + "</strong>")
  
  //change img object  
  //create element image
  var img = document.createElement('img')
  //set attr
  img.setAttribute('class', 'rounded-circle account-img')
  img.setAttribute('id', 'image')
  img.setAttribute('align','center')

  //append elements
  $(target).append(img)
  $(target).append(span)


  if(target=='#current_tech'){
    $('#image').attr('src', image_url)
  }
  
  //display div again
  try{
    console.log('show main')
    $('#main').removeAttr('hidden')
    $('#tech_done').remove()
  }
  catch(e){
    console.log(e)
  }
}

function UpdateHeader(team_list, completed, total_tech){
  console.log('Updating Header')
  $('#uncompleted').html("<strong>Uncompleted: </strong>" + team_list)
  $('#completed').html("<strong>Completed: </strong>"+ completed + '/' + total_tech)
}

//AJAX request to get new form (next or previous tech)
function GetForm(tech, action){
  response_data = {
    'tech' : tech,
    'action' : action
  }

  $.ajax({
    url: '/teamleaderworkspace/References/',
    method: "POST",
    data: response_data,
    type: 'JSON',
    success: function(response) {
        console.log(response)
        if(response['success']){
          //update uncompleted / completed
          total_tech = response['total_tech']
          UpdateHeader(response['uncompleted'], response['completed'], total_tech)

          if(response['action'] == 'load next tech'){
            GetForm(response['next_tech'], 'change tech')
          }
          else{
            DisplayNewReferenceForm(response['forms'])
            ChangeDisplayArrows(response['next_tech'], response['previous_tech'])
            ChangeProfile('#current_tech', response['profile_name'], response['profile_image'])
            console.log(response['profile_name'])
          }
        }
        //errors
        else{
          // here are the errors which you can append to .error-block
          $('.error-block').html(response['error']);
          console.log(response['error'])
          if(response['error']=='Data is completed'){
            DisplayContinueButton()
          }
        }
    },
    error: function(response) {
        // here are the errors which you can append to .error-block
        $('.error-block').html(response);
    }
  })
}

//get next tech name
function CreateNextElement(){
  next_tech = $('#next_tech').attr('value')
  console.log(next_tech)

  GetForm(next_tech, 'change tech')
  
}

//get previous tech name
function CreatePreviousElement(){
  previous_tech = $('#previous_tech').attr('value')
  console.log(previous_tech)

  GetForm(previous_tech, 'change tech')
}



// Slideshow
var slideIndex = 1;
showDivs(slideIndex);
var last_slideIndex = slideIndex
var init = 0

//Initiate the creation of a new tech page
function CreateNewElement(n){
  var x = document.getElementsByClassName("mySlides");
  console.log(n)
  console.log(slideIndex)
  console.log(last_slideIndex)
  if(slideIndex<last_slideIndex){
    console.log('previous')
    CreatePreviousElement()
    last_slideIndex = last_slideIndex -1
  }
  else if(slideIndex>last_slideIndex){
    console.log('next')
    CreateNextElement()
    last_slideIndex = last_slideIndex + 1
  }

  if (n > x.length) {
    last_slideIndex = 1
    console.log('Reset last_slideIndex next')
  }    

  else if (n < 1) {
    last_slideIndex = x.length
    console.log('Reset last_slideIndex previous')
  } 
  

}


function plusDivs(n) {
  showDivs(slideIndex += n);
  CreateNewElement(n)
}

function currentDiv(n) {
  showDivs(slideIndex = n);
}

function showDivs(n) {
  var i;
  var x = document.getElementsByClassName("mySlides");


  if (n > x.length) {
    slideIndex = 1
    console.log('Reset slideIndex next')
  }    

  if (n < 1) {
    slideIndex = x.length
    console.log('Reset slideIndex previous')
  } 

  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";  
  }


  x[slideIndex-1].style.display = "block";  

}


//init select2 plugin
$(document).ready(function(){
  //init select2
  window.onload = InitSelect2Ref()
})