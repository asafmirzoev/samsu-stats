Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

async function create_piechart(_data, id) {
	let data = JSON.parse(_data);
	let grades = [];
		counts = [];
		colors = [];
	for (let [grade, grade_data] of Object.entries(data)) {
		grades.push(grade);
		counts.push(grade_data.count);
		colors.push(grade_data.color);
	}
	$(`#BarPieChart-${id}`).remove();
	$(`.chart-bar-${id}`).html("");
	if (grades.length) {
		$(`.chart-bar-${id}`).append(`<canvas id="BarPieChart-${id}"><canvas>`);
		var ctx = $(`#BarPieChart-${id}`);
		var myLineChart = new Chart(ctx, {
			type: 'doughnut',
			data: {
				labels: grades,
				datasets: [{
					data: counts,
					backgroundColor: colors
				}]
			},
			options: {
				legend: {
					display: false
				},
			}
		});
	}
}