# This file provides logic for displaying notes to be used by note displaying commands and actions

from talon import Module, actions, app

from .note_loading import Note
from .canvas import Display, Items

from pathlib import Path

def compute_first_line(text: str):
	first_line = ""
	for character in text:
		if character == "\n":
			break
		else:
			first_line += character
	return first_line

canvas: Display = Display()
POSITION_FILE_NAME = "display_position.txt"

def compute_position_file_path():
	return Path(__file__).parents[0] / POSITION_FILE_NAME

module = Module()
@module.action_class
class Actions:
	def chicken_notes_display(note: Note):
		"""Displays the specified note"""
		items = Items()
		items.text(note.name)
		items.line()
		for line in note.body.split("\n"):
			items.text(line)
		canvas.update(items)
		canvas.refresh()

	def chicken_notes_display_brief(note: Note):
		"""Displays the early parts of a note with its name"""
		first_line = compute_first_line(note.body)
		text = f"Note: {note.name}\n{first_line}"
		items = Items()
		items.text(text)
		canvas.update(items)
		canvas.refresh()

	def chicken_notes_hide():
		"""Stops displaying chicken notes"""
		canvas.hide()

	def chicken_notes_show():
		"""Displays chicken notes"""
		canvas.show()

	def chicken_notes_move_display():
		"""Set the display position to the current mouse position"""
		global display
		x = int(actions.mouse_x())
		y = int(actions.mouse_y())
		canvas.set_position(x, y)
		actions.user.chicken_notes_save_display_position(x, y)
	
	def chicken_notes_save_display_position(x: int, y: int):
		"""Saves the position for the chicken notes display"""
		with open(compute_position_file_path(), "w") as f:
			f.write(f"{x} {y}")

	def chicken_notes_load_display_position() -> tuple[int, int]:
		"""Loads the position for the chicken notes display"""
		try:
			with open(compute_position_file_path(), "r") as f:
				line = f.readline()
				values = line.split(" ")
				x = int(values[0])
				y = int(values[1])
				return x, y
		except:
			return 0, 0

def on_ready():
	canvas.set_position(*actions.user.chicken_notes_load_display_position())

app.register("ready", on_ready)