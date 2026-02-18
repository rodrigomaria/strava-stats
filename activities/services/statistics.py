import logging
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

import pandas as pd

from ..constants import FIRST_DAY_YEAR, TRANSLATE_ACTIVITIES, TRANSLATE_WEEKDAYS
from .cache_service import CacheService

logger = logging.getLogger(__name__)


class StatisticsService:
    def __init__(self, activities: list, user_id: str = None):
        self.user_id = user_id or "default"
        self.df = self._create_dataframe(activities)

    def _create_dataframe(self, activities: list) -> pd.DataFrame:
        if not activities:
            return pd.DataFrame()

        df = pd.DataFrame.from_dict(activities, orient="columns")

        columns_to_drop = ["type", "resource_state", "athlete"]
        for col in columns_to_drop:
            if col in df.columns:
                df.drop(col, axis=1, inplace=True)

        df["start_date_local"] = pd.to_datetime(df["start_date_local"])
        df["start_date"] = pd.to_datetime(df["start_date"])

        first_day = pd.to_datetime(FIRST_DAY_YEAR, utc=True)
        df = df[df["start_date_local"] > first_day]

        return df

    @staticmethod
    def format_time(seconds: float) -> str:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    @staticmethod
    def get_number_days_year() -> int:
        timezone = ZoneInfo("America/Sao_Paulo")
        today = datetime.now(timezone).date()
        first_day = datetime(today.year, 1, 1).replace(tzinfo=timezone).date()
        return (today - first_day).days + 1

    def get_general_statistics(self) -> dict:
        """Obtém estatísticas gerais com cache"""
        cache_key = "general_stats"
        cached_stats = CacheService.get_stats(self.user_id, cache_key)
        
        if cached_stats is not None:
            return cached_stats
        
        stats = self._calculate_general_statistics()
        CacheService.set_stats(self.user_id, cache_key, stats)
        return stats
    
    def _calculate_general_statistics(self) -> dict:
        if self.df.empty:
            return {}

        df = self.df.copy()
        total_activities = len(df)
        total_time = self.format_time(df["elapsed_time"].sum())
        total_distance = df["distance"].sum() / 1000
        total_elevation = df["total_elevation_gain"].sum()

        total_activity_days = len(df["start_date_local"].dt.date.unique())

        df["day_of_week"] = df["start_date_local"].dt.day_name()
        best_week_day = df.groupby("day_of_week").size().sort_values(ascending=False).index[0]

        df["hour_of_day"] = df["start_date_local"].dt.hour
        best_active_hour = df.groupby("hour_of_day").size().sort_values(ascending=False).index[0]

        avg_activity_seconds = df["elapsed_time"].sum() / total_activities

        total_time_seconds = int(df["elapsed_time"].sum())

        return {
            "total_activities": total_activities,
            "total_time": total_time,
            "total_time_seconds": total_time_seconds,
            "total_distance": f"{total_distance:.1f}",
            "total_distance_raw": round(total_distance, 1),
            "total_elevation": f"{total_elevation:.1f}",
            "total_elevation_raw": round(total_elevation, 1),
            "activity_days": f"{total_activity_days}/{self.get_number_days_year()}",
            "best_week_day": TRANSLATE_WEEKDAYS.get(best_week_day, best_week_day),
            "best_active_hour": f"{best_active_hour}:00",
            "avg_activity_time": self.format_time(avg_activity_seconds),
        }

    def get_monthly_statistics(self) -> list:
        if self.df.empty:
            return []

        df = self.df.copy()
        df["month_year"] = df["start_date_local"].dt.strftime("%Y-%m")

        monthly_stats = (
            df.groupby("month_year")
            .agg({"elapsed_time": "sum", "start_date_local": "count", "distance": "sum"})
            .reset_index()
        )

        result = []
        for _, row in monthly_stats.iterrows():
            month_num = int(row["month_year"].split("-")[1])
            result.append({
                "month": row["month_year"],
                "month_number": month_num,
                "activities": int(row["start_date_local"]),
                "total_time": self.format_time(row["elapsed_time"]),
                "total_distance": f"{row['distance'] / 1000:.1f}",
            })

        return result

    def get_activity_type_statistics(self) -> list:
        if self.df.empty:
            return []

        df = self.df.copy()

        activity_counts = df["sport_type"].value_counts().to_dict()
        elapsed_time_by_activity = df.groupby("sport_type")["elapsed_time"].sum().to_dict()
        distance_by_activity = df.groupby("sport_type")["distance"].sum().to_dict()
        elevation_by_activity = df.groupby("sport_type")["total_elevation_gain"].sum().to_dict()

        result = []
        for sport_type in activity_counts.keys():
            translated_name = TRANSLATE_ACTIVITIES.get(sport_type, sport_type)
            result.append({
                "sport_type": translated_name,
                "sport_type_key": sport_type,
                "count": activity_counts[sport_type],
                "elapsed_time": self.format_time(elapsed_time_by_activity.get(sport_type, 0)),
                "distance": f"{distance_by_activity.get(sport_type, 0) / 1000:.1f}",
                "elevation": f"{elevation_by_activity.get(sport_type, 0):.1f}",
            })

        return result

    def get_weekly_statistics(self) -> list:
        if self.df.empty:
            return []

        weeks = self._generate_weeks_dict()
        result = []

        for week_name, week_dates in weeks.items():
            start_date = pd.to_datetime(f"{week_dates['start_date']}T00:00:00-00:00")
            end_date = pd.to_datetime(f"{week_dates['end_date']}T23:59:59-00:00")

            week_df = self.df[
                (self.df["start_date_local"] >= start_date) &
                (self.df["start_date_local"] <= end_date)
            ]

            if not week_df.empty:
                week_num = int(week_name.replace("Semana ", ""))
                result.append({
                    "week": week_name,
                    "week_number": week_num,
                    "start_date": week_dates["start_date"],
                    "end_date": week_dates["end_date"],
                    "activities": len(week_df),
                    "total_time": self.format_time(week_df["elapsed_time"].sum()),
                    "total_distance": f"{week_df['distance'].sum() / 1000:.1f}",
                })

        return result

    def _generate_weeks_dict(self) -> dict:
        current_year = datetime.now().year
        d = date(current_year, 1, 1)
        d += timedelta(days=(7 - d.weekday()) % 7)

        weeks = {}
        week_num = 1

        while d.year == current_year:
            weeks[f"Semana {week_num}"] = {
                "start_date": str(d),
                "end_date": str(d + timedelta(days=6)),
            }
            d += timedelta(days=7)
            week_num += 1

        return weeks

    def get_activities_by_sport_type(self, sport_type: str) -> list:
        if self.df.empty:
            return []

        filtered_df = self.df[self.df["sport_type"] == sport_type]

        activities = []
        for _, row in filtered_df.iterrows():
            activities.append({
                "name": row.get("name", ""),
                "date": row["start_date_local"].strftime("%d/%m/%Y %H:%M"),
                "distance": f"{row.get('distance', 0) / 1000:.2f}",
                "elapsed_time": self.format_time(row.get("elapsed_time", 0)),
                "elevation": f"{row.get('total_elevation_gain', 0):.1f}",
            })

        return activities

    def get_sport_types(self) -> list:
        if self.df.empty:
            return []

        sport_types = self.df["sport_type"].unique().tolist()
        return [
            {"value": st, "label": TRANSLATE_ACTIVITIES.get(st, st)}
            for st in sport_types
        ]

    def get_all_activities(self) -> list:
        if self.df.empty:
            return []

        activities = []
        sorted_df = self.df.sort_values("start_date_local", ascending=False)

        for _, row in sorted_df.iterrows():
            sport_type = row.get("sport_type", "")
            activity_date = row["start_date_local"]
            week_number = activity_date.isocalendar()[1]
            month_number = activity_date.month
            distance_km = row.get('distance', 0) / 1000
            elapsed_seconds = row.get("elapsed_time", 0)
            elevation_m = row.get('total_elevation_gain', 0)
            activities.append({
                "id": row.get("id", ""),
                "name": row.get("name", ""),
                "sport_type": TRANSLATE_ACTIVITIES.get(sport_type, sport_type),
                "sport_type_key": sport_type,
                "date": activity_date.strftime("%d/%m/%Y"),
                "time": activity_date.strftime("%H:%M"),
                "week": week_number,
                "month": month_number,
                "distance": f"{distance_km:.2f}",
                "distance_raw": round(distance_km, 2),
                "elapsed_time": self.format_time(elapsed_seconds),
                "elapsed_time_seconds": int(elapsed_seconds),
                "elevation": f"{elevation_m:.1f}",
                "elevation_raw": round(elevation_m, 1),
            })

        return activities
