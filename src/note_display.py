# This file provides logic for displaying notes to be used by note displaying commands and actions

from talon import Module, actions, app

from .note_loading import Note
from .canvas import Display, Items

def compute_first_line(text: str):
	first_line = ""
	for character in text:
		if character == "\n":
			break
		else:
			first_line += character
	return first_line

canvas: Display = Display()

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