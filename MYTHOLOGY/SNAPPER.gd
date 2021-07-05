extends Position2D

var grid_position = Vector2(-1, -1)
var grid_size = Vector2(256, 144)

onready var player = get_parent().get_child(2)

func _ready():
	set_as_toplevel(true)
	update_grid_position()

func _physics_process(delta):
	if player:
		if abs($Camera2D/HSlider.value) < 100:
			$Camera2D/HSlider.value = clamp(round(player.damage * 100), -100, 100)
		if abs(player.damage) < 1:
			$Camera2D/Label.text = "SCORE: " + str(get_parent().SCORE)
			update_grid_position()

func update_grid_position():
	var new_grid_position = Vector2(floor(player.position.x / grid_size.x), floor(player.position.y / grid_size.y))
	if new_grid_position == grid_position:
		return
	grid_position = new_grid_position
	position = grid_position * grid_size
