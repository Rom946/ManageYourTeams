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
    $('#id_package').select2({
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
    InitSelect2()
  });