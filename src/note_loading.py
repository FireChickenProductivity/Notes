from talon import Module, actions

class Note:
	def __init__(self, name: str, body: str, tags: list[str], links: list[str]):
		self.name = name
		self.body = body
		self.tags = tags
		self.links = links

NAME_PREFIX = "name:"
TAG_PREFIX = "tag:"
LINK_PREFIX = "link:"

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
	

def parse_note(file_name: str, text: str):
	name: str = ""
	tags: list[str] = []
	links: list[str] = []
	body: str = ""
	lines = text.split("\n")
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
		index += 1
	if index >= len(lines) - 1:
		raise InvalidNoteException(f"Note missing body: {file_name}")
	body = "\n".join(lines[index + 1:])
	return Note(name, body, tags, links)
		