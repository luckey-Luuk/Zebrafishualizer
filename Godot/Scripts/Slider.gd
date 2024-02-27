extends HSlider

var counter = 0
var delta_counter = 0

# Called when the node enters the scene tree for the first time.
func _ready():
	Global.paused = false
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	var slider_test = $"."
	if Global.paused == false:
		
		
		delta_counter += delta
		
	#	if Global.delta_counter > 0.5:
	#		counter += 1
		
		if delta_counter > 0.5:
			counter += 1
			delta_counter = 0
			
		slider_test.value = counter
	#	print("slider_test value is:",slider_test.value)
		
		if counter >119:
			counter = 0
	#	$BoxContainer/node_counter.text = str(Global.node_counter)
		$BoxContainer/node_counter.text = str(counter)
		



func _on_value_changed(value):
	var slider_test = $"."
#	print("value changed succefully to:", slider_test.value)
	Global.node_counter = int(value)
	$BoxContainer/node_counter.text = str(value)
#	get_tree().paused = false
	pass # Replace with function body.


func _input(event):
	var slider_test = $"."
	# Check if the left mouse button is pressed
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
		# Check if the mouse is over the slider
#		if slider_test.rect_min_size.has_point(event.position - slider_test.rect_min_position):
			# Update the counter based on the slider position
		counter = int(slider_test.value)
