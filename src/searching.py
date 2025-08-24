# This module contains support for searching the available notes for notes meeting a specific criteria

from talon import actions
from .note_loading import Note

class Search:
	def __init__(self, tags: list[str]):
		self.tags = tags

def does_note_have_every_tag(note: Note, tags: set[str]):
	matching_tags = 0
	for t in note.tags:
		if t in tags:
			matching_tags += 1
	return matching_tags == len(tags)
	

def compute_filtered_dictionary(dictionary, condition):
	filtered = {}
	for k in dictionary:
		if condition(dictionary[k]):
			filtered[k] = dictionary[k]
	return filtered

def find_notes_matching_search(search: Search)-> dict[str, Note]:
	notes: dict[str, Note] = actions.user.chicken_notes_get()
	if search.tags:
		tags_set = set(search.tags)
		notes = compute_filtered_dictionary(notes, lambda n: does_note_have_every_tag(n, tags_set))
	return notes