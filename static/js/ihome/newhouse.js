function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}
$.get('/house/area_facility/',function (data) {
    var area_html = ''
    for(var i=0; i<data.area.length; i++){
        area_html += '<option value="' + data.area[i].id + '">' + data.area[i].name + '</option>'
    }
    $('#area-id').html(area_html);

    var facility_html_list = ''
    for(var i=0; i<data.facility.length; i++){
        var facility_html = '<li><div class="checkbox"><label><input type="checkbox" name="facility"'
        facility_html += ' value="' + data.facility[i].id + '">' + data.facility[i].name
        facility_html += '</label></div></li>'
        facility_html_list += facility_html
    }
    $('.house-facility-list').html(facility_html_list);
});


$(document).ready(function(){
    $('#form-house-info').submit(function(e){
        e.preventDefault();
        $('.error-msg text-center').hide();
        $.post('/house/newhouse/',$(this).serialize(),function(data){
            if(data.code== '200'){
                $('#form-house-info').hide();
                $('#form-house-image').show();
                $('#house-id').val(data.house_id);
            }else{
            $('.error-msg.text-center').show().find('span').html(ret_map[data.code]);
            }
        })
    })

    $('#form-house-image').submit(function(e){
        e.preventDefault();
        $(this).ajaxSubmit({
            url:'/house/image/',
            dataType:'json',
            type:'POST',
            success:function(data){
                if(data.code == '200'){
                    $('.house-image-cons').append('<img src="'+data.url+'"/>')
                }
            }
        })

    })
})