document.addEventListener('DOMContentLoaded', function() {
    load_profile();
});

function load_profile() {
    document.querySelector('#post').innerHTML = "";
    username = document.querySelector("#profile-name").innerHTML;
    if (document.querySelector('#curr-user')) {
        curr_user = document.querySelector('#curr-user').innerHTML.replace(/<(\/)?strong[^>]*>/g, "");
    } 
    else { curr_user = 'none'}
    
    get_posts(username);
    load_followers(username);
    if (curr_user == username) {
        document.getElementById('follow-btn').style.display = 'none';
    }
    document.getElementById('follow-btn').onclick = () => follow(username);
};

function load_followers(username) {
    curr_prof_user = document.querySelector('#profile-name').innerHTML;
    curr_user = document.querySelector('#curr-user').innerHTML.replace(/<(\/)?strong[^>]*>/g, "");
    document.querySelector('.followerList').innerHTML = "";
    document.querySelector('.followingList').innerHTML = "";
    document.getElementById('follow-btn').innerHTML = 'Follow'
    fetch(`/follow/${username}`)
        
        .then(response => response.json())
        .then(followers => {
            followercounter = 0;
            followingcounter = 0;
            curr_user_isfollowing = false;

            followers.forEach(follower => {
                if (curr_prof_user != follower.follower) {
                    followercounter++;
                    const follower_user = document.createElement('div');
                    follower_user.innerHTML = `<span id="follower_user${follower.follower}" class="pointer">${follower.follower}</span>`;
                    document.querySelector('.followerList').append(follower_user);
                    document.getElementById(`follower_user${follower.follower}`).onclick = () => {
                        var url = 'profile';
                        document.location.pathname = `profile/${follower.follower}`;
                    }
                }
                if (curr_prof_user == follower.follower) {
                    followingcounter++;
                    const following_user = document.createElement('div');
                    following_user.innerHTML = `<span id="following_user${follower.following}" class="pointer">${ follower.following }</span>`;
                    document.querySelector('.followingList').append(following_user);
                    document.getElementById(`following_user${follower.following}`).onclick = () => {
                        document.location.pathname = `profile/${follower.following}`;
                    }
                }
                if (curr_user == follower.follower) {
                    curr_user_isfollowing = true;
                    if (curr_user_isfollowing == true) {
                        document.getElementById('follow-btn').innerHTML = 'Unfollow';
                    }
                } 
            })
            document.querySelector('.followerCount_btn').innerHTML = `<span class='bld'>${followercounter}</span> Followers`;
            document.querySelector('.followingCount_btn').innerHTML = `<span class='bld'>${followingcounter}</span> Following`;
            if (followercounter > 0 ) {
                document.querySelector('.followerCount_btn').style.cursor = 'pointer';
                document.querySelector('.followerCount_btn').style.pointerEvents = 'auto';
            }
            if (followingcounter > 0 ) {
                document.querySelector('.followingCount_btn').style.cursor = 'pointer';
                document.querySelector('.followingCount_btn').style.pointerEvents = 'auto';
            }
            if (followercounter == 0 ) {
                document.querySelector('.followerCount_btn').style.cursor = 'default';
                document.querySelector('.followerCount_btn').style.pointerEvents = 'none';
            }
            if (followingcounter == 0 ) {
                document.querySelector('.followingCount_btn').style.cursor = 'default';
                document.querySelector('.followingCount_btn').style.pointerEvents = 'none';
            }
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
}
