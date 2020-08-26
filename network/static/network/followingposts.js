var start = 0;
var end = start + 30;
var page = 1;
curr_user = '';

document.addEventListener('DOMContentLoaded', function() { 
    curr_user = document.querySelector('#curr-user').innerHTML.replace(/<(\/)?strong[^>]*>/g, "");
    load_page();
    page = 1;
    start = 0;
    end = start + 30;
    
});

function load_page() {
    document.querySelector('#post').innerHTML = "";
    fetch_posts_data(curr_user);
};

function fetch_posts_data(user = curr_user, start = 0, end = 30) {
    if (start == 0) {
        page = 1;
    }
    document.getElementById('post').innerHTML = "";
    if (start == 0) {
        document.querySelector('#previous').className = 'disabled';
    }
    else {
        document.querySelector('#previous').className = 'previous pointer';
    }
    curr_user = document.querySelector('#curr-user').innerHTML.replace(/<(\/)?strong[^>]*>/g, "");

    fetch(`/user/${user}/following/posts?start=${start}&end=${end}`)
        .then(response => response.json())
        .then(posts => {
            console.log(posts)
            load_posts(posts)
        })
    }

document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#next').onclick = e => {
        start = start + 10;
        end = end + 10;
        page++;
        let data = {
            user: curr_user,
            start: start,
            end: end,
            page: page,
        }

        paginate_forward(data);
    }
    document.querySelector('#previous').onclick = e => {
        start = start - 10;
        end = end - 10;
        page--;
        let data = {
            user: curr_user,
            start: start,
            end: end,
            page: page,
        }
        paginate_back(data);
    }
});
    
function paginate_forward(data) {
    fetch_posts_data(data.user, data.start, data.end);
    }

function paginate_back(data) {
    fetch_posts_data(data.user, data.start, data.end);
}
