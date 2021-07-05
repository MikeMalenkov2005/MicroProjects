extends Node2D

export (int) var speed = 10

func _ready():
	get_score()

func _physics_process(delta):
	$SKY.position.x -= delta * speed * 2
	if $SKY.position.x <= 128:
		$SKY.position.x += 256
	$SEA.position.x -= delta * speed
	if $SEA.position.x <= 128:
		$SEA.position.x += 256

func _on_PLAY_button_up():
	get_tree().change_scene("res://WORLD.tscn")

func _on_RESET_button_up():
	var file = File.new()
	file.open("user://high_score.save", File.WRITE)
	file.store_var(0)
	file.close()
	get_score()

func get_score():
	var file = File.new()
	var HS = 0
	if file.file_exists("user://high_score.save"):
		file.open("user://high_score.save", File.READ)
		HS = file.get_var()
		file.close()
	$SCORE.text = str(HS)

func _on_EXIT_button_up():
	 get_tree().quit()

func _on_MELODY_finished():
	$MELODY.play()
