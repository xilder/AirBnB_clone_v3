const $ = window.$;
('document').ready(() => {
  const amenities = {};
  $('INPUT[type=checkbox]').change(() => {
    if (this.checked) {
      amenities[this.dataset.id] = this.dataset.id;
    } else {
      delete amenities[this.dataset.name];
    }
    $('.amenities h4').text(Object.values(amenities).sort().join(', '));
  });
});
