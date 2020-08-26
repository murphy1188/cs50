
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('open-post-form').onclick = () => { new_post_modal() };
    load_home();
});


function load_home() {
    document.querySelector('#post').innerHTML = "";
    document.querySelector('#submit_post').onclick = () => submit_post();
    get_posts();
};


function new_post_modal() {
    const newPost = document.getElementById('new_post_body');
    newPost.value = '';
    document.getElementById('submit_post').disabled = true;
    document.getElementById('submit_post').style.cursor = 'default';

    document.getElementById('new_post_body').onkeyup = () => {
        if (newPost.value.length > 0) {
            document.getElementById('submit_post').disabled = false;
            document.getElementById('submit_post').style.cursor = 'pointer';
        }
        else {
            document.getElementById('submit_post').disabled = true;
            document.getElementById('submit_post').style.cursor = 'default';
        }
    }

}

