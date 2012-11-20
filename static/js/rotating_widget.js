$(document).ready(function () {
	var rotate_on = true;
	var next = function(clicked) {
		if (rotate_on || clicked) {
			$(".rotating_widget ul li:first-child").appendTo(".rotating_widget ul").slideUp();
			$(".rotating_widget .next_button").unbind("click");
			$(".rotating_widget ul li:first-child").slideDown(function () {
				$(".rotating_widget .next_button").click(next);
			});
		}
	}
	setInterval(function () {next(false)}, 5000);

	$(".rotating_widget ul li:first-child").show();
	$(".rotating_widget .next_button").click(function () {next(true)});
	$(".rotating_widget").mouseover(function () {
		rotate_on = false;
	});
	$(".rotating_widget").mouseout(function () {
		rotate_on = true;
	});
});