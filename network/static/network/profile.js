document.addEventListener('DOMContentLoaded', function() {

    load_profile();
});

function load_profile() {
    document.querySelector('#post').innerHTML = "";
    username = document.querySelector("#profile-name").innerHTML;
    curr_user = document.querySelector('#curr-user').innerHTML.replace(/<(\/)?strong[^>]*>/g, "");
    load_posts(username);
    load_followers(username);
    if (curr_user == username) {
        document.getElementById('follow-btn').style.display = 'none';
    }
    document.getElementById('follow-btn').addEventListener('click', () => {
        follow(username);
    })
};

function load_followers(username) {
    curr_user = document.querySelector('#curr-user').innerHTML.replace(/<(\/)?strong[^>]*>/g, "");
    document.querySelector('.followerList').innerHTML = "";
    fetch(`/follow/${username}`)
        .then(response => response.json())
        .then(followers => {
            if (followers.length > 0 ) {
                document.querySelector('.followerCount').style.cursor = 'pointer';
            }
            document.querySelector('.followerCount').innerHTML = `<span class='bld'>${followers.length}</span> Followers`;
            followers.forEach(followers => {
                const follower_user = document.createElement('div');
                follower_user.innerHTML = `<span class="pointer">${followers}</span>`;
                follower_user.addEventListener('click', function () {
                    var url = "profile";
                    document.location.pathname = `profile/${followers}`;
                })
                if (curr_user == followers) {
                    document.getElementById('follow-btn').innerHTML = 'Unfollow'
                } else {
                    document.getElementById('follow-btn').innerHTML = 'Follow'
                }
                document.querySelector('.followerList').append(follower_user);
            })
        })
}


