import json
import os


def get_user_choice(*options, none_option = None, index = False):
	'''Returns the user choice from options.

	Args:
		options - Any number of options.
		none_option - Option that will return None.
		index - If to return the index of the object instead of the object.

	Returns:
		Option or index of option of option.
	'''
	all_options = options if none_option is None else [none_option] + list(options)
	for i, option in enumerate(all_options):
		print('{}: {}'.format(i + 1, option))
   
	print('\nPlease enter your choice:')

	failure_message = 'You must only enter either {}or {}.\nPlease try again'.format(
		''.join(['{}, '.format(i + 1) for i in range(len(all_options) - 1)]),
		len(all_options)
	)
	
	value = -1
	while True:
		# Input is digit
		choice = input('> ')
		if not choice.isdigit():
			print(failure_message)
			continue

		# Input is in range
		value = int(choice)
		passed_max = value > len(options) if none_option is None else value > len(options) + 1
		if value < 1 or passed_max:
			print(failure_message)
			continue

		if none_option and value == 1:
			return None

		if index:
			return value - 1

		return options[value - 1 if none_option is None else value - 2]


def get_user_input(prompt = '> '):
	'''Return user input.

	Args:
		prompt - Prompt for user input.

	Returns:
		User inputted string.
	'''
	while True:
		value = input(prompt).strip()
		if not value:
			continue
		return value


def load_json(filepath, default_data = None):
	'''Return the loaded JSON file contents.

	Args:
		filepath - Filepath of the JSON file minus the .json extension.
		default_data - Data to return if unable to load the JSON file.

	Returns:
		Data from the JSON file or default_data if failed.
	'''
	try:
		with open('{}.json'.format(filepath), 'r') as json_file:
			return json.load(json_file)
	except:
		return default_data


def save_json(filepath, data):
	'''Save JSON data to a .json file.

	Args:
		filepath - Filepath of the JSON file minus the .json extension.
		data - JSON-able data to save.
	'''
	with open('{}.json'.format(filepath), 'w') as json_file:
		json.dump(data, json_file, indent = 2)


if __name__ == '__main__':
	import menus
	menus.start()
