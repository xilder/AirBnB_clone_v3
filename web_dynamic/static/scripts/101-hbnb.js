const api = 'http://' + window.location.hostname;
$('document').ready(function () {
  status_available();
  init_load_places();
  search_places();
});

function status_available() {
  $.get(api + ':5001/api/v1/status/', function (response) {
    if (response.status === 'OK') {
      $('DIV#api_status').addClass('available');
    } else {
      $('DIV#api_status').removeClass('available');
    }
  });
}
function init_load_places() {
  $.ajax({
    url: api + ':5001/api/v1/places_search/',
    type: 'POST',
    data: '{}',
    contentType: 'application/json',
    dataType: 'json',
    success: appendPlaces
  });
}

function search_places() {
  let amenities = {};
  $('.amenities input[type="checkbox"]').change(function () {
    if ($(this).is(':checked')) {
      amenities[$(this).attr('data-id')] = $(this).attr('data-name');
    } else {
      delete amenities[$(this).attr('data-id')];
    }
	  console.log($(this))
    if (Object.values(amenities).length === 0) {
      $('.amenities H4').html('&nbsp;');
    } else {
      $('.amenities H4').text(Object.values(amenities).join(', '));
    }
  });
  let states = {};
  $('.state_input').change(function () {
    if ($(this).is(':checked')) {
      states[$(this).attr('data-id')] = $(this).attr('data-name')
    } else {
      delete states[$(this).attr('data-id')]
    }
    let locations = Object.assign({}, states, cities)
    if (Object.keys(locations).length === 0) {
       $('.locations h4').html('&nbsp;');
    } else {
      $('.locations h4').text(Object.values(locations).join(', '));
    }
  });
  let cities = {};
  $('.city_input').change(function () {
    if ($(this).is(':checked')) {
      cities[$(this).attr('data-id')] = $(this).attr('data-name')
    } else {
      delete cities[$(this).attr('data-id')]
    }
    let locations = Object.assign({}, states, cities)
    if (Object.keys(locations).length === 0) {
      $('locations h4').html('&nbsp');
    } else {
      $('.locations h4').text(Object.values(locations).join(', '));
    }
  });


  $('BUTTON').click(function () {
    $.ajax({
      url: api + ':5001/api/v1/places_search/',
      type: 'POST',
      data: JSON.stringify({
	'states': Object.keys(states),
	'cities': Object.keys(cities),
	'amenities': Object.keys(amenities)
      }),
      contentType: 'application/json',
      dataType: 'json',
      success: appendPlaces
    });
  });
}

function appendPlaces (data) {
  $('SECTION.places').empty();
  data.map(place => {
    place_holder =`<ARTICLE>
              <DIV class="title_box">
                <H2>${place.name}</H2>
                  <DIV class="price_by_night">
                    \$${place.price_by_night}
                  </DIV>
                </DIV>
                <DIV class="information">
                  <DIV class="max_guest">
                    <I class="fa fa-users fa-3x" aria-hidden="true"></I>
                    </BR>
                    ${place.max_guest} Guest${
			    place.max_guest > 1 ? "s" : ""
		    }</DIV>
                  <DIV class="number_rooms">
                    <I class="fa fa-bed fa-3x" aria-hidden="true"></I>
                    </BR>
                    ${place.number_rooms} Bedroom${
			    place.number_rooms > 1 ? "s" : ""
		    }</DIV>
                  <DIV class="number_bathrooms">
                    <I class="fa fa-bath fa-3x" aria-hidden="true"></I>
                    </BR>
                    ${place.number_bathrooms} Bathroom${
			    place.number_bathrooms > 1 ? "s" : ""
		    }</DIV>
                </DIV>
                <DIV class="description">
                  ${place.description}
                </DIV>
		<div class="reviews">
          <h2>Reviews <span class="reviewSpan" data-id="${place.id}">show</span></h2>
          <ul>
          </ul>
          </div>

              </ARTICLE>`;
	  $('SECTION.places').append(place_holder);
  });
	$('.reviewSpan').click(function (event) {
        	console.log('here');
        	$.ajax(`${api}:5001/api/v1/places/${$(this).attr('data-id')}/reviews`).done(function (data) {
                	if ($('span').text('show')) {
                        	for (const review of data) {
                                	$('.reviews ul').append(`<li>${review.text}</li>`);
                        	}
                        	$('span').text('hide');
                	} else {
                        	$('.reviews ul').empty();
                        	$('span').text('show');
                	}
		});
	});
}
