extends Node2D

export (int) var speed = 10
var float_score = 0
var SCORE = 0
onready var rnd = RandomNumberGenerator.new()
onready var cloudscene = load("res://CLOUD.tscn")
onready var darkcloudscene = load("res://DARK_CLOUD.tscn")

export (int) var x_spawn = 544
export (int) var min_y = 16
export (int) var max_y = 80
var spawn_time = 0
var water = 0.1
var sun = 0.1

func _ready():
	$SNAPPER/Camera2D/RELOAD.visible = false
	$SNAPPER/Camera2D/RELOAD.set_process(false)

func _physics_process(delta):
	if $DEDAL:
		var x = 0
		var y = 0
		if $DEDAL.position.y > 64:
			y = -48
		if $DEDAL.position.x < 384:
			x = 48
		$DEDAL.move_and_slide(Vector2(x, y))
	if $IKAR:
		$SKY.position.x -= delta * speed * 2
		if $SKY.position.x <= 128:
			$SKY.position.x += 256
		spawn_time -= delta
		spawn_time = clamp(spawn_time, 0, 100)
		if spawn_time == 0:
			rnd.randomize()
			var check = rnd.randi_range(0, 3)
			rnd.randomize()
			var cloud = cloudscene.instance()
			if check == 0:
				cloud = darkcloudscene.instance()
			cloud.position = Vector2(x_spawn, rnd.randf_range(min_y, max_y))
			add_child(cloud)
			spawn_time = 15
		if $IKAR.position.x > 256:
			$SEA.position.x -= delta * speed
			if $SEA.position.x <= 256:
				$SEA.position.x += 256
			if abs($IKAR.damage) < 1:
				float_score += delta
			SCORE = int(float_score)
			$SEA.position.y = 136
			$WALLS/WALL1.position.y = $WALLS/WALL0.position.y
			if $IKAR.position.y > 80:
				$IKAR.damage -= water * delta
			if $IKAR.position.y < 50:
				$IKAR.damage += sun * delta

func _on_IKAR_death():
	$SNAPPER/Camera2D/RELOAD.set_process(true)
	$SNAPPER/Camera2D/RELOAD.visible = true

func _on_RELOAD_button_up():
	get_tree().change_scene("res://WORLD.tscn")


func _on_HOME_button_up():
	get_tree().change_scene("res://MENU.tscn")

func _on_WIND_finished():
	$SNAPPER/Camera2D/WIND.play()
