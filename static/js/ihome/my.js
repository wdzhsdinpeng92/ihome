
function logout() {
    $.ajax({
        url:'/user/logout/',
        type:'DELETE',
        success:function(data) {
            if(data.code=='200') {
                location.href = '/house/index/';
            }
        }
    });
}

$.get('/user/user_index/',function(data){
    $('#user-name').text(data.user_info.name)
    $('#user-mobile').text(data.user_info.phone)
    $('#user-avatar').attr('src','/static/images/'+data.user_info.avatar)

})

$(document).ready(function(){
})

