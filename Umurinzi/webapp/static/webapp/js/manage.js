$(document).ready(function () {
    $('#search-form').submit(function (event) {
        event.preventDefault(); // Prevent the form from submitting

        var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        var searchQuery = $('#search-input').val();
        if (searchQuery.trim() === '') {
            return;
        }

        // Make the AJAX POST request with the CSRF token in the headers
        $.ajax({
            type: 'POST',
            url: '/itemsearch/',
            headers: { 'X-CSRFToken': csrfToken },
            data: { 'search_query': searchQuery },
            dataType: 'json',
            success: function (data) {
                const content = $(".content")
                content.empty();

                data.forEach((item) => {
                    const itemDiv = $('<div class="card" style="width:200px">\
                    <a href=item/'+ item.id + '>\
                    <img class= "card-img-top" src = '+ item["image"] + ' alt = "Card image"/>\
                    <div class="card-body">\
                        <h4 class="card-title">'+ item.name + '</h4>\
                        <p class="card-text">'+ item.description + '</p>\
                        </a>\
                    </div>\
                    </div >')
                    content.append(itemDiv);
                });
            },
            error: function (error) {
                console.log('Error:', error);
            }
        });
    });

    function loadSubcategoryContent(categoryId, subcategoryId) {
        $.ajax({
            url: "/filter/" + categoryId + "/" + subcategoryId + "/",
            type: "GET",
            dataType: "json",
            success: function (data) {
                const content = $(".content")
                content.empty();

                data.forEach((item) => {
                    const itemDiv = $('<div class="card" style="width:200px">\
                    <a href=item/'+ item.id + '>\
                    <img class= "card-img-top" src = '+ item["image"] + ' alt = "Card image"/>\
                    <div class="card-body">\
                        <h4 class="card-title">'+ item.name + '</h4>\
                        <p class="card-text">'+ item.description + '</p>\
                        </a>\
                    </div>\
                    </div >')
                    content.append(itemDiv);
                });
            },
            error: function (error) {
                console.log("Error fetching data:", error);
            }
        });
    }

    $.ajax({
        url: "/registereditems/",
        type: "GET",
        dataType: "json",
        success: function (data) {
            data.forEach((item) => {
                const content = $(".content")
                const itemDiv = $('<div class="card" style="width:200px">\
                    <a href=item/'+ item.id + '>\
                    <img class= "card-img-top" src = '+ item["image"] + ' alt = "Card image"/>\
                    <div class="card-body">\
                        <h4 class="card-title">'+ item.name + '</h4>\
                        <p class="card-text">'+ item.description + '</p>\
                        </a>\
                    </div>\
                    </div >')
                content.append(itemDiv);
            });
        }

    })

    $.ajax({
        url: "/get_categories/",
        type: "GET",
        dataType: "json",
        success: function (data) {
            const categoryList = $(".category-list");
            data.forEach(function (category) {
                const categoryItem = $("<li><button type='button' class='category-btn' data-category-id='" + category.id + "'>" + category.name + "</button></li>");
                const subcategoryList = $("<ul class='subcategory-list'></ul>");
                category.subcategories.forEach(function (subcategory) {
                    const subcategoryItem = $("<li><a href='#' class='subcategories' category_id=" + category.id + " subcategory_id=" + subcategory.id + ">" + subcategory.name + "</a></li>");
                    subcategoryList.append(subcategoryItem);
                });
                categoryItem.append(subcategoryList);
                categoryList.append(categoryItem);
            });
        },
        error: function (error) {
            console.log("Error fetching categories:", error);
        }
    });

    // Handle toggling of subcategories when clicking on category button
    $(document).on("click", ".category-btn", function () {
        $(this).siblings(".subcategory-list").toggle();
    });

    $(document).on("click", ".subcategories", function (event) {
        event.preventDefault();
        const categoryId = $(this).attr("category_id");
        const subcategoryId = $(this).attr("subcategory_id");
        loadSubcategoryContent(categoryId, subcategoryId);
    });

});
