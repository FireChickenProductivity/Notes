# This file loads in the notes from the appropriate directory and provides access to the notes data structure

from talon import Module, actions, app, settings, fs

import os

class Note:
	def __init__(self, name: str, body: str, tags: list[str], links: list[str]):
		self.name = name
		self.body = body
		self.tags = tags
		self.links = links

NAME_PREFIX = "name:"
TAG_PREFIX = "tag:"
LINK_PREFIX = "link:"
FILE_EXTENSION = ".txt"

class InvalidNoteException(Exception):
	pass

def create_value_missing_exception(value_name: str, index: int, file_name: str):
	return InvalidNoteException(f"Note {value_name} is missing string on line {index + 1}: {file_name}")

def get_prefix_value(value_name: str, prefix: str, index: int, file_name, line: str):
	if len(line) == len(prefix):
		raise create_value_missing_exception(value_name, index, file_name)
	value = line[len(NAME_PREFIX):].strip()
	if value == "":
		raise create_value_missing_exception(value_name, index, file_name)
	return value

def parse_header(file_name: str, lines: list[str]):
	name: str = ""
	tags: list[str] = []
	links: list[str] = []
	index = 0
	while index < len(lines) and lines[index].strip() != "-":
		line = lines[index].strip()
		if line.startswith(NAME_PREFIX):
			name = get_prefix_value("name", NAME_PREFIX, index, file_name, line)
		elif line.startswith(TAG_PREFIX):
			tags.append(
				get_prefix_value("tag", TAG_PREFIX, index, file_name, line)
			)
		elif line.startswith(LINK_PREFIX):
			links.append(
				get_prefix_value("link", LINK_PREFIX, index, file_name, line)
			)
		elif len(line) > 0:
			raise InvalidNoteException(f"Could not parse line {index + 1} in the header of note {file_name}")
		index += 1
	return name, tags, links, index

def parse_body(file_name: str, lines: list[str], body_index: int):
	if body_index >= len(lines) - 1:
		raise InvalidNoteException(f"Note missing body: {file_name}")
	body = "\n".join(lines[body_index + 1:])
	return body

def compute_text_before_postfix(text: str, postfix: str):
	if not text.endswith(postfix):
		raise ValueError(f"Tried to compute text before postfix with the postfix {postfix} missing from {text}")
	return text[:len(text) - len(postfix)]

def parse_note(path: str, file_name: str,  text: str):
	body: str = ""
	lines = text.split("\n")
	name, tags, links, body_index = parse_header(path, lines)
	if not name:
		name = compute_text_before_postfix(file_name, FILE_EXTENSION)
	body = parse_body(path, lines, body_index)
	return Note(name, body, tags, links)


def load_notes(directory: str):
	notes = {}
	errors = []
	for name in os.listdir(directory):
		path = os.path.join(directory, name)
		if name.endswith(FILE_EXTENSION) and os.path.isfile(path):
			try:
				with open(path, "r") as f:
					note = parse_note(path, name, f.read())
					if note.name in notes:
						errors.append(InvalidNoteException(f"More than one note has the name {note.name}! Duplicate found at {path}."))
					else:
						notes[note.name] = note
			except InvalidNoteException as e:
				errors.append(e)
	return notes, errors


module = Module()
module.setting(
	'chicken_notes_directory',
	type = str,
	default = "",
	desc = "The directory to load notes from"
)

DEFAULT_NOTES_DIRECTORY: str
NOTES: dict[str, Note]

def get_directory():
	directory_setting = settings.get("user.chicken_notes_directory")
	return directory_setting if directory_setting else DEFAULT_NOTES_DIRECTORY

def warn_about_errors(errors):
	app.notify("There were errors loading notes. See the log for details.")
	for e in errors:
		print(e)

def load_notes_on_change_or_startup(path):
	global NOTES
	NOTES, errors = load_notes(path)
	if errors:
		warn_about_errors(errors)

def on_ready():
	global DEFAULT_NOTES_DIRECTORY
	DEFAULT_NOTES_DIRECTORY = os.path.join(actions.path.talon_user(), "note_files")
	directory_path = get_directory()
	if not os.path.exists(directory_path):
		os.mkdir(directory_path)
	load_notes_on_change_or_startup(directory_path)
	fs.watch(directory_path, lambda a, b: load_notes_on_change_or_startup(directory_path))

app.register("ready", on_ready)

@module.action_class
class Actions:
	def chicken_notes_get() -> dict[str, Note]:
		"""Returns the notes data structure"""
		global NOTES
		return NOTES