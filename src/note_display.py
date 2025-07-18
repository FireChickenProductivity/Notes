# This file provides logic for displaying notes to be used by note displaying commands and actions

from talon import Module, actions, app

from .note_loading import Note

def compute_first_line(text: str):
	first_line = ""
	for character in text:
		if character == "\n":
			break
		else:
			first_line += character
	return first_line

module = Module()
@module.action_class
class Actions:
	def notes_display(note: Note):
		"""Displays the specified note"""
		app.notify(note.body)

	def notes_display_brief(note: Note):
		"""Displays the early parts of a note with its name"""
		first_line = compute_first_line(note.body)
		text = f"Note: {note.name}\n{first_line}"
		app.notify(text)

		