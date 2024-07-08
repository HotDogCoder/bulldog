class LogReader:

    def __init__(self, counter, get_counter, post_counter, date_string, local_path, limit, timezone, read_all):
        self.counter = counter
        self.get_counter = get_counter
        self.post_counter = post_counter
        self.local_path = local_path
        self.message = 'success'
        self.last_read_file = 'no one'
        self.date_string = date_string
        self.limit = limit
        self.timezone = timezone
        self.read_all = read_all
        # self.daily_directory_list = daily_directory_list
