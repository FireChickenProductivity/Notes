# This file contains commands for accessing notes by name or metadata

from talon import Module, actions

from .note_loading import Note

def get_note(name: str) -> Note:
	notes = actions.user.notes_get()
	if name in notes:
		return notes[name]
	raise ValueError(f"Tried to access nonexistent note {name}")
	

current_note: Note | None = None

module = Module()
@module.action_class
class Actions:
	def display_note_brief_by_name(name: str):
		"""Displays the first part of the note with the name"""
		global current_note
		note = get_note(name)
		current_note = note
		actions.user.notes_display_brief(note)

	def display_note_by_name(name: str):
		"""Displays the note with the name"""
		global current_note
		note = get_note(name)
		current_note = note
		actions.user.notes_display(note)