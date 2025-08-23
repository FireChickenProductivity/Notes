# This file provides logic for displaying notes to be used by note displaying commands and actions

from talon import Module, actions, app, settings

from .note_loading import Note
from .canvas import Display, Items
from .searching import Search

from pathlib import Path
import math

def compute_first_line(text: str):
	first_line = ""
	for character in text:
		if character == "\n":
			break
		else:
			first_line += character
	return first_line

canvas: Display = Display()
POSITION_FILE_NAME: str = "display_position.txt"

def compute_position_file_path():
	return Path(__file__).parents[0] / POSITION_FILE_NAME

module = Module()

module.setting(
	'chicken_notes_max_line_length',
	type = int,
	default = 100,
	desc = "The maximum number of characters to put on a single line. Make this 0 for no limit."
)

module.setting(
	'chicken_notes_page_size',
	type = int,
	default = 10,
	desc = "The number of lines to show on each page. Make this 0 for no limit."
)

def compute_wrapped_lines(lines: list[str], max_line_length: int):
	result = []
	for line in lines:
		if max_line_length <= 0 or len(line) < max_line_length:
			result.append(line)
		else:
			start = 0
			while start < len(line):
				result.append(line[start:start+max_line_length])
				start += max_line_length
	return result

def add_wrapped_lines(items: Items, lines: list[str], max_line_length: int):
	wrapped_lines = compute_wrapped_lines(lines, max_line_length)
	for line in wrapped_lines:
		items.text(line)

def add_page(items: Items, lines: list[str], page_size: int, page: int):
	if page_size <= 0 or page_size >= len(lines):
		for line in lines:
			items.text(line)
	else:
		number_of_pages = math.ceil(len(lines)/page_size)
		if page < 1 or page > number_of_pages:
			raise ValueError(f"You tried to access invalid page {page}")
		start = (page - 1)*page_size
		end = min(start + page_size, len(lines))
		page_lines = lines[start:end]
		page_number_text = f"page {page}/{number_of_pages}"
		items.text(page_number_text)
		items.line()
		for page_line in page_lines:
			items.text(page_line)

def add_links(items: Items, note: Note):
	if note.links:
		items.line()
	for i, l in enumerate(note.links):
		items.text(f"{i + 1}: {l}")

@module.action_class
class Actions:
	def chicken_notes_display(note: Note, page: int=1):
		"""Displays the specified note"""
		max_line_length = settings.get('user.chicken_notes_max_line_length')

		items = Items()
		add_wrapped_lines(items, [note.name], max_line_length)
		items.line()
		body = compute_wrapped_lines(note.body.split("\n"), max_line_length)
		add_page(items, body, settings.get('user.chicken_notes_page_size'), page)
		add_links(items, note)

		canvas.update(items)
		canvas.refresh()

	def chicken_notes_display_brief(note: Note):
		"""Displays the early parts of a note with its name"""
		first_line = compute_first_line(note.body)
		text = f"Note: {note.name}\n{first_line}"
		items = Items()
		
		max_line_length = settings.get('user.chicken_notes_max_line_length')
		if max_line_length > 0 and len(text) > max_line_length:
			text = text[:max_line_length]
			
		items.text(text)
		canvas.update(items)
		canvas.refresh()

	def chicken_notes_display_search(search: Search, notes: dict[str, Note], page: int=1):
		"""Displays the chicken notes search results"""
		max_line_length = settings.get('user.chicken_notes_max_line_length')

		title = f"tags: {",".join(search.tags)} | keywords: {",".join(search.keywords)}"
		result_text = []
		for n in notes:
			result_text.append(n)
			result_text.append("\t" + compute_first_line(notes[n].body))
		items = Items()
		add_wrapped_lines(items, [title], max_line_length)
		items.line()
		add_page(items, result_text, settings.get('user.chicken_notes_page_size'), page)

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