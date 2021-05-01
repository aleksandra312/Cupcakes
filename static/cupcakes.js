const BASE_URL = 'http://localhost/:5000/api';

async function showAllCupcakes() {
	const response = await axios.get(`${BASE_URL}/cupcakes`);

	console.log(response);
	for (let cupcakeData of response.data.cupcakes) {
		let cupcake = $(generateCupcakeHTML(cupcakeData));
		$('#cupcakes-list').append(cupcake);
	}
}

function generateCupcakeHTML(cupcake) {
	return `
      <div data-cupcake-id=${cupcake.id}>
        <li>
          ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
        </li>
        <img class="Cupcake-img"
              src="${cupcake.image}"
              alt="(no image provided)">
      </div>
    `;
}

$('#new-cupcake-form').on('submit', async function(evt) {
	evt.preventDefault();

	let flavor = $('#form-flavor').val();
	let size = $('#form-size').val();
	let rating = $('#form-rating').val();
	let image = $('#form-image').val();

	const response = await axios.post(`${BASE_URL}/cupcakes`, {
		flavor,
		size,
		rating,
		image
	});

	let newCupcake = $(generateCupcakeHTML(response.data.cupcake));
	$('#cupcakes-list').append(newCupcake);
	$('#new-cupcake-form').trigger('reset');
});

$(showAllCupcakes);
