import re
import pandas as pd
def preprocess(data):
    # Define the regex pattern to split messages and extract dates
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern, data)[1:]  # Split the data using the pattern
    dates = re.findall(pattern, data)  # Find all date matches

    # Create a DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Convert `message_date` to datetime
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M - ', errors='coerce')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Separate users and messages
    users = []
    messages = []

    for msg in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', msg, maxsplit=1)
        if len(entry) > 2:  # If a user and message are present
            users.append(entry[1])  # User
            messages.append(entry[2])  # Message
        else:
            users.append('group_notification')  # Group notification
            messages.append(entry[0])  # Message content

    # Add user and message columns to DataFrame
    df['user'] = users
    df['message'] = messages

    # Drop the combined column
    df.drop(columns=['user_message'], inplace=True)
    df['only_date'] = df['date'].dt.date
    # Extract additional time features
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df
