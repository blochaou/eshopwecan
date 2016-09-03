/**
 * Created by blochaoufrancois on 22/08/16.
 */

$(function () {
    var asin = $('#product_asin').val()
    $.get('/product-price/'+asin,null,function (data) {
        $('#price_block').html(data)
    })
})