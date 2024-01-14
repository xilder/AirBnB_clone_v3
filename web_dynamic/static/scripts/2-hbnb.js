$('document').ready(() => {
	const url = `http://${HOST}:5001/api/v1/status`
	$.get(url, (data) => {
		if (data.status === 'OK') {
			$('div#api_status').addClass('available');
		} else {
			$('div#api_status').removeClass('available');
	let amenities = {}
	$('INPUT[type="checkbox"]').change(() => {
		if ($(this).is(':checked')) {
			amenities[$(this).attr('data-id')] = $(this).attr('data-name');
		} else {
			delete amenities[$(this).attr('data-id')];
		}
		$('.amenities h4').text(Object.values(amenities).join(', '));
	});
});
