import sys

from app import get_user_choice, get_user_input, load_json, save_json


def main():
  print("*********MAIN MENU***********\n")
  
  choice = get_user_choice('List Subscribed Shows', 'Search', 'Quit', index = True)

  if choice == 0:
    shows = [{
      'name': 'Supergirl',
      'release_year': 2016,
      'source': 'TVGuide'
    }]  # TODO - Read and Parse shows from 'shows.json'
    return list_shows(*shows)
  elif choice == 1:
    sources = ['TVGuide']  # TODO - Read shows from .py file.
    source = get_user_choice(*sources, none_option = 'Main Menu')
    return main() if source is None else search_source(source)
  elif choice == 2:
    sys.exit()
		

def search_source(source):
  # TODO
  # shows = source.search_for_show(query)
  pass


def list_shows(*shows):
  # TODO
  pass
  

def sign_up():
  '''Sign the user up for the first time.'''
  save_json('config', {
    'email': {
      'address': get_user_input('Email Address: '),
      'password': get_user_input('Email Password: ')
    },
    'timezone': get_user_input('Timezone: ')
  })
	
  return main()

  
def login(config):
	address = get_user_input('Email Address: ')
	password = get_user_input('Email Password: ')
	timezone = get_user_input('Timezone: ')
	
	correct = config['email']['address'] == address and config['email']['password'] == password and config['timezone'] == timezone
	if not correct:
		print('Invalid Information, try again.')
		return login(config)
	
	print("Now it is time to select your shows")
	return main()


def start():
  '''Initialize config and then continue to the main menu.'''
  config = load_json('config', False)
  return login(config) if config else sign_up()
