from datetime import datetime
from typing import Dict

class Clock:
    """
    A simple clock class that provides methods to 
    get the current date and time, as well as to 
    compare two datetime objects in various units 
    (seconds, minutes, hours, days, weeks, months, 
    years). 
    
    It also allows for the creation and management 
    of named counters
    """
    
    def __init__(self):
        """
        Initialize the clock.
        """
        self.counters: Dict[str, datetime] = {}
        
    def init_counter(
        self, name: str
    ) -> None:
        """
        Initialize a counter with the given name.
        
        Args:
            name (str): The name of the counter to initialize.
        """
        self.counters[name] = self.get_actual_date()
        return
        
    def poll_counter(
        self, name: str
    ) -> float:
        """
        Poll the value of a counter.
        
        Args:
            name (str): The name of the counter to poll.
        
        Returns:
            float: The value of the counter.
        """
        
        if name not in self.counters:
            raise ValueError(f"Counter '{name}' has not been initialized.")
        
        elapsed_time = self.get_actual_date() - self.counters[name]
        value: float = elapsed_time.total_seconds()
        self.counters.pop(name)
        return value
    
    def poll_all_counters(self) -> Dict[str, float]:
        """
        Poll the value of all counters.
        
        Returns:
            Dict[str, float]: A dictionary of counter names and their values.
        """
        return {name: self.poll_counter(name) for name in self.counters.keys()}
    
    def reset_counter(
        self, name: str
    ) -> None:
        """
        Reset the value of a counter.
        
        Args:
            name (str): The name of the counter to reset.
        """
        self.counters[name] = self.get_actual_date()
        return
    
    def reset_all_counters(self) -> None:
        """
        Reset the value of all counters.
        """
        for name in self.counters.keys():
            self.reset_counter(name)
        return
        
    def get_actual_date(self) -> datetime:
        """
        Get the actual date and time.
        
        Returns:
            datetime: The actual date and time.
        """
        return datetime.now()
    
    def get_day(self) -> int:
        """
        Get the current day of the month.
        
        Returns:
            int: The current day of the month.
        """
        return self.get_actual_date().day
    
    def get_month(self) -> int:
        """
        Get the current month.
        
        Returns:
            int: The current month.
        """
        return self.get_actual_date().month
    
    def get_year(self) -> int:
        """
        Get the current year.
        
        Returns:
            int: The current year.
        """
        return self.get_actual_date().year
    
    def get_hour(self) -> int:
        """
        Get the current hour.
        
        Returns:
            int: The current hour.
        """
        return self.get_actual_date().hour
    
    def get_minute(self) -> int:
        """
        Get the current minute.
        
        Returns:
            int: The current minute.
        """
        return self.get_actual_date().minute
    
    def get_second(self) -> int:
        """
        Get the current second.
        
        Returns:
            int: The current second.
        """
        return self.get_actual_date().second
    
    def get_millisecond(self) -> int:
        """
        Get the current millisecond.
        
        Returns:
            int: The current millisecond.
        """
        return self.get_actual_date().microsecond // 1000
    
    def get_microsecond(self) -> int:
        """
        Get the current microsecond.
        
        Returns:
            int: The current microsecond.
        """
        return self.get_actual_date().microsecond
    
    def cmp_seconds(self, a: datetime, b: datetime) -> float:
        """
        Compare two datetime objects and return the difference in seconds.
        
        Args:
            a (datetime): The first datetime object.
            b (datetime): The second datetime object.
        
        Returns:
            float: The difference in seconds.
        """
        return (a - b).total_seconds()
        
    def cmp_microseconds(self, a: datetime, b: datetime) -> float:
        """
        Compare two datetime objects and return the difference in microseconds.
        
        Args:
            a (datetime): The first datetime object.
            b (datetime): The second datetime object.
        
        Returns:
            float: The difference in microseconds.
        """
        return (a - b).microseconds
    
    def cmp_milliseconds(self, a: datetime, b: datetime) -> float:
        """
        Compare two datetime objects and return the difference in milliseconds.
        
        Args:
            a (datetime): The first datetime object.
            b (datetime): The second datetime object.
        
        Returns:
            float: The difference in milliseconds.
        """
        return self.cmp_microseconds(a, b) // 1000
    
    def cmp_minutes(self, a: datetime, b: datetime) -> float:
        """
        Compare two datetime objects and return the difference in minutes.
        
        Args:
            a (datetime): The first datetime object.
            b (datetime): The second datetime object.
        
        Returns:
            float: The difference in minutes.
        """
        return self.cmp_seconds(a, b) // 60
    
    def cmp_hours(self, a: datetime, b: datetime) -> float:
        """
        Compare two datetime objects and return the difference in hours.
        
        Args:
            a (datetime): The first datetime object.
            b (datetime): The second datetime object.
        
        Returns:
            float: The difference in hours.
        """
        return self.cmp_seconds(a, b) // 3600
    
    def cmp_days(self, a: datetime, b: datetime) -> float:
        """
        Compare two datetime objects and return the difference in days.
        
        Args:
            a (datetime): The first datetime object.
            b (datetime): The second datetime object.
        
        Returns:
            float: The difference in days.
        """
        return self.cmp_seconds(a, b) // 86400
    
    def cmp_weeks(self, a: datetime, b: datetime) -> float:
        """
        Compare two datetime objects and return the difference in weeks.
        
        Args:
            a (datetime): The first datetime object.
            b (datetime): The second datetime object.
        
        Returns:
            float: The difference in weeks.
        """
        return self.cmp_seconds(a, b) // 604800
    
    def cmp_months(self, a: datetime, b: datetime) -> float:
        """
        Compare two datetime objects and return the difference in months.
        
        Args:
            a (datetime): The first datetime object.
            b (datetime): The second datetime object.
        
        Returns:
            float: The difference in months.
        """
        return self.cmp_seconds(a, b) // 2592000
    
    def cmp_years(self, a: datetime, b: datetime) -> float:
        """
        Compare two datetime objects and return the difference in years.
        
        Args:
            a (datetime): The first datetime object.
            b (datetime): The second datetime object.
        
        Returns:
            float: The difference in years.
        """
        return self.cmp_seconds(a, b) // 31536000
