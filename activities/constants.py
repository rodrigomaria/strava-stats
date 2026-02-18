from datetime import datetime

FIRST_DAY_YEAR = datetime(datetime.now().year, 1, 1, 0, 0)
EPOCH_TIMESTAMP = FIRST_DAY_YEAR.timestamp()
QUANTITY_PER_PAGE = 100

TRANSLATE_ACTIVITIES = {
    "Walk": "Caminhada",
    "Run": "Corrida",
    "Workout": "Treino",
    "Racquetball": "Raquete",
    "Soccer": "Futebol",
    "Hike": "Trilha",
    "WeightTraining": "Musculação",
    "Yoga": "Yoga",
    "Swim": "Natação",
    "Crossfit": "Crossfit",
    "MountainBikeRide": "Mountain Bike",
    "Ride": "Ciclismo",
}

TRANSLATE_WEEKDAYS = {
    "Sunday": "Domingo",
    "Monday": "Segunda-feira",
    "Tuesday": "Terça-feira",
    "Wednesday": "Quarta-feira",
    "Thursday": "Quinta-feira",
    "Friday": "Sexta-feira",
    "Saturday": "Sábado",
}
