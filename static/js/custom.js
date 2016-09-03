/* Theme Name: The Project - Responsive Website Template
 * Author:HtmlCoder
 * Author URI:http://www.htmlcoder.me
 * Author e-mail:htmlcoder.me@gmail.com
 * Version:1.1.0
 * Created:March 2015
 * License URI:http://support.wrapbootstrap.com/
 * File Description: Place here your custom scripts
 */

$(function () {
    $('.add-to-db').click(function () {
        asin = $(this).attr('data-amazon-asin')
        parent_asin = $(this).attr('data-amazon-parent-asin')
        title = $(this).attr('data-amazon-title')
        large_image_url = $(this).attr('data-amazon-large-image-url')
        medium_image_url = $(this).attr('data-amazon-medium-image-url')
        small_image_url = $(this).attr('data-amazon-small-image-url')
        desc = $(this).attr('data-amazon-desc')
        index = $(this).attr('data-amazon-index')
        brand = $(this).attr('data-amazon-brand')
        label = $(this).attr('data-amazon-label')
        manufacturer = $(this).attr('data-amazon-manufacturer')
        editorial_reviews = $(this).attr('data-editorial-reviews')
        categorie_id = $(this).attr('data-categorie-id')
        ean = $(this).attr('data-amazon-ean')
        sku = $(this).attr('data-amazon-sku')
        isbn = $(this).attr('data-amazon-isbn')
        mpn = $(this).attr('data-amazon-mpn')
        upc = $(this).attr('data-amazon-upc')
        color = $(this).attr('data-amazon-color')
        features = $(this).attr('data-amazon-features')
        price = $(this).attr('data-amazon-price')

        $('#product-edit-form').find('#error').html("")

        $('#product-edit-form').find("input[type=text], textarea").val("")

        $('#product-edit-form').find('#product_title').html(title)
        $('#product-edit-form').find('#product_desc').html(desc)
        $('#product-edit-form').find('#product_brand').html(brand)
        $('#product-edit-form').find('#product_label').html(label)
        $('#product-edit-form').find('#product_editorial_reviews').html(editorial_reviews)
        $('#product-edit-form').find('#product_manufacturer').html(manufacturer)
        $('#product-edit-form').find('#product_image').attr('src',large_image_url)
        $('#product-edit-form').find('#product_url').attr('href','/buy-products/'+asin)


         $('#product-edit-form').find('#product_price_form').val(price)
        $('#product-edit-form').find('#product_features_form').val(features)
        $('#product-edit-form').find('#product_ama_title_form').val(title)
         $('#product-edit-form').find('#product_ean_form').val(ean)
         $('#product-edit-form').find('#product_sku_form').val(sku)
         $('#product-edit-form').find('#product_upc_form').val(upc)
         $('#product-edit-form').find('#product_mpn_form').val(mpn)
         $('#product-edit-form').find('#product_color_form').val(color)
         $('#product-edit-form').find('#product_isbn_form').val(isbn)
        $('#product-edit-form').find('#product_index_form').val(index)
        $('#product-edit-form').find('#product_categorie_id_form').val(categorie_id)
        $('#product-edit-form').find('#product_image_large_form').val(large_image_url)
        $('#product-edit-form').find('#product_image_medium_form').val(medium_image_url)
        $('#product-edit-form').find('#product_image_small_form').val(small_image_url)
        $('#product-edit-form').find('#product_asin_form').val(asin)
        $('#product-edit-form').find('#product_parent_asin_form').val(parent_asin)
        $('#product-edit-form').find('#product_title_form').val(title)
        $('#product-edit-form').find('#product_brand_form').val(brand)
        $('#product-edit-form').find('#product_label_form').val(label)
        $('#product-edit-form').find('#product_manufacturer_form').val(manufacturer)
        $('#product-edit-form').find('#product_editorial_reviews_form').val(editorial_reviews)

        $('#loading_product_form').hide()
        $('#product-edit-form').modal()
        return false
    })
})

$(function () {
    $("#add_to_db_form").submit(function(e) {

    e.preventDefault();
    e.returnValue = false;

    // do things
        $('#loading_product_form').show()
        $.post($(this).attr('action'),$(this).serialize(),function (data) {
            if(data.result == true){
                $('#product-edit-form').modal('hide')
                $('#loading_product_form').hide()
            }else{

                $('#product-edit-form').find('#error').html(data.error)
                $('#loading_product_form').hide()
            }
        })
  });
})
