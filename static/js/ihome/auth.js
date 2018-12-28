function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

$.get('/user/user_auth/',function(data){
    if(data.code == '200'){
        $('#real-name').val(data.user_auth.id_name)
        $('#id-card').val(data.user_auth.id_card)
        $('#real-name').attr('disabled','disabled')
        $('#id-card').attr('disabled','disabled')
        $('input[type=submit]').hide()
    }
})

$(document).ready(function(){
    $('#form-auth').submit(function(e){
        e.preventDefault();
        $(this).ajaxSubmit({
            url:'/user/user_auth/',
            dataType:'json',
            type:'POST',
            success:function(data){
                if(data.code == '200'){
                    $('#real-name').val(data.user_auth.id_name)
                    $('#id-card').val(data.user_auth.id_card)
                    $('#real-name').attr('disabled','disabled')
                    $('#id-card').attr('disabled','disabled')
                    $('input[type=submit]').hide()
                }
                if(data.code == '1006'){
                    $('.error-msg').text(data.msg)
                    $('.error-msg').show()
                }
                if(data.code == '1008'){
                    $('.error-msg').text(data.msg)
                    $('.error-msg').show()
                }
            }

        })

    })




})

