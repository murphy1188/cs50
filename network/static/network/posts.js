document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#new-cmnt-form').addEventListener('submit', (event) => {
        event.preventDefault();
    })
});

function submit_post() {
    document.querySelector('#new-post-form').addEventListener('submit', (event) => {
        event.preventDefault();
    })
    fetch('/posts', {
        method: 'POST',
        body: JSON.stringify({
            poster: document.querySelector('#poster').value,
            post: document.querySelector('#new_post_body').value,
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
    });

    history.pushState('', '', '/');
    reset_pagination();
    load_home();
    
};
function get_posts (user = 'all', start = 0, end = 30) {
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
    if (curr_user = document.querySelector('#curr-user')) {
        curr_user = document.querySelector('#curr-user').innerHTML.replace(/<(\/)?strong[^>]*>/g, "");
    }
    else curr_user = 'none';
    

    fetch(`/posts/${user}?start=${start}&end=${end}`)
        .then(response => response.json())
        .then(posts => {
            load_posts(posts);
        })
}

function load_posts(posts) {
    if (posts.length < 11) {
        document.querySelector('#next').className = 'disabled';
    }
    else {
        document.querySelector('#next').className = 'next pointer';
    }
    posts = posts.slice(0,10);
    posts.forEach(posts => {
        const post_item = document.createElement('div');
        const post_user = document.createElement('div');
        const edit_link = document.createElement('div');
        const post_details = document.createElement('div');
        const tmstmp = document.createElement('div');
        const post_likes = document.createElement('div');
        const cmnt_btn = document.createElement('div');
        const view_cmnt = document.createElement('div');
        const hide_cmnt = document.createElement('div');
        const comment_box = document.createElement('div');
        const like_list = document.createElement('ul');
        const show_likers = document.createElement('div');
        const like_modal = document.createElement('div');
        comment_box.className = 'comment-box';
        comment_box.id = `comments${posts.id}`
        comments = posts.comments;
        comments.forEach(comments => {
            const comment = document.createElement('div');
            comment.className = "comment-box-cmnt";
            const commenter = document.createElement('div');
            commenter.className = "comment-box-cmntr bld";
            commenter.onclick = () => { document.location.pathname = `profile/${comments.commenter}`; }
            const cmnt_time = document.createElement('div');
            cmnt_time.className = 'comment-box-time';
            comment.innerHTML = `<span class='cursor'>${comments.comment}</span>`;
            commenter.innerHTML = `<span class='pointer hov'>${comments.commenter}</span>`;
            cmnt_time.innerHTML = `<span class='cursor'>${comments.timestamp}</span>`;
            comment_box.append(cmnt_time);
            comment_box.append(commenter);
            comment_box.append(comment);
        })

        show_likers.className = 'show-likers-btn';
        show_likers.innerHTML = (`<div id='show-likes-list${posts.id}'>${posts.likers}</div>`).replace(/,/g, ", ");
        show_likers.id = `showlikers${posts.id}`;

        post_likes.innerHTML = `<div class="bld"><span id='heart${posts.id}' class='heart'>&#10084; </span><span class="likes_count" id='likes_count${posts.id}'>${posts.likers.length}</span></div>`;
        post_likes.className = 'post-likes';

        tmstmp.innerHTML = `<span class='cursor'>${posts.timestamp}</span>`;
        tmstmp.className = 'tmstmp';

        cmnt_btn.innerHTML = `<div data-toggle='modal' data-target='#addCommentModal' data-whatever='comment'><span class='pointer'>Add Comment</span></div>`;
        cmnt_btn.className = 'cmnt-btn';
        cmnt_btn.id =  `cmnt_btn${posts.id}`;
        cmnt_btn.onclick = () => comment_modal(posts);
        cmnt_count = posts.comments.length;
        view_cmnt.innerHTML = `<div class="showComments" id='showComments${posts.id}'><span id='show_comments${posts.id}'>Comments </span><span id='scmnt_cnt${posts.id}'>(${cmnt_count})</span></div>`;
        view_cmnt.className = 'cmnt-btn-right show';
        view_cmnt.id = `comShow${posts.id}`;
        hide_cmnt.innerHTML = `<div id='hideComments${posts.id}'><span id='hide_comments${posts.id}'>Hide Comments </span><span id='hcmnt_cnt${posts.id}'>(${cmnt_count})</span></div>`;
        hide_cmnt.className = 'cmnt-btn-right hide';
        hide_cmnt.id = `comHide${posts.id}`;
        
        post_item.className = 'post_item';
        post_item.id = posts.id;

        post_user.innerHTML = `${posts.poster}`;
        post_user.className = 'bld post-uname pointer';
        post_user.onclick = () => { document.location.pathname= `profile/${posts.poster}`; }

        post_details.id = `post${posts.id}`;
        post_details.innerHTML = posts.post;
        post_details.className = 'post-text'

        edit_link.id = `link${posts.id}`;
        edit_link.className = 'post-edit-lnk';
        edit_link.innerHTML = "<div data-toggle='modal' data-target='#editPostModal' data-whatever='edit-post'><span class='pointer blue'>Edit Post</span></div>";
        edit_link.onclick = () => edit_post_modal(posts);

        document.querySelector('#post').append(post_item);
        document.getElementById(post_item.id).append(tmstmp);
        document.getElementById(post_item.id).append(post_user);
        if (curr_user == posts.poster) {
            document.getElementById(post_item.id).append(edit_link);
        }
        document.getElementById(post_item.id).append(post_details);
        document.getElementById(post_item.id).append(post_likes);
        document.getElementById(post_item.id).append(show_likers);
        document.getElementById(post_item.id).append(cmnt_btn);
        document.getElementById(post_item.id).append(view_cmnt);
        document.getElementById(post_item.id).append(hide_cmnt);
        
        listlen = document.getElementById(`show-likes-list${posts.id}`);
        listlen.style.width = 'auto';
        if (listlen.clientWidth > 160) {
            document.getElementById(`show-likes-list${posts.id}`).style.cursor = 'pointer';
            document.getElementById(`show-likes-list${posts.id}`).className = 'showlikersHov';
        }
        listlen.style.width = '8rem';

        document.getElementById(`heart${posts.id}`).onclick = () => likeunlike(posts.id, posts.likers)
        document.getElementById(`show-likes-list${posts.id}`).onclick = () => show_liker_list(posts.id);
            
        document.querySelector("#post").append(comment_box);
        
        if (cmnt_count > 0) {
            document.getElementById(`show_comments${posts.id}`).className = 'pointer';
            document.getElementById(`hide_comments${posts.id}`).className = 'pointer';
            document.getElementById(`show_comments${posts.id}`).onclick = () => show_comments(posts.id);
            document.getElementById(`hide_comments${posts.id}`).onclick = () => hide_comments(posts.id);
        } 
    })
}

function edit_post(post) {
    post_text = document.querySelector('#edit-post-text');
    fetch(`/postss/${post.id}`, {
        method: 'PUT',
        body: JSON.stringify({
            post: post_text.value
        })
        })
        .then(response => {
            response.text();
        
        });
    document.getElementById(`post${post.id}`).innerHTML =  post_text.value;   
}
function edit_post_modal(post) {
    post_text = document.querySelector('#edit-post-text');
    post_text.value = document.getElementById(`post${post.id}`).innerHTML
    document.getElementById('edit-post-sub-btn').onclick = () => edit_post(post);
}

function comment_modal(posts) {
    const newComm = document.getElementById('comment-text');
    newComm.value = '';
    document.getElementById('cmnt-sub-btn').disabled = true;
    document.getElementById('cmnt-sub-btn').style.cursor = 'default';
    
    newComm.onkeyup = () => {
        if (newComm.value.length > 0) {
            document.getElementById('cmnt-sub-btn').disabled = false;
            document.getElementById('cmnt-sub-btn').style.cursor = 'pointer';
        } 
        else {
            document.getElementById('cmnt-sub-btn').disabled = true;
            document.getElementById('cmnt-sub-btn').style.cursor = 'default';
        }
    }
    document.getElementById('cmnt-sub-btn').onclick = () => add_comment(posts);
}

function add_comment(posts) {
    comment_text = document.querySelector('#comment-text').value;
    
    fetch(`/posts/comments/${posts.id}`, {
        method: 'POST',
        body: JSON.stringify({
            comment: comment_text
        })
    })
    .then(response => response.text())
    .then(result => {
        console.log(result);
    });
    document.querySelector('#comment-text').value = "";
    setTimeout(update_comments, 1000, posts);
};

function update_comments(posts) {
    fetch(`/posts/comments/${posts.id}`)
        .then(response => response.json())
        .then(comments => {
            
            document.getElementById(`comments${posts.id}`).innerHTML = '';
            const view_cmnt = document.createElement('div');
            comment_box = document.getElementById(`comments${posts.id}`);
            comments = comments.comments;
            comments.forEach(comments => {
                const comment = document.createElement('div');
                comment.className = "comment-box-cmnt";
                const commenter = document.createElement('div');
                commenter.className = "comment-box-cmntr bld";
                commenter.onclick = () => {
                    var url = "profile";
                    var username = comments.commenter;
                    document.location.pathname = `${url}/${username}`;
                }
                const cmnt_time = document.createElement('div');
                cmnt_time.className = 'comment-box-time';
                comment.innerHTML = `<span class='cursor'>${comments.comment}</span>`;
                commenter.innerHTML = `<span class='pointer hov'>${comments.commenter}</span>`;
                cmnt_time.innerHTML = `<span class='cursor'>${comments.timestamp}</span>`;
                comment_box.append(cmnt_time);
                comment_box.append(commenter);
                comment_box.append(comment);
            })
            cmnt_count = comments.length;
            document.getElementById(`scmnt_cnt${posts.id}`).innerHTML = `(${cmnt_count})`;
            document.getElementById(`hcmnt_cnt${posts.id}`).innerHTML = `(${cmnt_count})`;
            document.getElementById(`show_comments${posts.id}`).onclick = () => show_comments(posts.id);
            document.getElementById(`show_comments${posts.id}`).style.cursor = 'pointer';
            document.getElementById(`hide_comments${posts.id}`).onclick = () => hide_comments(posts.id);
            document.getElementById(`hide_comments${posts.id}`).style.cursor = 'pointer';
        })
    }


function show_liker_list(postId) {
    show_likers = document.getElementById(`show-likes-list${postId}`);
    if (show_likers.style.width != 'auto') {
        show_likers.style.width = 'auto';
        show_likers.className = '';
        //show_likers.style.transform = 'none';
        //show_likers.style.webkittransform = 'none';
    } 
    else {
        show_likers.style.width = '8rem';
        show_likers.className = 'showlikersHov';
    }
};

function show_comments(postId) {
    show_button = document.getElementById(`comShow${postId}`);
    show_button.style.display = 'none';
    hide_button = document.getElementById(`comHide${postId}`);
    hide_button.style.display = 'inline-block';
    cmnt_box = document.getElementById(`comments${postId}`);
    cmnt_box.className = 'comment-box';
    cmnt_box.style.display = 'block';
    cmnt_box.style.animationPlayState = 'running';
}
function hide_comments(postId) {
    show_button = document.getElementById(`comShow${postId}`);
    hide_button = document.getElementById(`comHide${postId}`);
    show_button.style.display = 'inline-block';
    hide_button.style.display = 'none';
    cmnt_box = document.getElementById(`comments${postId}`);
    cmnt_box.className = 'hide-cmnt-box';
    cmnt_box.style.animationPlayState = 'running';
    setTimeout(function(){ cmnt_box.style.display = 'none'; }, 200);
}

function likeunlike(id, likers) {
    user_id = document.getElementById('user_id').value;
    fetch(`/postss/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            likers: user_id
        })
      })
      .then(response => {
          response.text();
          return like_count(id);
        });
}
function like_count(id) {
    fetch(`/postss/${id}`)
        .then(response => response.json())
        .then( posts => {
            //document.getElementById(`heart${posts.id}`).innerHTML = `<div class="bld"><span id='heart${posts.id}' class='heart'>&#10084; </span><span class='likes_count'>${posts.likers.length}</span></div>`;
            document.getElementById(`likes_count${posts.id}`).innerHTML = `${posts.likers.length}`;
            document.getElementById(`showlikers${posts.id}`).innerHTML = (`<div id='show-likes-list${posts.id}'>${posts.likers}</div>`).replace(/,/g, ", ");
            document.getElementById(`showlikers${posts.id}`).onclick = () => show_liker_list(posts.id);
        });
}