function load_posts(user) {
    fetch(`/posts/${user}`)
        .then(response => response.json())
        .then(posts => {
            posts.forEach(posts => {
                const post_item = document.createElement('div');
                const post_user = document.createElement('div');
                const edit_link = document.createElement('div');
                const post_details = document.createElement('div');
                const tmstmp = document.createElement('div');
                const post_likes = document.createElement('div');
                const cmnt_btn = document.createElement('div');
                const view_cmnt = document.createElement('div');
                const comment_box = document.createElement('div');
                const like_list = document.createElement('ul');
                const show_likers = document.createElement('div');
                const like_modal = document.createElement('div');

                comment_box.className = 'comment-box';
                comment_box.id = `comments${posts.id}`
                //comments = posts.comments;
                //comments.forEach(comments => {
                    //const comment = document.createElement('div');
                    //comment.className = "comment-box-cmnt";
                    //const commenter = document.createElement('div');
                    //commenter.className = "comment-box-cmntr";
                    //commenter.addEventListener('click', function () {
                        //var url = "profile";
                        //var username = comments.commenter;
                        //document.location.pathname = `${url}/${username}`;
                    //})
                    //const cmnt_time = document.createElement('div');
                    //cmnt_time.className = 'comment-box-time';
                    //comment.innerHTML = `<span class='cursor'>${comments.comment}</span>`;
                    //commenter.innerHTML = `<span class='pointer uline'>${comments.commenter}</span>`;
                    //cmnt_time.innerHTML = `<span class='cursor'>${comments.timestamp}</span>`;
                    //comment_box.append(cmnt_time);
                    //comment_box.append(commenter);
                    //comment_box.append(comment);
                //})
                //load_comments(posts);
                show_likers.className = 'show-likers-btn';
                show_likers.innerHTML = (`<div id='show-likes-list${posts.id}'>${posts.likers}</div>`).replace(/,/g, ", ");
                show_likers.id = `showlikers${posts.id}`;

                post_likes.innerHTML = `<div class="bld"><span id='heart${posts.id}' class='heart'>&#10084; ${posts.likers.length}</span></div>`;
                post_likes.className = 'post-likes';

                tmstmp.innerHTML = `<span class='cursor'>${posts.timestamp}</span>`;
                tmstmp.className = 'tmstmp';

                cmnt_btn.innerHTML = `<div data-toggle='modal' data-target='#addCommentModal' data-whatever='comment'><span class='pointer'>Add Comment</span></div>`;
                cmnt_btn.className = 'cmnt-btn';
                cmnt_btn.id =  `cmnt_btn${posts.id}`;
                cmnt_btn.addEventListener('click', () => comment_modal(posts));
                cmnt_count = posts.comments.length;
                view_cmnt.innerHTML = `<div id='showComments${posts.id}'><span id='show_comments${posts.id}'>Comments </span><span id='cmnt_cnt${posts.id}'>(${cmnt_count})</span></div>`;
                view_cmnt.className = 'cmnt-btn-right show';
                
                post_item.className = 'post_item';
                post_item.id = posts.id;

                post_user.innerHTML = `<span class='cursor'>${posts.poster}</span>`;
                post_user.className = 'bld post-uname';

                post_details.id = `post${posts.id}`;
                post_details.innerHTML = `<div>${posts.post}</div>`;
                post_details.className = 'post-text'

                edit_link.id = `link${posts.id}`;
                edit_link.className = 'post-edit-lnk';
                edit_link.innerHTML = "<a href='#'>Edit Post</a>";
                
                document.querySelector('#post').append(post_item);
                document.getElementById(post_item.id).append(tmstmp);
                document.getElementById(post_item.id).append(post_user);
                document.getElementById(post_item.id).append(edit_link);
                document.getElementById(post_item.id).append(post_details);
                document.getElementById(post_item.id).append(post_likes);
                document.getElementById(post_item.id).append(show_likers);
                document.getElementById(post_item.id).append(cmnt_btn);
                document.getElementById(post_item.id).append(view_cmnt);
                
                listlen = document.getElementById(`show-likes-list${posts.id}`);
                listlen.style.width = 'auto';
        
                if (listlen.clientWidth > 160) {
                    document.getElementById(`show-likes-list${posts.id}`).style.cursor = 'pointer';
                }
                listlen.style.width = '10rem';

                document.getElementById(`heart${posts.id}`).addEventListener('click', () => likeunlike(posts.id, posts.likers));
                
                if (document.getElementById(`showlikers${posts.id}`).className == 'show-likers-btn') {
                    document.getElementById(`showlikers${posts.id}`).addEventListener('click', () => show_liker_list(posts.id));
                }
                 
                if ( curr_user != posts.poster ) {
                    document.getElementById(edit_link.id).style.display = "none";
                }
                document.querySelector("#post").append(comment_box);
                update_comments(posts);
                if (cmnt_count > 0) {
                    document.getElementById(`show_comments${posts.id}`).style.cursor = 'pointer';
                    document.getElementById(`show_comments${posts.id}`).addEventListener('click', () => {
                        
                        show_comments(posts.id);
                    });
                } 
            });
        })
}

function update_comments(posts) {
    fetch(`/posts/comments/${posts.id}`)
        .then(response => response.json())
        .then(comments => {

            document.getElementById(`comments${posts.id}`).innerHTML = '';
            const view_cmnt = document.createElement('div');
            console.log(`Post Id: ${posts.id}`);
            console.log(`Post Comments: ${posts.comments}`)
            comment_box = document.getElementById(`comments${posts.id}`);
            comments = posts.comments;
            console.log(comments);
            comments.forEach(comments => {
                const comment = document.createElement('div');
                comment.className = "comment-box-cmnt";
                const commenter = document.createElement('div');
                commenter.className = "comment-box-cmntr bld";
                commenter.addEventListener('click', function () {
                    var url = "profile";
                    var username = comments.commenter;
                    document.location.pathname = `${url}/${username}`;
                })
                const cmnt_time = document.createElement('div');
                cmnt_time.className = 'comment-box-time';
                comment.innerHTML = `<span class='cursor'>${comments.comment}</span>`;
                commenter.innerHTML = `<span class='pointer uline'>${comments.commenter}</span>`;
                cmnt_time.innerHTML = `<span class='cursor'>${comments.timestamp}</span>`;
                comment_box.append(cmnt_time);
                comment_box.append(commenter);
                comment_box.append(comment);
                console.log('end of comment loop');

            })
            cmnt_count = posts.comments.length;
            document.getElementById(`cmnt_cnt${posts.id}`).innerHTML = `(${cmnt_count})`;
        })
    }



