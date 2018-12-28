
function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$.get('/user/myprofile/',function(data){
    $('#user-avatar').attr('src','/static/images/'+data.user_info.avatar)
    $('#user-name').val(data.user_info.name)
})

$(document).ready(function() {
    $('#form-avatar').submit(function(e){
    e.preventDefault();
    $(this).ajaxSubmit({
        url:'/user/profile/',
        dataType:'json',
        type:'POST',
        success:function(data){
            $('#user-avatar').attr('src','/static/images/'+data.user_info.avatar)
        }
    })
    })

    $('#form-name').submit(function(e){
    e.preventDefault();
    $(this).ajaxSubmit({
        url:'/user/profile/',
        dataType:'json',
        type:'POST',
        success:function(data){
            $('#user-name').val(data.user_info.name);
            showSuccessMsg();
        }
    })
    })
})