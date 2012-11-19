$(document).ready(function () {
	var next = function() {
		$(".rotating_widget ul li:first-child").appendTo(".rotating_widget ul").slideUp();
		$(".rotating_widget .next_button").unbind("click");
		$(".rotating_widget ul li:first-child").slideDown(function () {
			$(".rotating_widget .next_button").click(next);
		});
	}
	setInterval(next, 5000);

	$(".rotating_widget ul li:first-child").show();
	$(".rotating_widget .next_button").click(next);
});