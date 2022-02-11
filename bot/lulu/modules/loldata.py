import mwclient
from datetime import datetime, timezone, timedelta
import urllib.request
import re
from PIL import Image, ImageDraw, ImageFont
import os

class LOLData():
    def __init__(self) -> None:
        self.site = mwclient.Site('lol.fandom.com', path='/')
        self.dt = datetime.utcnow()
        self.white_list = ['LCK', 'LPL', 'LCS', 'LEC', 'VCS']
    
    # Return all matches from db
    def matches(self):
        self.dt = datetime.utcnow()
        res = self.site.api('cargoquery', 
            limit = 'max',
            tables = "MatchSchedule=MS,Teams=T1,Teams=T2",
            fields = "MS.Team1, MS.Team2, MS.DateTime_UTC, MS.ShownName, MS.BestOf, T1.Image=Image1, T2.Image=Image2",
            where = f"MS.DateTime_UTC >= '{self.dt.strftime('%Y-%m-%d %H:%M:%S')}'",
            join_on = "MS.Team1=T1.Name,MS.Team2=T2.Name",
            order_by = "MS.DateTime_UTC"
        )

        # print(res)
        return res

    # Return all matches of filtered leagues
    def filtered_matches(self, max=10, to_string = False, regions=['global']):
        def league_filter(match):
            white_list = self.white_list if regions == ['global'] else [str(region).upper() for region in regions]
            for el in white_list:
                if match['ShownName'].startswith(el + ' ' + str(self.dt.year)):
                    return True
            return False    

        def match_to_string(match):
            return f"[{match['ShownName']}] ({match['DateTime UTC']} - BO{match['BestOf']}) {match['Team1']} - {match['Team2']}\n"

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

    def filtered_matches_image(self, max=10, regions='global'):
        matches = self.filtered_matches(max, to_string=False, regions=regions)
        len = matches.__len__()
        img = Image.new(mode="RGBA", size=(1080, 80 * len), color=(255, 255, 255, 255))
        draw = ImageDraw.Draw(img)
        base_x = 30
        x, y = 30, 40
        padding = 15
        img_path = './img/teams/'

        row_height = 0
        def write_text(text, fontsize=26):
            nonlocal row_height, x
            font = ImageFont.truetype("./.fonts/Ubuntu-Regular.ttf", fontsize)
            _w, _h = draw.textsize(text, font)
            if _h > row_height:
                row_height = _h
            draw.text((x, y - _h//2), text, (0, 0, 0), font=font)

            x += _w + padding
            return _w, _h

        def write_image(team_image, team_name, align='left'):
            nonlocal row_height, x

            if self.get_filename_url_to_open(team_image, img_path + team_name):
                image = Image.open(img_path + team_name + '.png')
                image = image.resize((image.width * 64//image.height, 64)).convert('RGBA')
                if align == 'left':
                    img.paste(image, (x, y - image.height//2), image)
                if align == 'right':
                    img.paste(image, (x + 200 - image.width, y - image.height//2), image)

                if image.height > row_height:
                    row_height = image.height
                x += 200 + padding
            else:
                _w, _h = write_text(team_name, 14)
                x += 200 - _w

        for match in matches:
            write_text(f"[{match['ShownName']}] ({match['DateTime UTC']} - BO{match['BestOf']})")
            x += 2 * padding
            # paste teams image
            write_image(match['Image1'], match['Team1'], align='right')
            write_text(' - ')
            write_image(match['Image2'], match['Team2'], align='left')

            y += row_height + padding
            x = base_x
        
        file_name = f'./img/schedule/{str(datetime.now().microsecond)}.png'
        img.save(file_name)
        return file_name

    def get_filename_url_to_open(self, filename, save_name, size=None):
        if os.path.exists(save_name + '.png'):
            return True

        pattern = r'.*src\=\"(.+?)\".*'
        size = '|' + str(size) + 'px' if size else ''
        to_parse_text = '[[File:{}|link=%s]]'.format(filename, size)
        result = self.site.api('parse', title='Main Page', text=to_parse_text, disablelimitreport=1)
        parse_result_text = result['parse']['text']['*']

        try:
            url = re.match(pattern, parse_result_text)[1]
            #In case you would like to save the image in a specific location, you can add the path after 'url,' in the line below.
            urllib.request.urlretrieve(url, save_name + '.png')
            return True
        except Exception as e:
            pass
        return False
