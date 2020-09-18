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



var colors = ["Crimson ", "Cyan ", "DarkBlue ", "DarkCyan ", "DarkGoldenRod ", "DarkGray ", "DarkGrey ", "DarkGreen ", "DarkKhaki ", "DarkMagenta ", "DarkOliveGreen ", "DarkOrange "];
var sampleData = []
var endpoint = '../../api/v1/profiles/'
    


$(document).ready(function () {
    function getData(){
        $.ajax({
            method: "GET",
            url: endpoint,
            success : function(api_data){
                sampleData = api_data.results
                
                var table = $('#register').DataTable({
                    dom: 'fitlp',
                    pagingType: 'full_numbers',
                    pageLength: 5,
                    lengthMenu: [5, 10, 15, 20, 100],
                    select: 'single',
                    data: sampleData,
                    columns: [
                        {   /* created column to show a picture just to make this demo look better */
                            orderable: false, data: '', name: 'Photo', orderable: false, defaultContent: '', title: 'Photo',
                            visible: true, className: 'text-center', width: '20px',

                            createdCell: function (td, cellData, rowData, row, col) {
                                var $ctl = $("<i><img src="+rowData.url+" class='avatar border rounded-circle' width='100vh'></i>")
                                $(td).append($ctl);
                            }
                        },
                        /* I added a label to the column for the field name which will show up in the card display */
                        
                        {
                            data: "fullname", name: "user", title: "Name", visible: true, class: 'text-right',
                            render: function (data, type, full, meta) { var title = $('#register').DataTable().column(meta.col).header(); return '<label>'+ $(title).html() +':</label>' + data; }
                        },
                        {
                            data: "position", name: "position", title: "Position", visible: true, class: 'text-right',
                            render: function (data, type, full, meta) { var title = $('#register').DataTable().column(meta.col).header(); return '<label>'+ $(title).html() +':</label>' + data; }
                        },
                        {
                            data: "days_since_joined", name: "days_since_joined", title: "Days since joined", visible: true, class: 'text-right',
                            render: function (data, type, full, meta) { var title = $('#register').DataTable().column(meta.col).header(); return '<label>'+ $(title).html() +':</label>' + data + ' days'; }
                        },
                        {
                            data: "email", name: "email", title: "Email", visible: true, class: 'text-right',
                            render: function (data, type, full, meta) { var title = $('#register').DataTable().column(meta.col).header(); return '<label>'+ $(title).html() +':</label>' + data; }
                        },
                        {
                            data: "performancemonth", name: "performancemonth", title: "Performance this month", visible: true, class: 'text-right',
                            render: function (data, type, full, meta) { var title = $('#register').DataTable().column(meta.col).header(); return '<label>'+ $(title).html() +':</label>' + data; }
                        },
                        {
                            data: "workmonth", name: "workmonth", title: "Applied/created this month", visible: true, class: 'text-right',
                            render: function (data, type, full, meta) { var title = $('#register').DataTable().column(meta.col).header(); return '<label>'+ $(title).html() +':</label>' + data + ' units'; }
                        },
                        {
                            data: "wastemonth", name: "wastemonth", title: "Wasted this month", visible: true, class: 'text-right',
                            render: function (data, type, full, meta) { var title = $('#register').DataTable().column(meta.col).header(); return '<label>'+ $(title).html() +':</label>' + data + ' units'; }
                        },
                        {
                            data: "surfaceappliedmonth", name: "surfacemonth", title: "Surface applied this month", visible: true, class: 'text-right',
                            render: function (data, type, full, meta) { var title = $('#register').DataTable().column(meta.col).header(); return '<label>'+ $(title).html() +':</label>' + data + ' m²'; }
                        },
                        {
                            data: "costmonth", name: "costmonth", title: "Cost this month", visible: true, class: 'text-right',
                            render: function (data, type, full, meta) { var title = $('#register').DataTable().column(meta.col).header(); return '<label>'+ $(title).html() +':</label>' + data + ' R'; }
                        }
                    ]
                })
                .on('select', function (e, dt, type, indexes) {
                    var rowData = table.rows(indexes).data().toArray()
                    $('#row-data').html(JSON.stringify(rowData))
                })
                .on('deselect', function () {
                    $('#row-data').html('')
                })

                $('#btToggleDisplay').on('click', function () {
                    $("#register").toggleClass('cards')
                    $("#register thead").toggle()
                })
                        },
                        error : function(error){
                            console.log(error)
                        }
                    })
                
                }

    getData()

    

});