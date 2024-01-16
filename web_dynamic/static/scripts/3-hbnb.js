const HOST = '0.0.0.0';
$('document').ready(() => {
	const url = `http://0.0.0.0:5001/api/v1/status`
	$.get(url, (data) => {
		if (data.status === 'OK') {
			$('div#api_status').addClass('available');
		} else {
			$('div#api_status').removeClass('available');
		}
	});

	let amenities = {}
	$('input[type="checkbox"]').change(() => {
		if (this.checked) {
			amenities[this.dataset.id] = this.dataset.name;
		} else {
			delete amenities[this.dataset.id];
		}
		$('.amenities h4').text(Object.values(amenities).sort().join(', '));
	});
});
