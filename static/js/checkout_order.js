//for whatsapp
$(document).on("click", '#whatsapp_2', function(event) {
    document.getElementById('whatsapp_text1').classList.remove('hidden')
    document.getElementById('whatsapp_paybtn').classList.remove('hidden')
        document.getElementById('method2').classList.add('hidden')

});

$(document).ready(function(){
    $(document).on('click', '#whatsapp_2', function(){

        var info=$(this).attr('info');

        req= $.ajax({

            url:'/checkout/',
            type:'POST',
            data:{info:info},
            headers:{
               'X-CSRFToken':csrftoken,
                 },
        });


        $('#whatsapp2').fadeOut(1000);
    });
});


//for flutterwave

$(document).on("click", '#method2_btn', function(event) {
    document.getElementById('method2_text').classList.remove('hidden')
    document.getElementById('method2_paybtn').classList.remove('hidden')
        document.getElementById('method1').classList.add('hidden')

});

$(document).ready(function(){
    $(document).on('click', '#method2_btn', function(){

        var info2=$(this).attr('info2');

        req= $.ajax({

            url:'/checkout/',
            type:'POST',
            data:{info2:info2},
            headers:{
               'X-CSRFToken':csrftoken,
                 },
        });


        $('#method2_confirm').fadeOut(1000);
    });
});

$(document).ready(function(){
    $(document).on('click', '#shipmeth', function(){


        var order=$(this).attr('wan');
        console.log(order);
        req= $.ajax({

            url:'/shipping_method/',
            type:'POST',
            data:{order:order},
            headers:{
               'X-CSRFToken':csrftoken,
                 },
            success: function() {
                location.reload(true)
            }
        });


    });
});

$(document).ready(function(){
    $(document).on('click', '#change_btn', function(){


        var chng_btn=$(this).attr('ban');
        console.log(chng_btn);
        req= $.ajax({

            url:'/shipping_method/',
            type:'POST',
            data:{chng_btn:chng_btn},
            headers:{
               'X-CSRFToken':csrftoken,
                 },
            success: function() {
                location.reload(true)
            }
        });
    });
});


