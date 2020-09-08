import os
# from src.LocationManagement import LocationDatabaseSQL

def add_new_location(user_input_choice, location, location_dict, sql_object):
    """Function to handle menu choices"""

    tweet_location = location

    if (user_input_choice == '1') or (user_input_choice == '2'):

        if user_input_choice == '1':
            bool_high_accuracy = '1'
        if user_input_choice == '2':
            bool_high_accuracy = '0'

        print('Enter decimal degrees coordinates in this format: LATITUDE,LONGITUDE')
        user_input_coords = input('Enter coordinates:')
        user_input_coords = user_input_coords.replace(' ', '')
        tweet_latitude = user_input_coords.split(',')[0]
        tweet_longitude = user_input_coords.split(',')[1]
        print(f'\nData to be added:')
        print(
            f'Location: {tweet_location}\nLatitude: {tweet_latitude}\nLongitude: {tweet_longitude}')
        user_confirm_add = input(
            'Confirm information is correct? (Y/N)').upper()

        if user_confirm_add == 'Y':
            location_dict[tweet_location] = f'{tweet_latitude},{tweet_longitude}'
            return (tweet_location, f'{tweet_latitude},{tweet_longitude}', location_dict, bool_high_accuracy)

        elif user_confirm_add == 'N':
            return 'BREAK'

        elif user_confirm_add == 'BREAK':
            return 'BREAK'

    elif user_input_choice == '3':
        user_search = input('Search database for existing location: ').upper()
        if user_search == 'BREAK':
            return 'BREAK'

        print(f'Search results of "{user_search}"')
        # search_result returns (location, coords) tuple
        search_results = sql_object.search_matching_location(user_search)
        if search_results == 'BREAK':
            return 'BREAK'
        else:
            location_dict[location] = search_results[1]
            search_results = (search_results[0], search_results[1], location_dict)
            return search_results

    elif user_input_choice == '4':
        revised_location = input('Input revised name: ').upper()
        return ('REVISED', revised_location)

    elif user_input_choice == '5':
        tweet_latitude = '0'
        tweet_longitude = '0'
        user_input_coords = tweet_latitude + ',' + tweet_longitude
        location_dict[tweet_location] = user_input_coords
        return (tweet_location, user_input_coords, location_dict)
