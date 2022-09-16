const IP = "localhost";
const PORT = "8000";
 const URL = "http://" + IP + ":" + PORT + "/";

async function getTweets(tweets) {
    return fetch(URL + "tweet?id=" + tweets.join(",")).then(response => response.json());
}

async function sendTweet(tweet, user) {
    return fetch(URL + "tweet/" + user, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(tweet)
    }).then(response => response.json());
}

async function deleteTweet(tweet_id, user) {
    return fetch(URL + "tweet/" + user + "/" + tweet_id, {
        method: "DELETE"
    }).then(response => response.json());
}

async function getUserTimeline(user) {
    return fetch(URL + "timeline/" + user + "/user").then(response => response.json());
}

async function getHomeTimeline(user) {
    return fetch(URL + "timeline/" + user + "/home").then(response => response.json());
}

async function getFollowers(user) {
    return fetch(URL + "follower/" + user).then(response => response.json());
}

async function followUser(user, follower) {
    return fetch(URL + "follower/" + user + "/" + follower, {
        method: "POST"
    }).then(response => response.json());
}

async function unfollowUser(user, follower) {
    return fetch(URL + "follower/" + user + "/" + follower, {
        method: "DELETE"
    }).then(response => response.json());
}

async function getProfile(user) {
    return fetch(URL + "user/" + user).then(response => response.json());
}

export {
    getTweets,
    sendTweet,
    deleteTweet,
    getUserTimeline,
    getHomeTimeline,
    getFollowers,
    followUser,
    unfollowUser,
    getProfile
};