
class UI:
	def __init__(self) -> None:
		self.__all_ui = {}

	def get_ui(self, name):
		return self.__all_ui.get(name, False)

	def set_ui(self, name, value):
		self.__all_ui[name] = value

	def clean_ui(self, name):
		self.__all_ui.pop(name)