extends KinematicBody2D

export (float) var MASS = 1
export (int) var JUMP_HEIGHT = 64
export (int) var GRAVITY = 80
export (int) var ACCELERATION = 256
export (float) var FRICTION = 0.25
export (int) var MAX_SPEED = 64
signal death

const UP = Vector2.UP

var dead = false
var motion = Vector2.ZERO
var on_floor = false
var damage = 0

func _physics_process(delta):
	check_score()
	on_floor = is_on_floor()
	motion.y += GRAVITY * delta * (abs(damage) + MASS)
	damage = clamp(damage, -1, 1)
	if abs(damage) == 1 or dead:
		if damage < 0:
			damage -1
		else:
			damage = 1
		dead = true
		check_score()
		emit_signal("death")
	else:
		var input_x = Input.get_action_strength("ui_right") - Input.get_action_strength("ui_left")
		if input_x != 0:
			motion.x += input_x * delta * ACCELERATION
			motion.x = clamp(motion.x, -MAX_SPEED, MAX_SPEED)
			if input_x < 0:
				$PICTURE.flip_h = true
			else:
				$PICTURE.flip_h = false
			if on_floor:
				$ANIMATOR.play("WALK")
		else:
			motion.x = lerp(motion.x, 0, FRICTION)
			if on_floor:
				$ANIMATOR.play("IDLE")
		if motion.y > 0 and on_floor == false:
			$ANIMATOR.play("FALL")
		if Input.is_action_just_pressed("jump") and abs(damage) < 1:
			motion.y = -clamp(lerp(JUMP_HEIGHT, 0, 1 - (position.y / 136)), 16, JUMP_HEIGHT)
			if on_floor:
				$FLAPER.play()
				$ANIMATOR.play("JUMP")
			else:
				$FLAPER.play()
				$ANIMATOR.play("FLY")
	motion = move_and_slide(motion, UP)

func _on_SEA_body_entered(body):
	damage = -1

func _on_DEATH1_body_entered(body):
	damage = 1

func check_score():
	var HS = 0
	var S = get_parent().SCORE
	var high_score = File.new()
	high_score.open("user://high_score.save", File.READ)
	if high_score.file_exists("user://high_score.save"):
		HS = high_score.get_var()
		print("OK")
	high_score.close()
	if HS < S:
		HS = S
		high_score.open("user://high_score.save", File.WRITE)
		high_score.store_var(S)
		high_score.close()
	get_parent().get_child(6).get_child(0).get_child(3).text = "HIGH SCORE: " + str(HS)
