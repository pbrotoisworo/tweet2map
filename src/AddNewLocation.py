import os
# from src.LocationManagement import LocationDatabaseSQL

def add_new_location(user_input_choice, location, location_dict, location_accuracy_dict, sql_object):
    """Function to handle menu choices"""

    tweet_location = location

    if (user_input_choice == '1') or (user_input_choice == '2'):

        if user_input_choice == '1':
            bool_high_accuracy = '1'
        if user_input_choice == '2':
            bool_high_accuracy = '0'

        print('Enter decimal degrees coordinates in this format: LATITUDE,LONGITUDE')
        user_input_coords = input('Enter coordinates:')
        if user_input_coords == 'BREAK':
            return 'BREAK'
        user_input_coords = user_input_coords.replace(' ', '')
        tweet_latitude = user_input_coords.split(',')[0]
        tweet_longitude = user_input_coords.split(',')[1]
        print(f'Data to be added:')
        print(f'High Accuracy: {bool_high_accuracy}')
        print(f'Latitude: {tweet_latitude}')
        print(f'Longitude: {tweet_longitude}')
        user_confirm_add = input('Confirm information is correct? (Y/N)').upper()

        if user_confirm_add == 'Y':
            # Update dict
            location_dict[tweet_location] = f'{tweet_latitude},{tweet_longitude}'
            location_accuracy_dict[tweet_location] = bool_high_accuracy
            # Update SQL database
            sql_object.insert(tweet_location, f'{tweet_latitude},{tweet_longitude}', bool_high_accuracy)
            print(f'Added "{tweet_location}" to database')
            return (tweet_location, f'{tweet_latitude},{tweet_longitude}', location_dict, location_accuracy_dict, bool_high_accuracy)

        elif user_confirm_add == 'N':
            return 'BREAK'

        elif user_confirm_add == 'BREAK':
            return 'BREAK'

    elif user_input_choice == '3':
        user_search_existing_location = input('Search database for existing location: ').upper()
        
        if user_search_existing_location == 'BREAK':
            return 'BREAK'
        
        print(f'Search results of "{user_search_existing_location}"')
        # search_result returns (location, coords, bool_high_accuracy) tuple
        search_results = sql_object.search_matching_location(user_search_existing_location)
        
        if search_results == 'BREAK':
            return 'BREAK'
        
        coord_match = search_results[1]
        bool_high_accuracy = int(search_results[2])
        tweet_latitude = coord_match.split(',')[0]
        tweet_longitude = coord_match.split(',')[1]

        print(f'Data to be added:')
        print(f'High Accuracy: {bool_high_accuracy}')
        print(f'Latitude: {tweet_latitude}')
        print(f'Longitude: {tweet_longitude}')
        user_confirm_add = input('Confirm information is correct? (Y/N)').upper()

        if user_confirm_add == 'Y':
            # Add new location to dictionary based on existing coords
            location_dict[location] = coord_match
            location_accuracy_dict[location] = bool_high_accuracy
            # Update SQL database
            sql_object.insert(location, coord_match, bool_high_accuracy)
            print(f'Added "{location}" to database')

            search_results = (location, coord_match, location_dict, location_accuracy_dict, bool_high_accuracy)
            return search_results

        elif user_confirm_add == 'N':
            return 'BREAK'

        elif user_confirm_add == 'BREAK':
            return 'BREAK'

        

    elif user_input_choice == '4':
        revised_location = input('Input revised name: ').upper()
        return ('REVISED', revised_location)

    elif user_input_choice == '5':
        tweet_latitude = '0'
        tweet_longitude = '0'
        bool_high_accuracy = '0'
        user_input_coords = tweet_latitude + ',' + tweet_longitude
        location_dict[tweet_location] = user_input_coords
        location_accuracy_dict[location] = bool_high_accuracy
        sql_object.insert(location, user_input_coords, bool_high_accuracy)
        return (tweet_location, user_input_coords, location_dict, location_accuracy_dict, bool_high_accuracy)
    
    else:
        print(f'Input "{user_input_choice}" is not recognized')
        return 'BREAK'
