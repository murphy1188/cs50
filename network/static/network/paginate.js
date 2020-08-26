var start = 0;
var end = start + 30;
var page = 1;

function reset_pagination() {
    start = 0;
    end = start + 30;
    page = 1;
}
document.addEventListener('DOMContentLoaded', function() {
    
    if (document.querySelector('#profile-name')) {
        profile_name = document.querySelector('#profile-name').innerHTML;
    } 
    else profile_name = 'all';
    console.log(profile_name);

    document.querySelector('#next').onclick = e => {
        start = start + 10;
        end = end + 10;
        page++;
        let data = {
            user: profile_name,
            start: start,
            end: end,
            page: page,
        }

        history.pushState(data, '',  `/profile/${profile_name}` + `/page` + page);
        paginate_forward(data);
    }
    document.querySelector('#previous').onclick = () => {
        start = start - 10;
        end = end - 10;
        page--;
        let data = {
            user: profile_name,
            start: start,
            end: end,
            page: page,
        }
        history.pushState(data, '',  `/profile/${profile_name}` + `/page` + page);
        paginate_back(data);
    }
});

function paginate_forward(data) {
    get_posts(data.user, data.start, data.end);
    }

window.addEventListener("popstate", e => {
    get_posts(e.state.user, e.state.start, e.state.end);
    page = e.state.page;
    start = e.state.start;
    end = e.state.end;
});
history.replaceState({data: null}, 'Default state', '')

function paginate_back(data) {
    get_posts(data.user, data.start, data.end);
}