//模态框居中的控制
function centerModals(){
    $('.modal').each(function(i){   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');    
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top-30);  //修正原先已经有的30个像素
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}



$(document).ready(function(){
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);
    $.get('/order/allorders/',function (data) {
        var order_html=template('orders-list-tmpl',{olist:data.olist});
        $('.orders-list').html(order_html);
        $(".order-comment").on("click",function(){
            var orderId = $(this).parents("li").attr("order-id");
            $(".modal-comment").attr("order-id", orderId);
        });
    });


    $('.modal-comment').click(function () {
        var order_id = $(this).attr('order-id');
        var comment=$('#comment').val();
        $.ajax({
            url: '/order/order/' + order_id + '/',
            type: 'put',
            data: {'status': 'COMPLETE','comment':comment},
            success: function (data) {
                $('#comment-modal').modal("hide");
                $('li[order-id='+order_id+'] .order-comment').hide();
//                $('.modal-backdrop').css({'display': 'None'});
                $('#' + order_id).text('已完成');
            }
        });
    });
});