function follow(username) {
    fetch(`/follow/${username}`, {
        method: 'POST',
        body: JSON.stringify({
            to_person: username
        })
    })
    .then(response => response.text())
    .then(result => {
        console.log(result);
        load_followers(username);
    });
    
    //load_followers(username);
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
    document.getElementById('cmnt-sub-btn').addEventListener('click', () => {
        console.log('comment button clicked');
        add_comment(posts);
    });
}

async function add_comment(posts) {
    comment_text = document.querySelector('#comment-text').value;
    document.querySelector('#new-cmnt-form').addEventListener('submit', (event) => {
        event.preventDefault();
    })
    await fetch(`/posts/comments/${posts.id}`, {
        method: 'POST',
        body: JSON.stringify({
            comment: comment_text
        })

    })
    .then(response => response.text())
    .then(result => {
        console.log(result);
        //console.log('load_comments function called');
        //update_comments(posts);
    })
    .then(update => {
        setTimeout(() => {
            console.log('load_comments function called');
            update_comments(posts);
        }, 1000)
    });
    document.querySelector('#comment-text').value = "";
};

function show_liker_list(postId) {
    show_likers = document.getElementById(`show-likes-list${postId}`);
    show_likers.style.width = 'auto';
    document.getElementById(`showlikers${postId}`).removeEventListener('click', () => show_liker_list(postId));
    document.getElementById(`showlikers${postId}`).addEventListener('click', () => hide_liker_list(postId));
};
function hide_liker_list(postId) {
    show_likers = document.getElementById(`show-likes-list${postId}`);
    show_likers.style.width = '8rem';
    document.getElementById(`showlikers${postId}`).removeEventListener('click', () => hide_liker_list(postId));
    document.getElementById(`showlikers${postId}`).addEventListener('click', () => show_liker_list(postId));
};

function show_comments(postId) {
    show_button = document.getElementById(`show_comments${postId}`);
    cmnt_box = document.getElementById(`comments${postId}`);
    cmnt_box.className = 'comment-box';
    cmnt_box.style.animationPlayState = 'running';
    show_button.innerHTML = `<span id='show_comments${postId}' class='pointer'>Hide Comments </span>`;
    show_btn = document.getElementById(`show_comments${postId}`);
    show_btn.removeEventListener('click', () => show_comments(postId, cmnt_count));
    show_btn.addEventListener('click', () => hide_comments(postId, cmnt_count));
}
function hide_comments(postId) {
    show_button = document.getElementById(`show_comments${postId}`);
    cmnt_box = document.getElementById(`comments${postId}`);
    cmnt_box.className = 'hide-cmnt-box';
    cmnt_box.style.animationPlayState = 'running';
    show_button.innerHTML = `<span id='show_comments${postId}' class='pointer'>Comments </span>`;
    show_btn = document.getElementById(`show_comments${postId}`);
    show_btn.removeEventListener('click', () => hide_comments(postId, cmnt_count));
    show_btn.addEventListener('click', () => show_comments(postId, cmnt_count));
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
            document.getElementById(`heart${posts.id}`).innerHTML = `<div class="bld"><span id='heart${posts.id}' class='heart'>&#10084; ${posts.likers.length}</span></div>`;
            document.getElementById(`showlikers${posts.id}`).innerHTML = (`<div id='show-likes-list${posts.id}'>${posts.likers}</div>`).replace(/,/g, ", ");
        });
}