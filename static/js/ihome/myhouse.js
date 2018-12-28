$(document).ready(function(){
    $(".auth-warn").show();
})

$.get('/user/user_myhouse/',function(data){
    if(data.code == '200'){
        $('.houses-list.auth-warn').hide()
        var html=template('house_list',{hlist:data.hlist});
        $('#houses-list').append(html);
    }
    if(data.code == '1005'){
        $('#houses-list').hide()
    }

})