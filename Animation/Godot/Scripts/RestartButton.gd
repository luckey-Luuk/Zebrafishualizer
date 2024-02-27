extends Button


# Called when the node enters the scene tree for the first time.
func _ready():
	Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)
	pass


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass

func _on_pressed():
	Global.node_counter = 0
	get_tree().change_scene_to_file("res://Main_scene.tscn")
	pass # Replace with function body.
