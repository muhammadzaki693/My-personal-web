const test = document.getElementById('test');
const input = document.getElementById('input');
const color = document.getElementById('color');
function change(){
	test.innerHTML = input.value;
	console.log("changed test to " + input.value)
}
function onChange(){
	var value = color.options[color.selectedIndex].text;
	test.style.color = value;
	console.log("changed test color to " + value)
}