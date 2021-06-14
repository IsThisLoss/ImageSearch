function load_all_images() {
    $.ajax({
        url: "/api/image",
        type: "GET",
        success: function(data) {
            draw_images(data.images);
        },
    });
}

function search_images() {
    text = document.getElementById("search_input").value;
    
    if (!text || text.length == 0) {
        load_all_images();
        return;
    }

    $.ajax({
        url: "/api/search/image",
        data: {
            "text": text
        },
        type: "GET",
        success: function(data) {
            draw_images(data.images);
        },
    });
}

function delete_image(id) {
    $.ajax({
    	url: "/api/image/" + id,
	type: "DELETE",
	success: function(data) {
	    load_images();
	}
    });
}

function save_image() {
    new_image_title = document.getElementById("new_image_title");
    new_image_description = document.getElementById("new_image_description");
    new_image_url = document.getElementById("new_image_url");

    $.ajax({
        url: "/api/image",
        data: JSON.stringify({
            "title": new_image_title.value,
            "description": new_image_description.value,
            "url": new_image_url.value
        }),
        dataType: "json",
        type: "POST",
        success: function(data) {
            new_image_title.value = '';
            new_image_description.value = '';
            new_image_url.value = '';
            load_all_images()
        },
    });
}

function draw_images(images) {
    let images_block = document.getElementById('images');
    // 4 
    // - id
    // - class
    // - block with form to add image
    // - template block
    while (images_block.childNodes.length > 4) {
        console.log(images_block.lastChild);
        images_block.removeChild(images_block.lastChild);
    }
    for (let i = 0; i < images.length; i++) {
        let image_block = images_block.querySelector("div[data-type='template']").cloneNode(true);
        image_block.querySelector('h6').textContent = images[i].title;
        image_block.querySelector('p').textContent = images[i].description;
        image_block.querySelector('img').src = images[i].url;
        image_block.querySelector('a').href = images[i].url;
        image_block.style.display = "";
        images_block.appendChild(image_block);
    }
};

load_all_images();
