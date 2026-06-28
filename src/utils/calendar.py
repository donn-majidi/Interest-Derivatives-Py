import datetime

class schedule:
    def __init__(self, valuation_date: datetime.date, maturity_date: datetime.date,
                 payment_freq: int):
        
        ## Input validation
        if type(valuation_date) is not datetime.date:
            raise TypeError(f"Valuation date must be a datetime object. {type(valuation_date)} passed instead.")
            
        if type(maturity_date) is not datetime.date:
            raise TypeError(f"Maturity date must be a datetime object. {type(maturity_date)} passed instead.")
            
        self.today = valuation_date
        self.payment_freq = payment_freq
        self.tomorrow = self._tomorrow(valuation_date)
        self.spot = self._spot(valuation_date)
    
    def _easter_date_USNO(self, y: int) -> datetime.date:
        
        '''
        United States Naval Observatory Algorithm for computing Easter dates.
        
        This is the python implementation of the algorithm developed by J.-M. Oudin (1940).
        Source: https://aa.usno.navy.mil/faq/easter
        '''
        
        ## Year input validation
        if type(y) is not int or y < 1900:
            if type(y) is not int:
                raise TypeError('Invalid input type. Year must be an integer.')
            else:
                raise ValueError('Unsupported year range. Must be after 1900.')
        
        c = int(y/100)
        N = y - 19 * int(y/19)
        k = int( (c - 17) / 25 )
        i = c - int(c/4) - int( (c - k) / 3 ) + 19 * N +15
        i = i - 30 * int(i/30)
        i = i - int(i/28) * ( 1 - int(i/28) * int(29/(i+1)) * int((21 - N) / 11) )
        j = y + int(y/4) + i + 2 - c + int(c/4)
        j = j - 7 * int(j/7)
        L = i - j
        M = 3 + int((L + 40)/44)
        d = L + 28 - 31 * int(M/4)
        
        easter_date = datetime.date(y, M, d)
        
        return easter_date
    
    def _weekend(self, date: datetime.date) -> bool:
        if date.weekday() >= 5:
            return True
       
        return False
        
    def _holiday_target(self, date: datetime.date) -> bool:
        y = date.year
        M = date.month
        d = date.day
        
        if d == 1 and M == 1:   ## New Year's day
            return True
        
        easter_day = self._easter_date_USNO(y)
        
        if date == easter_day + datetime.timedelta(days=-2):    ## Good Friday
            return True
        
        if date == easter_day + datetime.timedelta(days=1): ## Easter Monday
            return True
        
        if M == 5 and d == 1:   ## Labor day
            return True
        
        if M == 12 and d == 25: ## Christmas day
            return True
        
        if M == 12 and d == 26: ## Christmas holiday
            return True
        
        return False
        
    def _business_day(self, date: datetime.date) -> bool:
        if self._weekend(date) or self._holiday_target(date):
            return False
        
        return True
    
    def _tomorrow(self, date: datetime.date) -> datetime.date:
        i = 1
        next_business_day = date + datetime.timedelta(days=i)
        while self._business_day(next_business_day) == False:
            i+=1
            next_business_day = date + datetime.timedelta(days=i)
        
        return next_business_day
    
    def _spot(self, date: datetime.date) -> datetime.date:
        next_business_day = self._tomorrow(date)
        i = 1
        spot_date = next_business_day + datetime.timedelta(days=i)
        while self._business_day(spot_date) == False:
            i+=1
            spot_date = next_business_day + datetime.timedelta(days=i)
            
        return spot_date
    
    