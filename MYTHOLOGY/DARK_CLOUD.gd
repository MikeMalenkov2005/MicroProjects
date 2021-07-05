extends Area2D

var power = 0.2
onready var player = get_parent().get_child(2)
onready var speed = get_parent().speed / 2

var player_in = false

func _physics_process(delta):
	if position.x < -16:
		queue_free()
	position.x -= speed * delta
	if player:
		if player_in:
			player.damage -= delta * power

func _on_DARK_CLOUD_body_entered(body):
	player_in = true

func _on_DARK_CLOUD_body_exited(body):
	player_in = false
