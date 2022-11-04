$(document).on("click", '#product_search_btn', function(event) {
    document.getElementById('product_search_div').classList.add('hidden')
    document.getElementById('product_search_form').classList.remove('hidden')
        document.getElementById('store_search_div').classList.add('hidden')
        });

$(document).on("click", '#store_search_btn', function(event) {
    document.getElementById('product_search_btn').classList.add('hidden')
    document.getElementById('store_search_form').classList.remove('hidden')
        document.getElementById('store_search_btn').classList.add('hidden')
        });