
//checkout page
function refresh() {
    $.ajax({
        url: '/checkout/',
        type: 'GET',
        credentials:'include',
        success: function(data) {
                        data=$(data).find('#checkout_box1');
            $('#checkout_box1').replaceWith(data);
            inte=setTimeout(refresh, 1000);

        }
    });
}
function stop(){
    clearTimeout(inte);
}
