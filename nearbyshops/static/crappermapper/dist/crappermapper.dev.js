"use strict";

document.addEventListener('DOMContentLoaded', function () {
  document.querySelector('#new-review-form').addEventListener('submit', function (event) {
    event.preventDefault();
  });
  document.querySelector('#new-john-form').addEventListener('submit', function (event) {
    event.preventDefault();
  });
});

function avg_review(john) {
  reviewCount = john.reviews.length;
  var avgReview;

  if (reviewCount > 0) {
    var reviewTotal = 0;
    john.reviews.forEach(function (review) {
      reviewTotal += review.rating;
    });
    avgReview = reviewTotal / reviewCount;
  }

  return avgReview;
}

function submit_review_edit(currentJohn) {
  latlng = {
    'lat': currentJohn.geometry.coordinates[0],
    'lng': currentJohn.geometry.coordinates[1]
  };
  fetch("/review", {
    method: 'PUT',
    body: JSON.stringify({
      review_title: document.querySelector('#review_title').value,
      review_text: document.querySelector('#review_text').value,
      review_rating: getRadioValue(),
      john_id: currentJohn.id
    }),
    credentials: 'same-origin',
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    }
  }).then(function (response) {
    return response.text();
  }).then(function (result) {
    console.log(result);
    buildLocationList(latlng, 'all');
    setTimeout(update_popup, 1000, currentJohn.id);
  });
}

function update_popup(currentJohnId) {
  fetch("/fetch_data/".concat(currentJohnId)).then(function (response) {
    return response.json();
  }).then(function (johns) {
    createPopUp(johns.data[0]);
  });
}

function submit_new_john(latlng) {
  fetch("/add_new_john", {
    method: 'POST',
    body: JSON.stringify({
      location: document.querySelector('#njf-location').value,
      street_no: document.querySelector('#njf-street-no').value,
      street_name: document.querySelector('#njf-street-name').value,
      city: document.querySelector('#njf-city').value,
      state: document.querySelector('#njf-state').value,
      zip_code: document.querySelector('#njf-zip').value,
      county: document.querySelector('#njf-county').value,
      country: document.querySelector('#njf-country').value,
      address: document.querySelector('#njf-address').value,
      lat: latlng.lat,
      lng: latlng.lng
    }),
    credentials: 'same-origin',
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    }
  }).then(function (response) {
    return response.text();
  }).then(function (newJohnId) {
    if (newJohnId === "alreadyExists") {
      alert("Error: This Crapper location has already been added.");
      var popUps = document.getElementsByClassName('leaflet-popup');
      if (popUps[0]) popUps[0].remove();
    } else if (newJohnId !== "alreadyExists") {
      fetch("/fetch_data/".concat(newJohnId)).then(function (response) {
        return response.json();
      }).then(function (newJohn) {
        submit_review(newJohn.data[0]);
      });
    }
  });
}

function submit_review(currentJohn) {
  latlng = {
    'lat': currentJohn.geometry.coordinates[0],
    'lng': currentJohn.geometry.coordinates[1]
  };
  fetch("/review", {
    method: 'POST',
    body: JSON.stringify({
      review_title: document.querySelector('#review_title').value,
      review_text: document.querySelector('#review_text').value,
      review_rating: getRadioValue(),
      john_id: currentJohn.id
    }),
    credentials: 'same-origin',
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    }
  }).then(function (response) {
    return response.text();
  }).then(function (result) {
    console.log(result);
    buildLocationList(latlng, 'all');
    setTimeout(update_popup, 1000, currentJohn.id);
  });
}

function new_review_modal(currentJohn) {
  document.querySelector('#newReviewModal').hidden = false;
  document.querySelector('#new-review-form-error').style.display = 'none';
  document.querySelector('#new-review-form-loc-name').innerHTML = currentJohn.display_name;
  document.querySelector('#review_title').value = "";
  document.querySelector('#review_text').value = "";
  document.querySelector('#newReviewModalLabel').innerHTML = 'What did you think of this Crapper?';

  if (document.querySelector('#submit_review_edit')) {
    document.querySelector('#submit_review_edit').id = 'submit_review';
  }

  stars = document.getElementsByName('star');

  document.querySelector('#submit_review').onclick = function () {
    document.querySelector('#new-review-form-error').style.display = 'block';
  };

  stars.forEach(function (star) {
    if (star.checked == true) {
      star.checked = false;
    }
  });
  stars.forEach(function (star) {
    var isRated = false;

    star.onchange = function () {
      isRated = check_selection();

      if (isRated == false) {
        document.querySelector('#submit_review').onclick = function () {
          document.querySelector('#new-review-form-error').style.display = 'block';
        };
      } else {
        document.querySelector('#submit_review').onclick = function () {
          document.querySelector('#newReviewModal').hidden = true;
          document.querySelector('.modal-backdrop').classList.replace('show', 'hide');
          submit_review(currentJohn);
        };
      }
    };
  });
}

function open_edit_review_modal(currentJohn, currentUser) {
  document.querySelector('#newReviewModal').hidden = false;
  document.querySelector('#new-review-form-error').style.display = 'none';
  document.querySelector('#new-review-form-loc-name').innerHTML = currentJohn.display_name;
  currentJohn.reviews.forEach(function (review) {
    if (currentUser == review.username) {
      document.querySelector('#review_title').value = review.review_title;
      document.querySelector('#review_text').value = review.review_text;
      document.querySelector("#star".concat(review.rating)).checked = true;
      document.querySelector('#newReviewModalLabel').innerHTML = 'Update your review...';
    }
  });

  if (document.querySelector('#submit_review')) {
    document.querySelector('#submit_review').id = 'submit_review_edit';
  }

  fetch("/fetch_data/".concat(currentJohn.id)).then(function (response) {
    return response.json();
  }).then(function (johns) {
    console.log(johns.data[0]);
  });

  document.getElementById('submit_review_edit').onclick = function () {
    submit_review_edit(currentJohn);
    document.querySelector('#newReviewModal').hidden = true;
    document.querySelector('.modal-backdrop').classList.replace('show', 'hide');
  };
}

function getRadioValue() {
  var ele = document.getElementsByName('star');

  for (i = 0; i < ele.length; i++) {
    if (ele[i].checked) {
      return ele[i].value;
    }
  }
}

function getCookie(name) {
  var cookieValue = null;

  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');

    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);

      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }

  return cookieValue;
}

function check_selection() {
  var rated = false;
  stars = document.getElementsByName('star');
  stars.forEach(function (star) {
    if (star.checked == true) {
      rated = true;
    }
  });
  return rated;
}