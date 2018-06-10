from unittest.mock import patch as Patch, call as Call
import unittest

import time
import json
import os

import app

def reset_mocks(*mocks):
	for mock in mocks:
		mock.reset_mock()

def assert_calls(self, mock, *expected):
	expected = list(expected)
	for i, args in enumerate(expected):
		args_type = type(args)
		if args_type != Call:
			if args_type == list:
				expected[i] = Call(*args)
			else:
				expected[i] = Call(args)

	self.assertEqual(mock.call_args_list, expected, 'Expected {} to have {} calls but instead got {}'.format(mock, expected, mock.call_args_list))


class GetUserChoice(unittest.TestCase):
	def assertCalls(self, mock, *expected):
		return assert_calls(self, mock, *expected)


	@Patch('app.print', create = True)
	@Patch('builtins.input', side_effect = ['2'])
	def test_returns_chosen(self, input_mock, print_mock):
		self.assertEqual(app.get_user_choice('a', 'b'), 'b')
		self.assertCalls(print_mock, '1: a', '2: b', '\nPlease enter your choice:')
		self.assertCalls(input_mock, '> ')


	@Patch('app.print', create = True)
	@Patch('builtins.input', side_effect = ['f'])
	def test_non_digit(self, input_mock, print_mock):
		with self.assertRaises(StopIteration):
			app.get_user_choice('c', 'd')
		input_mock.assert_called_with('> ')
		self.assertCalls(print_mock, '1: c', '2: d', '\nPlease enter your choice:', 'You must only enter either 1, or 2.\nPlease try again')


	@Patch('app.print', create = True)
	@Patch('builtins.input', side_effect = ['3'])
	def test_invalid_max(self, input_mock, print_mock):
		with self.assertRaises(StopIteration):
			app.get_user_choice('e', 'f')
		input_mock.assert_called_with('> ')
		self.assertCalls(print_mock, '1: e', '2: f', '\nPlease enter your choice:', 'You must only enter either 1, or 2.\nPlease try again')


	@Patch('app.print', create = True)
	@Patch('builtins.input', side_effect = ['0'])
	def test_invalid_min(self, input_mock, print_mock):
		with self.assertRaises(StopIteration):
			app.get_user_choice('g', 'h')
		input_mock.assert_called_with('> ')
		self.assertCalls(print_mock, '1: g', '2: h', '\nPlease enter your choice:', 'You must only enter either 1, or 2.\nPlease try again')


	@Patch('app.print', create = True)
	@Patch('builtins.input', side_effect = ['1', '3'])
	def test_returns_index(self, input_mock, print_mock):
		self.assertEqual(app.get_user_choice('a', 'b', 'c', index = True), 0)

		reset_mocks(input_mock, print_mock)

		self.assertEqual(app.get_user_choice('a', 'b', 'c', index = True), 2)


	@Patch('app.print', create = True)
	@Patch('builtins.input', side_effect = ['1', '1'])
	def test_returns_none(self, input_mock, print_mock):
		self.assertIsNone(app.get_user_choice('b', 'c', none_option = 'a'))

		reset_mocks(input_mock, print_mock)

		self.assertIsNone(app.get_user_choice('e', 'f', none_option = 'd', index = True))


class GetUserInput(unittest.TestCase):
	def assertCalls(self, mock, *expected):
		return assert_calls(self, mock, *expected)


	@Patch('app.print', create = True)
	@Patch('builtins.input', side_effect = ['Hello World!'])
	def test_returns(self, input_mock, print_mock):
		self.assertEqual(app.get_user_input(), 'Hello World!')
		self.assertCalls(input_mock, '> ')


	@Patch('app.print', create = True)
	@Patch('builtins.input', side_effect = [' Hello World! \n\t\r'])
	def test_returns_striped(self, input_mock, print_mock):
		self.assertEqual(app.get_user_input(), 'Hello World!')
		self.assertCalls(input_mock, '> ')


	@Patch('app.print', create = True)
	@Patch('builtins.input', side_effect = ['', ' ', '\r  \n  \t  ', 'Hello World!'])
	def test_requires_content(self, input_mock, print_mock):
		self.assertEqual(app.get_user_input(), 'Hello World!')
		self.assertCalls(input_mock, *['> ' for _ in range(4)])


	@Patch('app.print', create = True)
	@Patch('builtins.input', side_effect = ['Answer'])
	def test_prompts(self, input_mock, print_mock):
		self.assertEqual(app.get_user_input('Question: '), 'Answer')
		self.assertCalls(input_mock, 'Question: ')


class LoadJson(unittest.TestCase):
	def test_loads(self):
		filename = str(time.time())
		filepath = '{}.json'.format(filename)
		with open(filepath, 'w') as test_file:
			json.dump({'a': 'b'}, test_file)
		
		self.assertEqual(app.load_json(filename), {'a': 'b'})
		os.path.exists(filepath) and os.remove(filepath)


	def test_loads_default(self):
		filename = str(time.time())
		filepath = '{}.json'.format(filename)

		os.path.exists(filepath) and os.remove(filepath)

		self.assertEqual(app.load_json(filename, {'c': 'd'}), {'c': 'd'})


class SaveJson(unittest.TestCase):
	def test_saves(self):
		filename = str(time.time())
		filepath = '{}.json'.format(filename)

		os.path.exists(filepath) and os.remove(filepath)

		app.save_json(filename, {'e': 'f'})

		self.assertTrue(os.path.exists(filepath))
		with open(filepath, 'r') as test_file:
			self.assertEqual(json.load(test_file), {'e': 'f'})

		os.path.exists(filepath) and os.remove(filepath)


if __name__ == '__main__':
	unittest.main()
