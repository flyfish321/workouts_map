import calendar
import datetime
import locale

import svgwrite

from .exceptions import PosterError
from .poster import Poster
from .tracks_drawer import TracksDrawer
from .utils import format_float
from .xy import XY


class GithubDrawer(TracksDrawer):
    """Draw a gtihub profile-like poster"""

    def __init__(self, the_poster: Poster):
        super().__init__(the_poster)

    def draw(self, dr: svgwrite.Drawing, size: XY, offset: XY):
        if self.poster.tracks is None:
            raise PosterError("No tracks to draw")
        year_size = 200 * 4.0 / 80.0
        year_style = f"font-size:{year_size}px; font-family:Arial;"
        year_length_style = f"font-size:{110 * 3.0 / 80.0}px; font-family:Arial;"
        month_names_style = "font-size:2.5px; font-family:Arial"
        total_length_year_dict = self.poster.total_length_year_dict

        is_align_monday = self.poster.github_style == "align-monday"
        # 新增：检查是否使用1月1日左上角对齐
        is_align_january_first = self.poster.github_style == "align-january-first"
        
        for year in range(self.poster.years.from_year, self.poster.years.to_year + 1)[
            ::-1
        ]:
            start_date_weekday, _ = calendar.monthrange(year, 1)
            github_rect_first_day = datetime.date(year, 1, 1)

            # 修改：根据不同的对齐方式设置起始日期和星期
            if is_align_january_first:
                # 新的对齐方式：1月1日始终在第一行第一列
                github_rect_day = github_rect_first_day
                first_day_weekday = 0  # 强制设为0，让1月1日在第一行
            elif is_align_monday:
                # 原有的Monday对齐方式
                github_rect_day = github_rect_first_day + datetime.timedelta(
                    -start_date_weekday
                )
                first_day_weekday = 0
            else:
                # 默认的对齐方式
                github_rect_day = github_rect_first_day
                first_day_weekday = github_rect_first_day.weekday()

            year_length = total_length_year_dict.get(year, 0)
            year_length = format_float(self.poster.m2u(year_length))

            if str(year_length) == "0.0":
                continue
            try:
                month_names = [
                    locale.nl_langinfo(day)[:3]  # Get only first three letters
                    for day in [
                        locale.MON_1,
                        locale.MON_2,
                        locale.MON_3,
                        locale.MON_4,
                        locale.MON_5,
                        locale.MON_6,
                        locale.MON_7,
                        locale.MON_8,
                        locale.MON_9,
                        locale.MON_10,
                        locale.MON_11,
                        locale.MON_12,
                    ]
                ]
                # support windows or others doesn't support locale Name, by Hard code
            except Exception as e:
                print(str(e))
                month_names = [
                    "Jan",
                    "Feb",
                    "Mar",
                    "Apr",
                    "May",
                    "Jun",
                    "Jul",
                    "Aug",
                    "Sep",
                    "Oct",
                    "Nov",
                    "Dec",
                ]
            km_or_mi = "mi"
            if self.poster.units == "metric":
                km_or_mi = "km"
            dr.add(
                dr.text(
                    f"{year}",
                    insert=offset.tuple(),
                    fill=self.poster.colors["text"],
                    dominant_baseline="hanging",
                    style=year_style,
                )
            )

            dr.add(
                dr.text(
                    f"{year_length} {km_or_mi}",
                    insert=(offset.tuple()[0] + 165, offset.tuple()[1] + 5),
                    fill=self.poster.colors["text"],
                    dominant_baseline="hanging",
                    style=year_length_style,
                )
            )
            # add month name up to the poster one by one because of svg text auto trim the spaces.
            for num, name in enumerate(month_names):
                dr.add(
                    dr.text(
                        f"{name}",
                        insert=(offset.tuple()[0] + 15.5 * num, offset.tuple()[1] + 14),
                        fill=self.poster.colors["text"],
                        style=month_names_style,
                    )
                )

            rect_x = 10.0
            dom = (2.6, 2.6)

            # 修改：处理1月1日左上角对齐的情况
            if is_align_january_first:
                # 新的绘制逻辑：1月1日在左上角，按自然顺序排列
                rect_y = offset.y + year_size + 2
                current_date = github_rect_first_day
                days_in_year = 366 if calendar.isleap(year) else 365
                
                # 按周排列（每列7天）
                for week in range(54):  # 最多需要54周
                    if current_date.year > year:
                        break
                        
                    temp_rect_y = rect_y
                    for day_in_week in range(7):
                        if current_date.year > year:
                            break
                            
                        color = "#444444"
                        date_title = str(current_date)
                        if date_title in self.poster.tracks_by_date:
                            tracks = self.poster.tracks_by_date[date_title]
                            length = sum([t.length for t in tracks])
                            distance1 = self.poster.special_distance["special_distance"]
                            distance2 = self.poster.special_distance["special_distance2"]
                            has_special = distance1 < length / 1000 < distance2
                            color = self.color(
                                self.poster.length_range_by_date, length, has_special
                            )
                            if length / 1000 >= distance2:
                                color = self.poster.colors.get(
                                    "special2"
                                ) or self.poster.colors.get("special")
                            str_length = format_float(self.poster.m2u(length))
                            date_title = f"{date_title} {str_length} {km_or_mi}"

                        rect = dr.rect((rect_x, temp_rect_y), dom, fill=color)
                        rect.set_desc(title=date_title)
                        dr.add(rect)
                        
                        current_date += datetime.timedelta(1)
                        temp_rect_y += 3.5
                    
                    rect_x += 3.5
            else:
                # 原有的绘制逻辑
                for i in range(54):
                    # the first day of the first week of the year may not Monday
                    # so we need to skip some empty spaces
                    if i == 0:
                        rect_y = offset.y + year_size + 2 + 3.5 * first_day_weekday
                    else:
                        # the first day of the n week (n >1) must be  Monday
                        # so set first_day_weekday = 0
                        first_day_weekday = 0
                        rect_y = offset.y + year_size + 2
                    for j in range(7 - first_day_weekday):
                        if int(github_rect_day.year) > year:
                            break
                        rect_y += 3.5
                        color = "#444444"
                        date_title = str(github_rect_day)
                        if date_title in self.poster.tracks_by_date:
                            tracks = self.poster.tracks_by_date[date_title]
                            length = sum([t.length for t in tracks])
                            distance1 = self.poster.special_distance["special_distance"]
                            distance2 = self.poster.special_distance["special_distance2"]
                            has_special = distance1 < length / 1000 < distance2
                            color = self.color(
                                self.poster.length_range_by_date, length, has_special
                            )
                            if length / 1000 >= distance2:
                                color = self.poster.colors.get(
                                    "special2"
                                ) or self.poster.colors.get("special")
                            str_length = format_float(self.poster.m2u(length))
                            date_title = f"{date_title} {str_length} {km_or_mi}"

                        rect = dr.rect((rect_x, rect_y), dom, fill=color)
                        rect.set_desc(title=date_title)
                        dr.add(rect)
                        github_rect_day += datetime.timedelta(1)
                    rect_x += 3.5
            offset.y += 3.5 * 9 + year_size + 1.0
