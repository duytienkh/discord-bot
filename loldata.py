import mwclient
from datetime import datetime, timezone, timedelta

class LOLData():
    def __init__(self) -> None:
        self.site = mwclient.Site('lol.fandom.com', path='/')
        self.dt = datetime.utcnow()
    
    # Return all matches from db
    def matches(self):
        res = self.site.api('cargoquery', 
            limit = 'max',
            tables = "MatchSchedule=MS",
            fields = "MS.Team1, MS.Team2, MS.DateTime_UTC, MS.ShownName, MS.BestOf",
            where = f"MS.DateTime_UTC >= '{self.dt.strftime('%Y-%m-%d')}'",
            order_by = "MS.DateTime_UTC"
        )

        # print(res)
        return res

    # Return all matches of filtered leagues
    def filtered_matches(self, max=10, to_string = False, filter='global'):
        def league_filter(match):
            white_list = ['LCK', 'LPL', 'LCS', 'LEC', 'VCS'] if filter == 'global' else [str(filter).upper()]
            for el in white_list:
                if match['ShownName'].startswith(el + ' ' + str(self.dt.year)):
                    return True
            return False    

        def match_to_string(match):
            return f"[{match['ShownName']}] {match['Team1']} - {match['Team2']} ({match['DateTime UTC']} - BO{match['BestOf']})\n"

        def shift_datetime(match):
            dt = datetime.strptime(match['DateTime UTC'], '%Y-%m-%d %H:%M:%S')
            dt += timedelta(hours=7)
            match['DateTime UTC'] = datetime.strftime(dt, '%d/%m %H:%M')

        res = []
        res_str = 'Upcoming matches\n'
        for data in self.matches()['cargoquery']:
            match = data['title']
            shift_datetime(match)
            if league_filter(match):
                res.append(match)
                res_str += match_to_string(match)

                if res.__len__() == max:
                    break
        
        return res_str if to_string else res


# print(LOLData().filtered_matches(to_string=True))
