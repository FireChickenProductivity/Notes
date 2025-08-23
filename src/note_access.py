# This file contains commands for accessing notes by name or metadata

from talon import Module, actions, clip

from .note_loading import Note
from .searching import Search, find_notes_matching_search

def get_note(name: str) -> Note:
	notes = actions.user.chicken_notes_get()
	if name in notes:
		return notes[name]
	raise ValueError(f"Tried to access nonexistent note {name}")
	
current_note: Note | None = None
current_page: int = 1
search: Search | None = None
search_results: dict | None = None
is_search_focused: bool = False

module = Module()
@module.action_class
class Actions:
	def chicken_notes_display_brief_by_name(name: str):
		"""Displays the first part of the note with the name"""
		global current_note, is_search_focused
		note = get_note(name)
		current_note = note
		actions.user.chicken_notes_display_brief(note)
		is_search_focused = False

	def chicken_notes_display_by_name(name: str):
		"""Displays the note with the name"""
		global current_note, current_page, is_search_focused
		note = get_note(name)
		current_note = note
		actions.user.chicken_notes_display(note)
		current_page = 1
		is_search_focused = False

	def chicken_notes_expand():
		"""Expands the current chicken note"""
		if current_note:
			actions.user.chicken_notes_display(current_note)
			global is_search_focused
			is_search_focused = False
	
	def chicken_notes_collapse():
		"""Collapses the current chicken note"""
		if current_note:
			actions.user.chicken_notes_display_brief(current_note)
			global is_search_focused
			is_search_focused = False

	def chicken_notes_go_to_page(number: int):
		"""Opens the specified chicken notes page for the currently expanded note"""
		if current_note:
			global current_page
			actions.user.chicken_notes_display(current_note, number)
			current_page = number

	def chicken_notes_go_to_next_page():
		"""Opens the next chicken notes page"""
		if current_note:
			global current_page
			page = current_page + 1
			actions.user.chicken_notes_display(current_note, page)
			current_page = page

	def chicken_notes_go_to_previous_page():
		"""Opens the previous chicken notes page"""
		if current_note:
			global current_page
			page = current_page - 1
			actions.user.chicken_notes_display(current_note, page)
			current_page = page

	def chicken_notes_get_link(number: int) -> str:
		"""Retrieves the specified link from the current note"""
		if not current_note:
			raise TypeError("There is currently no note selected")
		if is_search_focused:
			raise TypeError("The search is focused, not a note!")
		if number < 1 or number > len(current_note.links):
			raise ValueError(f"Received invalid link number {number}")
		return current_note.links[number - 1]

	def chicken_notes_copy_link(number: int):
		"""Copies the specified link to the clipboard"""
		link = actions.user.chicken_notes_get_link(number)
		clip.set_text(link)

	def chicken_notes_open_link(number: int):
		"""Opens the specified link"""
		link = actions.user.chicken_notes_get_link(number)
		actions.user.open_url(link)

	def chicken_notes_perform_tag_search(tag: str):
		"""Searches for chicken notes with the tag"""
		global search, search_results, is_search_focused, current_page
		search = Search([tag], [])
		search_results = find_notes_matching_search(search)
		is_search_focused = True
		current_page = 1
		actions.user.chicken_notes_display_search(search, search_results,current_page)